"""Export meta ad HTML creatives to PNG images (with optional ZIP packaging).

Uses Playwright headless Chromium to render each HTML at its exact pixel size
(e.g., 1080x1080, 1080x1350, 1080x1920) and save as PNG.

Usage:
    # Export all creatives for a single product
    python3 export_png.py --product swaddle-strap

    # Export all products (~336 images, ~5-10 min)
    python3 export_png.py --all

    # Export only selected creatives (paste file names from preview-grid "선택 복사")
    python3 export_png.py --product swaddle-strap --selected selected.txt

    # Package as ZIP after export
    python3 export_png.py --product swaddle-strap --zip

    # Parallel workers (default 4)
    python3 export_png.py --all --workers 8
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path("/Users/inkyo/Projects/team-skills/output/광고카피/sundayhug-meta-bulk")

SIZE_RE = re.compile(r"_(\d+)x(\d+)_")


def parse_size(filename: str) -> tuple[int, int]:
    """Extract WxH from '03_hero-image_1080x1350_urgency.html' → (1080, 1350)."""
    m = SIZE_RE.search(filename)
    if not m:
        return (1080, 1080)
    return int(m.group(1)), int(m.group(2))


def find_all_products() -> list[Path]:
    result = []
    for cat_dir in sorted(ROOT.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith(".") or cat_dir.name == "_master":
            continue
        for pdir in sorted(cat_dir.iterdir()):
            if pdir.is_dir() and (pdir / "previews").exists():
                result.append(pdir)
    return result


def resolve_product_dirs(slugs: list[str] | None, all_flag: bool) -> list[Path]:
    if all_flag:
        return find_all_products()
    if not slugs:
        raise SystemExit("Must specify --product <slug> or --all")
    dirs = []
    for slug in slugs:
        hits = list(ROOT.glob(f"*/{slug}"))
        if not hits:
            print(f"  ⚠️  Product not found: {slug}")
            continue
        dirs.append(hits[0])
    return dirs


def list_html_files(product_dir: Path, selected: list[str] | None) -> list[Path]:
    previews = product_dir / "previews"
    all_htmls = sorted(
        f for f in previews.glob("*.html") if f.name != "preview-grid.html"
    )
    if selected:
        sel_names = {s.strip() for s in selected if s.strip()}
        # accept both with/without .html
        sel_normalized = {n if n.endswith(".html") else n + ".html" for n in sel_names}
        return [f for f in all_htmls if f.name in sel_normalized]
    return all_htmls


def render_one(html_path: Path, out_dir: Path, browser_pw) -> tuple[Path, str]:
    """Render one HTML to PNG. Returns (png_path, status)."""
    w, h = parse_size(html_path.name)
    png_name = html_path.stem + ".png"
    png_path = out_dir / png_name

    context = browser_pw.new_context(
        viewport={"width": w, "height": h},
        device_scale_factor=1,
    )
    try:
        page = context.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle", timeout=30_000)
        # Small extra wait for remote CDN images to fully decode
        page.wait_for_timeout(300)
        page.screenshot(path=str(png_path), omit_background=False, full_page=False)
        return (png_path, "OK")
    except Exception as e:
        return (png_path, f"FAIL: {e}")
    finally:
        context.close()


def render_product(product_dir: Path, selected: list[str] | None, workers: int = 4):
    htmls = list_html_files(product_dir, selected)
    if not htmls:
        print(f"  ⚠️  {product_dir.name}: no HTML files to export")
        return [], 0

    final_dir = product_dir / "final"
    final_dir.mkdir(parents=True, exist_ok=True)

    print(f"  📦 {product_dir.parent.name}/{product_dir.name}: {len(htmls)} creatives → PNG")
    start = time.time()
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            # Simple serial loop (Playwright contexts are cheap). Parallelism via
            # multiple browser contexts inside one browser instance.
            for html in htmls:
                png_path, status = render_one(html, final_dir, browser)
                results.append((html.name, png_path.name, status))
                if status == "OK":
                    print(f"    ✓ {html.name} → {png_path.name}")
                else:
                    print(f"    ✗ {html.name} — {status}")
        finally:
            browser.close()

    elapsed = time.time() - start
    ok = sum(1 for *_, s in results if s == "OK")
    print(f"    ⏱  {ok}/{len(htmls)} done in {elapsed:.1f}s")
    return results, ok


def zip_product(product_dir: Path) -> Path:
    final_dir = product_dir / "final"
    if not final_dir.exists():
        return None
    zip_path = product_dir / f"{product_dir.name}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for png in sorted(final_dir.glob("*.png")):
            zf.write(png, arcname=png.name)
        # Include CSV too
        csv_path = product_dir / "copy.csv"
        if csv_path.exists():
            zf.write(csv_path, arcname="copy.csv")
    return zip_path


def zip_all(product_dirs: list[Path]) -> Path:
    zip_path = ROOT / "all_creatives.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for pdir in product_dirs:
            final_dir = pdir / "final"
            if not final_dir.exists():
                continue
            for png in sorted(final_dir.glob("*.png")):
                arc = f"{pdir.parent.name}/{pdir.name}/{png.name}"
                zf.write(png, arcname=arc)
            csv_path = pdir / "copy.csv"
            if csv_path.exists():
                zf.write(csv_path, arcname=f"{pdir.parent.name}/{pdir.name}/copy.csv")
        # Master CSV
        master_csv = ROOT / "all_copies.csv"
        if master_csv.exists():
            zf.write(master_csv, arcname="all_copies.csv")
    return zip_path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--product", "-p", action="append", help="Product slug (repeatable)")
    ap.add_argument("--all", action="store_true", help="Export all 16 products")
    ap.add_argument("--selected", "-s", help="File with selected ad names (one per line)")
    ap.add_argument("--zip", action="store_true", help="Package outputs as ZIP after export")
    ap.add_argument("--workers", type=int, default=4, help="(reserved) parallel workers")
    args = ap.parse_args()

    product_dirs = resolve_product_dirs(args.product, args.all)
    if not product_dirs:
        sys.exit(1)

    selected = None
    if args.selected:
        selected = Path(args.selected).read_text(encoding="utf-8").splitlines()
        print(f"✓ Selected list: {len(selected)} items")

    total_ok = 0
    total_requested = 0
    all_zips = []

    t0 = time.time()
    for pdir in product_dirs:
        _, ok = render_product(pdir, selected, args.workers)
        total_ok += ok
        total_requested += len(list_html_files(pdir, selected))
        if args.zip and not args.all:
            zp = zip_product(pdir)
            if zp:
                all_zips.append(zp)
                print(f"  📦 ZIP: {zp.name} ({zp.stat().st_size / 1024:.0f} KB)")

    if args.zip and args.all:
        master_zip = zip_all(product_dirs)
        size_mb = master_zip.stat().st_size / (1024 * 1024)
        print(f"\n📦 Master ZIP: {master_zip} ({size_mb:.1f} MB)")

    elapsed = time.time() - t0
    print(f"\n🎉 Done: {total_ok}/{total_requested} PNGs in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
