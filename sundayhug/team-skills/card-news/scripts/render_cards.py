#!/usr/bin/env python3
"""
카드뉴스 HTML을 이미지로 렌더링

Usage:
    python render_cards.py --input-dir ./cards --output-dir ./output
    python render_cards.py --html-file card1.html --output card1.png

Requirements:
    pip install playwright
    playwright install chromium

Note:
    첫 실행 시 playwright install chromium 명령으로 브라우저 설치 필요
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path


async def render_html_to_image(html_path: str, output_path: str, width: int = 1080, height: int = 1350) -> dict:
    """HTML 파일을 이미지로 렌더링"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return {
            'success': False,
            'error': 'playwright가 설치되어 있지 않습니다. pip install playwright && playwright install chromium'
        }

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': width, 'height': height})

            # HTML 파일 로드
            html_path = Path(html_path).absolute()
            await page.goto(f'file://{html_path}')

            # 폰트 로딩 대기
            await page.wait_for_timeout(500)

            # 스크린샷 저장
            await page.screenshot(path=output_path, type='png')
            await browser.close()

            return {
                'success': True,
                'output': output_path
            }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


async def render_directory(input_dir: str, output_dir: str, width: int = 1080, height: int = 1350) -> dict:
    """디렉토리 내 모든 HTML 파일을 이미지로 렌더링"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    html_files = sorted(input_path.glob('*.html'))

    if not html_files:
        return {
            'success': False,
            'error': f'{input_dir}에 HTML 파일이 없습니다.'
        }

    results = []
    for html_file in html_files:
        output_file = output_path / f'{html_file.stem}.png'
        result = await render_html_to_image(str(html_file), str(output_file), width, height)
        results.append({
            'input': str(html_file),
            **result
        })

    success_count = sum(1 for r in results if r.get('success'))

    return {
        'success': success_count == len(results),
        'total': len(results),
        'rendered': success_count,
        'results': results
    }


def main():
    parser = argparse.ArgumentParser(description='카드뉴스 HTML을 이미지로 렌더링')
    parser.add_argument('--html-file', help='단일 HTML 파일 경로')
    parser.add_argument('--output', help='출력 이미지 경로 (단일 파일용)')
    parser.add_argument('--input-dir', help='HTML 파일들이 있는 디렉토리')
    parser.add_argument('--output-dir', help='출력 디렉토리')
    parser.add_argument('--width', type=int, default=1080, help='이미지 너비 (기본: 1080)')
    parser.add_argument('--height', type=int, default=1350, help='이미지 높이 (기본: 1350)')

    args = parser.parse_args()

    if args.html_file:
        output = args.output or args.html_file.replace('.html', '.png')
        result = asyncio.run(render_html_to_image(args.html_file, output, args.width, args.height))
    elif args.input_dir:
        output_dir = args.output_dir or f'{args.input_dir}_output'
        result = asyncio.run(render_directory(args.input_dir, output_dir, args.width, args.height))
    else:
        print(json.dumps({'error': '--html-file 또는 --input-dir를 지정해주세요.'}, ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
