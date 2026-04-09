#!/usr/bin/env python3
"""
Step 3: AI 장면 영상 생성기
Google Veo 3.1 + Nano Banana 2 (Gemini 3.1 Flash Image)를 사용하여
가사 섹션별 장면 영상을 생성한다.
"""

import argparse
import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai 패키지가 필요합니다: pip install google-genai --break-system-packages")
    sys.exit(1)


def generate_key_image(client, scene_description: str, style: str) -> object:
    """Nano Banana 2로 키 이미지를 생성한다."""
    prompt = f"""Create a visually striking image for a short-form video scene.
Scene: {scene_description}
Style: {style}
Format: Vertical 9:16 aspect ratio, vibrant colors, high quality.
Do NOT include any text or words in the image."""

    print(f"   🖼️ 키 이미지 생성 중...")

    response = client.models.generate_content(
        model="gemini-3.1-flash-image-preview",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE"],
        )
    )

    # Extract image part
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            if part.inline_data.mime_type.startswith("image/"):
                return part

    raise RuntimeError("이미지 생성 실패")


def generate_video_from_image(client, image_part, scene_description: str,
                               aspect_ratio: str = "9:16") -> bytes:
    """Veo 3.1로 이미지 기반 영상 클립을 생성한다."""
    prompt = f"""Smooth, cinematic motion: {scene_description}
Camera slowly pans or zooms. Gentle movement. Vertical video format."""

    print(f"   🎬 영상 클립 생성 중 (Veo 3.1)...")

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        image=image_part.as_image() if hasattr(image_part, "as_image") else image_part,
        config=types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            number_of_videos=1,
        )
    )

    # Poll until done
    attempts = 0
    max_attempts = 60  # 최대 5분 대기
    while not operation.done:
        if attempts >= max_attempts:
            raise TimeoutError("영상 생성 시간 초과 (5분)")
        time.sleep(5)
        operation = client.operations.get(operation)
        attempts += 1
        if attempts % 6 == 0:
            print(f"   ⏳ 영상 생성 대기 중... ({attempts * 5}초)")

    # Extract video
    if operation.response and operation.response.generated_videos:
        video = operation.response.generated_videos[0]
        if hasattr(video.video, "video_bytes") and video.video.video_bytes:
            return video.video.video_bytes
        # If video_bytes not directly available, download
        result = client.files.download(video.video)
        return result

    raise RuntimeError("영상 생성 실패")


def generate_video_text_only(client, scene_description: str, style: str,
                              aspect_ratio: str = "9:16") -> bytes:
    """텍스트만으로 영상 클립을 생성한다 (이미지 없이)."""
    prompt = f"""{scene_description}
Style: {style}
Vertical video, smooth cinematic motion, vibrant and engaging."""

    print(f"   🎬 텍스트→영상 생성 중 (Veo 3.1)...")

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        config=types.GenerateVideosConfig(
            aspect_ratio=aspect_ratio,
            number_of_videos=1,
        )
    )

    attempts = 0
    max_attempts = 60
    while not operation.done:
        if attempts >= max_attempts:
            raise TimeoutError("영상 생성 시간 초과")
        time.sleep(5)
        operation = client.operations.get(operation)
        attempts += 1
        if attempts % 6 == 0:
            print(f"   ⏳ 대기 중... ({attempts * 5}초)")

    if operation.response and operation.response.generated_videos:
        video = operation.response.generated_videos[0]
        if hasattr(video.video, "video_bytes") and video.video.video_bytes:
            return video.video.video_bytes
        result = client.files.download(video.video)
        return result

    raise RuntimeError("영상 생성 실패")


def generate_scenes(lyrics_data: dict, output_dir: str,
                    mode: str = "image-to-video") -> list:
    """모든 섹션의 장면 영상을 생성한다."""
    client = genai.Client()
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    scene_files = []

    for i, section in enumerate(lyrics_data["sections"]):
        print(f"\n📹 장면 {i+1}/{len(lyrics_data['sections'])} 생성 중")
        print(f"   [{section['type']}] {section.get('lyrics', '')[:40]}...")

        scene_desc = section.get("scene_description", section.get("lyrics", ""))
        scene_style = section.get("scene_style", "cinematic, vibrant")

        video_path = output_path / f"scene_{i:03d}.mp4"
        image_path = output_path / f"scene_{i:03d}_key.png"

        try:
            if mode == "image-to-video":
                # Step A: 키 이미지 생성
                image_part = generate_key_image(client, scene_desc, scene_style)

                # Save key image
                if hasattr(image_part, "inline_data"):
                    img_data = image_part.inline_data.data
                    if isinstance(img_data, str):
                        img_data = base64.b64decode(img_data)
                    with open(image_path, "wb") as f:
                        f.write(img_data)
                    print(f"   ✅ 키 이미지: {image_path}")

                # Step B: 이미지 → 영상
                video_bytes = generate_video_from_image(
                    client, image_part, scene_desc
                )
            else:
                # 텍스트만으로 영상 생성
                video_bytes = generate_video_text_only(
                    client, scene_desc, scene_style
                )

            # Save video
            if isinstance(video_bytes, str):
                video_bytes = base64.b64decode(video_bytes)
            with open(video_path, "wb") as f:
                f.write(video_bytes)

            print(f"   ✅ 영상 클립: {video_path}")

            scene_files.append({
                "index": i,
                "type": section["type"],
                "start_sec": section["start_sec"],
                "end_sec": section["end_sec"],
                "lyrics": section.get("lyrics", ""),
                "video_path": str(video_path),
                "image_path": str(image_path) if image_path.exists() else None,
            })

        except Exception as e:
            print(f"   ❌ 장면 {i+1} 생성 실패: {e}")
            # Create a placeholder entry
            scene_files.append({
                "index": i,
                "type": section["type"],
                "start_sec": section["start_sec"],
                "end_sec": section["end_sec"],
                "lyrics": section.get("lyrics", ""),
                "video_path": None,
                "image_path": None,
                "error": str(e),
            })

    # Save manifest
    manifest_path = output_path / "scenes_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(scene_files, f, ensure_ascii=False, indent=2)

    print(f"\n📋 장면 매니페스트: {manifest_path}")

    success_count = sum(1 for s in scene_files if s.get("video_path"))
    print(f"✅ 생성 완료: {success_count}/{len(scene_files)} 장면")

    return scene_files


def main():
    parser = argparse.ArgumentParser(description="Veo 3.1 장면 영상 생성기")
    parser.add_argument("--scenes", required=True, help="가사 JSON 파일 경로")
    parser.add_argument("--output", default="scenes/", help="출력 디렉토리")
    parser.add_argument("--mode", choices=["image-to-video", "text-to-video"],
                        default="image-to-video",
                        help="image-to-video: 이미지 먼저 생성 후 영상화, text-to-video: 바로 영상 생성")
    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        print("❌ GEMINI_API_KEY 환경변수를 설정해주세요.")
        sys.exit(1)

    if os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

    with open(args.scenes, "r", encoding="utf-8") as f:
        lyrics_data = json.load(f)

    generate_scenes(lyrics_data, args.output, args.mode)


if __name__ == "__main__":
    main()
