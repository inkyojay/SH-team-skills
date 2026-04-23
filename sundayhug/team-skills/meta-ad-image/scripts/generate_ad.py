#!/usr/bin/env python3
"""
메타 광고 HTML을 고해상도 PNG 이미지로 변환하는 스크립트.

사용법:
    python3 generate_ad.py --html-file output/광고카피/ad.html --output-dir output/광고카피/
    python3 generate_ad.py --html-file ad.html --output-dir ./output --scale 2 --width 1080
"""

import argparse
import asyncio
import sys
from pathlib import Path


async def generate_ad_image(
    html_file: str,
    output_dir: str,
    scale: float = 2.0,
    viewport_width: int = 1080,
    format: str = "png"
):
    """
    HTML 광고 파일을 고해상도 PNG로 변환.

    Args:
        html_file: HTML 파일 경로
        output_dir: 출력 디렉토리
        scale: 이미지 스케일 (기본 2.0)
        viewport_width: 뷰포트 너비 (기본 1080px)
        format: 이미지 포맷 (png 또는 jpeg)
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: playwright가 설치되어 있지 않습니다.")
        print("설치: pip install playwright && playwright install chromium")
        sys.exit(1)

    html_path = Path(html_file).resolve()
    if not html_path.exists():
        print(f"Error: HTML 파일을 찾을 수 없습니다: {html_file}")
        sys.exit(1)

    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    output_name = html_path.stem + f".{format}"
    output_file = output_path / output_name

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": viewport_width, "height": 900},
            device_scale_factor=scale
        )
        page = await context.new_page()

        file_url = f"file://{html_path}"
        print(f"Loading: {html_path}")
        await page.goto(file_url, wait_until="networkidle")
        await page.wait_for_timeout(1500)

        await page.screenshot(path=str(output_file), full_page=True, type=format)
        print(f"Saved: {output_file}")

        await browser.close()
        print("Done!")


def main():
    parser = argparse.ArgumentParser(
        description="메타 광고 HTML을 고해상도 이미지로 변환"
    )
    parser.add_argument(
        "--html-file", "-f",
        required=True,
        help="변환할 HTML 파일 경로"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./output/광고카피",
        help="이미지 저장 디렉토리 (기본: ./output/광고카피)"
    )
    parser.add_argument(
        "--scale", "-s",
        type=float,
        default=2.0,
        help="이미지 스케일 (기본: 2.0)"
    )
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=1080,
        help="뷰포트 너비 (기본: 1080px)"
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpeg"],
        default="png",
        help="이미지 포맷 (기본: png)"
    )

    args = parser.parse_args()

    asyncio.run(generate_ad_image(
        html_file=args.html_file,
        output_dir=args.output_dir,
        scale=args.scale,
        viewport_width=args.width,
        format=args.format
    ))


if __name__ == "__main__":
    main()
