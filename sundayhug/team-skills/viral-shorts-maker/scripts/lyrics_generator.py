#!/usr/bin/env python3
"""
Step 1: 가사 + 장면 설명 생성기
Claude API를 사용하여 주제에 맞는 위트 있는 가사와 장면 설명을 생성한다.
"""

import argparse
import json
import os
import sys

try:
    from google import genai
except ImportError:
    print("❌ google-genai 패키지가 필요합니다: pip install google-genai --break-system-packages")
    sys.exit(1)


SYSTEM_PROMPT = """너는 바이럴 숏폼 콘텐츠를 위한 가사 작가야.
주어진 주제에 대해 재미있고 위트 있는 가사를 만들어야 해.

규칙:
1. 가사는 잡지식/꿀팁을 전달하되, 중독성 있고 재밌어야 함
2. 한국어로 작성하되, 라임과 리듬감이 있어야 함
3. 각 섹션(verse/chorus)마다 어울리는 장면 설명도 함께 작성
4. 장면 설명은 영어로 (Veo API 프롬프트용)
5. 음악 스타일 프롬프트도 함께 생성

반드시 아래 JSON 형식으로만 응답해. 다른 텍스트 없이 순수 JSON만:

{
  "title": "영상 제목",
  "total_duration_sec": 30,
  "sections": [
    {
      "type": "verse|chorus|intro|outro",
      "start_sec": 0,
      "end_sec": 8,
      "lyrics": "가사 텍스트",
      "scene_description": "English scene description for video generation",
      "scene_style": "visual style keywords"
    }
  ],
  "music_prompt": "Detailed music style description in English for Lyria API",
  "subtitle_color": "#FFFFFF",
  "subtitle_bg_color": "#00000088"
}
"""


def generate_lyrics(topic: str, style: str = "catchy k-pop", duration: int = 30) -> dict:
    """Gemini API로 가사와 장면 설명을 생성한다."""
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = f"""주제: {topic}
음악 스타일: {style}
목표 길이: {duration}초

이 주제에 대해 바이럴 가능한 숏폼 영상용 가사를 만들어줘.
잡지식이나 꿀팁을 위트 있는 가사에 담아야 해.
총 {duration}초 분량으로, 섹션별로 나눠서 작성해줘.
각 섹션은 대략 6~10초 길이로."""

    print(f"🎵 가사 생성 중... (주제: {topic})")

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"{SYSTEM_PROMPT}\n\n{user_prompt}",
    )

    # Parse JSON response
    text = response.text.strip()
    # Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    lyrics_data = json.loads(text)

    print(f"✅ 가사 생성 완료: {lyrics_data['title']}")
    print(f"   섹션 수: {len(lyrics_data['sections'])}")
    print(f"   총 길이: {lyrics_data['total_duration_sec']}초")

    return lyrics_data


def main():
    parser = argparse.ArgumentParser(description="바이럴 쇼츠 가사 생성기")
    parser.add_argument("--topic", required=True, help="영상 주제")
    parser.add_argument("--style", default="catchy k-pop", help="음악 스타일")
    parser.add_argument("--duration", type=int, default=30, help="목표 길이(초)")
    parser.add_argument("--output", default="lyrics.json", help="출력 파일 경로")
    args = parser.parse_args()

    # Check API key
    if not (os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")):
        print("❌ GEMINI_API_KEY 환경변수를 설정해주세요.")
        sys.exit(1)

    lyrics = generate_lyrics(args.topic, args.style, args.duration)

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(lyrics, f, ensure_ascii=False, indent=2)

    print(f"📝 가사 저장: {args.output}")

    # Preview
    print("\n--- 가사 미리보기 ---")
    for section in lyrics["sections"]:
        print(f"\n[{section['type']}] {section['start_sec']}s ~ {section['end_sec']}s")
        print(section["lyrics"])


if __name__ == "__main__":
    main()
