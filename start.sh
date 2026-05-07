#!/bin/bash

# AI 마케팅 스킬팩 시작 스크립트
# 더블클릭하면 바로 시작!

cd "$(dirname "$0")"

echo "================================================"
echo "  AI 마케팅 스킬팩"
echo "  144개 스킬 | 11개 에이전트"
echo "================================================"
echo ""

# Claude 설치 확인
if ! command -v claude &> /dev/null; then
    echo "❌ Claude Code가 설치되지 않았습니다."
    echo ""
    echo "설치 명령어:"
    echo "  npm install -g @anthropic-ai/claude-code"
    echo ""
    read -p "Enter 키를 눌러 종료..."
    exit 1
fi

# 스킬 가이드 열기
echo "📚 스킬 가이드 열기..."
open "사용가이드.html"

echo ""
echo "💡 사용 예시:"
echo "   - 카톡 배너 만들어줘"
echo "   - 상세페이지 작성해줘"
echo "   - 이벤트 페이지를 레퍼런스 느낌으로 바꿔줘"
echo "   - 브랜드 분석해줘"
echo ""
echo "🚪 종료: /exit 또는 Ctrl+C"
echo "================================================"
echo ""


# Claude 실행
exec claude
