"""Live page section HTML → PNG 배치 추출.

메타 광고 export_png.py 패턴을 라이브 페이지에 맞게 변형:
  - viewport 폭은 600px 고정 (라이브 페이지 컨벤션)
  - height는 가변 → `full_page=True`로 콘텐츠 전체 캡처

Usage:
    # 캠페인 전체 PNG 추출
    python3 export_png.py --campaign silky-bamboo-smoke

    # 특정 섹션만
    python3 export_png.py --campaign silky-bamboo-smoke --sections 01-live-hero,15-review

    # 다른 캠페인 슬러그 위치
    python3 export_png.py --campaign 2026-05-가정의달 --base ~/Desktop/output/상세페이지/라이브
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright


DEFAULT_BASE = Path.home() / "Desktop" / "output" / "상세페이지" / "라이브"
LIVE_PAGE_WIDTH = 600   # 라이브 페이지 표준 폭


def list_section_htmls(previews_dir: Path, sections: list[str] | None) -> list[Path]:
    """previews/ 안의 섹션 HTML 파일 리스트.

    sections 필터가 주어지면 (예: ["01-live-hero", "15-review"])
    파일명이 그 prefix로 시작하는 것만.
    preview-grid.html은 항상 제외.
    """
    htmls = sorted(f for f in previews_dir.glob("*.html") if f.name != "preview-grid.html")
    if sections:
        prefixes = {s.strip() for s in sections if s.strip()}
        htmls = [f for f in htmls if any(f.name.startswith(p) for p in prefixes)]
    return htmls


def render_one(html_path: Path, png_path: Path, browser) -> tuple[Path, str]:
    """단일 섹션 HTML을 600px 폭으로 콘텐츠 실제 높이만큼 PNG 추출.

    full_page=True는 viewport보다 작은 콘텐츠일 때 viewport 크기로 캡처돼서 흰 여백이
    생긴다. scrollHeight를 직접 측정 후 clip으로 잘라야 정확.
    """
    png_path.parent.mkdir(parents=True, exist_ok=True)
    context = browser.new_context(
        viewport={"width": LIVE_PAGE_WIDTH, "height": 800},
        device_scale_factor=1,
    )
    try:
        page = context.new_page()
        page.goto(f"file://{html_path.resolve()}", wait_until="networkidle", timeout=30_000)
        page.wait_for_timeout(300)
        # 콘텐츠 실제 높이 측정. documentElement.scrollHeight는 viewport 크기를 그대로
        # 반환하는 경우가 있어서 (HTML이 viewport를 채움) body.scrollHeight만 사용.
        height = page.evaluate("document.body.scrollHeight")
        height = max(int(height), 60)
        # viewport보다 큰 경우 viewport도 늘려야 정확한 layout이 나옴
        if height > 800:
            page.set_viewport_size({"width": LIVE_PAGE_WIDTH, "height": height})
            page.wait_for_timeout(100)
        page.screenshot(
            path=str(png_path),
            clip={"x": 0, "y": 0, "width": LIVE_PAGE_WIDTH, "height": height},
            omit_background=False,
        )
        return (png_path, "OK")
    except Exception as e:
        return (png_path, f"FAIL: {e}")
    finally:
        context.close()


def render_campaign(campaign_slug: str, sections: list[str] | None, base: Path):
    """캠페인 폴더 안의 모든(or 선택된) 섹션 PNG 추출."""
    previews_dir = base / campaign_slug / "previews"
    final_dir = base / campaign_slug / "final"

    if not previews_dir.exists():
        print(f"❌ {previews_dir} not found — build_live.py로 빌드 먼저 실행")
        sys.exit(1)

    htmls = list_section_htmls(previews_dir, sections)
    if not htmls:
        print(f"⚠️  No section HTML to export in {previews_dir}")
        return

    final_dir.mkdir(parents=True, exist_ok=True)
    print(f"▶ {campaign_slug}: {len(htmls)} 섹션 → PNG (600px 폭, full-page)")
    t0 = time.time()
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for html in htmls:
                png_path = final_dir / (html.stem + ".png")
                _, status = render_one(html, png_path, browser)
                results.append((html.name, png_path.name, status))
                mark = "✓" if status == "OK" else "✗"
                size_info = ""
                if status == "OK":
                    size_kb = png_path.stat().st_size // 1024
                    size_info = f" ({size_kb} KB)"
                print(f"  {mark} {html.name} → {png_path.name}{size_info}"
                      + ("" if status == "OK" else f"  {status}"))
        finally:
            browser.close()

    ok = sum(1 for *_, s in results if s == "OK")
    elapsed = time.time() - t0
    print(f"\n🎉 Done: {ok}/{len(htmls)} PNGs in {elapsed:.1f}s")
    print(f"   Output: {final_dir}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--campaign", "-c", required=True, help="Campaign slug (folder name)")
    ap.add_argument("--sections", "-s", help="콤마 구분 섹션 ID prefix (예: 01-live-hero,15-review)")
    ap.add_argument("--base", help=f"출력 루트 (기본: {DEFAULT_BASE})")
    args = ap.parse_args()

    base = Path(args.base).expanduser() if args.base else DEFAULT_BASE
    sections = [s.strip() for s in args.sections.split(",")] if args.sections else None
    render_campaign(args.campaign, sections, base)


if __name__ == "__main__":
    main()
