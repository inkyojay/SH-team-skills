#!/usr/bin/env python3
"""
Google Gemini API (Imagen 3)를 활용한 블로그 이미지 자동 생성 스크립트

사용법:
  python google_imagen.py \
    --api-key YOUR_GOOGLE_API_KEY \
    --prompts prompts.json \
    --output-dir blog_images/ \
    --count 4

prompts.json 형식:
[
  {
    "id": "image_01",
    "description": "대표 이미지 - 제품 전체",
    "prompt": "Cozy baby sleeping bag, soft pastel colors, white background...",
    "filename": "신생아-슬리핑백-대표이미지.png"
  },
  ...
]

API 키 발급: https://aistudio.google.com → Get API key
무료 티어: 분당 10회 요청 가능
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests


# Gemini API Imagen endpoint
GEMINI_IMAGEN_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"


def generate_image(api_key: str, prompt: str, aspect_ratio: str = "4:3") -> bytes | None:
    """
    Google Imagen 3로 이미지 생성
    aspect_ratio: "1:1", "4:3", "16:9", "3:4", "9:16"
    """
    url = f"{GEMINI_IMAGEN_URL}?key={api_key}"
    payload = {
        "instances": [
            {
                "prompt": prompt
            }
        ],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": aspect_ratio,
            "safetyFilterLevel": "BLOCK_SOME",
            "personGeneration": "DONT_ALLOW"  # 실제 사람 얼굴 생성 차단
        }
    }

    try:
        response = requests.post(url, json=payload, timeout=60)

        if response.status_code == 200:
            data = response.json()
            predictions = data.get("predictions", [])
            if predictions and "bytesBase64Encoded" in predictions[0]:
                return base64.b64decode(predictions[0]["bytesBase64Encoded"])
            else:
                print(f"  ⚠️  이미지 데이터 없음: {data}")
                return None
        else:
            print(f"  ❌ API 오류: HTTP {response.status_code}")
            error_detail = response.json().get("error", {}).get("message", response.text[:200])
            print(f"     {error_detail}")
            return None

    except Exception as e:
        print(f"  ❌ 요청 실패: {e}")
        return None


def generate_prompt_from_topic(topic: str, image_type: str, brand: str = "썬데이허그") -> str:
    """
    블로그 주제와 이미지 유형에 맞는 프롬프트 자동 생성
    image_type: "hero", "lifestyle", "detail", "infographic"
    """
    base_style = (
        "professional product photography, clean background, "
        "soft natural lighting, high resolution, commercial quality, "
        "no text overlay, no watermark"
    )

    brand_style = (
        "soft mint green and cream color palette, "
        "cozy and gentle atmosphere, premium Korean baby brand aesthetic"
    ) if brand else ""

    type_styles = {
        "hero": f"Full product shot, {topic}, centered composition, white or light background",
        "lifestyle": f"Lifestyle photography of {topic}, cozy home setting, warm morning light, serene atmosphere",
        "detail": f"Close-up macro shot of {topic}, texture detail, soft bokeh background",
        "infographic": f"Flat lay arrangement of {topic} items, top-down view, minimal clean composition",
    }

    style = type_styles.get(image_type, type_styles["hero"])
    parts = [style, brand_style, base_style]
    return ", ".join(p for p in parts if p)


def generate_blog_images(api_key: str, prompts: list, output_dir: str) -> list:
    """블로그용 이미지 일괄 생성"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    results = []

    print(f"\n🎨 총 {len(prompts)}개 이미지 생성 시작...")

    for i, prompt_info in enumerate(prompts, 1):
        image_id = prompt_info.get("id", f"image_{i:02d}")
        description = prompt_info.get("description", f"이미지 {i}")
        prompt = prompt_info.get("prompt", "")
        filename = prompt_info.get("filename", f"{image_id}.png")
        aspect_ratio = prompt_info.get("aspect_ratio", "4:3")

        print(f"\n  [{i}/{len(prompts)}] {description}")
        print(f"  프롬프트: {prompt[:80]}...")

        if not prompt:
            print("  ⚠️  프롬프트가 없습니다. SKIP")
            continue

        image_bytes = generate_image(api_key, prompt, aspect_ratio)

        if image_bytes:
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            file_size = len(image_bytes) / 1024
            print(f"  ✅ 저장완료: {filepath} ({file_size:.0f}KB)")
            results.append({
                "id": image_id,
                "description": description,
                "filename": filename,
                "filepath": filepath,
                "status": "success",
                "file_size_kb": round(file_size, 1)
            })
        else:
            print(f"  ❌ 생성 실패: {description}")
            results.append({
                "id": image_id,
                "description": description,
                "filename": filename,
                "status": "failed"
            })

        # Rate limit (무료 티어: 분당 10회)
        if i < len(prompts):
            print(f"  ⏳ 7초 대기 (Rate limit 방지)...")
            time.sleep(7)

    return results


