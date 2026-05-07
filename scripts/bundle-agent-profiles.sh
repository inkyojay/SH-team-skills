#!/bin/bash
# bundle-agent-profiles.sh
# 13인 에이전트 프로필을 Desktop으로 일괄 배포 + 통합본 빌드
#
# Usage: ./scripts/bundle-agent-profiles.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC_DIR="$REPO_ROOT/skills/_team-agents"
DEST_DIR="$HOME/Desktop/team-skills/agents"

# 13명 에이전트 (브랜드실장은 별도 위치에 있음)
AGENTS=(
  "ceo-director:대표이사"
  "market-analyst:시장분석관"
  "cfo-director:재무이사"
  "strategy-director:전략실장"
  "data-dev-lead:데이터개발팀장"
  "marketing-lead:마케팅팀장"
  "product-planning-lead:상품기획팀장"
  "operations-lead:운영팀장"
  "gov-support-lead:지원사업팀장"
  "overseas-strategy-lead:해외전략팀장"
  "cs-lead:CS팀장"
  "designer:디자이너"
)

BRAND_DIRECTOR_SRC="$REPO_ROOT/skills/brand/sundayhug-brand-director"

echo "🚀 Agent profiles 배포 시작..."
echo "   Source: $SRC_DIR"
echo "   Dest:   $DEST_DIR"
echo ""

mkdir -p "$DEST_DIR"

# INDEX.md 복사
cp "$SRC_DIR/INDEX.md" "$DEST_DIR/INDEX.md"
echo "✅ INDEX.md"

# 12명 에이전트 처리
for entry in "${AGENTS[@]}"; do
  slug="${entry%%:*}"
  ko_name="${entry##*:}"

  src="$SRC_DIR/$slug"
  dest="$DEST_DIR/$slug"

  if [ ! -d "$src" ]; then
    echo "⚠️  Skip: $slug (소스 없음)"
    continue
  fi

  mkdir -p "$dest"

  # 핵심 파일 복사
  [ -f "$src/PROFILE.md" ]      && cp "$src/PROFILE.md"      "$dest/01_PROFILE.md"
  [ -f "$src/skills-map.md" ]   && cp "$src/skills-map.md"   "$dest/02_skills-map.md"
  [ -f "$src/cron.md" ]         && cp "$src/cron.md"         "$dest/03_cron.md"

  # guides 복사
  if [ -d "$src/guides" ]; then
    mkdir -p "$dest/guides"
    cp -R "$src/guides/." "$dest/guides/" 2>/dev/null || true
  fi

  # checklists 복사 (있으면)
  if [ -d "$src/checklists" ] && [ -n "$(ls -A "$src/checklists" 2>/dev/null)" ]; then
    mkdir -p "$dest/checklists"
    cp -R "$src/checklists/." "$dest/checklists/" 2>/dev/null || true
  fi

  # 통합본 빌드 (페이퍼클립 단일본)
  combined="$dest/00_통합본-페르소나-인스트럭션.md"
  {
    echo "# $ko_name — 통합 인스트럭션 (페이퍼클립 단일본)"
    echo ""
    echo "> 페이퍼클립 / Custom Instructions 등에 한 번에 붙여넣기 위한 통합본."
    echo "> 빌드 시점: $(date '+%Y-%m-%d %H:%M')"
    echo ""
    echo "---"
    echo ""

    for f in "$dest/01_PROFILE.md" "$dest/02_skills-map.md" "$dest/03_cron.md"; do
      if [ -f "$f" ]; then
        echo ""
        echo "---"
        echo ""
        echo "# 📂 $(basename "$f")"
        echo ""
        cat "$f"
        echo ""
      fi
    done

    if [ -d "$dest/guides" ]; then
      for f in "$dest/guides"/*.md; do
        if [ -f "$f" ]; then
          echo ""
          echo "---"
          echo ""
          echo "# 📂 guides/$(basename "$f")"
          echo ""
          cat "$f"
          echo ""
        fi
      done
    fi

    if [ -d "$dest/checklists" ]; then
      for f in "$dest/checklists"/*.md; do
        if [ -f "$f" ]; then
          echo ""
          echo "---"
          echo ""
          echo "# 📂 checklists/$(basename "$f")"
          echo ""
          cat "$f"
          echo ""
        fi
      done
    fi
  } > "$combined"

  size=$(du -k "$combined" | cut -f1)
  echo "✅ $slug ($ko_name) — 통합본 ${size}KB"
done

# 브랜드실장 미러 (이미 별도로 배포되어 있지만, agents/ 하위에도 링크용 README)
brand_dir="$DEST_DIR/sundayhug-brand-director"
mkdir -p "$brand_dir"
cat > "$brand_dir/README.md" <<EOF
# 브랜드실장 (Brand Director)

이 폴더는 참조 안내. 실제 파일은 다음 두 곳:

## 1. 레포 소스
\`$BRAND_DIRECTOR_SRC\`

## 2. Desktop 배포본 (이미 있음)
\`$HOME/Desktop/team-skills/브랜드실장/\`

페이퍼클립 단일본:
\`$HOME/Desktop/team-skills/브랜드실장/00_통합본-페르소나-인스트럭션.md\`
EOF
echo "✅ sundayhug-brand-director (참조 README만)"

echo ""
echo "✨ 완료!"
echo "📁 배포 경로: $DEST_DIR"
echo ""
echo "🎯 페이퍼클립 등록 방법:"
echo "   - 단일 인스트럭션: 각 에이전트의 00_통합본*.md 사용"
echo "   - 다중 첨부: PROFILE / skills-map / cron + guides 모두 첨부"
