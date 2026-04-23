#!/bin/bash
# FFmpeg 오디오 트리밍 스크립트
#
# TTS로 생성된 오디오의 앞뒤 무음 구간을 제거합니다.
#
# 사용법:
#   ./trim-audio.sh <입력파일>              # 무음 제거 후 덮어쓰기
#   ./trim-audio.sh <입력파일> <출력파일>   # 별도 파일로 저장
#
# 예시:
#   ./trim-audio.sh audio/scene1.mp3
#   ./trim-audio.sh audio/scene1.mp3 audio/scene1_trimmed.mp3
#
# 사전 요구사항:
#   - FFmpeg 설치 (brew install ffmpeg)

set -euo pipefail

INPUT="${1:?입력 파일을 지정하세요}"
OUTPUT="${2:-}"

if [ -z "$OUTPUT" ]; then
  # 출력 미지정 시 임시파일로 처리 후 덮어쓰기
  TEMP=$(mktemp /tmp/trim-audio-XXXXXX.mp3)
  OUTPUT="$TEMP"
  OVERWRITE=true
else
  OVERWRITE=false
fi

echo "✂️  트리밍: $INPUT"

# silenceremove: 앞뒤 무음 제거
# start_periods=1: 첫 번째 무음 구간 제거
# stop_periods=1: 마지막 무음 구간 제거
# start_threshold/stop_threshold: 무음 판정 기준 (-50dB)
ffmpeg -y -i "$INPUT" \
  -af "silenceremove=start_periods=1:start_threshold=-50dB:stop_periods=1:stop_threshold=-50dB" \
  "$OUTPUT" 2>/dev/null

if [ "$OVERWRITE" = true ]; then
  mv "$OUTPUT" "$INPUT"
  echo "   ✅ 트리밍 완료: $INPUT"
else
  echo "   ✅ 트리밍 완료: $OUTPUT"
fi

# 길이 표시
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$INPUT" 2>/dev/null || echo "?")
echo "   ⏱️  길이: ${DURATION}초"
