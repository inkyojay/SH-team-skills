---
name: promo-html
description: 썬데이허그 프로모션 원스톱 제작. 기획부터 14개 채널 HTML 디자인 생성, PNG 변환, .pen 파일까지 통합 워크플로우.
triggers:
  - "프로모션 HTML"
  - "프로모션 제작"
  - "프로모션 원스톱"
  - "promo html"
  - "프로모션 디자인 HTML"
---

# 프로모션 원스톱 제작 스킬 (기획 → HTML → PNG → .pen)

자연어 대화로 프로모션을 기획하고, 14개 채널별 HTML 디자인을 병렬 생성하며, PNG 변환과 .pen 파일까지 원스톱으로 처리합니다.

---

## Phase 1: 기획서 로딩 또는 인터랙티브 기획

### 1-A: 기존 기획서 검색

```
1. Glob으로 "{{WORKSPACE_DIR}}/output/*/plan.json" 검색
2. 여러 개면 목록 표시 → 사용자에게 선택 요청
3. 하나면 로드 → 요약 표시 → "이 기획서를 사용할까요?" 확인
4. 없으면 Phase 1-B로
```

기획서 로드 시 요약:
```markdown
## 기획서 로드 완료

**{promotion_name}**
| 항목 | 내용 |
|------|------|
| 컨셉 | {concept} |
| 기간 | {period.start} ~ {period.end} |
| 채널 | {channels 목록} |
| 혜택 | {offer.description} |
| 제품 | {products 목록} |

이 기획서로 디자인을 진행할까요?
```

### 1-B: 인터랙티브 기획 (기획서 없을 때)

브랜드 컨텍스트를 먼저 로드합니다:
```
1. Glob으로 ~/.claude/shared-references/ 하위 sundayhug 관련 파일 탐색
2. brand-guide → 톤앤매너, 핵심 가치
3. products.json → 제품 정보
```

없으면 기본 브랜드 정보 사용:
- **브랜드**: 썬데이허그 (SUNDAYHUG), 프리미엄 베이비 슬립케어
- **핵심 가치**: 따뜻함, 편안함, 자연친화, 신뢰
- **타겟**: 0-36개월 아기 부모 (주로 30대 여성)
- **톤앤매너**: 따뜻하고 신뢰감 있는 육아 전문가

사용자와 대화하며 아래 항목을 확정합니다. 이미 제공된 정보는 건너뜁니다:

| 항목 | 필드명 | 예시 |
|------|--------|------|
| 프로모션명 | `promotion_name` | 봄 슬리핑백 특가 |
| 한줄 컨셉 | `concept` | 봄맞이 슬리핑백 전 라인업 20% 특가 |
| 톤앤매너 | `tone_manner` | 따뜻하고 설레는 봄 느낌 |
| 목적 | `intent` | 매출/인지도/재구매/신규유입 |
| 타겟 | `target_audience` | 0-12개월 아기 부모 |
| 기간 | `period` | 3월 1일 ~ 3월 15일 |
| 채널 | `channels` | 인스타그램, 네이버, 자사몰, 카카오톡 |
| 핵심 메시지 | `key_message` | 우리 아기 첫 봄잠 |
| 대상 제품 | `products` | 코지 슬리핑백 89,000→71,200 |
| 혜택 | `offer` | 20% 할인 + 무료배송 |

모든 항목이 확정되면 요약 테이블 제시 → 사용자 확인 → plan.json 저장:
```bash
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}"
```
Write 도구로 `{{WORKSPACE_DIR}}/output/{slug}/plan.json` 저장.

JSON 스키마는 기존 promotion-plan과 동일:
```json
{
  "version": "1.0",
  "created_at": "{ISO_DATE}",
  "status": "confirmed",
  "promotion_name": "...",
  "slug": "...",
  "concept": "...",
  "tone_manner": "...",
  "intent": "...",
  "target_audience": "...",
  "period": { "start": "YYYY-MM-DD", "end": "YYYY-MM-DD" },
  "key_message": "...",
  "products": [{ "name": "...", "price": 0, "discount_price": 0, "image": "" }],
  "offer": { "type": "...", "value": "...", "description": "...", "additional": "..." },
  "channels": ["인스타그램", "네이버"],
  "deliverables": [],
  "project_dir": "{{WORKSPACE_DIR}}/output/{slug}/",
  "json_file": "{{WORKSPACE_DIR}}/output/{slug}/plan.json"
}
```

---

## Phase 2: 채널별 디자인 목록 확정

### 채널 스펙 로드

`references/channel-specs.md`를 Read로 읽어 채널 마스터 테이블을 참조합니다.
경로: `{{REPO_DIR}}/skills/promotion/promo-html/references/channel-specs.md`

### 채널 매핑

plan.json의 `channels` 배열에서 해당 포맷을 자동 매핑합니다:

