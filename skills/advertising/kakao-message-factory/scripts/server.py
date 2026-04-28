"""
server.py — 카카오 메시지 인터랙티브 편집 서버 (FastAPI)

API:
  GET  /                            → 캠페인 인덱스
  GET  /preview/{slug}              → 캠페인 preview-grid.html
  GET  /preview/{slug}/{filename}   → 개별 메시지 HTML
  GET  /img/{slug}/{filename}       → 이미지 파일
  GET  /png/{slug}/{filename}       → 생성된 PNG
  POST /api/png                     → On-demand PNG 생성
  POST /api/save-text               → 텍스트 + 인라인 스타일 패치
  POST /api/transform-image         → Gemini AI 이미지 변환

실행:
    python3 server.py                              # 자동으로 최신 캠페인 열기
    python3 server.py --slug abc-folding-crib     # 특정 캠페인
    python3 server.py --port 8765
    python3 server.py --no-open
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
from typing import Any, Optional

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
    from pydantic import BaseModel
except ImportError:
    print("❌ FastAPI 미설치. 설치: pip install fastapi uvicorn", file=sys.stderr)
    sys.exit(1)

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT = Path.home() / "Desktop" / "team-skills" / "카카오메시지"

# meta-ad-factory의 batch-transform 재사용
BATCH_TRANSFORM = (
    SCRIPT_DIR.parents[3]  # team-skills/skills/
    / "batch-image-transform" / "scripts" / "batch-transform.mjs"
)
META_AD_BATCH = (
    SCRIPT_DIR.parents[1] / "meta-ad-factory" / "scripts"
)  # 백업 경로

SIZE_RE = re.compile(r"_(\d+)x(\d+)\.html$")


def parse_size(filename: str) -> tuple[int, int]:
    m = SIZE_RE.search(filename)
    return (int(m.group(1)), int(m.group(2))) if m else (800, 600)


def find_campaign_dir(slug: str) -> Path | None:
    """{brand}/{slug} 형태로 검색."""
    if not ROOT.exists():
        return None
    hits = list(ROOT.glob(f"*/{slug}"))
    return hits[0] if hits else None


def list_campaigns() -> list[tuple[str, str]]:
    """모든 (brand, slug) 리스트."""
    if not ROOT.exists():
        return []
    out = []
    for brand_dir in sorted(ROOT.iterdir()):
        if not brand_dir.is_dir() or brand_dir.name.startswith("."):
            continue
        for cdir in sorted(brand_dir.iterdir()):
            if cdir.is_dir() and (cdir / "preview-grid.html").exists():
                out.append((brand_dir.name, cdir.name))
    return out


def latest_campaign() -> tuple[str, str] | None:
    campaigns = list_campaigns()
    if not campaigns:
        return None
    campaigns.sort(
        key=lambda bs: (ROOT / bs[0] / bs[1] / "preview-grid.html").stat().st_mtime,
        reverse=True,
    )
    return campaigns[0]


# ─── Playwright (PNG 변환) ──────────────────────────────────────────────────
_browser: Any = None
_pw_ctx: Any = None
_browser_lock = asyncio.Lock()


async def get_browser():
    global _browser, _pw_ctx
    async with _browser_lock:
        if _browser is None:
            try:
                from playwright.async_api import async_playwright
            except ImportError:
                raise HTTPException(500, "Playwright 미설치. pip install playwright && playwright install chromium")
            _pw_ctx = await async_playwright().start()
            _browser = await _pw_ctx.chromium.launch(headless=True)
    return _browser


async def close_browser():
    global _browser, _pw_ctx
    if _browser:
        await _browser.close()
        _browser = None
    if _pw_ctx:
        await _pw_ctx.stop()
        _pw_ctx = None


async def capture_png(html_path: Path, png_path: Path) -> None:
    w, h = parse_size(html_path.name)
    browser = await get_browser()
    context = await browser.new_context(
        viewport={"width": w, "height": h},
        device_scale_factor=2,
    )
    try:
        page = await context.new_page()
        await page.goto(f"file://{html_path.resolve()}", wait_until="networkidle", timeout=30_000)
        await page.wait_for_timeout(300)
        png_path.parent.mkdir(parents=True, exist_ok=True)
        # 카드 영역만 캡처 시도
        target = page.locator(".card, .km-card, .kakao-frame").first
        if await target.count() > 0:
            await target.screenshot(path=str(png_path))
        else:
            await page.screenshot(path=str(png_path), full_page=False)
    finally:
        await context.close()


# ─── Models ──────────────────────────────────────────────────────────────────
class PngReq(BaseModel):
    slug: str
    filename: str


class TextPatch(BaseModel):
    field: str
    html: Optional[str] = None
    styles: Optional[dict] = None


class SaveTextReq(BaseModel):
    slug: str
    filename: str
    patches: list[TextPatch]


class TransformReq(BaseModel):
    slug: str
    filename: str
    image_key: str
    prompt: str


# ─── 동시 편집 lock ─────────────────────────────────────────────────────────
_locks: dict[str, asyncio.Lock] = {}


def _lock_for(key: str) -> asyncio.Lock:
    if key not in _locks:
        _locks[key] = asyncio.Lock()
    return _locks[key]


def _backup_once(html_path: Path) -> None:
    bak = html_path.with_suffix(html_path.suffix + ".bak")
    if not bak.exists():
        shutil.copy2(html_path, bak)


# ─── App ─────────────────────────────────────────────────────────────────────
app = FastAPI(title="Kakao Message Factory Server")


@app.on_event("shutdown")
async def on_shutdown():
    await close_browser()


@app.get("/", response_class=HTMLResponse)
async def index():
    campaigns = list_campaigns()
    latest = latest_campaign()
    rows = "".join(
        f'<li><a href="/preview/{slug}">{brand}/{slug}</a></li>'
        for brand, slug in campaigns
    )
    return HTMLResponse(f"""<!doctype html><html><head><meta charset="utf-8"><title>Kakao Message Factory</title>
