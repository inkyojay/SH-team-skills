#!/bin/bash
#
# 스킬 설치 및 자동 정리 스크립트
#
# 사용법:
#   ./scripts/install-skills.sh <repo> <category>
#
# 예시:
#   ./scripts/install-skills.sh coreyhaines31/marketingskills marketing
#   ./scripts/install-skills.sh vercel-labs/agent-skills tools
#
# 카테고리 목록:
#   - marketing      (마케팅 전략)
#   - tools          (유틸리티 도구)
#   - content-creation (콘텐츠 제작)
#   - video          (영상 제작)
#   - brand          (브랜드 관리)
#   - advertising    (광고)
#   - promotion      (프로모션)
#

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SKILLS_DIR="$PROJECT_DIR/skills"

# 인자 확인
if [ $# -lt 2 ]; then
    echo -e "${RED}오류: 인자가 부족합니다${NC}"
    echo ""
    echo "사용법: $0 <repo> <category>"
    echo ""
    echo "예시:"
    echo "  $0 coreyhaines31/marketingskills marketing"
    echo "  $0 vercel-labs/agent-skills tools"
    echo ""
    echo "카테고리: marketing, tools, content-creation, video, brand, advertising, promotion"
    exit 1
fi

REPO="$1"
CATEGORY="$2"
TARGET_DIR="$SKILLS_DIR/$CATEGORY"

# 카테고리 유효성 검사
VALID_CATEGORIES="marketing tools content-creation video brand advertising promotion"
if [[ ! " $VALID_CATEGORIES " =~ " $CATEGORY " ]]; then
    echo -e "${RED}오류: 유효하지 않은 카테고리 '$CATEGORY'${NC}"
    echo "유효한 카테고리: $VALID_CATEGORIES"
    exit 1
fi

# 타겟 디렉토리 생성
mkdir -p "$TARGET_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}스킬 설치 스크립트${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "레포지토리: ${GREEN}$REPO${NC}"
echo -e "카테고리:   ${GREEN}$CATEGORY${NC}"
echo -e "설치 경로:  ${GREEN}$TARGET_DIR${NC}"
echo ""

# 1. npx skills add 실행
echo -e "${YELLOW}[1/4] 스킬 다운로드 중...${NC}"
cd "$PROJECT_DIR"
npx skills add "$REPO" -y

# 2. .agents/skills/에서 새 스킬 이동
echo ""
echo -e "${YELLOW}[2/4] 스킬 정리 중...${NC}"

MOVED=0
SKIPPED=0

for AGENT_DIR in ".agents" ".agent"; do
    if [ -d "$PROJECT_DIR/$AGENT_DIR/skills" ]; then
        for skill_path in "$PROJECT_DIR/$AGENT_DIR/skills"/*; do
            if [ -d "$skill_path" ]; then
                skill_name=$(basename "$skill_path")

                if [ -d "$TARGET_DIR/$skill_name" ]; then
                    echo -e "  ${YELLOW}스킵:${NC} $skill_name (이미 존재)"
                    ((SKIPPED++))
                else
                    cp -r "$skill_path" "$TARGET_DIR/"
                    echo -e "  ${GREEN}이동:${NC} $skill_name → skills/$CATEGORY/"
                    ((MOVED++))
                fi
            fi
        done
    fi
done

# 3. 임시 폴더 정리
echo ""
echo -e "${YELLOW}[3/4] 임시 폴더 정리 중...${NC}"

for AGENT_DIR in ".agents" ".agent"; do
    if [ -d "$PROJECT_DIR/$AGENT_DIR" ]; then
        rm -rf "$PROJECT_DIR/$AGENT_DIR"
        echo -e "  ${GREEN}삭제:${NC} $AGENT_DIR/"
    fi
done

# 4. 문서 업데이트
echo ""
echo -e "${YELLOW}[4/4] 문서 업데이트 중...${NC}"
python3 "$SCRIPT_DIR/generate-catalog.py"

# 완료 메시지
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}완료!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "  새로 추가: ${GREEN}${MOVED}개${NC}"
echo -e "  스킵 (중복): ${YELLOW}${SKIPPED}개${NC}"
echo ""