def create_sample_prompts(keyword: str, blog_type: str = "정보성") -> list:
    """키워드 기반 기본 프롬프트 자동 생성"""

    prompts = [
        {
            "id": "image_01",
            "description": f"대표 이미지 - {keyword}",
            "prompt": f"{keyword} product, soft pastel colors, white clean background, natural soft lighting, centered composition, commercial product photography, high resolution, no text",
            "filename": f"01-{keyword.replace(' ', '-')}-대표.png",
            "aspect_ratio": "4:3"
        },
        {
            "id": "image_02",
            "description": f"라이프스타일 이미지 - {keyword} 사용 장면",
            "prompt": f"Lifestyle scene with {keyword}, cozy home interior, warm soft morning light, comfortable and safe atmosphere, no faces shown, serene nursery setting, professional photography",
            "filename": f"02-{keyword.replace(' ', '-')}-라이프스타일.png",
            "aspect_ratio": "4:3"
        },
        {
            "id": "image_03",
            "description": f"디테일/비교 이미지 - {keyword} 상세",
            "prompt": f"Close-up detail of {keyword}, premium quality materials, soft texture, top-down flat lay, white background, commercial product shot, crisp and clear",
            "filename": f"03-{keyword.replace(' ', '-')}-디테일.png",
            "aspect_ratio": "1:1"
        },
        {
            "id": "image_04",
            "description": f"마무리 이미지 - {keyword} 전체",
            "prompt": f"{keyword} arranged beautifully, premium minimal presentation, soft pastel background, gift-worthy appearance, warm and inviting, high-end product styling",
            "filename": f"04-{keyword.replace(' ', '-')}-마무리.png",
            "aspect_ratio": "4:3"
        }
    ]
    return prompts


def main():
    parser = argparse.ArgumentParser(description="Google Imagen 3 블로그 이미지 생성")
    parser.add_argument("--api-key", required=True, help="Google AI Studio API 키")
    parser.add_argument("--prompts", help="프롬프트 JSON 파일 경로 (없으면 --keyword로 자동 생성)")
    parser.add_argument("--keyword", help="블로그 핵심 키워드 (자동 프롬프트 생성 시)")
    parser.add_argument("--output-dir", default="blog_images", help="이미지 저장 폴더")
    parser.add_argument("--count", type=int, default=4, help="생성할 이미지 수")
    parser.add_argument("--test", action="store_true", help="API 연결 테스트만 수행")

    args = parser.parse_args()

    # API 연결 테스트
    if args.test:
        print("🧪 Google Imagen API 연결 테스트 중...")
        test_image = generate_image(
            args.api_key,
            "Simple white background with a soft mint green circle, minimal style",
            "1:1"
        )
        if test_image:
            print("✅ API 연결 성공! 이미지 생성 가능합니다.")
        else:
            print("❌ API 연결 실패. API 키를 확인해주세요.")
        return

    # 프롬프트 로드 or 자동 생성
    if args.prompts:
        with open(args.prompts, "r", encoding="utf-8") as f:
            prompts = json.load(f)
        prompts = prompts[:args.count]
    elif args.keyword:
        print(f"💡 [{args.keyword}] 키워드로 프롬프트 자동 생성")
        prompts = create_sample_prompts(args.keyword)[:args.count]

        # 프롬프트 파일 저장
        prompts_file = "auto_prompts.json"
        with open(prompts_file, "w", encoding="utf-8") as f:
            json.dump(prompts, f, ensure_ascii=False, indent=2)
        print(f"   생성된 프롬프트: {prompts_file} (수정 후 재실행 가능)")
    else:
        print("❌ --prompts 또는 --keyword 중 하나를 지정해주세요.")
        sys.exit(1)

    # 이미지 생성
    results = generate_blog_images(args.api_key, prompts, args.output_dir)

    # 결과 요약
    success = [r for r in results if r.get("status") == "success"]
    failed = [r for r in results if r.get("status") == "failed"]

    print(f"\n{'='*55}")
    print(f"🎨 이미지 생성 완료")
    print(f"{'='*55}")
    print(f"  성공: {len(success)}개")
    print(f"  실패: {len(failed)}개")
    print(f"  저장 위치: {args.output_dir}/")

    if success:
        print(f"\n생성된 파일:")
        for r in success:
            print(f"  ✅ {r['filename']} ({r.get('file_size_kb', '?')}KB)")

    # 결과 JSON 저장
    result_file = os.path.join(args.output_dir, "generation_results.json")
    with open(result_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n📄 결과 리포트: {result_file}")
    print(f"\n💡 다음 단계: 생성된 이미지를 Claude에 업로드하면 블로그 완성본에 삽입됩니다.")


if __name__ == "__main__":
    main()