<style>body{{font-family:system-ui;padding:40px;max-width:720px;margin:auto}}
a{{color:#FAE100;background:#1A1A1A;padding:6px 12px;border-radius:6px;text-decoration:none}}
a:hover{{background:#000}}
li{{padding:8px 0;font-size:18px;list-style:none}}
ul{{padding:0}}</style></head>
<body><h1>📨 Kakao Message Factory</h1>
<p>사용 가능한 캠페인:</p><ul>{rows or '<li>(없음) — 먼저 kakao_factory.py build 실행</li>'}</ul>
{'<p>최신: <a href="/preview/' + latest[1] + '">' + latest[1] + '</a></p>' if latest else ''}
</body></html>""")


@app.get("/preview/{slug}", response_class=HTMLResponse)
async def preview(slug: str):
    cdir = find_campaign_dir(slug)
    if not cdir:
        raise HTTPException(404, f"Campaign not found: {slug}")
    grid = cdir / "preview-grid.html"
    if not grid.exists():
        raise HTTPException(404, "preview-grid.html missing — kakao_factory.py build 먼저 실행")
    html = grid.read_text(encoding="utf-8")
    # base href + slug 메타 주입
    injection = (
        f'<meta name="kf-slug" content="{slug}">\n'
        f'<base href="/preview/{slug}/">\n'
        + _editor_script_tag()
    )
    html = html.replace("</head>", injection + "</head>", 1)
    return HTMLResponse(html)


@app.get("/preview/{slug}/{filename}")
async def preview_asset(slug: str, filename: str):
    cdir = find_campaign_dir(slug)
    if not cdir:
        raise HTTPException(404)
    target = (cdir / filename).resolve()
    if not str(target).startswith(str(cdir.resolve())):
        raise HTTPException(403)
    if not target.exists():
        raise HTTPException(404)
    return FileResponse(target, media_type="text/html; charset=utf-8")


@app.get("/preview/{slug}/images/{filename}")
async def preview_image(slug: str, filename: str):
    cdir = find_campaign_dir(slug)
    if not cdir:
        raise HTTPException(404)
    target = (cdir / "images" / filename).resolve()
    if not target.exists():
        raise HTTPException(404)
    ext = target.suffix.lower()
    media = {".webp": "image/webp", ".png": "image/png",
             ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
             ".gif": "image/gif"}.get(ext, "application/octet-stream")
    return FileResponse(target, media_type=media)


@app.get("/png/{slug}/{filename}")
async def get_png(slug: str, filename: str):
    cdir = find_campaign_dir(slug)
    if not cdir:
        raise HTTPException(404)
    target = (cdir / "png" / filename).resolve()
    if not target.exists():
        raise HTTPException(404, "PNG 미생성 — 📥 버튼 클릭 시 생성됨")
    return FileResponse(target, media_type="image/png")


@app.post("/api/png")
async def api_png(req: PngReq):
    cdir = find_campaign_dir(req.slug)
    if not cdir:
        raise HTTPException(404)
    html_path = cdir / req.filename
    if not html_path.exists():
        raise HTTPException(404, "HTML 없음")
    png_path = cdir / "png" / (html_path.stem + ".png")

    async with _lock_for(str(png_path)):
        if not png_path.exists() or html_path.stat().st_mtime > png_path.stat().st_mtime:
            t0 = time.time()
            await capture_png(html_path, png_path)
            elapsed = time.time() - t0
        else:
            elapsed = 0.0

    # 자동 압축 (alimtalk 500KB / friendtalk 2MB)
    type_m = re.search(r"_(\d{2}-[a-z-]+)_", html_path.name)
    type_id = type_m.group(1) if type_m else ""
    target_kb = 500 if type_id.startswith(("07-alimtalk", "08-alimtalk")) else 2048
    try:
        import kakao_validator as kv
        success, kb, q = kv.compress_to_target(png_path, target_kb)
    except Exception as e:
        kb, q, success = png_path.stat().st_size / 1024, None, True

    return JSONResponse({
        "ok": True,
        "url": f"/png/{req.slug}/{png_path.name}",
        "name": png_path.name,
        "kb": round(kb, 1),
        "elapsed": round(elapsed, 2),
        "compressed": q is not None,
    })


@app.post("/api/save-text")
async def api_save_text(req: SaveTextReq):
    cdir = find_campaign_dir(req.slug)
    if not cdir:
        raise HTTPException(404)
    html_path = cdir / req.filename
    if not html_path.exists():
        raise HTTPException(404)

    async with _lock_for(str(html_path)):
        from bs4 import BeautifulSoup
        _backup_once(html_path)
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        applied = []
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
                    decls: dict[str, str] = {}
                    for d in current.split(";"):
                        if ":" in d:
                            k, v = d.split(":", 1)
                            decls[k.strip().lower()] = v.strip()
                    for raw_k, v in patch.styles.items():
                        if not v:
                            continue
                        css_key = re.sub(r"(?<!^)(?=[A-Z])", "-", raw_k).lower()
                        decls[css_key] = v.strip()
                    node["style"] = "; ".join(f"{k}:{v}" for k, v in decls.items()) + ";"
                applied.append(patch.field)
        html_path.write_text(str(soup), encoding="utf-8")
        png = cdir / "png" / (html_path.stem + ".png")
        if png.exists():
            png.unlink()

    return {"ok": True, "applied": applied}


@app.post("/api/transform-image")
async def api_transform(req: TransformReq):
    cdir = find_campaign_dir(req.slug)
    if not cdir:
        raise HTTPException(404)
    html_path = cdir / req.filename
    if not html_path.exists():
        raise HTTPException(404)

    # batch-transform 경로 탐색
    transform_script = BATCH_TRANSFORM
    if not transform_script.exists():
        transform_script = (
            SCRIPT_DIR.parents[2] / "batch-image-transform" / "scripts" / "batch-transform.mjs"
        )
    if not transform_script.exists():
        # team-skills/skills/batch-image-transform 검색
        candidates = list(SCRIPT_DIR.parents[2].rglob("batch-transform.mjs"))
        if candidates:
            transform_script = candidates[0]
    if not transform_script.exists():
        raise HTTPException(500, f"batch-transform.mjs 미발견. team-skills/skills/batch-image-transform 확인 필요")

    async with _lock_for(str(html_path)):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_path.read_text(encoding="utf-8"), "html.parser")
        img = soup.select_one(f'img[data-image-key="{req.image_key}"]')
        if img is None:
            raise HTTPException(404, f"image_key '{req.image_key}' not found")

        src = img.get("src", "")
        # 이미지 파일 경로 결정
        if src.startswith("data:"):
            # base64 inline
            header, b64 = src.split(",", 1)
            mime = header.split(";")[0].replace("data:", "")
            ext = {"image/webp": "webp", "image/png": "png", "image/jpeg": "jpg"}.get(mime, "png")
            src_bytes = base64.b64decode(b64)
        elif src.startswith("images/"):
            img_path = cdir / src
            if not img_path.exists():
                raise HTTPException(404, f"이미지 파일 없음: {img_path}")
            src_bytes = img_path.read_bytes()
            ext = img_path.suffix.lstrip(".")
            mime = {"webp": "image/webp", "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}.get(ext, "image/png")
        else:
            raise HTTPException(400, f"지원하지 않는 src 형식: {src[:50]}")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            input_dir = tmp_path / "in"
            output_dir = tmp_path / "out"
            input_dir.mkdir()
            output_dir.mkdir()
            in_file = input_dir / f"source.{ext}"
            in_file.write_bytes(src_bytes)

            env = os.environ.copy()
            # .env 파일에서 GEMINI_API_KEY 로드
            for env_path in [SCRIPT_DIR.parents[2] / ".env", Path.home() / ".env"]:
                if env_path.exists():
                    for line in env_path.read_text(encoding="utf-8").splitlines():
                        s = line.strip()
                        if "=" in s and not s.startswith("#"):
                            k, v = s.split("=", 1)
                            env.setdefault(k.strip(), v.strip().strip('"').strip("'"))
                    break
            if "GEMINI_API_KEY" in env and "GOOGLE_AI_API_KEY" not in env:
                env["GOOGLE_AI_API_KEY"] = env["GEMINI_API_KEY"]

            try:
                proc = await asyncio.create_subprocess_exec(
                    "node", str(transform_script),
                    "--input", str(input_dir),
                    "--output", str(output_dir),
                    "--prompt", req.prompt,
                    "--model", "gemini-2.5-flash",
                    "--concurrency", "1",
                    cwd=transform_script.parent,
                    env=env,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
            except FileNotFoundError:
                raise HTTPException(500, "node not in PATH")

            if proc.returncode != 0:
                msg = (stderr or stdout or b"").decode("utf-8", errors="ignore")[-500:]
                raise HTTPException(500, f"Gemini 변환 실패: {msg}")

            results = sorted(output_dir.rglob("*-transformed.*"))
            if not results:
                results = sorted(f for f in output_dir.rglob("*") if f.is_file())
            if not results:
                raise HTTPException(500, "변환 결과 없음")

            # 새 이미지 → cdir/images/{key}-transformed-{timestamp}.{ext}
            new_file = results[0]
            new_ext = new_file.suffix.lower().lstrip(".")
            ts = int(time.time())
            new_name = f"{req.image_key}_ai_{ts}.{new_ext}"
            new_path = cdir / "images" / new_name
            new_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(new_file, new_path)

            img["src"] = f"images/{new_name}"

        _backup_once(html_path)
        html_path.write_text(str(soup), encoding="utf-8")
        png = cdir / "png" / (html_path.stem + ".png")
        if png.exists():
            png.unlink()

    return {"ok": True, "new_src": f"images/{new_name}", "size_kb": new_path.stat().st_size // 1024}


# ─── 편집 UI 스크립트 ──────────────────────────────────────────────────────
def _editor_script_tag() -> str:
    """preview-grid.html에 자동 주입되는 편집 UI 스크립트."""
    return """
<style>
  .kf-edit-toolbar{position:fixed;top:12px;right:12px;background:#1a1a1a;color:#fff;padding:8px 14px;border-radius:8px;z-index:9999;font-family:system-ui;font-size:13px;display:flex;gap:8px;align-items:center;box-shadow:0 4px 12px rgba(0,0,0,.3);}
  .kf-edit-toolbar button{background:#FAE100;color:#1a1a1a;border:0;padding:6px 12px;border-radius:6px;cursor:pointer;font-weight:600;font-size:12px;}
  .kf-edit-toolbar button:hover{background:#fff;}
  .kf-edit-toolbar.editing button{background:#FF6B35;color:#fff;}
  .kf-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:10000;align-items:center;justify-content:center;}
  .kf-modal.show{display:flex;}
  .kf-modal-inner{background:#fff;border-radius:12px;padding:24px;max-width:560px;width:90%;max-height:80vh;overflow:auto;}
  .kf-modal h2{margin:0 0 12px;font-size:18px;}
  .kf-modal label{display:block;font-size:12px;color:#666;margin-top:12px;margin-bottom:4px;}
  .kf-modal input,.kf-modal textarea{width:100%;padding:8px;border:1px solid #ccc;border-radius:6px;font-size:14px;box-sizing:border-box;font-family:inherit;}
  .kf-modal textarea{min-height:80px;resize:vertical;}
  .kf-modal .row{display:flex;gap:8px;}
  .kf-modal .row > *{flex:1;}
  .kf-modal-buttons{display:flex;justify-content:flex-end;gap:8px;margin-top:20px;}
  .kf-modal-buttons button{padding:8px 16px;border-radius:6px;border:0;cursor:pointer;font-weight:600;}
  .kf-modal-buttons .save{background:#1D9E75;color:#fff;}
  .kf-modal-buttons .cancel{background:#eee;color:#333;}
</style>
<div class="kf-edit-toolbar" id="kf-toolbar">
  <span>✏️ 편집 모드</span>
  <button onclick="kfToggleEdit()">OFF</button>
</div>

<div class="kf-modal" id="kf-text-modal">
  <div class="kf-modal-inner">
    <h2>텍스트 편집</h2>
    <label>필드: <code id="kf-text-field"></code></label>
    <label>텍스트</label>
    <textarea id="kf-text-input"></textarea>
    <label>색상</label>
    <div class="row">
      <input type="color" id="kf-text-color" style="height:40px;">
      <input type="text" id="kf-text-color-hex" placeholder="#ffffff">
    </div>
    <label>글자 크기 (px)</label>
    <input type="number" id="kf-text-size" placeholder="48">
    <label>굵기 (100~900)</label>
    <input type="number" id="kf-text-weight" min="100" max="900" step="100" placeholder="700">
    <div class="kf-modal-buttons">
      <button class="cancel" onclick="kfCloseModal('kf-text-modal')">취소</button>
      <button class="save" onclick="kfSaveText()">저장</button>
    </div>
  </div>
</div>

<div class="kf-modal" id="kf-img-modal">
  <div class="kf-modal-inner">
    <h2>🤖 AI 이미지 변환</h2>
    <label>이미지 키: <code id="kf-img-key"></code></label>
    <label>변환 프롬프트 (한글/영문)</label>
    <textarea id="kf-img-prompt" placeholder="예: 부드러운 자연광이 들어오는 따뜻한 라이프스타일 톤으로 바꿔줘"></textarea>
    <p style="font-size:12px;color:#888;margin-top:8px;">Gemini AI로 변환 (15~30초 소요)</p>
    <div class="kf-modal-buttons">
      <button class="cancel" onclick="kfCloseModal('kf-img-modal')">취소</button>
      <button class="save" id="kf-img-go" onclick="kfTransformImg()">변환 시작</button>
    </div>
  </div>
</div>

<script>
const KF_SLUG = document.querySelector('meta[name="kf-slug"]').content;
let kfEditing = false;
let kfCurrent = {iframe:null, field:null, key:null};

function kfToggleEdit(){
  kfEditing = !kfEditing;
  const tb = document.getElementById('kf-toolbar');
  tb.classList.toggle('editing', kfEditing);
  tb.querySelector('button').textContent = kfEditing ? 'ON' : 'OFF';
  document.querySelectorAll('iframe').forEach(f=>{
    f.style.pointerEvents = kfEditing ? 'auto' : 'none';
    if(kfEditing) kfAttachIframe(f);
  });
}

function kfAttachIframe(iframe){
  try{
    const doc = iframe.contentDocument;
    if(!doc) return;
    doc.querySelectorAll('[data-editable]').forEach(el=>{
      el.style.outline = '2px dashed #FAE100';
      el.style.cursor = 'pointer';
      el.onclick = e=>{e.preventDefault();kfOpenTextModal(iframe, el);};
    });
    doc.querySelectorAll('[data-image-key]').forEach(el=>{
      el.style.outline = '2px dashed #FF6B35';
      el.style.cursor = 'pointer';
      el.onclick = e=>{e.preventDefault();kfOpenImgModal(iframe, el);};
    });
  }catch(e){console.error('iframe attach failed', e);}
}

function kfOpenTextModal(iframe, el){
  kfCurrent = {iframe, field:el.dataset.editable, el};
  document.getElementById('kf-text-field').textContent = el.dataset.editable;
  document.getElementById('kf-text-input').value = el.textContent.trim();
  const cs = el.ownerDocument.defaultView.getComputedStyle(el);
  document.getElementById('kf-text-color').value = rgbToHex(cs.color);
  document.getElementById('kf-text-color-hex').value = rgbToHex(cs.color);
  document.getElementById('kf-text-size').value = parseInt(cs.fontSize);
  document.getElementById('kf-text-weight').value = cs.fontWeight;
  document.getElementById('kf-text-modal').classList.add('show');
}

function kfOpenImgModal(iframe, el){
  kfCurrent = {iframe, key:el.dataset.imageKey, el};
  document.getElementById('kf-img-key').textContent = el.dataset.imageKey;
  document.getElementById('kf-img-prompt').value = '';
  document.getElementById('kf-img-modal').classList.add('show');
}

function kfCloseModal(id){document.getElementById(id).classList.remove('show');}

async function kfSaveText(){
  const filename = kfCurrent.iframe.getAttribute('src');
  const newText = document.getElementById('kf-text-input').value;
  const color = document.getElementById('kf-text-color-hex').value;
  const size = document.getElementById('kf-text-size').value;
  const weight = document.getElementById('kf-text-weight').value;
  const styles = {};
  if(color) styles.color = color;
  if(size) styles.fontSize = size + 'px';
  if(weight) styles.fontWeight = weight;
  const res = await fetch('/api/save-text', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({slug:KF_SLUG, filename, patches:[{field:kfCurrent.field, html:newText, styles}]})
  });
  if(res.ok){kfCloseModal('kf-text-modal');kfCurrent.iframe.contentWindow.location.reload();}
  else alert('저장 실패: ' + (await res.text()));
}

async function kfTransformImg(){
  const filename = kfCurrent.iframe.getAttribute('src');
  const prompt = document.getElementById('kf-img-prompt').value.trim();
  if(!prompt){alert('프롬프트 입력 필요');return;}
  const btn = document.getElementById('kf-img-go');
  btn.disabled = true; btn.textContent = '변환 중... (15~30초)';
  try{
    const res = await fetch('/api/transform-image', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({slug:KF_SLUG, filename, image_key:kfCurrent.key, prompt})
    });
    if(res.ok){
      kfCloseModal('kf-img-modal');
      kfCurrent.iframe.contentWindow.location.reload();
    } else {
      alert('변환 실패: ' + (await res.text()));
    }
  } finally {
    btn.disabled = false; btn.textContent = '변환 시작';
  }
}

function rgbToHex(rgb){
  const m = rgb.match(/\\d+/g);
  if(!m || m.length<3) return '#000000';
  return '#' + m.slice(0,3).map(x=>parseInt(x).toString(16).padStart(2,'0')).join('');
}

// PNG 다운로드 버튼 강화 (on-demand 생성)
document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('a[download]').forEach(a=>{
    a.addEventListener('click', async e=>{
      const href = a.getAttribute('href');
      if(!href.startsWith('png/')) return;
      e.preventDefault();
      const filename = href.replace('png/', '').replace('.png', '.html');
      const orig = a.textContent; a.textContent = '⏳';
      try{
        const res = await fetch('/api/png', {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({slug:KF_SLUG, filename})
        });
        const j = await res.json();
        if(j.ok){window.open(j.url, '_blank');a.textContent='✓ ' + j.kb + 'KB';}
        else a.textContent='✗ 실패';
      } finally { setTimeout(()=>{a.textContent=orig;}, 2000); }
    });
  });
});
</script>
"""


# ─── Launcher ────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", "-s", help="캠페인 슬러그 (자동 오픈)")
    ap.add_argument("--port", "-p", type=int, default=8765)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--no-open", action="store_true")
    args = ap.parse_args()

    target_slug = args.slug
    if not target_slug:
        lp = latest_campaign()
        if lp:
            target_slug = lp[1]
    base_url = f"http://{args.host}:{args.port}"
    target_url = f"{base_url}/preview/{target_slug}" if target_slug else base_url

    print(f"▶ Kakao Message Factory Server → {base_url}")
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
