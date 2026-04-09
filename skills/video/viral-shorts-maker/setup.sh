#!/bin/bash
# Viral Shorts Maker — 설치 스크립트

set -e

echo "🚀 Viral Shorts Maker 설치 시작"
echo "================================"

# Python dependencies
echo ""
echo "📦 Python 패키지 설치..."
pip install anthropic google-genai --break-system-packages 2>/dev/null || \
pip install anthropic google-genai

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️ Node.js가 설치되어 있지 않습니다."
    echo "   설치: https://nodejs.org/ 또는 nvm install 18"
else
    echo "✅ Node.js $(node --version)"
fi

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️ ffmpeg가 설치되어 있지 않습니다."
    echo "   설치: sudo apt install ffmpeg (Ubuntu) / brew install ffmpeg (Mac)"
else
    echo "✅ ffmpeg 설치됨"
fi

# Check API keys
echo ""
echo "🔑 API 키 확인..."

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "⚠️ ANTHROPIC_API_KEY가 설정되지 않았습니다."
    echo "   export ANTHROPIC_API_KEY='your-key-here'"
else
    echo "✅ ANTHROPIC_API_KEY 설정됨"
fi

if [ -z "$GEMINI_API_KEY" ] && [ -z "$GOOGLE_API_KEY" ]; then
    echo "⚠️ GEMINI_API_KEY가 설정되지 않았습니다."
    echo "   발급: https://aistudio.google.com/apikey"
    echo "   export GEMINI_API_KEY='your-key-here'"
else
    echo "✅ Gemini API Key 설정됨"
fi

echo ""
echo "================================"
echo "✅ 설치 완료!"
echo ""
echo "사용법:"
echo "  python scripts/pipeline.py --topic '아기 수면의 놀라운 비밀 5가지'"
echo ""
echo "개별 실행:"
echo "  python scripts/lyrics_generator.py --topic '주제' --output lyrics.json"
echo "  python scripts/music_generator.py --lyrics lyrics.json --output music.mp3"
echo "  python scripts/scene_generator.py --scenes lyrics.json --output scenes/"