| channels 값 | 생성 포맷 |
|------------|----------|
| 인스타그램 | 스토리, 피드(이벤트), 재입고, 체험단 모집 |
| 네이버 | 브랜드홈 카드, 모바일 배너, PC 배너 |
| 네쇼라 | 프로모 스토리 |
| 자사몰 | PC 배너, 모바일 배너 |
| 카카오톡 | 단일 이미지, 리스트형, 캐러셀 |
| 라이브 | 페이지 |

### 사용자 확인

```markdown
## 생성할 디자인 목록

| # | 채널 | 포맷 | 사이즈 | 파일명 |
|---|------|------|--------|--------|
| 1 | 인스타그램 | 스토리 | 1080×1920 | 01-insta-story.html |
| 2 | 인스타그램 | 피드(이벤트) | 1080×1350 | 02-insta-event.html |
| ... |

총 {N}개 디자인을 생성합니다. 수정하거나 제외할 항목이 있으면 알려주세요.
```

**사용자가 확인하면 Phase 3으로 진행합니다.**

---

## Phase 3: 채널별 카피 및 디자인 방향 수립

### 변수 매핑

`references/variable-guide.md`를 Read로 읽어 plan.json → 변수 매핑을 수행합니다.
경로: `{{REPO_DIR}}/skills/promotion/promo-html/references/variable-guide.md`

### 디자인 시스템 로드

`references/design-system.md`를 Read로 읽어 브랜드 컬러/타이포/컴포넌트를 확인합니다.
경로: `{{REPO_DIR}}/skills/promotion/promo-html/references/design-system.md`

### 채널별 카피 생성

plan.json의 tone_manner + key_message를 기반으로 각 채널에 맞는 카피를 생성합니다:

```markdown
## 채널별 카피 및 디자인 방향

### 1. 인스타그램 스토리
- **HEADLINE**: {감성적 15자 카피}
- **SUBHEAD**: {혜택 요약}
- **BADGE**: {OFFER_VALUE} OFF
- **디자인 방향**: 세로 풀스크린, 상단 로고+뱃지, 중앙 히어로, 하단 CTA

### 2. 네이버 PC 배너
- **HEADLINE**: {정보형 25자 카피}
- **SUBHEAD**: {상세 혜택}
- **디자인 방향**: 좌측 카피 + 우측 제품 이미지
...

이 카피와 방향으로 진행할까요?
```

**사용자가 확인하면 Phase 4로 진행합니다.**

---

## Phase 4: 병렬 HTML 생성

### 출력 폴더 생성

```bash
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}/html"
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}/png"
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}/pen"
```

### HTML 생성 규칙 로드

`references/html-generation-rules.md`를 Read로 읽어 HTML 작성 규칙을 확인합니다.
경로: `{{REPO_DIR}}/skills/promotion/promo-html/references/html-generation-rules.md`

### 레퍼런스 이미지 확인

각 채널의 레퍼런스 이미지를 Read로 확인하여 레이아웃/스타일을 파악합니다.
레퍼런스 이미지 베이스 경로: `{{WORKSPACE_DIR}}/`
채널별 레퍼런스 폴더는 `references/channel-specs.md`의 레퍼런스 폴더 참조.

### 병렬 에이전트 스폰

Agent 도구로 채널별 에이전트를 **병렬 스폰**합니다. 한 메시지에 여러 Agent 호출을 포함하여 최대 병렬성을 확보합니다.

각 에이전트에 전달할 정보:

```
당신은 프로모션 HTML 디자인 에이전트입니다.
아래 정보를 바탕으로 자체 완결형 HTML 파일을 생성하세요.

## 채널 정보
- 채널: {channel}
- 포맷: {format}
- 사이즈: {width} × {height}
- 출력 파일: {{WORKSPACE_DIR}}/output/{slug}/html/{filename}

## 프로모션 컨텍스트
- 프로모션명: {promotion_name}
- 핵심 메시지: {key_message}
- 톤앤매너: {tone_manner}
- 혜택: {offer_description}
- 기간: {period}
- 대상 제품: {products 정보}

## 카피
- HEADLINE: {채널별 생성 카피}
- SUBHEAD: {보조 카피}
- BADGE_TEXT: {뱃지 텍스트}
- CTA_TEXT: {CTA 문구}

## 필수 작업
1. 아래 레퍼런스 이미지를 Read로 확인하여 레이아웃 참고:
   {{WORKSPACE_DIR}}/{레퍼런스 경로}
2. 아래 디자인 시스템 파일을 Read로 읽어 브랜드 컬러/타이포 확인:
   {{REPO_DIR}}/skills/promotion/promo-html/references/design-system.md
3. 아래 HTML 규칙 파일을 Read로 읽어 구조/규칙 확인:
   {{REPO_DIR}}/skills/promotion/promo-html/references/html-generation-rules.md
4. Write 도구로 HTML 파일 생성
5. 생성한 HTML이 품질 체크리스트를 만족하는지 자체 검증

## 품질 체크
- body width/height가 {width}×{height}과 정확히 일치
- Pretendard 폰트 CDN @import 포함
- CSS 변수 블록 포함
- 외부 CSS/JS 없음 (폰트 CDN 제외)
- 브랜드 팔레트 색상만 사용
- 텍스트가 컨테이너 벗어나지 않음
- 변수 플레이스홀더 남아있지 않음
```

