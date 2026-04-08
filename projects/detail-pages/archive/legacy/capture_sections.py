#!/usr/bin/env python3
"""Capture swaddle-sb.html sections as high-resolution (2x) PNG images."""

import re
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

HTML_FILE = Path(__file__).parent / "swaddle-sb.html"
OUTPUT_DIR = Path(__file__).parent / "swaddle-sb_sections"
VIEWPORT_WIDTH = 600
DEVICE_SCALE = 2  # 2x for high resolution

# Section markers derived from HTML comments
SECTIONS = [
    ("01_intro", "<!--Intro-->", "<!--Intro-->", 3, 13),
    ("02_review", "<!--후기리뷰-->", "<!--후기리뷰-->", 14, 20),
    ("03_hooking", "<!--후킹 멘트 시작-->", "<!--후킹 멘트 끝 -->", 21, 46),
    ("04_lineup", "<!--라인업 시작 -->", "<!--컬러 차트 끝-->", 47, 123),
    ("05_banner", "<!--후킹 배너 시작-->", "<!--후킹 배너 끝-->", 124, 138),
    ("06_compare", "<!--비교차트 시작-->", "<!--비교차트  끝-->", 139, 161),
    ("07_overview", "<!--오버뷰 시작 -->", "<!--배너 2단 끝-->", 162, 175),
    ("08_point1_fabric", "<!--포인트1-->", "<!--포인트1 끝-->", 176, 209),
    ("09_point2", "<!--포인트2-->", "<!--포인트2-->", 210, 229),
    ("10_point3", "<!--포인트3-->", "<!--포인트3-->", 230, 242),
    ("11_point4_detail", "<!--포인트4-->", "<!--포인트4-->", 243, 253),
    ("12_swipe_features", "<!--⬇️제품 특징 설명스와이프⬇️-->", "<!--⬆️제품 특징 설명스와이프 끝⬆️-->", 254, 267),
    ("13_notice", "<!-- 잠깐 -->", "<!-- 잠깐 끝-->", 268, 288),
    ("14_photo_banner", "<!--배너 사진 시작 -->", "<!--배너 사진 끝 -->", 289, 293),
    ("15_howto", "<!--HOW TO-->", "<!--HOW TO-->", 294, 304),
    ("16_photo_banner2", "<!--배너 사진 시작 -->", "<!--배너 사진 끝 -->", 305, 312),
    ("17_brand_vision", "<!--브랜드 비전 공유 시작 -->", "<!--브랜드 비전 공유 끝 -->", 313, 327),
    ("18_size_guide", "<!-- 사이즈 가이드 시작 -->", "<!-- 사이즈 가이드 끝 -->", 328, 382),
]


def extract_section_html(lines, start_line, end_line):
    """Extract HTML lines (1-indexed) inclusive."""
    return "\n".join(lines[start_line - 1 : end_line])


def wrap_section(section_html, css_path):
    """Wrap section HTML with proper head/style for standalone rendering."""
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width={VIEWPORT_WIDTH}">
<link rel="stylesheet" href="{css_path}">
<style>
  body {{ margin: 0; padding: 0; background: white; }}
</style>
</head>
<body>
{section_html}
</body>
</html>"""


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    html_text = HTML_FILE.read_text(encoding="utf-8")
    lines = html_text.splitlines()
    # CSS is one level up: archive/userCSS.css
    css_rel = "../userCSS.css"

    print(f"📄 Source: {HTML_FILE.name}")
    print(f"📁 Output: {OUTPUT_DIR.name}/")
    print(f"🔍 Sections: {len(SECTIONS)}")
    print(f"📐 Resolution: {VIEWPORT_WIDTH}px × {DEVICE_SCALE}x = {VIEWPORT_WIDTH * DEVICE_SCALE}px")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(
            viewport={"width": VIEWPORT_WIDTH, "height": 800},
            device_scale_factor=DEVICE_SCALE,
        )
        page = context.new_page()

        # 1) Full page capture
        print("⏳ Capturing full page...")
        page.goto(HTML_FILE.as_uri(), wait_until="networkidle")
        page.wait_for_timeout(1000)
        full_path = OUTPUT_DIR / "00_full_page.png"
        page.screenshot(path=str(full_path), full_page=True)
        size_mb = full_path.stat().st_size / 1024 / 1024
        print(f"  ✅ 00_full_page.png ({size_mb:.1f} MB)")

        # 2) Section captures
        for name, _, _, start, end in SECTIONS:
            section_html = extract_section_html(lines, start, end)
            wrapped = wrap_section(section_html, css_rel)

            # Save temp HTML next to original so relative image paths resolve
            tmp_file = HTML_FILE.parent / f"_tmp_{name}.html"
            tmp_file.write_text(wrapped, encoding="utf-8")

            page.goto(tmp_file.as_uri(), wait_until="networkidle")
            page.wait_for_timeout(500)

            out_path = OUTPUT_DIR / f"{name}.png"
            page.screenshot(path=str(out_path), full_page=True)
            size_kb = out_path.stat().st_size / 1024
            print(f"  ✅ {name}.png ({size_kb:.0f} KB)")

            tmp_file.unlink()  # cleanup temp

        browser.close()

    print(f"\n🎉 Done! {len(SECTIONS) + 1} images saved to {OUTPUT_DIR.name}/")


if __name__ == "__main__":
    main()
