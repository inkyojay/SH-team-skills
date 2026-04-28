"""
export_png.py — 카카오 메시지 HTML을 Playwright로 PNG 변환 + 자동 압축

사용:
    # 캠페인 폴더 전체 변환
    python3 export_png.py ~/Desktop/team-skills/카카오메시지/sundayhug/abc-promo

    # 단일 HTML
    python3 export_png.py path/to/single.html

    # 압축 비활성화 (원본 PNG 유지)
    python3 export_png.py <dir> --no-compress

    # ZIP으로 묶기
    python3 export_png.py <dir> --zip

알림톡(07/08)은 자동으로 500KB 이하로 압축, 친구톡은 2MB 이하.
"""
from __future__ import annotations

import argparse
import re
import sys
import time
import zipfile
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("❌ Playwright 미설치. 설치: pip install playwright && playwright install chromium",
          file=sys.stderr)
    sys.exit(1)

import kakao_validator as kv

SIZE_RE = re.compile(r"_(\d+)x(\d+)\.html$")
TYPE_RE = re.compile(r"_(\d{2}-[a-z-]+)_")


def parse_size(filename: str) -> tuple[int, int]:
    """파일명에서 사이즈 추출 (없으면 (800, 600) 기본값)."""
    m = SIZE_RE.search(filename)
    if not m:
        return (800, 600)
    return int(m.group(1)), int(m.group(2))


def parse_type(filename: str) -> str:
    """파일명에서 카카오 타입 ID 추출."""
    m = TYPE_RE.search(filename)
    return m.group(1) if m else ""


def get_size_limit_kb(filename: str) -> int:
    """파일명 기반 용량 한도 결정."""
    type_id = parse_type(filename)
    if type_id.startswith(("07-alimtalk", "08-alimtalk")):
        return kv.SIZE_LIMITS_KB["alimtalk"]
    return kv.SIZE_LIMITS_KB["friendtalk"]


def list_html_files(directory: Path) -> list[Path]:
    """캠페인 폴더 내 HTML 파일 리스트 (preview-grid 제외)."""
    if directory.is_file():
        return [directory] if directory.suffix == ".html" else []
    return sorted(
        f for f in directory.glob("*.html")
        if f.name != "preview-grid.html" and f.name != "template-guide.html"
    )


def render_one(html_path: Path, out_dir: Path, browser) -> tuple[Path, str]:
    """단일 HTML → PNG. (png_path, status) 반환."""
    w, h = parse_size(html_path.name)
    png_name = html_path.stem + ".png"
    png_path = out_dir / png_name

    context = browser.new_context(
        viewport={"width": w, "height": h},
        device_scale_factor=2,  # 카카오 200dpi 대응
    )
    try:
        page = context.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle", timeout=30_000)
        page.wait_for_timeout(300)
        # frame이 viewport보다 클 수 있으므로 .kakao-frame 또는 .km-card 영역만 캡처
        target_locator = page.locator(".kakao-frame, .km-card").first
        if target_locator.count() > 0:
            target_locator.screenshot(path=str(png_path), omit_background=False)
        else:
            page.screenshot(path=str(png_path), full_page=False)
        return (png_path, "OK")
    except Exception as e:
        return (png_path, f"FAIL: {e}")
    finally:
        context.close()


def render_directory(
    directory: Path,
    compress: bool = True,
) -> tuple[int, int, list[tuple[str, str]]]:
    """디렉토리 내 모든 HTML → PNG. (성공, 전체, 결과리스트) 반환."""
    htmls = list_html_files(directory)
    if not htmls:
        print(f"⚠️  HTML 파일 없음: {directory}")
        return 0, 0, []

    out_dir = directory / "png" if directory.is_dir() else directory.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n🎨 변환 시작: {len(htmls)}개 파일 → {out_dir}")

    results = []
    ok_count = 0
    start = time.time()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for html in htmls:
                png_path, status = render_one(html, out_dir, browser)
                if status == "OK":
                    # 자동 압축
                    if compress and png_path.exists():
                        target_kb = get_size_limit_kb(html.name)
                        success, kb, q = kv.compress_to_target(png_path, target_kb)
                        marker = "✓" if success else "⚠"
                        q_str = f" q={q}" if q else ""
                        print(f"  {marker} {html.name} → {png_path.name} ({kb:.0f}KB{q_str})")
                        if not success:
                            print(f"      ⚠️  {target_kb}KB 한도 초과 (실제 {kb:.0f}KB) — "
                                  f"원본 이미지 리사이즈 필요", file=sys.stderr)
                    else:
                        kb = png_path.stat().st_size / 1024
                        print(f"  ✓ {html.name} → {png_path.name} ({kb:.0f}KB)")
                    ok_count += 1
                    results.append((html.name, "OK"))
                else:
                    print(f"  ✗ {html.name} — {status}", file=sys.stderr)
                    results.append((html.name, status))
        finally:
            browser.close()

    elapsed = time.time() - start
    print(f"\n⏱  {ok_count}/{len(htmls)} 완료 ({elapsed:.1f}s)")
    return ok_count, len(htmls), results


def zip_directory(directory: Path) -> Path:
    """캠페인 폴더의 png/ 를 zip으로 묶기."""
    png_dir = directory / "png"
    if not png_dir.exists():
        raise FileNotFoundError(f"png/ 폴더 없음: {png_dir}")
    zip_path = directory / f"{directory.name}_kakao_messages.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for png in sorted(png_dir.glob("*.png")):
            zf.write(png, arcname=png.name)
    return zip_path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", help="캠페인 폴더 또는 단일 HTML 파일")
    ap.add_argument("--no-compress", action="store_true", help="자동 압축 비활성화")
    ap.add_argument("--zip", action="store_true", help="변환 후 ZIP으로 묶기")
    args = ap.parse_args()

    target = Path(args.path).expanduser().resolve()
    if not target.exists():
        print(f"❌ 경로 없음: {target}", file=sys.stderr)
        return 1

    ok, total, _ = render_directory(target, compress=not args.no_compress)

    if args.zip and target.is_dir():
        zip_path = zip_directory(target)
        size_kb = zip_path.stat().st_size / 1024
        print(f"\n📦 ZIP: {zip_path.name} ({size_kb:.0f} KB)")

    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
