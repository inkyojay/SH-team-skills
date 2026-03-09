#!/usr/bin/env python3
"""
프로모션 HTML → PNG 배치 변환 스크립트.

input-dir 내 모든 .html 파일을 순회하여 각 HTML의 body width/height를 파싱,
Playwright로 스크린샷 → output-dir에 동일 파일명.png 저장.

사용법:
    python3 render_all.py --input-dir ./html/ --output-dir ./png/
    python3 render_all.py --input-dir ./html/ --output-dir ./png/ --scale 2
    python3 render_all.py --input-dir ./html/ --output-dir ./png/ --scale 2 --concurrency 4
"""

import argparse
import asyncio
import re
import sys
from pathlib import Path


def parse_body_dimensions(html_content: str) -> tuple[int, int]:
    """HTML에서 body의 width와 height를 파싱합니다."""
    width = 1080
    height = 1350

    # body style에서 width/height 추출
    body_match = re.search(r'body\s*\{[^}]*\}', html_content, re.DOTALL)
    if body_match:
        body_style = body_match.group()
        w_match = re.search(r'width:\s*(\d+)px', body_style)
        h_match = re.search(r'height:\s*(\d+)px', body_style)
        if w_match:
            width = int(w_match.group(1))
        if h_match:
            height = int(h_match.group(1))

    # inline style에서도 확인
    inline_match = re.search(r'<body[^>]*style="([^"]*)"', html_content)
    if inline_match:
        style = inline_match.group(1)
        w_match = re.search(r'width:\s*(\d+)px', style)
        h_match = re.search(r'height:\s*(\d+)px', style)
        if w_match:
            width = int(w_match.group(1))
        if h_match:
            height = int(h_match.group(1))

    return width, height


async def render_single(page, html_path: Path, output_path: Path, scale: float):
    """단일 HTML 파일을 PNG로 변환합니다."""
    html_content = html_path.read_text(encoding='utf-8')
    width, height = parse_body_dimensions(html_content)

    await page.set_viewport_size({"width": width, "height": height})

    file_url = f"file://{html_path.resolve()}"
    await page.goto(file_url, wait_until="networkidle")
    await page.wait_for_timeout(1000)

    output_file = output_path / f"{html_path.stem}.png"
    await page.screenshot(
        path=str(output_file),
        full_page=False,
        clip={"x": 0, "y": 0, "width": width, "height": height},
        type="png"
    )
    print(f"  ✅ {html_path.name} → {output_file.name} ({width}×{height})")
    return output_file


async def render_batch(
    input_dir: str,
    output_dir: str,
    scale: float = 2.0,
    concurrency: int = 3
):
    """HTML 파일들을 배치로 PNG 변환합니다."""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: playwright가 설치되어 있지 않습니다.")
        print("설치: pip install playwright && playwright install chromium")
        sys.exit(1)

    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    html_files = sorted(input_path.glob("*.html"))
    if not html_files:
        print(f"Error: {input_dir}에 HTML 파일이 없습니다.")
        sys.exit(1)

    print(f"📁 입력: {input_path}")
    print(f"📁 출력: {output_path}")
    print(f"📐 스케일: {scale}x")
    print(f"📄 파일 수: {len(html_files)}개")
    print(f"⚡ 동시 처리: {concurrency}개")
    print("─" * 50)

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        semaphore = asyncio.Semaphore(concurrency)
        results = []

        async def render_with_limit(html_file):
            async with semaphore:
                context = await browser.new_context(
                    device_scale_factor=scale,
                    viewport={"width": 1080, "height": 1350}
                )
                page = await context.new_page()
                try:
                    result = await render_single(page, html_file, output_path, scale)
                    results.append(result)
                finally:
                    await context.close()

        tasks = [render_with_limit(f) for f in html_files]
        await asyncio.gather(*tasks)

        await browser.close()

    print("─" * 50)
    print(f"✅ 완료: {len(results)}/{len(html_files)}개 변환됨")
    return results


def main():
    parser = argparse.ArgumentParser(
        description="프로모션 HTML → PNG 배치 변환"
    )
    parser.add_argument(
        "--input-dir", "-i",
        required=True,
        help="HTML 파일이 있는 디렉토리"
    )
    parser.add_argument(
        "--output-dir", "-o",
        required=True,
        help="PNG 저장 디렉토리"
    )
    parser.add_argument(
        "--scale", "-s",
        type=float,
        default=2.0,
        help="이미지 스케일 (기본: 2.0)"
    )
    parser.add_argument(
        "--concurrency", "-c",
        type=int,
        default=3,
        help="동시 렌더링 수 (기본: 3)"
    )

    args = parser.parse_args()

    asyncio.run(render_batch(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        scale=args.scale,
        concurrency=args.concurrency
    ))


if __name__ == "__main__":
    main()
