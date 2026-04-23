#!/usr/bin/env python3
"""
나노바나(Nano Banana) API를 통한 이미지 생성

Usage:
    python nanobanana_api.py --prompt "설명" --output image.png
    python nanobanana_api.py --setup  # API 키 설정

Requirements:
    pip install requests pyyaml

API 키 발급: https://nanobnana.com/dashboard
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
    import yaml
except ImportError:
    print(json.dumps({
        "error": "필수 패키지가 설치되어 있지 않습니다.",
        "install": "pip install requests pyyaml"
    }))
    sys.exit(1)


def get_config_path() -> Path:
    """설정 파일 경로 반환"""
    if sys.platform == "darwin":
        config_dir = Path.home() / ".config" / "card-news-creator"
    elif sys.platform == "win32":
        config_dir = Path(os.environ.get("APPDATA", "")) / "card-news-creator"
    else:
        config_dir = Path.home() / ".config" / "card-news-creator"

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / "config.yaml"


def load_api_key() -> str | None:
    """저장된 API 키 로드"""
    config_path = get_config_path()
    if not config_path.exists():
        return None

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}
        return config.get("nanobanana_api_key")


def save_api_key(api_key: str):
    """API 키 저장"""
    config_path = get_config_path()
    config = {}

    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}

    config["nanobanana_api_key"] = api_key

    with open(config_path, 'w') as f:
        yaml.dump(config, f)

    print(f"API 키가 저장되었습니다: {config_path}")


def generate_image(
    prompt: str,
    output_path: str,
    style_prefix: str = "",
    resolution: str = "1k",
    api_key: str | None = None
) -> dict:
    """
    나노바나 API로 이미지 생성

    Args:
        prompt: 이미지 설명
        output_path: 출력 파일 경로
        style_prefix: 스타일 프롬프트 접두사
        resolution: 해상도 (1k, 2k, 4k)
        api_key: API 키 (없으면 저장된 키 사용)

    Returns:
        dict: 결과 정보
    """
    if not api_key:
        api_key = load_api_key()

    if not api_key:
        return {
            "success": False,
            "error": "API 키가 설정되지 않았습니다. --setup으로 설정하세요."
        }

    # 스타일 접두사 추가
    full_prompt = f"{style_prefix}, {prompt}" if style_prefix else prompt

    # API 호출
    url = "https://nanobnana.com/api/v2/generate"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # 해상도에 따른 크기 매핑
    size_map = {
        "1k": {"width": 1024, "height": 1280},
        "2k": {"width": 2048, "height": 2560},
        "4k": {"width": 4096, "height": 5120}
    }
    size = size_map.get(resolution, size_map["1k"])

    payload = {
        "prompt": full_prompt,
        "width": size["width"],
        "height": size["height"],
        "num_images": 1
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code == 200:
            result = response.json()

            # 이미지 URL에서 다운로드
            if "images" in result and result["images"]:
                image_url = result["images"][0].get("url")
                if image_url:
                    img_response = requests.get(image_url, timeout=30)
                    if img_response.status_code == 200:
                        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, 'wb') as f:
                            f.write(img_response.content)
                        return {
                            "success": True,
                            "output": output_path,
                            "prompt": full_prompt
                        }

            # base64 형식인 경우
            if "images" in result and result["images"]:
                import base64
                image_data = result["images"][0].get("b64_json") or result["images"][0].get("base64")
                if image_data:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    with open(output_path, 'wb') as f:
                        f.write(base64.b64decode(image_data))
                    return {
                        "success": True,
                        "output": output_path,
                        "prompt": full_prompt
                    }

            return {
                "success": False,
                "error": "이미지 데이터를 찾을 수 없습니다.",
                "response": result
            }

        elif response.status_code == 401:
            return {
                "success": False,
                "error": "API 키가 유효하지 않습니다."
            }
        elif response.status_code == 429:
            return {
                "success": False,
                "error": "API 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요."
            }
        else:
            return {
                "success": False,
                "error": f"API 오류: {response.status_code}",
                "detail": response.text
            }

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "error": "API 요청 시간 초과"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def generate_card_images(
    cards_data: list[dict],
    output_dir: str,
    style_prefix: str = "",
    api_key: str | None = None
) -> list[dict]:
    """
    여러 카드에 대한 배경 이미지 일괄 생성

    Args:
        cards_data: [{"index": 1, "prompt": "..."}, ...]
        output_dir: 출력 디렉토리
        style_prefix: 공통 스타일 접두사
        api_key: API 키

    Returns:
        list[dict]: 각 카드별 결과
    """
    results = []
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    for card in cards_data:
        idx = card.get("index", len(results) + 1)
        prompt = card.get("prompt", "")

        if not prompt:
            results.append({
                "index": idx,
                "success": False,
                "error": "프롬프트가 없습니다."
            })
            continue

        output_file = output_path / f"{idx:02d}_background.png"
        result = generate_image(
            prompt=prompt,
            output_path=str(output_file),
            style_prefix=style_prefix,
            api_key=api_key
        )
        result["index"] = idx
        results.append(result)

    return results


def setup_api_key():
    """대화형 API 키 설정"""
    print("나노바나 API 키 설정")
    print("-" * 40)
    print("API 키는 https://nanobnana.com/dashboard 에서 발급받을 수 있습니다.")
    print()

    api_key = input("API 키를 입력하세요: ").strip()

    if not api_key:
        print("API 키가 입력되지 않았습니다.")
        return

    save_api_key(api_key)
    print("설정이 완료되었습니다.")


def main():
    parser = argparse.ArgumentParser(description="나노바나 API 이미지 생성")
    parser.add_argument("--setup", action="store_true", help="API 키 설정")
    parser.add_argument("--prompt", help="이미지 생성 프롬프트")
    parser.add_argument("--output", default="output.png", help="출력 파일 경로")
    parser.add_argument("--style", default="", help="스타일 프롬프트 접두사")
    parser.add_argument("--resolution", default="1k", choices=["1k", "2k", "4k"])
    parser.add_argument("--api-key", help="API 키 (환경변수 NANOBANANA_API_KEY도 가능)")

    args = parser.parse_args()

    if args.setup:
        setup_api_key()
        return

    if not args.prompt:
        print(json.dumps({"error": "--prompt를 지정하거나 --setup으로 API 키를 설정하세요."}))
        sys.exit(1)

    api_key = args.api_key or os.environ.get("NANOBANANA_API_KEY")

    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        style_prefix=args.style,
        resolution=args.resolution,
        api_key=api_key
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
