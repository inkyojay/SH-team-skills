#!/usr/bin/env python3
"""
Step 2: AI 음악 생성기
Google Lyria 3 Pro API (Gemini API)를 사용하여 가사에 맞는 음악을 생성한다.
"""

import argparse
import base64
import json
import os
import sys
import time

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("❌ google-genai 패키지가 필요합니다: pip install google-genai --break-system-packages")
    sys.exit(1)


# 음악 스타일 프리셋
STYLE_PRESETS = {
    "catchy-kpop": "Catchy upbeat K-pop with playful synth melody, bright vocals, fun and energetic, 120 BPM",
    "lofi-chill": "Lofi chill hop with soft piano, warm vinyl crackle, relaxed and cozy, 85 BPM",
    "edm-hype": "Energetic EDM with heavy bass drops, synth leads, festival energy, 128 BPM",
    "acoustic-warm": "Warm acoustic guitar with gentle vocals, folk-inspired, heartfelt and intimate, 100 BPM",
    "funky-groove": "Funky groove with slap bass, brass stabs, retro disco vibe, 110 BPM",
    "reggaeton-bounce": "Reggaeton beat with dembow rhythm, tropical vibes, danceable, 95 BPM",
}


def generate_music_clip(lyrics_data: dict, model: str = "lyria-3-clip-preview") -> bytes:
    """Lyria 3 Clip으로 30초 음악 클립을 생성한다."""
    client = genai.Client()

    # Build prompt from lyrics data
    music_prompt = lyrics_data.get("music_prompt", "Catchy upbeat pop song")

    # Add lyrics to prompt for vocal generation
    lyrics_text = "\n".join(
        section["lyrics"] for section in lyrics_data["sections"]
    )

    full_prompt = f"""{music_prompt}

Lyrics (Korean):
{lyrics_text}

Generate a catchy, memorable track with these Korean lyrics sung with clear pronunciation.
The song should be fun, witty, and perfect for a viral short-form video."""

    print(f"🎶 음악 생성 중... (모델: {model})")
    print(f"   프롬프트: {music_prompt[:80]}...")

    response = client.models.generate_content(
        model=model,
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO", "TEXT"],
        )
    )

    # Extract audio data
    audio_data = None
    generated_lyrics = None

    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            if part.inline_data.mime_type.startswith("audio/"):
                audio_data = part.inline_data.data
                print(f"   오디오 형식: {part.inline_data.mime_type}")
        elif hasattr(part, "text") and part.text:
            generated_lyrics = part.text

    if generated_lyrics:
        print(f"   생성된 가사 구조:\n{generated_lyrics[:200]}...")

    if not audio_data:
        raise RuntimeError("음악 생성 실패: 오디오 데이터가 없습니다.")

    return audio_data


def generate_music_pro(lyrics_data: dict) -> bytes:
    """Lyria 3 Pro로 최대 3분 길이 음악을 생성한다."""
    client = genai.Client()

    music_prompt = lyrics_data.get("music_prompt", "Catchy upbeat pop song")
    lyrics_text = "\n".join(
        section["lyrics"] for section in lyrics_data["sections"]
    )

    # Pro model supports composer-mode style prompts
    sections_prompt = []
    for section in lyrics_data["sections"]:
        dur = section["end_sec"] - section["start_sec"]
        sections_prompt.append(
            f"[{section['type'].upper()}] ({dur}s): {section['lyrics']}"
        )

    full_prompt = f"""{music_prompt}

Song structure with Korean lyrics:
{chr(10).join(sections_prompt)}

Create a professional-quality track following this exact structure.
Sing the Korean lyrics clearly. Make it catchy and viral-worthy."""

    print(f"🎶 음악 생성 중... (모델: lyria-3-pro-preview)")

    response = client.models.generate_content(
        model="lyria-3-pro-preview",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO", "TEXT"],
        )
    )

    audio_data = None
    for part in response.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data:
            if part.inline_data.mime_type.startswith("audio/"):
                audio_data = part.inline_data.data

    if not audio_data:
        raise RuntimeError("음악 생성 실패: 오디오 데이터가 없습니다.")

    return audio_data


def main():
    parser = argparse.ArgumentParser(description="Lyria 3 음악 생성기")
    parser.add_argument("--lyrics", required=True, help="가사 JSON 파일 경로")
    parser.add_argument("--style", default=None, help="음악 스타일 프리셋 또는 커스텀 프롬프트")
    parser.add_argument("--model", choices=["clip", "pro"], default="clip",
                        help="clip=30초, pro=최대3분")
    parser.add_argument("--output", default="music.mp3", help="출력 파일 경로")
    args = parser.parse_args()

    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        print("❌ GEMINI_API_KEY 환경변수를 설정해주세요.")
        print("   발급: https://aistudio.google.com/apikey")
        sys.exit(1)

    # Set API key for google-genai
    if os.environ.get("GEMINI_API_KEY"):
        os.environ["GOOGLE_API_KEY"] = os.environ["GEMINI_API_KEY"]

    with open(args.lyrics, "r", encoding="utf-8") as f:
        lyrics_data = json.load(f)

    # Apply style preset if specified
    if args.style:
        if args.style in STYLE_PRESETS:
            lyrics_data["music_prompt"] = STYLE_PRESETS[args.style]
        else:
            lyrics_data["music_prompt"] = args.style

    # Generate
    if args.model == "pro":
        audio_bytes = generate_music_pro(lyrics_data)
    else:
        audio_bytes = generate_music_clip(lyrics_data)

    # Save
    with open(args.output, "wb") as f:
        if isinstance(audio_bytes, str):
            f.write(base64.b64decode(audio_bytes))
        else:
            f.write(audio_bytes)

    file_size = os.path.getsize(args.output)
    print(f"✅ 음악 저장: {args.output} ({file_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
