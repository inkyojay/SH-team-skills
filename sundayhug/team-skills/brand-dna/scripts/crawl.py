#!/usr/bin/env python3
"""
Brand DNA Extractor - 웹 크롤링 스크립트
웹사이트에서 브랜드 관련 정보를 추출합니다.

사용법:
    python crawl.py "https://example.com" --output /tmp/crawl_result.json
"""

import argparse
import json
import re
import sys
from urllib.parse import urljoin, urlparse
from collections import Counter

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("필요한 패키지를 설치합니다...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "requests", "beautifulsoup4", "--break-system-packages", "-q"])
    import requests
    from bs4 import BeautifulSoup


def extract_texts(soup, url):
    """페이지에서 브랜드 관련 텍스트 추출"""
    texts = {
        "title": "",
        "meta_description": "",
        "headings": [],
        "taglines": [],
        "about": [],
        "product_descriptions": [],
        "all_text": ""
    }
    
    # 타이틀
    if soup.title:
        texts["title"] = soup.title.string or ""
    
    # 메타 설명
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        texts["meta_description"] = meta_desc.get("content", "")
    
    # OG 태그
    og_title = soup.find("meta", property="og:title")
    og_desc = soup.find("meta", property="og:description")
    if og_title:
        texts["taglines"].append(og_title.get("content", ""))
    if og_desc:
        texts["taglines"].append(og_desc.get("content", ""))
    
    # 헤딩 태그
    for tag in ["h1", "h2", "h3"]:
        for heading in soup.find_all(tag):
            text = heading.get_text(strip=True)
            if text and len(text) > 3:
                texts["headings"].append(text)
    
    # 슬로건/태그라인 추정 (짧은 텍스트)
    for selector in [".tagline", ".slogan", ".hero-text", ".banner-text", 
                     "[class*='tagline']", "[class*='slogan']", "[class*='hero']"]:
        for el in soup.select(selector):
            text = el.get_text(strip=True)
            if text and 5 < len(text) < 200:
                texts["taglines"].append(text)
    
    # About 섹션
    for selector in ["#about", ".about", "[class*='about']", 
                     "#story", ".story", "[class*='mission']"]:
        for el in soup.select(selector):
            text = el.get_text(strip=True)
            if text and len(text) > 50:
                texts["about"].append(text[:1000])
    
    # 제품 설명
    for selector in [".product-description", "[class*='product'] p", 
                     ".item-description", "[class*='description']"]:
        for el in soup.select(selector):
            text = el.get_text(strip=True)
            if text and len(text) > 30:
                texts["product_descriptions"].append(text[:500])
    
    # 전체 텍스트 (분석용)
    body = soup.find("body")
    if body:
        # 스크립트, 스타일 제거
        for tag in body.find_all(["script", "style", "noscript"]):
            tag.decompose()
        texts["all_text"] = body.get_text(separator=" ", strip=True)[:5000]
    
    return texts


def extract_images(soup, base_url):
    """페이지에서 이미지 URL 추출"""
    images = []
    
    # img 태그
    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src")
        if src:
            full_url = urljoin(base_url, src)
            images.append({
                "url": full_url,
                "alt": img.get("alt", ""),
                "type": "image"
            })
    
    # 배경 이미지 (인라인 스타일)
    for el in soup.find_all(style=True):
        style = el.get("style", "")
        urls = re.findall(r'url\(["\']?([^"\')\s]+)["\']?\)', style)
        for url in urls:
            full_url = urljoin(base_url, url)
            images.append({
                "url": full_url,
                "type": "background"
            })
    
    # OG 이미지
    og_image = soup.find("meta", property="og:image")
    if og_image:
        images.append({
            "url": og_image.get("content", ""),
            "type": "og_image"
        })
    
    # 로고 추정
    for selector in [".logo img", "[class*='logo'] img", "header img", 
                     "img[alt*='logo']", "img[class*='logo']"]:
        for img in soup.select(selector):
            src = img.get("src") or img.get("data-src")
            if src:
                images.append({
                    "url": urljoin(base_url, src),
                    "type": "logo"
                })
    
    # 중복 제거
    seen = set()
    unique_images = []
    for img in images:
        if img["url"] not in seen and img["url"].startswith("http"):
            seen.add(img["url"])
            unique_images.append(img)
    
    return unique_images[:50]  # 최대 50개


def extract_colors(soup):
    """페이지에서 색상 추출 (CSS에서)"""
    colors = []
    
    # 인라인 스타일에서 색상 추출
    color_pattern = r'#[0-9A-Fa-f]{3,6}|rgb\([^)]+\)|rgba\([^)]+\)'
    
    for el in soup.find_all(style=True):
        style = el.get("style", "")
        found = re.findall(color_pattern, style)
        colors.extend(found)
    
    # style 태그에서 색상 추출
    for style_tag in soup.find_all("style"):
        if style_tag.string:
            found = re.findall(color_pattern, style_tag.string)
            colors.extend(found)
    
    # 빈도 계산
    color_counts = Counter(colors)
    
    # 상위 색상 반환
    top_colors = []
    for color, count in color_counts.most_common(20):
        if color.startswith("#"):
            top_colors.append({"color": color, "count": count})
        elif color.startswith("rgb"):
            # RGB를 HEX로 변환
            try:
                nums = re.findall(r'\d+', color)
                if len(nums) >= 3:
                    r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    top_colors.append({"color": hex_color, "count": count})
            except:
                pass
    
    return top_colors


def extract_metadata(soup, url):
    """메타데이터 추출"""
    metadata = {
        "url": url,
        "domain": urlparse(url).netloc,
        "title": "",
        "keywords": [],
        "og_data": {}
    }
    
    if soup.title:
        metadata["title"] = soup.title.string or ""
    
    # 키워드
    keywords_meta = soup.find("meta", attrs={"name": "keywords"})
    if keywords_meta:
        keywords = keywords_meta.get("content", "").split(",")
        metadata["keywords"] = [k.strip() for k in keywords if k.strip()]
    
    # OG 데이터
    for og in soup.find_all("meta", property=re.compile(r"^og:")):
        prop = og.get("property", "").replace("og:", "")
        metadata["og_data"][prop] = og.get("content", "")
    
    return metadata


def crawl_url(url):
    """URL 크롤링 메인 함수"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
    except Exception as e:
        return {"error": str(e)}
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    result = {
        "url": url,
        "texts": extract_texts(soup, url),
        "images": extract_images(soup, url),
        "colors": extract_colors(soup),
        "metadata": extract_metadata(soup, url),
        "brand_name": ""
    }
    
    # 브랜드명 추정
    if result["texts"]["title"]:
        # 타이틀에서 브랜드명 추출 (보통 | 또는 - 앞에 있음)
        title = result["texts"]["title"]
        for sep in ["|", "-", "–", "—", ":"]:
            if sep in title:
                result["brand_name"] = title.split(sep)[0].strip()
                break
        if not result["brand_name"]:
            result["brand_name"] = title.split()[0] if title else ""
    
    return result


def main():
    parser = argparse.ArgumentParser(description="웹사이트 브랜드 정보 크롤링")
    parser.add_argument("url", help="크롤링할 URL")
    parser.add_argument("--output", "-o", default="crawl_result.json", 
                       help="출력 파일 경로")
    
    args = parser.parse_args()
    
    print(f"크롤링 시작: {args.url}")
    result = crawl_url(args.url)
    
    if "error" in result:
        print(f"에러: {result['error']}")
        sys.exit(1)
    
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"완료! 결과 저장: {args.output}")
    print(f"- 브랜드명: {result['brand_name']}")
    print(f"- 이미지: {len(result['images'])}개")
    print(f"- 색상: {len(result['colors'])}개")
    

if __name__ == "__main__":
    main()
