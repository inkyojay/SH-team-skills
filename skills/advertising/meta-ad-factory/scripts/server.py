"""Meta Ad Factory — interactive local server.

Serves preview-grid.html and provides on-demand APIs:
  - /api/png               → single PNG generation (Playwright async)
  - /api/save-text         → patch editable fields in a creative HTML
  - /api/transform-image   → Gemini AI image swap via batch-image-transform

Run:
    python3 server.py                      # auto-open latest product preview
    python3 server.py --slug swaddle-strap
    python3 server.py --no-open            # do not auto-open browser
    python3 server.py --port 8765

Stop with Ctrl+C.
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import webbrowser
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


# ── Paths ─────────────────────────────────────────────────────────────────────
SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT = Path.home() / "Desktop" / "team-skills" / "광고카피" / "sundayhug-meta-bulk"
BATCH_TRANSFORM = (
    Path(__file__).resolve().parents[3]
    / "batch-image-transform" / "scripts" / "batch-transform.mjs"
)

SIZE_RE = re.compile(r"_(\d+)x(\d+)_")


def parse_size(filename: str) -> tuple[int, int]:
    m = SIZE_RE.search(filename)
    return (int(m.group(1)), int(m.group(2))) if m else (1080, 1080)


def find_product_dir(slug: str) -> Path | None:
    hits = list(ROOT.glob(f"*/{slug}"))
    return hits[0] if hits else None


def list_products() -> list[tuple[str, str]]:
    """Return list of (category, slug) for products with previews/."""
    if not ROOT.exists():
        return []
    out = []
    for cat_dir in sorted(ROOT.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith((".", "_")):
            continue
        for pdir in sorted(cat_dir.iterdir()):
            if pdir.is_dir() and (pdir / "previews" / "preview-grid.html").exists():
                out.append((cat_dir.name, pdir.name))
    return out


def latest_product() -> tuple[str, str] | None:
    products = list_products()
    if not products:
        return None
    # Sort by preview-grid mtime desc
    products.sort(
        key=lambda cs: (ROOT / cs[0] / cs[1] / "previews" / "preview-grid.html").stat().st_mtime,
        reverse=True,
    )
    return products[0]


# ── Playwright lifecycle (async) ──────────────────────────────────────────────
_playwright_ctx: Any = None
_browser: Any = None
_browser_lock = asyncio.Lock()


async def get_browser():
    """Lazy-init a shared Chromium instance."""
    global _playwright_ctx, _browser
    async with _browser_lock:
        if _browser is None:
            from playwright.async_api import async_playwright
            _playwright_ctx = await async_playwright().start()
            _browser = await _playwright_ctx.chromium.launch(headless=True)
    return _browser


async def close_browser():
    global _playwright_ctx, _browser
    if _browser:
        await _browser.close()
        _browser = None
    if _playwright_ctx:
        await _playwright_ctx.stop()
        _playwright_ctx = None


async def capture_png(html_path: Path, png_path: Path) -> None:
    """Render one HTML to PNG at its native pixel size."""
    w, h = parse_size(html_path.name)
    browser = await get_browser()
    context = await browser.new_context(
        viewport={"width": w, "height": h},
        device_scale_factor=1,
    )
    try:
        page = await context.new_page()
        await page.goto(f"file://{html_path.resolve()}", wait_until="networkidle", timeout=30_000)
        await page.wait_for_timeout(300)
        png_path.parent.mkdir(parents=True, exist_ok=True)
        await page.screenshot(path=str(png_path), full_page=False)
    finally:
        await context.close()


# ── Models ────────────────────────────────────────────────────────────────────
class PngReq(BaseModel):
    slug: str
    filename: str   # e.g. "01_hero-image_1080x1080_emotional.html"


class TextPatch(BaseModel):
    field: str                      # data-editable value: headline / subtext / cta / badge
    html: str | None = None         # text/HTML content (if None, only styles applied)
    styles: dict[str, str] | None = None  # CSS property dict, e.g. {"color":"#fff","fontSize":"72px"}


class SaveTextReq(BaseModel):
    slug: str
    filename: str
    patches: list[TextPatch]


class TransformReq(BaseModel):
    slug: str
    filename: str
    image_key: str  # data-image-key value
    prompt: str


# ── File lock (per HTML file) for save/transform concurrency ─────────────────
_locks: dict[str, asyncio.Lock] = {}


def _lock_for(key: str) -> asyncio.Lock:
    if key not in _locks:
        _locks[key] = asyncio.Lock()
    return _locks[key]


def _backup_once(html_path: Path) -> None:
    """Create .bak sidecar only if it doesn't already exist."""
    bak = html_path.with_suffix(html_path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(html_path, bak)


# ── FastAPI app ──────────────────────────────────────────────────────────────
app = FastAPI(title="Meta Ad Factory Server")


@app.on_event("shutdown")
async def on_shutdown():
    await close_browser()


@app.get("/", response_class=HTMLResponse)
async def index():
    products = list_products()
    latest = latest_product()
    rows = "".join(
        f'<li><a href="/preview/{slug}">{cat}/{slug}</a></li>'
        for cat, slug in products
    )
    return HTMLResponse(
        f"""<!doctype html><html><head><meta charset="utf-8"><title>Meta Ad Factory</title>
        <style>body{{font-family:system-ui;padding:40px;max-width:720px;margin:auto}}
        a{{color:#1D9E75;text-decoration:none}}a:hover{{text-decoration:underline}}
        li{{padding:6px 0;font-size:18px}}</style></head>
        <body><h1>Meta Ad Factory</h1>
        <p>사용 가능한 제품:</p><ul>{rows or '<li>(없음) — 먼저 products/*.py 실행</li>'}</ul>
        {'<p>최신: <a href="/preview/' + latest[1] + '">' + latest[1] + '</a></p>' if latest else ''}
        </body></html>"""
    )


@app.get("/preview/{slug}", response_class=HTMLResponse)
async def preview(slug: str):
    pdir = find_product_dir(slug)
    if not pdir:
        raise HTTPException(404, f"Product not found: {slug}")
    grid = pdir / "previews" / "preview-grid.html"
    if not grid.exists():
        raise HTTPException(404, "preview-grid.html missing — rebuild first")
    html = grid.read_text(encoding="utf-8")
    # Inject slug meta + <base href> so relative iframe src (./01_...html) resolves
    injection = (
        f'<meta name="mf-slug" content="{slug}">\n'
        f'<base href="/preview/{slug}/">\n'
    )
    html = html.replace("</head>", injection + "</head>", 1)
    return HTMLResponse(html)


@app.get("/preview/{slug}/{filename}")
async def preview_asset(slug: str, filename: str):
    """Serve individual ad HTML files referenced by iframe."""
    pdir = find_product_dir(slug)
    if not pdir:
        raise HTTPException(404)
    target = (pdir / "previews" / filename).resolve()
    if not str(target).startswith(str(pdir.resolve())):
        raise HTTPException(403)
    if not target.exists():
        raise HTTPException(404)
    return FileResponse(target, media_type="text/html; charset=utf-8")


@app.get("/assets/{slug}/{filename}")
async def asset(slug: str, filename: str):
    # Kept for backward compat; serve same as /preview/{slug}/{filename}
    return await preview_asset(slug, filename)


@app.get("/src-image/{slug}/{key}")
async def src_image(slug: str, key: str):
    """Serve original source image for the 'original photos' gallery."""
    pdir = find_product_dir(slug)
    if not pdir:
        raise HTTPException(404, f"Product not found: {slug}")
    sources_file = pdir / "previews" / "_sources.json"
    if not sources_file.exists():
        raise HTTPException(404, "_sources.json missing — rebuild the product")
    import json as _json
    try:
        sources = _json.loads(sources_file.read_text(encoding="utf-8"))
    except _json.JSONDecodeError:
        raise HTTPException(500, "invalid _sources.json")
    entry = sources.get(key)
    if not entry:
        raise HTTPException(404, f"Image key '{key}' not found")
    if entry.get("type") == "url":
        # Redirect to the remote URL
        from fastapi.responses import RedirectResponse
        return RedirectResponse(entry["url"])
    target = Path(entry["path"]).resolve()
    if not target.exists():
        raise HTTPException(404, f"File missing: {target}")
    ext = target.suffix.lower()
    media = {
        ".webp": "image/webp", ".png": "image/png",
        ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".gif": "image/gif",
    }.get(ext, "application/octet-stream")
    return FileResponse(target, media_type=media, filename=target.name)


@app.get("/final/{slug}/{filename}")
async def final_png(slug: str, filename: str):
    pdir = find_product_dir(slug)
    if not pdir:
        raise HTTPException(404)
    target = (pdir / "final" / filename).resolve()
    if not str(target).startswith(str(pdir.resolve())):
        raise HTTPException(403)
    if not target.exists():
        raise HTTPException(404, "PNG not yet generated — click download button")
    return FileResponse(target, media_type="image/png", filename=filename)


@app.post("/api/png")
async def api_png(req: PngReq):
    pdir = find_product_dir(req.slug)
    if not pdir:
        raise HTTPException(404, f"Product not found: {req.slug}")
    html_path = pdir / "previews" / req.filename
    if not html_path.exists():
        raise HTTPException(404, "HTML not found")
    png_path = pdir / "final" / (html_path.stem + ".png")

    async with _lock_for(str(png_path)):
        if not png_path.exists() or html_path.stat().st_mtime > png_path.stat().st_mtime:
            t0 = time.time()
            await capture_png(html_path, png_path)
            elapsed = time.time() - t0
        else:
            elapsed = 0.0

    return JSONResponse(
        {
            "ok": True,
            "url": f"/final/{req.slug}/{png_path.name}",
            "name": png_path.name,
            "elapsed": round(elapsed, 2),
            "cached": elapsed == 0.0,
        }
    )


@app.post("/api/save-text")
async def api_save_text(req: SaveTextReq):
    pdir = find_product_dir(req.slug)
    if not pdir:
        raise HTTPException(404)
    html_path = pdir / "previews" / req.filename
    if not html_path.exists():
        raise HTTPException(404)

    async with _lock_for(str(html_path)):
        from bs4 import BeautifulSoup
        _backup_once(html_path)
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        applied: list[str] = []
        for patch in req.patches:
            nodes = soup.select(f'[data-editable="{patch.field}"]')
            if not nodes:
                continue
            for node in nodes:
                if patch.html is not None:
                    node.clear()
                    fragment = BeautifulSoup(patch.html, "html.parser")
                    for el in list(fragment.contents):
                        node.append(el)
                if patch.styles:
                    current = node.get("style", "") or ""
                    declarations: dict[str, str] = {}
                    for decl in current.split(";"):
                        if ":" in decl:
                            k, v = decl.split(":", 1)
                            declarations[k.strip().lower()] = v.strip()
                    for raw_k, v in patch.styles.items():
                        if not v:
                            continue
                        # Convert camelCase → kebab-case
                        css_key = re.sub(r"(?<!^)(?=[A-Z])", "-", raw_k).lower()
                        declarations[css_key] = v.strip()
                    node["style"] = "; ".join(f"{k}:{v}" for k, v in declarations.items()) + ";"
                applied.append(patch.field)
        html_path.write_text(str(soup), encoding="utf-8")
        # Invalidate old PNG
        png = pdir / "final" / (html_path.stem + ".png")
        if png.exists():
            png.unlink()

    return {"ok": True, "applied": applied}


@app.post("/api/transform-image")
async def api_transform(req: TransformReq):
    pdir = find_product_dir(req.slug)
    if not pdir:
        raise HTTPException(404)
    html_path = pdir / "previews" / req.filename
    if not html_path.exists():
        raise HTTPException(404)
    if not BATCH_TRANSFORM.exists():
        raise HTTPException(500, f"batch-transform.mjs not found at {BATCH_TRANSFORM}")

    async with _lock_for(str(html_path)):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        img = soup.select_one(f'img[data-image-key="{req.image_key}"]')
        if img is None:
            raise HTTPException(404, f"Image key '{req.image_key}' not found")

        src = img.get("src", "")
        if not src.startswith("data:"):
            raise HTTPException(400, "Only base64-embedded images supported")
        header, b64 = src.split(",", 1)
        mime = header.split(";")[0].replace("data:", "")
        ext = {"image/webp": "webp", "image/png": "png", "image/jpeg": "jpg"}.get(mime, "png")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "input"
            output_dir = tmp_path / "output"
            input_dir.mkdir()
            output_dir.mkdir()
            in_file = input_dir / f"source.{ext}"
            in_file.write_bytes(base64.b64decode(b64))

            # Load .env and map GEMINI_API_KEY → GOOGLE_AI_API_KEY (what batch-transform.mjs expects)
            env = os.environ.copy()
            env_file = Path(__file__).resolve().parents[3].parent / ".env"
            if env_file.exists():
                for line in env_file.read_text(encoding="utf-8").splitlines():
                    s = line.strip()
                    if "=" in s and not s.startswith("#"):
                        k, v = s.split("=", 1)
                        env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            if "GEMINI_API_KEY" in env and "GOOGLE_AI_API_KEY" not in env:
                env["GOOGLE_AI_API_KEY"] = env["GEMINI_API_KEY"]

            try:
                proc = await asyncio.create_subprocess_exec(
                    "node", str(BATCH_TRANSFORM),
                    "--input", str(input_dir),
                    "--output", str(output_dir),
                    "--prompt", req.prompt,
                    "--model", "gemini-2.5-flash",
                    "--concurrency", "1",
                    cwd=BATCH_TRANSFORM.parent,
                    env=env,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
            except FileNotFoundError:
                raise HTTPException(500, "node not found in PATH")

            if proc.returncode != 0:
                msg = (stderr or stdout or b"").decode("utf-8", errors="ignore")[-500:]
                raise HTTPException(500, f"Gemini transform failed: {msg}")

            # batch-transform names outputs like `source-transformed.webp`
            results = sorted(output_dir.rglob("*-transformed.*"))
            if not results:
                results = sorted(f for f in output_dir.rglob("*") if f.is_file())
            if not results:
                msg = (stdout or b"").decode("utf-8", errors="ignore")[-300:]
                raise HTTPException(500, f"No output from batch-transform. stdout: {msg}")
            new_bytes = results[0].read_bytes()
            suffix = results[0].suffix.lower()
            new_mime = {
                ".webp": "image/webp", ".png": "image/png",
                ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
            }.get(suffix, mime)
            new_b64 = base64.b64encode(new_bytes).decode("ascii")
            img["src"] = f"data:{new_mime};base64,{new_b64}"

        _backup_once(html_path)
        html_path.write_text(str(soup), encoding="utf-8")
        # Invalidate PNG
        png = pdir / "final" / (html_path.stem + ".png")
        if png.exists():
            png.unlink()

    return {"ok": True, "mime": new_mime, "size_kb": len(new_bytes) // 1024}


# ── Launcher ──────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", "-s", help="Product slug to auto-open")
    ap.add_argument("--port", "-p", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--no-open", action="store_true", help="Don't auto-open browser")
    args = ap.parse_args()

    # Resolve target URL
    target_slug = args.slug
    if not target_slug:
        lp = latest_product()
        if lp:
            target_slug = lp[1]
    base_url = f"http://{args.host}:{args.port}"
    target_url = f"{base_url}/preview/{target_slug}" if target_slug else base_url

    print(f"▶ Meta Ad Factory Server → {base_url}")
    if target_slug:
        print(f"  Opening: {target_url}")
    print("  Stop: Ctrl+C\n")

    if not args.no_open:
        def _open():
            time.sleep(0.6)
            webbrowser.open(target_url)
        threading.Thread(target=_open, daemon=True).start()

    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port, log_level="warning")


if __name__ == "__main__":
    main()
