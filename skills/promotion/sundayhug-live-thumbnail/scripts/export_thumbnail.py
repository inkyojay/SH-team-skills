#!/usr/bin/env python3
"""Render SundayHug live thumbnail HTML and export 1:1 PNG without bottom bars.

Example:
  python3 export_thumbnail.py \
    --background /path/hero.webp \
    --live-badge /path/live-badge.png \
    --out-dir ~/Desktop/team-skills/카드뉴스/sundayhug-live-thumbnail/bloomingdays \
    --date '5월 7일 (목) 오전 11시' \
    --title-line-1 'ABC 아기침대 라이브 혜택' \
    --title-line-2 '+ 전용 악세사리 쿠폰 공개'
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


def q(path: Path) -> str:
    return str(path.expanduser().resolve())


def chrome_path() -> str:
    candidates = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        shutil.which("google-chrome"),
        shutil.which("chromium"),
    ]
    for c in candidates:
        if c and Path(c).exists():
            return c
    raise SystemExit("Chrome/Chromium not found. Install Google Chrome or adjust chrome_path().")


def file_url(path: Path) -> str:
    return path.expanduser().resolve().as_uri()


def render_template(template: Path, out_html: Path, values: dict[str, str]) -> None:
    text = template.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    out_html.write_text(text, encoding="utf-8")


def screenshot(html: Path, raw: Path, scale: int) -> None:
    chrome = chrome_path()
    # macOS Chrome headless needs extra height. 1080x1080 directly can leave bottom body/background bar.
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        "--allow-file-access-from-files",
        f"--force-device-scale-factor={scale}",
        "--window-size=1080,1167",
        f"--screenshot={q(raw)}",
        file_url(html),
    ]
    subprocess.run(cmd, check=True)


def crop_square(raw: Path, out: Path, size: int) -> None:
    try:
        from PIL import Image
    except Exception as e:
        raise SystemExit("Pillow required for reliable top-left crop. Run: python3 -m pip install --user pillow") from e
    im = Image.open(raw).convert("RGB")
    im.crop((0, 0, size, size)).save(out)


def check_no_bottom_bar(out: Path) -> None:
    from PIL import Image
    import numpy as np
    im = Image.open(out).convert("RGB")
    arr = np.array(im)
    bg = np.array([17, 21, 24])
    rows = ((arr == bg).all(axis=2)).mean(axis=1)
    first = next((i for i, v in enumerate(rows) if v > 0.99), None)
    if first is not None:
        raise SystemExit(f"Bottom/background bar detected from row {first}. Check viewport/crop/background coverage.")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--background", required=True, help="Background image path")
    ap.add_argument("--live-badge", default="/Users/inkyo/Desktop/templates/promotion/assets/live-badge.png")
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--date", default="5월 7일 (목) 오전 11시")
    ap.add_argument("--kicker", default="Blooming Days · Shopping Live")
    ap.add_argument("--title-line-1", default="ABC 아기침대 라이브 혜택")
    ap.add_argument("--title-line-2", default="+ 전용 쿨매트 할인")
    ap.add_argument("--slug", default="sundayhug-live-thumbnail")
    args = ap.parse_args()

    here = Path(__file__).resolve().parent.parent
    template = here / "templates" / "thumbnail.html"
    out_dir = Path(args.out_dir).expanduser().resolve()
    assets = out_dir / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    bg_src = Path(args.background).expanduser().resolve()
    badge_src = Path(args.live_badge).expanduser().resolve()
    bg_dst = assets / bg_src.name
    badge_dst = assets / "live-badge.png"
    shutil.copy2(bg_src, bg_dst)
    shutil.copy2(badge_src, badge_dst)

    html = out_dir / f"{args.slug}.html"
    values = {
        "BACKGROUND_SRC": "./assets/" + bg_dst.name,
        "LIVE_BADGE_SRC": "./assets/live-badge.png",
        "DATE_TEXT": args.date,
        "KICKER_TEXT": args.kicker,
        "TITLE_LINE_1": args.title_line_1,
        "TITLE_LINE_2": args.title_line_2,
    }
    render_template(template, html, values)

    raw1080 = out_dir / ".raw-1080.png"
    raw3240 = out_dir / ".raw-3240.png"
    out1080 = out_dir / f"{args.slug}-1080.png"
    out3240 = out_dir / f"{args.slug}-3240.png"

    screenshot(html, raw1080, 1)
    crop_square(raw1080, out1080, 1080)
    check_no_bottom_bar(out1080)

    screenshot(html, raw3240, 3)
    crop_square(raw3240, out3240, 3240)
    check_no_bottom_bar(out3240)

    raw1080.unlink(missing_ok=True)
    raw3240.unlink(missing_ok=True)

    print("HTML:", html)
    print("PNG 1080:", out1080)
    print("PNG 3240:", out3240)


if __name__ == "__main__":
    main()