**중요**: 산출물이 여러 개이면 가능한 한 병렬로 스폰합니다 (한 메시지에 여러 Agent tool 호출).
에이전트 mode는 `"bypassPermissions"`를 사용하여 Write 도구 자동 허용.

### 완료 확인

모든 에이전트가 완료되면 생성된 HTML 파일 목록을 Glob으로 확인:
```
Glob: "{{WORKSPACE_DIR}}/output/{slug}/html/*.html"
```

---

## Phase 5: 검토 및 수정

### HTML 파일 목록 표시

```markdown
## 생성된 HTML 파일

| # | 파일 | 채널 | 사이즈 |
|---|------|------|--------|
| 1 | 01-insta-story.html | 인스타그램 스토리 | 1080×1920 |
| ... |

수정이 필요한 파일이 있으면 알려주세요.
파일 번호와 수정 내용을 말씀해주시면 바로 반영합니다.
```

### 수정 프로세스

사용자 피드백이 있으면:
1. 해당 HTML 파일을 Read로 읽기
2. Edit 도구로 직접 수정
3. 수정 완료 알림

수정이 완료되거나 사용자가 만족하면 Phase 6으로 진행합니다.

---

## Phase 6: PNG 변환 + .pen 파일 생성

### 6-A: PNG 변환

render_all.py 스크립트를 실행하여 HTML → PNG 배치 변환:

```bash
python3 {{REPO_DIR}}/skills/promotion/promo-html/scripts/render_all.py \
  --input-dir "{{WORKSPACE_DIR}}/output/{slug}/html/" \
  --output-dir "{{WORKSPACE_DIR}}/output/{slug}/png/" \
  --scale 2
```

스크립트가 실패하면 (Playwright 미설치 등):
```bash
pip install playwright && playwright install chromium
```
후 재실행.

### 6-B: .pen 파일 생성

Pencil MCP 도구를 사용하여 각 채널별 .pen 파일을 생성합니다.

각 채널에 대해:
1. `open_document("new")` → 새 .pen 파일 생성
2. `batch_design`으로 HTML과 동일한 레이아웃/콘텐츠 구성
   - 브랜드 디자인 시스템의 컬러/타이포 적용
   - HTML의 구조를 pen 노드로 변환
3. `get_screenshot`으로 결과 확인

출력 경로: `{{WORKSPACE_DIR}}/output/{slug}/pen/{filename}.pen`

**참고**: .pen 파일 생성은 선택적입니다. 사용자가 원하지 않으면 건너뜁니다.

---

## Phase 7: 완료 리포트

```markdown
## 프로모션 디자인 완료: {promotion_name}

| # | 채널 | 포맷 | 사이즈 | HTML | PNG | PEN |
|---|------|------|--------|------|-----|-----|
| 1 | 인스타그램 | 스토리 | 1080×1920 | ✅ | ✅ | ✅ |
| 2 | 인스타그램 | 피드(이벤트) | 1080×1350 | ✅ | ✅ | ✅ |
| ... |

### 파일 위치
- 기획서: `{{WORKSPACE_DIR}}/output/{slug}/plan.json`
- HTML: `{{WORKSPACE_DIR}}/output/{slug}/html/`
- PNG: `{{WORKSPACE_DIR}}/output/{slug}/png/`
- PEN: `{{WORKSPACE_DIR}}/output/{slug}/pen/`

### 프로모션 요약
- **프로모션**: {promotion_name}
- **기간**: {period}
- **혜택**: {offer}
- **총 산출물**: {N}개 채널 × 3 포맷(HTML/PNG/PEN)
```

---

## 주의사항

- 사용자가 이미 제공한 정보는 다시 묻지 마세요
- 채널 선택 시 반드시 channel-specs.md의 정확한 사이즈를 사용하세요
- HTML은 자체 완결형 — 외부 의존성 없이 단독 렌더링 가능해야 합니다
- 브랜드 디자인 시스템(design-system.md)의 컬러/타이포를 반드시 준수하세요
- 병렬 에이전트는 서로 독립적으로 작업합니다 (교차 의존 없음)
- 레퍼런스 이미지는 참고용 — 그대로 복사하지 않고 구조만 참고합니다
- plan.json은 기존 promotion-plan 스킬과 동일한 스키마를 사용합니다
- PNG 변환은 Playwright가 필요합니다 (미설치 시 자동 설치 안내)
