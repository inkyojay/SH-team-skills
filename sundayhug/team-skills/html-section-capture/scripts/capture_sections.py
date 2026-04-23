#!/usr/bin/env python3
"""
HTML 상세페이지를 섹션별로 고해상도 이미지로 캡처하는 스크립트.

사용법:
    python3 capture_sections.py --html-file input.html --output-dir ./output
    python3 capture_sections.py --html-file input.html --output-dir ./output --scale 3
    python3 capture_sections.py --html-file input.html --output-dir ./output --selectors "section,.product-section,div[class*='section']"
"""

import argparse
import asyncio
import os
import sys
import re
from pathlib import Path
from urllib.parse import urljoin


async def capture_html_sections(
    html_file: str,
    output_dir: str,
    scale: float = 2.0,
    viewport_width: int = 1440,
    selectors: str = None,
    full_page: bool = False,
    format: str = "png"
):
    """
    HTML 파일을 섹션별로 캡처하여 이미지로 저장.

    Args:
        html_file: HTML 파일 경로
        output_dir: 출력 디렉토리
        scale: 이미지 스케일 (기본 2.0 = 2배 해상도)
        viewport_width: 뷰포트 너비 (기본 1440px)
        selectors: 섹션 선택자 (쉼표로 구분, 기본값 사용시 None)
        full_page: 전체 페이지도 캡처할지 여부
        format: 이미지 포맷 (png 또는 jpeg)
    """
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        print("Error: playwright가 설치되어 있지 않습니다.")
        print("설치 명령어: pip install playwright && playwright install chromium")
        sys.exit(1)

    # 파일 경로 검증
    html_path = Path(html_file).resolve()
    if not html_path.exists():
        print(f"Error: HTML 파일을 찾을 수 없습니다: {html_file}")
        sys.exit(1)

    # 출력 디렉토리 생성
    output_path = Path(output_dir).resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    # 기본 섹션 선택자
    default_selectors = [
        "section",
        "[class*='section']",
        "[class*='Section']",
        "[class*='block']",
        "[class*='Block']",
        "article",
        "main > div",
    ]

    if selectors:
        section_selectors = [s.strip() for s in selectors.split(",")]
    else:
        section_selectors = default_selectors

    async with async_playwright() as p:
        # Chromium 브라우저 실행
        browser = await p.chromium.launch()

        # 고해상도를 위한 device scale factor 설정
        context = await browser.new_context(
            viewport={"width": viewport_width, "height": 900},
            device_scale_factor=scale
        )

        page = await context.new_page()

        # HTML 파일 로드
        file_url = f"file://{html_path}"
        print(f"Loading: {html_path}")
        await page.goto(file_url, wait_until="networkidle")

        # 모든 이미지 로딩 및 레이아웃 안정화 대기
        await page.wait_for_timeout(1000)

        # 전체 페이지 높이 계산
        page_height = await page.evaluate("document.body.scrollHeight")
        print(f"Page height: {page_height}px")

        # 전체 페이지 캡처 (옵션)
        if full_page:
            full_page_path = output_path / f"00_full_page.{format}"
            await page.screenshot(path=str(full_page_path), full_page=True, type=format)
            print(f"Saved: {full_page_path}")

        # 섹션 찾기
        sections = []
        for selector in section_selectors:
            try:
                elements = await page.query_selector_all(selector)
                for el in elements:
                    box = await el.bounding_box()
                    if box and box["height"] > 100:  # 최소 높이 100px 이상인 요소만
                        # 중복 체크 (비슷한 위치의 요소 제외)
                        is_duplicate = False
                        for existing in sections:
                            if (abs(existing["box"]["y"] - box["y"]) < 50 and
                                abs(existing["box"]["height"] - box["height"]) < 50):
                                is_duplicate = True
                                break
                        if not is_duplicate:
                            class_name = await el.get_attribute("class") or ""
                            tag_name = await el.evaluate("el => el.tagName.toLowerCase()")
                            sections.append({
                                "element": el,
                                "box": box,
                                "selector": selector,
                                "class": class_name,
                                "tag": tag_name
                            })
            except Exception as e:
                continue

        # Y 좌표로 정렬
        sections.sort(key=lambda x: x["box"]["y"])

        if not sections:
            print("Warning: 섹션을 찾지 못했습니다. 전체 페이지를 분할하여 캡처합니다.")
            # 전체 페이지를 일정 높이로 분할
            chunk_height = 1200  # 분할 높이

            num_chunks = int(page_height / chunk_height) + 1
            for i in range(num_chunks):
                y_start = i * chunk_height
                remaining_height = page_height - y_start
                if remaining_height < 100:
                    break

                actual_height = min(chunk_height, remaining_height)

                # 해당 위치로 스크롤
                await page.evaluate(f"window.scrollTo(0, {y_start})")
                await page.wait_for_timeout(300)

                img_path = output_path / f"{i+1:02d}_section.{format}"
                await page.screenshot(
                    path=str(img_path),
                    clip={"x": 0, "y": 0, "width": viewport_width, "height": actual_height},
                    type=format
                )
                print(f"Saved: {img_path} (y: {y_start}px, height: {actual_height}px)")
        else:
            print(f"Found {len(sections)} sections")

            # 각 섹션을 개별적으로 캡처 (element.screenshot 사용)
            for i, section in enumerate(sections):
                box = section["box"]

                # 파일명 생성 (클래스명 활용)
                class_name = section["class"].split()[0] if section["class"] else section["tag"]
                class_name = re.sub(r'[^\w\-]', '_', class_name)[:30]
                img_name = f"{i+1:02d}_{class_name}.{format}"
                img_path = output_path / img_name

                try:
                    # 요소를 뷰포트로 스크롤
                    await section["element"].scroll_into_view_if_needed()
                    await page.wait_for_timeout(200)

                    # 요소 직접 스크린샷
                    await section["element"].screenshot(path=str(img_path), type=format)
                    print(f"Saved: {img_path} (height: {int(box['height'])}px)")
                except Exception as e:
                    # 요소 스크린샷 실패시 전체 페이지에서 clip으로 시도
                    try:
                        # 해당 위치로 스크롤
                        await page.evaluate(f"window.scrollTo(0, {max(0, box['y'] - 50)})")
                        await page.wait_for_timeout(300)

                        # 현재 뷰포트에서의 상대 위치 계산
                        new_box = await section["element"].bounding_box()
                        if new_box:
                            clip = {
                                "x": max(0, new_box["x"] - 10),
                                "y": max(0, new_box["y"]),
                                "width": min(viewport_width, new_box["width"] + 20),
                                "height": min(new_box["height"] + 10, 900)
                            }
                            await page.screenshot(path=str(img_path), clip=clip, type=format)
                            print(f"Saved: {img_path} (height: {int(new_box['height'])}px) [fallback]")
                        else:
                            print(f"Skipped section {i+1}: element not visible")
                    except Exception as e2:
                        print(f"Error capturing section {i+1}: {e2}")

        await browser.close()
        print(f"\nDone! Images saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="HTML 상세페이지를 섹션별 고해상도 이미지로 변환"
    )
    parser.add_argument(
        "--html-file", "-f",
        required=True,
        help="변환할 HTML 파일 경로"
    )
    parser.add_argument(
        "--output-dir", "-o",
        default="./output",
        help="이미지 저장 디렉토리 (기본: ./output)"
    )
    parser.add_argument(
        "--scale", "-s",
        type=float,
        default=2.0,
        help="이미지 스케일 (기본: 2.0 = 2배 해상도, 3.0 = 3배 해상도)"
    )
    parser.add_argument(
        "--width", "-w",
        type=int,
        default=1440,
        help="뷰포트 너비 (기본: 1440px)"
    )
    parser.add_argument(
        "--selectors",
        help="섹션 CSS 선택자 (쉼표로 구분, 예: 'section,.product-block,div.content')"
    )
    parser.add_argument(
        "--full-page",
        action="store_true",
        help="전체 페이지 스크린샷도 함께 저장"
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpeg"],
        default="png",
        help="이미지 포맷 (기본: png)"
    )

    args = parser.parse_args()

    asyncio.run(capture_html_sections(
        html_file=args.html_file,
        output_dir=args.output_dir,
        scale=args.scale,
        viewport_width=args.width,
        selectors=args.selectors,
        full_page=args.full_page,
        format=args.format
    ))


if __name__ == "__main__":
    main()
