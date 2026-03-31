#!/usr/bin/env python3
"""
Brand DNA Extractor - 무드보드 생성 스크립트
수집된 이미지와 브랜드 요소로 무드보드 이미지를 생성합니다.

사용법:
    python generate_moodboard.py \
        --images /tmp/images/ \
        --colors "#1E40AF,#7C3AED,#059669" \
        --keywords "혁신,신뢰,프리미엄" \
        --brand "BrandName" \
        --template grid \
        --output /tmp/moodboard.png
"""

import argparse
import os
import sys
import json
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("필요한 패키지를 설치합니다...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "Pillow", "--break-system-packages", "-q"])
    from PIL import Image, ImageDraw, ImageFont

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", 
                          "requests", "--break-system-packages", "-q"])
    import requests


def hex_to_rgb(hex_color):
    """HEX 색상을 RGB로 변환"""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def download_image(url, save_path):
    """이미지 URL 다운로드"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True
    except:
        return False


def load_images(image_source, max_images=9):
    """이미지 로드 (폴더 또는 JSON 파일)"""
    images = []
    
    if os.path.isdir(image_source):
        # 폴더에서 이미지 로드
        for ext in ["*.jpg", "*.jpeg", "*.png", "*.webp"]:
            for img_path in Path(image_source).glob(ext):
                try:
                    img = Image.open(img_path).convert("RGB")
                    images.append(img)
                except:
                    continue
                if len(images) >= max_images:
                    break
            if len(images) >= max_images:
                break
    
    elif image_source.endswith(".json"):
        # JSON 파일에서 이미지 URL 로드
        with open(image_source, "r") as f:
            data = json.load(f)
        
        image_urls = []
        if isinstance(data, list):
            image_urls = [item.get("url") for item in data if item.get("url")]
        elif isinstance(data, dict) and "images" in data:
            image_urls = [item.get("url") for item in data["images"] if item.get("url")]
        
        temp_dir = "/tmp/moodboard_images"
        os.makedirs(temp_dir, exist_ok=True)
        
        for i, url in enumerate(image_urls[:max_images]):
            temp_path = f"{temp_dir}/img_{i}.jpg"
            if download_image(url, temp_path):
                try:
                    img = Image.open(temp_path).convert("RGB")
                    images.append(img)
                except:
                    continue
    
    return images


def create_grid_moodboard(images, colors, keywords, brand_name, size=(1920, 1080)):
    """그리드 레이아웃 무드보드 생성"""
    width, height = size
    canvas = Image.new("RGB", size, (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    # 여백 설정
    margin = 40
    gap = 20
    
    # 이미지 영역 (좌측 70%)
    img_area_width = int((width - margin * 2) * 0.7)
    img_area_height = height - margin * 2 - 100  # 상단 헤더 공간
    
    # 헤더 (브랜드명)
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
    except:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()
    
    # 브랜드명 그리기
    if brand_name:
        draw.text((margin, margin), brand_name, fill=(30, 30, 30), font=font_large)
    
    # 이미지 그리드 (3x2 또는 3x3)
    header_height = 100
    start_y = margin + header_height
    
    if images:
        cols = 3
        rows = min(2, (len(images) + cols - 1) // cols)
        
        cell_width = (img_area_width - gap * (cols - 1)) // cols
        cell_height = (img_area_height - gap * (rows - 1)) // rows
        
        for i, img in enumerate(images[:cols * rows]):
            row = i // cols
            col = i % cols
            
            x = margin + col * (cell_width + gap)
            y = start_y + row * (cell_height + gap)
            
            # 이미지 리사이즈 (cover 방식)
            img_ratio = img.width / img.height
            cell_ratio = cell_width / cell_height
            
            if img_ratio > cell_ratio:
                new_height = cell_height
                new_width = int(cell_height * img_ratio)
            else:
                new_width = cell_width
                new_height = int(cell_width / img_ratio)
            
            resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # 중앙 크롭
            left = (new_width - cell_width) // 2
            top = (new_height - cell_height) // 2
            cropped = resized.crop((left, top, left + cell_width, top + cell_height))
            
            canvas.paste(cropped, (x, y))
    
    # 우측 사이드바 (색상 팔레트 + 키워드)
    sidebar_x = margin + img_area_width + margin
    sidebar_width = width - sidebar_x - margin
    
    # 색상 팔레트
    if colors:
        draw.text((sidebar_x, start_y), "Color Palette", fill=(100, 100, 100), font=font_medium)
        
        swatch_size = 50
        swatch_y = start_y + 40
        
        for i, color in enumerate(colors[:5]):
            swatch_x = sidebar_x + (i % 3) * (swatch_size + 10)
            swatch_row = i // 3
            y_pos = swatch_y + swatch_row * (swatch_size + 30)
            
            rgb = hex_to_rgb(color)
            draw.rectangle(
                [swatch_x, y_pos, swatch_x + swatch_size, y_pos + swatch_size],
                fill=rgb,
                outline=(200, 200, 200)
            )
            draw.text((swatch_x, y_pos + swatch_size + 5), color.upper(), 
                     fill=(100, 100, 100), font=font_small)
    
    # 키워드
    if keywords:
        keyword_y = start_y + 250
        draw.text((sidebar_x, keyword_y), "Keywords", fill=(100, 100, 100), font=font_medium)
        
        for i, keyword in enumerate(keywords[:8]):
            y_pos = keyword_y + 40 + i * 35
            
            # 키워드에 색상 적용
            if colors:
                keyword_color = hex_to_rgb(colors[i % len(colors)])
            else:
                keyword_color = (50, 50, 50)
            
            draw.text((sidebar_x, y_pos), f"• {keyword}", fill=keyword_color, font=font_medium)
    
    return canvas


def create_presentation_moodboard(images, colors, keywords, brand_name, size=(1920, 1080)):
    """프레젠테이션용 무드보드"""
    width, height = size
    canvas = Image.new("RGB", size, (250, 250, 250))
    draw = ImageDraw.Draw(canvas)
    
    margin = 60
    
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
        font_subtitle = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        font_body = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
    except:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_body = ImageFont.load_default()
    
    # 상단 헤더
    if brand_name:
        draw.text((margin, margin), brand_name, fill=(30, 30, 30), font=font_title)
        draw.text((margin, margin + 70), "Brand Moodboard", fill=(120, 120, 120), font=font_subtitle)
    
    # 메인 이미지 (좌측 상단, 큰 이미지)
    main_img_x = margin
    main_img_y = margin + 140
    main_img_w = int((width - margin * 3) * 0.5)
    main_img_h = int((height - main_img_y - margin) * 0.6)
    
    if images:
        img = images[0]
        img_ratio = img.width / img.height
        cell_ratio = main_img_w / main_img_h
        
        if img_ratio > cell_ratio:
            new_height = main_img_h
            new_width = int(main_img_h * img_ratio)
        else:
            new_width = main_img_w
            new_height = int(main_img_w / img_ratio)
        
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - main_img_w) // 2
        top = (new_height - main_img_h) // 2
        cropped = resized.crop((left, top, left + main_img_w, top + main_img_h))
        canvas.paste(cropped, (main_img_x, main_img_y))
    
    # 작은 이미지들 (좌측 하단)
    small_img_y = main_img_y + main_img_h + 20
    small_img_h = height - small_img_y - margin
    small_img_w = (main_img_w - 20) // 2
    
    for i, img in enumerate(images[1:3]):
        x = main_img_x + i * (small_img_w + 20)
        
        img_ratio = img.width / img.height
        cell_ratio = small_img_w / small_img_h
        
        if img_ratio > cell_ratio:
            new_height = small_img_h
            new_width = int(small_img_h * img_ratio)
        else:
            new_width = small_img_w
            new_height = int(small_img_w / img_ratio)
        
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        left = (new_width - small_img_w) // 2
        top = (new_height - small_img_h) // 2
        cropped = resized.crop((left, top, left + small_img_w, top + small_img_h))
        canvas.paste(cropped, (x, small_img_y))
    
    # 우측 패널
    panel_x = main_img_x + main_img_w + margin
    panel_y = main_img_y
    
    # 색상 팔레트
    draw.text((panel_x, panel_y), "Color Palette", fill=(80, 80, 80), font=font_subtitle)
    
    swatch_y = panel_y + 50
    swatch_size = 60
    
    for i, color in enumerate(colors[:5]):
        x = panel_x + i * (swatch_size + 15)
        rgb = hex_to_rgb(color)
        draw.rectangle([x, swatch_y, x + swatch_size, swatch_y + swatch_size], 
                      fill=rgb, outline=(220, 220, 220))
        draw.text((x, swatch_y + swatch_size + 8), color.upper()[:7], 
                 fill=(120, 120, 120), font=font_body)
    
    # 키워드 섹션
    keyword_y = swatch_y + 120
    draw.text((panel_x, keyword_y), "Brand Keywords", fill=(80, 80, 80), font=font_subtitle)
    
    for i, keyword in enumerate(keywords[:6]):
        y = keyword_y + 50 + i * 40
        color = hex_to_rgb(colors[i % len(colors)]) if colors else (60, 60, 60)
        draw.text((panel_x, y), f"→ {keyword}", fill=color, font=font_body)
    
    return canvas


def main():
    parser = argparse.ArgumentParser(description="무드보드 이미지 생성")
    parser.add_argument("--images", "-i", required=True, 
                       help="이미지 폴더 경로 또는 JSON 파일")
    parser.add_argument("--colors", "-c", default="",
                       help="색상 HEX 코드 (쉼표 구분)")
    parser.add_argument("--keywords", "-k", default="",
                       help="키워드 (쉼표 구분)")
    parser.add_argument("--brand", "-b", default="Brand",
                       help="브랜드명")
    parser.add_argument("--template", "-t", default="grid",
                       choices=["grid", "presentation", "minimal"],
                       help="무드보드 템플릿")
    parser.add_argument("--output", "-o", default="moodboard.png",
                       help="출력 파일 경로")
    parser.add_argument("--width", type=int, default=1920)
    parser.add_argument("--height", type=int, default=1080)
    
    args = parser.parse_args()
    
    # 입력 파싱
    colors = [c.strip() for c in args.colors.split(",") if c.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    
    print(f"이미지 로드 중: {args.images}")
    images = load_images(args.images)
    print(f"로드된 이미지: {len(images)}개")
    
    if not images:
        print("경고: 이미지가 없습니다. 빈 무드보드를 생성합니다.")
    
    # 무드보드 생성
    size = (args.width, args.height)
    
    if args.template == "presentation":
        moodboard = create_presentation_moodboard(images, colors, keywords, args.brand, size)
    else:  # grid (default)
        moodboard = create_grid_moodboard(images, colors, keywords, args.brand, size)
    
    # 저장
    moodboard.save(args.output, quality=95)
    print(f"무드보드 생성 완료: {args.output}")


if __name__ == "__main__":
    main()
