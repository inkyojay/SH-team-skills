#!/bin/bash
# Supertone TTS 나레이션 생성 스크립트
#
# 사용법:
#   ./generate-tts.sh <텍스트> <출력파일명> [voice_id] [style] [speed]
#
# 예시:
#   ./generate-tts.sh "이불을 덮어줘도 항상 밖으로 나와있는 우리 아이" audio/scene1.mp3
#   ./generate-tts.sh "안녕하세요" audio/intro.mp3 e5f6fb1a53d0add87afb4f serene 0.95
#
# 사전 요구사항:
#   - SUPERTONE_API_KEY 환경변수 설정
#
# 음성 목록 (한국어 여성):
#   - e5f6fb1a53d0add87afb4f  Agatha  (narration/serene/neutral/happy) - 전문 나레이션
#   - 7c56c6a6471a12816604f0  Ariel   (neutral/happy/sad/shy) - 캐주얼 대화
#   - 52dc253df44d06aa7f0867  Bella   (neutral/happy/kind/angry) - 감성 톤
#   - 2cd6c38c7087106be21888  Aya     (neutral) - 오디오북/다큐
#
# 음성 목록 (한국어 남성):
#   - 91992bbd4758bdcf9c9b01  Adam    (neutral) - 밈/대화/비즈니스
#
# 전체 목록 조회:
#   curl -s -H "x-sup-api-key: $SUPERTONE_API_KEY" "https://supertoneapi.com/v1/voices"

set -euo pipefail

TEXT="${1:?텍스트를 입력하세요}"
OUTPUT="${2:?출력 파일명을 입력하세요 (예: audio/scene1.mp3)}"
VOICE_ID="${3:-e5f6fb1a53d0add87afb4f}"
STYLE="${4:-neutral}"
SPEED="${5:-1.0}"

# API 키 확인
if [ -z "${SUPERTONE_API_KEY:-}" ]; then
  echo "❌ SUPERTONE_API_KEY 환경변수가 설정되지 않았습니다."
  echo "   export SUPERTONE_API_KEY=\"your-api-key\""
  exit 1
fi

# 출력 디렉토리 생성
mkdir -p "$(dirname "$OUTPUT")"

# 출력 포맷 결정 (확장자 기반)
EXT="${OUTPUT##*.}"
if [ "$EXT" = "wav" ]; then
  FORMAT="wav"
else
  FORMAT="mp3"
fi

echo "🎙️ TTS 생성: \"$TEXT\""
echo "   음성: $VOICE_ID, 스타일: $STYLE, 속도: $SPEED"

# JSON 페이로드 안전하게 생성
JSON_PAYLOAD=$(jq -n \
  --arg text "$TEXT" \
  --arg style "$STYLE" \
  --argjson speed "$SPEED" \
  '{text: $text, language: "ko", style: $style, voice_settings: {speed: $speed}}')

# Supertone API 호출
HTTP_CODE=$(curl -s -w "%{http_code}" \
  -X POST "https://supertoneapi.com/v1/text-to-speech/${VOICE_ID}?output_format=${FORMAT}" \
  -H "x-sup-api-key: ${SUPERTONE_API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$JSON_PAYLOAD" \
  -o "$OUTPUT")

# 결과 확인
if [ "$HTTP_CODE" -eq 200 ]; then
  SIZE=$(stat -f%z "$OUTPUT" 2>/dev/null || stat --printf="%s" "$OUTPUT" 2>/dev/null || echo "?")
  DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUTPUT" 2>/dev/null || echo "?")
  echo "   ✅ 저장: $OUTPUT (${SIZE} bytes, ${DURATION}초)"
else
  echo "   ❌ 오류 (HTTP ${HTTP_CODE}):"
  cat "$OUTPUT" 2>/dev/null
  echo ""
  rm -f "$OUTPUT"
  exit 1
fi
