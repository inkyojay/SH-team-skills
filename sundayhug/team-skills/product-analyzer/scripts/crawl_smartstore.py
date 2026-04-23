#!/usr/bin/env python3
"""
Product Analyzer - 스마트스토어 크롤링 스크립트
스마트스토어 상세페이지에서 제품 정보와 이미지를 추출합니다.

사용법:
    python crawl_smartstore.py "https://smartstore.naver.com/store/products/123" --output /tmp/result.json
"""

import argparse
import base64
import json
import re
import sys
from urllib.parse import urljoin, urlparse
from io import BytesIO

try:
    import requests
    from bs4 import BeautifulSoup
    from PIL import Image
except ImportError:
    print("필요한 패키지를 설치합니다...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                          "requests", "beautifulsoup4", "Pillow",
                          "--break-system-packages", "-q"])
    import requests
    from bs4 import BeautifulSoup
    from PIL import Image


def is_smartstore_url(url: str) -> bool:
    """스마트스토어 URL인지 확인"""
    parsed = urlparse(url)
    return "smartstore.naver.com" in parsed.netloc


def is_supported_url(url: str) -> bool:
    """지원되는 쇼핑몰 URL인지 확인"""
    parsed = urlparse(url)
    # 스마트스토어 및 일반 쇼핑몰 지원
    return parsed.scheme in ["http", "https"] and parsed.netloc


