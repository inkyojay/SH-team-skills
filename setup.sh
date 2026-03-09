#!/bin/bash
# ──────────────────────────────────────────────
# team-skills 설치 스크립트
# 클론 후 한 번 실행하면 모든 스킬/커맨드 자동 설치
# ──────────────────────────────────────────────

set -e

# 색상 정의
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 이 스크립트가 위치한 디렉토리 = 레포 루트
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo ""
echo -e "${BLUE}══════════════════════════════════════════════${NC}"
echo -e "${BLUE}  team-skills 설치 스크립트${NC}"
echo -e "${BLUE}══════════════════════════════════════════════${NC}"
echo ""
echo -e "레포 경로: ${GREEN}${REPO_DIR}${NC}"

# ──────────────────────────────────────────────
# 1. 작업 디렉토리 설정
# ──────────────────────────────────────────────
DEFAULT_WORKSPACE="$HOME/ai 디자인"

echo ""
echo -e "${YELLOW}[1/5] 작업 디렉토리 설정${NC}"
echo -e "프로모션 결과물(HTML, PNG 등)이 저장될 폴더입니다."
echo -e "기본값: ${GREEN}${DEFAULT_WORKSPACE}${NC}"
read -r -p "작업 디렉토리 경로 (Enter로 기본값 사용): " WORKSPACE_DIR
WORKSPACE_DIR="${WORKSPACE_DIR:-$DEFAULT_WORKSPACE}"

# 작업 디렉토리 생성
mkdir -p "$WORKSPACE_DIR/output"
echo -e "  ✅ 작업 디렉토리: ${GREEN}${WORKSPACE_DIR}${NC}"

# ──────────────────────────────────────────────
# 2. Claude Code 커맨드 설치
# ──────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[2/5] Claude Code 슬래시 커맨드 설치${NC}"

CLAUDE_COMMANDS_DIR="$HOME/.claude/commands"
mkdir -p "$CLAUDE_COMMANDS_DIR"

INSTALLED=0
SKIPPED=0

for cmd_file in "$REPO_DIR/commands/"*.md; do
  [ -f "$cmd_file" ] || continue
  filename="$(basename "$cmd_file")"

  # 플레이스홀더 치환하여 설치
  sed \
    -e "s|{{REPO_DIR}}|${REPO_DIR}|g" \
    -e "s|{{WORKSPACE_DIR}}|${WORKSPACE_DIR}|g" \
    "$cmd_file" > "$CLAUDE_COMMANDS_DIR/$filename"

  INSTALLED=$((INSTALLED + 1))
done

echo -e "  ✅ ${GREEN}${INSTALLED}개${NC} 슬래시 커맨드 설치 완료 → ${CLAUDE_COMMANDS_DIR}/"

# ──────────────────────────────────────────────
# 3. 스킬/에이전트 파일 경로 치환 (레포 내부)
# ──────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[3/5] 스킬 파일 경로 설정${NC}"

PATCHED=0
# 플레이스홀더가 있는 모든 파일을 찾아서 치환
while IFS= read -r -d '' file; do
  sed -i '' \
    -e "s|{{REPO_DIR}}|${REPO_DIR}|g" \
    -e "s|{{WORKSPACE_DIR}}|${WORKSPACE_DIR}|g" \
    "$file"
  PATCHED=$((PATCHED + 1))
done < <(grep -rlZ '{{REPO_DIR}}\|{{WORKSPACE_DIR}}' "$REPO_DIR/skills/" "$REPO_DIR/agents/" 2>/dev/null)

echo -e "  ✅ ${GREEN}${PATCHED}개${NC} 스킬/에이전트 파일 경로 설정 완료"

# git에서 로컬 변경 무시 (경로 치환된 파일들)
if command -v git &> /dev/null && [ -d "$REPO_DIR/.git" ]; then
  while IFS= read -r -d '' file; do
    git -C "$REPO_DIR" update-index --skip-worktree "$file" 2>/dev/null || true
  done < <(git -C "$REPO_DIR" diff --name-only -z 2>/dev/null)
  echo -e "  ✅ Git skip-worktree 설정 (로컬 경로 변경 무시)"
fi

# ──────────────────────────────────────────────
# 4. 설정 파일 저장 (나중에 업데이트 시 재사용)
# ──────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[4/5] 설정 저장${NC}"

cat > "$REPO_DIR/.env.local" <<EOF
# team-skills 로컬 설정 (setup.sh가 자동 생성)
# 이 파일은 .gitignore에 포함되어 커밋되지 않습니다
REPO_DIR=${REPO_DIR}
WORKSPACE_DIR=${WORKSPACE_DIR}
INSTALLED_AT=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
EOF

echo -e "  ✅ 설정 저장 → ${GREEN}.env.local${NC}"

# ──────────────────────────────────────────────
# 4. Python 의존성 확인
# ──────────────────────────────────────────────
echo ""
echo -e "${YELLOW}[5/5] 의존성 확인${NC}"

# Python 확인
if command -v python3 &> /dev/null; then
  echo -e "  ✅ Python3: $(python3 --version)"
else
  echo -e "  ${RED}⚠️  Python3가 설치되어 있지 않습니다${NC}"
  echo "     PNG 변환 기능을 사용하려면 Python3을 설치하세요"
fi

# Playwright 확인
if python3 -c "import playwright" 2>/dev/null; then
  echo -e "  ✅ Playwright: 설치됨"
else
  echo ""
  read -r -p "  Playwright(PNG 변환용)를 설치할까요? (y/N): " INSTALL_PW
  if [[ "$INSTALL_PW" =~ ^[Yy]$ ]]; then
    pip install playwright && playwright install chromium
    echo -e "  ✅ Playwright 설치 완료"
  else
    echo -e "  ${YELLOW}⏭️  건너뜀 (나중에 pip install playwright && playwright install chromium)${NC}"
  fi
fi

# ──────────────────────────────────────────────
# 완료
# ──────────────────────────────────────────────
echo ""
echo -e "${BLUE}══════════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✅ 설치 완료!${NC}"
echo -e "${BLUE}══════════════════════════════════════════════${NC}"
echo ""
echo "  사용 방법:"
echo "    1. Claude Code를 실행합니다"
echo "    2. /promo-html 등 슬래시 커맨드를 사용합니다"
echo ""
echo "  설치된 커맨드 목록:"

for cmd_file in "$CLAUDE_COMMANDS_DIR/"*.md; do
  [ -f "$cmd_file" ] || continue
  name="$(basename "$cmd_file" .md)"
  echo "    /${name}"
done

echo ""
echo -e "  레포 경로:   ${GREEN}${REPO_DIR}${NC}"
echo -e "  작업 디렉토리: ${GREEN}${WORKSPACE_DIR}${NC}"
echo -e "  커맨드 경로:  ${GREEN}${CLAUDE_COMMANDS_DIR}/${NC}"
echo ""
