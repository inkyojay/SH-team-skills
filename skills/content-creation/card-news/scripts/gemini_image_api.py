#!/usr/bin/env python3
"""
Google Gemini API를 통한 이미지 생성

Usage:
    python gemini_image_api.py --prompt "설명" --output image.png
    python gemini_image_api.py --setup  # API 키 설정

Requirements:
    pip install google-genai pillow

API 키 발급: https://aistudio.google.com/apikey
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

try:
    from google import genai
    from google.genai import types
except ImportError:
    print(json.dumps({
        "error": "google-genai 패키지가 설치되어 있지 않습니다.",
        "install": "pip install google-genai pillow"
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
    # 환경변수 우선
    env_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")
    if env_key:
        return env_key

    config_path = get_config_path()
    if not config_path.exists():
        return None

    if yaml:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}
            return config.get("google_api_key") or config.get("gemini_api_key")

    return None


def save_api_key(api_key: str):
    """API 키 저장"""
    config_path = get_config_path()
    config = {}

    if config_path.exists() and yaml:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f) or {}

    config["google_api_key"] = api_key

    if yaml:
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
    else:
        # yaml 없으면 간단히 저장
        with open(config_path, 'w') as f:
            f.write(f"google_api_key: {api_key}\n")

    print(f"API 키가 저장되었습니다: {config_path}")


def generate_image(
    prompt: str,
    output_path: str,
    style_prefix: str = "",
    api_key: str | None = None
) -> dict:
    """
    Gemini API로 이미지 생성

    Args:
        prompt: 이미지 설명
        output_path: 출력 파일 경로
        style_prefix: 스타일 프롬프트 접두사
        api_key: API 키 (없으면 저장된 키 사용)

    Returns:
        dict: 결과 정보
    """
    if not api_key:
        api_key = load_api_key()

    if not api_key:
        return {
            "success": False,
            "error": "API 키가 설정되지 않았습니다. --setup으로 설정하거나 GOOGLE_API_KEY 환경변수를 설정하세요."
        }

    # 스타일 접두사 추가
    full_prompt = f"{style_prefix}, {prompt}" if style_prefix else prompt

    try:
        # Gemini 클라이언트 초기화
        client = genai.Client(api_key=api_key)

        # 이미지 생성 요청
        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE']
            )
        )

        # 이미지 추출
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)

                with open(output_path, 'wb') as f:
                    f.write(image_data)

                return {
                    "success": True,
                    "output": output_path,
                    "prompt": full_prompt
                }

        return {
            "success": False,
            "error": "이미지가 생성되지 않았습니다. 프롬프트를 수정해보세요."
        }

    except Exception as e:
        error_msg = str(e)
        if "API_KEY_INVALID" in error_msg or "401" in error_msg:
            return {
                "success": False,
                "error": "API 키가 유효하지 않습니다. Google AI Studio에서 키를 확인하세요."
            }
        elif "RESOURCE_EXHAUSTED" in error_msg or "429" in error_msg:
            return {
                "success": False,
                "error": "API 요청 한도를 초과했습니다. 잠시 후 다시 시도하세요."
            }
        else:
            return {
                "success": False,
                "error": error_msg
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
    print("Google Gemini API 키 설정")
    print("-" * 40)
    print("API 키는 https://aistudio.google.com/apikey 에서 발급받을 수 있습니다.")
    print()

    api_key = input("API 키를 입력하세요: ").strip()

    if not api_key:
        print("API 키가 입력되지 않았습니다.")
        return

    save_api_key(api_key)
    print("설정이 완료되었습니다.")


def main():
    parser = argparse.ArgumentParser(description="Gemini API 이미지 생성")
    parser.add_argument("--setup", action="store_true", help="API 키 설정")
    parser.add_argument("--prompt", help="이미지 생성 프롬프트")
    parser.add_argument("--output", default="output.png", help="출력 파일 경로")
    parser.add_argument("--style", default="", help="스타일 프롬프트 접두사")
    parser.add_argument("--api-key", help="API 키")

    args = parser.parse_args()

    if args.setup:
        setup_api_key()
        return

    if not args.prompt:
        print(json.dumps({"error": "--prompt를 지정하거나 --setup으로 API 키를 설정하세요."}))
        sys.exit(1)

    api_key = args.api_key or os.environ.get("GOOGLE_API_KEY")

    result = generate_image(
        prompt=args.prompt,
        output_path=args.output,
        style_prefix=args.style,
        api_key=api_key
    )

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
