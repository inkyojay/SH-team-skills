#!/usr/bin/env python3
"""
카드 배너 더미 이미지 생성 (Google Imagen API)

배너 사이즈:
  1번 (큰 카드)  PC: 1200x525  Mobile: 750x562
  2번 (작은 카드) PC: 600x600   Mobile: 375x375
  3번 (작은 카드) PC: 600x600   Mobile: 375x375
"""

import base64
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
    import requests

try:
    from PIL import Image
    import io
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow", "-q"])
    from PIL import Image
    import io


IMAGEN_URL = "https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict"

# 배너별 설정
BANNERS = [
    {
        "id": "banner_1_pc",
        "label": "1번 큰 카드 PC",
        "size": (1200, 525),
        "aspect_ratio": "16:9",
        "prompt": "Bright cheerful banner with yellow and green banana theme, tropical summer feel, clean minimal design, no text, soft gradient background, playful and fresh aesthetic, product banner style",
    },
    {
        "id": "banner_1_mobile",
        "label": "1번 큰 카드 모바일",
        "size": (750, 562),
        "aspect_ratio": "4:3",
        "prompt": "Bright cheerful banner with yellow and green banana theme, tropical summer feel, clean minimal design, no text, soft gradient background, playful and fresh aesthetic, product banner style",
    },
    {
        "id": "banner_2_pc",
        "label": "2번 작은 카드 PC",
        "size": (600, 600),
        "aspect_ratio": "1:1",
        "prompt": "Small square product card banner, nano banana branding, playful yellow color palette, cute minimal illustration style, no text, clean white background, modern e-commerce style",
    },
    {
        "id": "banner_2_mobile",
        "label": "2번 작은 카드 모바일",
        "size": (375, 375),
        "aspect_ratio": "1:1",
        "prompt": "Small square product card banner, nano banana branding, playful yellow color palette, cute minimal illustration style, no text, clean white background, modern e-commerce style",
    },
    {
        "id": "banner_3_pc",
        "label": "3번 작은 카드 PC",
        "size": (600, 600),
        "aspect_ratio": "1:1",
        "prompt": "Square lifestyle card banner, fresh tropical fruits, soft pastel yellow and green tones, flat lay style, no text, clean background, minimal modern design",
    },
    {
        "id": "banner_3_mobile",
        "label": "3번 작은 카드 모바일",
        "size": (375, 375),
        "aspect_ratio": "1:1",
        "prompt": "Square lifestyle card banner, fresh tropical fruits, soft pastel yellow and green tones, flat lay style, no text, clean background, minimal modern design",
    },
]


def generate_image(api_key: str, prompt: str, aspect_ratio: str) -> bytes | None:
    url = f"{IMAGEN_URL}?key={api_key}"
    payload = {
        "instances": [{"prompt": prompt}],
        "parameters": {
            "sampleCount": 1,
            "aspectRatio": aspect_ratio,
            "safetyFilterLevel": "BLOCK_SOME",
            "personGeneration": "DONT_ALLOW",
        },
    }
    try:
        resp = requests.post(url, json=payload, timeout=60)
        if resp.status_code == 200:
            predictions = resp.json().get("predictions", [])
            if predictions and "bytesBase64Encoded" in predictions[0]:
                return base64.b64decode(predictions[0]["bytesBase64Encoded"])
            print(f"  ⚠️  이미지 데이터 없음")
        else:
            print(f"  ❌ HTTP {resp.status_code}: {resp.text[:200]}")
    except Exception as e:
        print(f"  ❌ 요청 실패: {e}")
    return None


def resize_to_exact(image_bytes: bytes, target_size: tuple[int, int]) -> bytes:
    """정확한 사이즈로 크롭 + 리사이즈"""
    img = Image.open(io.BytesIO(image_bytes))
    img = img.convert("RGB")

    # 비율 맞춰 리사이즈 후 센터 크롭
    tw, th = target_size
    iw, ih = img.size
    scale = max(tw / iw, th / ih)
    new_w = int(iw * scale)
    new_h = int(ih * scale)
    img = img.resize((new_w, new_h), Image.LANCZOS)

    left = (new_w - tw) // 2
    top = (new_h - th) // 2
    img = img.crop((left, top, left + tw, top + th))

    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def main():
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY 환경변수가 없습니다.")
        sys.exit(1)

    output_dir = Path("output/카드배너/nano-banana-dummy")
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"🍌 나노바나나 카드 배너 더미 이미지 생성")
    print(f"   저장 위치: {output_dir}\n")

    for i, banner in enumerate(BANNERS):
        w, h = banner["size"]
        print(f"[{i+1}/{len(BANNERS)}] {banner['label']} ({w}×{h}px)")

        raw = generate_image(api_key, banner["prompt"], banner["aspect_ratio"])
        if not raw:
            print(f"  ⏭️  SKIP\n")
            continue

        resized = resize_to_exact(raw, banner["size"])
        out_path = output_dir / f"{banner['id']}_{w}x{h}.png"
        out_path.write_bytes(resized)

        size_kb = len(resized) / 1024
        print(f"  ✅ 저장: {out_path.name} ({size_kb:.0f}KB)\n")

        if i < len(BANNERS) - 1:
            print(f"  ⏳ 7초 대기...")
            time.sleep(7)

    print("🎉 완료!")
    print(f"   {output_dir}/")


if __name__ == "__main__":
    main()