def download_image_as_base64(url: str, max_size: int = 1024) -> dict | None:
    """이미지를 다운로드하고 base64로 인코딩"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # 이미지 열기
        img = Image.open(BytesIO(response.content))

        # 이미지 리사이즈 (Claude Vision 최적화)
        if img.width > max_size or img.height > max_size:
            ratio = min(max_size / img.width, max_size / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)

        # RGBA를 RGB로 변환 (JPEG 저장용)
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')

        # base64 인코딩
        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=85)
        base64_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return {
            "url": url,
            "base64": base64_data,
            "media_type": "image/jpeg",
            "width": img.width,
            "height": img.height
        }
    except Exception as e:
        print(f"이미지 다운로드 실패: {url} - {e}")
        return None


def extract_product_info(soup, url: str) -> dict:
    """제품 기본 정보 추출"""
    info = {
        "url": url,
        "store_name": "",
        "product_name": "",
        "price": "",
        "original_price": "",
        "category": "",
        "rating": "",
        "review_count": ""
    }

    # URL에서 스토어명 추출
    parsed = urlparse(url)
    path_parts = parsed.path.strip('/').split('/')
    if path_parts:
        info["store_name"] = path_parts[0]

    # 제품명 (여러 선택자 시도)
    name_selectors = [
        "h3._22kNQuEXmb",  # 최신 스마트스토어
        ".product-title",
        "h1[class*='title']",
        ".prd_name",
        "meta[property='og:title']"
    ]
    for selector in name_selectors:
        elem = soup.select_one(selector)
        if elem:
            if selector.startswith("meta"):
                info["product_name"] = elem.get("content", "")
            else:
                info["product_name"] = elem.get_text(strip=True)
            break

    # OG 태그에서 제품명 백업
    if not info["product_name"]:
        og_title = soup.find("meta", property="og:title")
        if og_title:
            info["product_name"] = og_title.get("content", "").split(":")[0].strip()

    # 가격
    price_selectors = [
        "._1LY7DqCnwR",  # 최신 스마트스토어
        ".product-price",
        "[class*='price'] strong",
        ".sale_price",
        ".total_price"
    ]
    for selector in price_selectors:
        elem = soup.select_one(selector)
        if elem:
            price_text = elem.get_text(strip=True)
            # 숫자만 추출
            price_nums = re.findall(r'[\d,]+', price_text)
            if price_nums:
                info["price"] = price_nums[0] + "원"
            break

    # 카테고리
    category_selectors = [
        ".category_area a",
        "[class*='category']",
        "meta[property='product:category']"
    ]
    for selector in category_selectors:
        elem = soup.select_one(selector)
        if elem:
            if selector.startswith("meta"):
                info["category"] = elem.get("content", "")
            else:
                info["category"] = elem.get_text(strip=True)
            break

    return info


def extract_detail_images(soup, base_url: str) -> list:
    """상세페이지 이미지 URL 추출"""
    images = []
    seen_urls = set()

    # 상세 이미지 컨테이너 선택자들
    detail_selectors = [
        ".product-detail-content img",
        ".detail_img img",
        "[class*='detail'] img",
        ".se-component img",  # 스마트에디터 이미지
        ".product_detail img",
        "#productDetail img",
        ".content img"
    ]

    for selector in detail_selectors:
        for img in soup.select(selector):
            src = img.get("src") or img.get("data-src") or img.get("data-lazy-src")
            if not src:
                continue

            # 절대 URL로 변환
            full_url = urljoin(base_url, src)

            # 필터링: 아이콘, 로고, 작은 이미지 제외
            skip_patterns = ["icon", "logo", "button", "arrow", "close", "banner_ad"]
            if any(p in full_url.lower() for p in skip_patterns):
                continue

            # 중복 제거
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            # 이미지 확장자 확인
            if any(ext in full_url.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
                images.append({
                    "url": full_url,
                    "alt": img.get("alt", ""),
                    "type": "detail"
                })

    # 대표 이미지 (썸네일)
    thumbnail_selectors = [
        ".product-img img",
        "[class*='thumbnail'] img",
        "[class*='main-image'] img",
        "meta[property='og:image']"
    ]
    for selector in thumbnail_selectors:
        elem = soup.select_one(selector)
        if elem:
            if selector.startswith("meta"):
                thumb_url = elem.get("content", "")
            else:
                thumb_url = elem.get("src") or elem.get("data-src")

            if thumb_url and thumb_url not in seen_urls:
                images.insert(0, {
                    "url": urljoin(base_url, thumb_url),
                    "alt": "thumbnail",
                    "type": "thumbnail"
                })
            break

    return images


def crawl_smartstore(url: str, max_images: int = 10) -> dict:
    """쇼핑몰 상세페이지 크롤링 메인 함수"""

    if not is_supported_url(url):
        return {"error": "유효한 URL이 아닙니다."}

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        return {"error": f"페이지 로드 실패: {str(e)}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # 제품 정보 추출
    product_info = extract_product_info(soup, url)

    # 상세 이미지 URL 추출
    image_urls = extract_detail_images(soup, url)

    # 이미지 다운로드 및 base64 인코딩
    print(f"총 {len(image_urls)}개 이미지 발견, 최대 {max_images}개 다운로드 중...")

    images_with_base64 = []
    for i, img_info in enumerate(image_urls[:max_images]):
        print(f"  [{i+1}/{min(len(image_urls), max_images)}] {img_info['url'][:60]}...")
        base64_result = download_image_as_base64(img_info["url"])
        if base64_result:
            images_with_base64.append({
                **img_info,
                **base64_result
            })

    result = {
        "product_info": product_info,
        "images": images_with_base64,
        "image_count": len(images_with_base64),
        "raw_html_length": len(response.text)
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="스마트스토어 상세페이지 크롤링")
    parser.add_argument("url", help="스마트스토어 상품 URL")
    parser.add_argument("--output", "-o", default="smartstore_result.json",
                       help="출력 파일 경로")
    parser.add_argument("--max-images", "-m", type=int, default=10,
                       help="다운로드할 최대 이미지 수 (기본: 10)")

    args = parser.parse_args()

    print(f"스마트스토어 크롤링 시작: {args.url}")
    print("-" * 50)

    result = crawl_smartstore(args.url, args.max_images)

    if "error" in result:
        print(f"에러: {result['error']}")
        sys.exit(1)

    # base64 데이터 제외한 결과 저장 (용량 문제)
    result_for_save = {
        "product_info": result["product_info"],
        "images": [
            {k: v for k, v in img.items() if k != "base64"}
            for img in result["images"]
        ],
        "image_count": result["image_count"]
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result_for_save, f, ensure_ascii=False, indent=2)

    # base64 포함 전체 결과는 별도 파일로
    base64_output = args.output.replace(".json", "_with_base64.json")
    with open(base64_output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print("-" * 50)
    print(f"완료!")
    print(f"- 제품명: {result['product_info']['product_name']}")
    print(f"- 가격: {result['product_info']['price']}")
    print(f"- 이미지: {result['image_count']}개")
    print(f"- 결과 저장: {args.output}")
    print(f"- Base64 포함: {base64_output}")


if __name__ == "__main__":
    main()
