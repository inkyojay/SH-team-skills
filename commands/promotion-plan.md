---
name: promotion-plan
description: 썬데이허그 프로모션 기획서 작성. 자연어 대화로 프로모션 컨셉을 정의하고, .pen 기획서 + .json 데이터 파일 생성.
triggers:
  - "프로모션 기획"
  - "프로모션 기획서"
  - "프로모션 플랜"
  - "promotion plan"
---

# 프로모션 기획 스킬

자연어 대화를 통해 프로모션 컨셉을 정의하고, .pen 기획서 + .json 데이터 파일을 생성합니다.

## Phase 1: 브랜드 컨텍스트 로딩

작업 시작 전 반드시 다음을 읽어 브랜드 정보를 파악하세요:

```
1. Glob으로 .claude/shared-references/ 하위 sundayhug 관련 파일 탐색
2. brand-guide → 톤앤매너, 핵심 가치
3. products.json → 제품 정보 (이름, 가격, 카테고리)
4. target-customers → 타겟 고객 페르소나
```

없으면 기본 브랜드 정보 사용:
- **브랜드**: 썬데이허그 (SUNDAYHUG)
- **카테고리**: 프리미엄 베이비 슬립케어
- **핵심 가치**: 따뜻함, 편안함, 자연친화, 신뢰
- **타겟**: 0-36개월 아기를 둔 부모 (주로 30대 여성)
- **톤앤매너**: 따뜻하고 신뢰감 있는 육아 전문가
- **컬러**: 썬데이 베이지(#F5E6D3), 허그 브라운(#8B7355)

## Phase 2: 대화형 기획

사용자와 자연어 대화를 통해 아래 항목을 하나씩 확정합니다.
이미 제공된 정보는 건너뛰고, 부족한 부분만 질문합니다.

### 필수 확정 항목

| 항목 | 설명 | 예시 |
|------|------|------|
| `promotion_name` | 프로모션명 | 봄 슬리핑백 특가 |
| `concept` | 한줄 컨셉 | 봄맞이 슬리핑백 전 라인업 20% 특가 |
| `tone_manner` | 톤앤매너 | 따뜻하고 설레는 봄 느낌 |
| `intent` | 목적 | 매출 / 인지도 / 재구매 / 신규유입 |
| `target_audience` | 타겟 | 0-12개월 아기 부모 |
| `period` | 기간 | 3월 1일 ~ 3월 15일 |
| `channels` | 채널 목록 | 인스타그램, 네이버, 자사몰, 카카오톡 |
| `key_message` | 핵심 메시지 | 우리 아기 첫 봄잠, 썬데이허그와 함께 |
| `products` | 대상 제품 | 코지 슬리핑백, 스와들포켓 |
| `offer` | 혜택 | 20% 할인 + 5만원 이상 무료배송 |
| `deliverables_preview` | 예상 산출물 | 인스타 스토리 1장, 네이버 PC 배너 1장 |

### 대화 흐름 가이드

1. **프로모션 주제가 있으면** → 바로 세부 항목 논의 시작
2. **아이디어만 있으면** → 유사 프로모션 제안 + 방향 함께 결정
3. **채널 선택 시** → `references/channel-specs.md` 참조하여 가능한 포맷 안내
4. **제품 선택 시** → products.json에서 정확한 정보 확인

### 채널 선택 도움

채널 사양은 `references/channel-specs.md`를 Read로 읽어서 참조합니다.
사용자가 채널을 고르면, 해당 채널에서 제작 가능한 포맷을 표로 보여주세요:

```
| 채널 | 포맷 | 사이즈 | 레퍼런스 |
|------|------|--------|---------|
```

## Phase 3: 룩앤필 레퍼런스 등록

프로모션 내용이 확정되면, 디자인 방향(룩앤필)을 정합니다.

### 레퍼런스 이미지 수집

사용자에게 레퍼런스 이미지를 요청합니다:

```markdown
## 디자인 룩앤필 설정

프로모션 디자인의 감성/스타일을 정하기 위해 레퍼런스 이미지를 등록해주세요.
원하는 분위기의 이미지 파일 경로를 알려주시면 됩니다. (여러 장 가능)

예시:
- "~/Downloads/봄감성참고.png" — 이 색감이 좋아요
- "~/Desktop/레이아웃참고.jpg" — 이런 배치로
- "인스타에서 본 이 느낌으로" (URL이나 스크린샷 경로)

레퍼런스 이미지가 없으면 "건너뛰기"라고 말씀해주세요.
브랜드 기본 스타일로 진행합니다.
```

### 이미지 분석

사용자가 이미지를 제공하면:
1. Read 도구로 각 이미지를 열어 시각적으로 분석
2. 각 이미지에서 파악한 디자인 특성을 정리:
   - **색감**: 따뜻한 톤 / 쿨한 톤 / 파스텔 / 비비드 등
   - **레이아웃**: 미니멀 / 가득찬 / 좌우분할 / 센터형 등
   - **타이포**: 굵은 산세리프 / 가벼운 세리프 / 손글씨 등
   - **무드**: 고급스러운 / 캐주얼 / 따뜻한 / 시원한 등

3. 분석 결과를 사용자에게 제시:

```markdown
## 레퍼런스 분석 결과

### 이미지 1: {파일명}
- 색감: 부드러운 베이지 + 연한 그린 파스텔
- 레이아웃: 미니멀, 여백 넉넉
- 무드: 따뜻하고 자연스러운 봄 느낌

### 이미지 2: {파일명}
- 색감: 화이트 + 골드 포인트
- 레이아웃: 센터형, 제품 강조
- 무드: 고급스럽고 세련된

### 종합 룩앤필 방향
> {분석을 종합한 한 줄 방향}

이 방향으로 진행할까요? 추가/수정할 부분이 있으면 알려주세요.
```

### 룩앤필 확정

사용자가 확인하면 다음을 확정합니다:
- `look_and_feel`: 종합 디자인 방향 (한 줄 설명)
- `visual_references`: 이미지 경로 + 메모 배열
- `point_color`: 레퍼런스에서 추출한 포인트 컬러 (있으면)

건너뛰기를 선택하면 브랜드 기본 스타일 사용:
- `look_and_feel`: "썬데이허그 브랜드 기본 — 따뜻한 베이지톤, 미니멀 여백"
- `visual_references`: []

## Phase 4: 디자인 소재 사진 등록

디자인에 실제 사용할 사진(제품 사진, 감성 사진 등)을 폴더에 정리하도록 안내합니다.

### 소재 폴더 생성

먼저 프로젝트 소재 폴더를 생성합니다:
```bash
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}/photos/products"
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}/photos/lifestyle"
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}/photos/logo"
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}/photos/etc"
```

### 사용자에게 사진 등록 안내

```markdown
## 디자인 소재 사진 등록

디자인에 사용할 사진을 아래 폴더에 넣어주세요.
폴더를 열어드릴게요!

📁 **소재 폴더**: `{{WORKSPACE_DIR}}/output/{slug}/photos/`

| 폴더 | 넣을 사진 | 예시 |
|------|----------|------|
| `products/` | 제품 사진 (누끼, 착용샷 등) | 슬리핑백_정면.png, 착용샷1.jpg |
| `lifestyle/` | 감성/분위기 사진 | 아기잠자는모습.jpg, 봄인테리어.png |
| `logo/` | 브랜드 로고 | sundayhug_logo.png |
| `etc/` | 기타 (뱃지, 아이콘 등) | sale_badge.png |

사진을 넣으셨으면 "완료" 또는 "준비됐어"라고 말씀해주세요.
사진 없이 진행하려면 "건너뛰기"라고 해주세요.
```

### 소재 폴더 열기

Bash로 Finder/탐색기에서 폴더를 열어줍니다:
```bash
open "{{WORKSPACE_DIR}}/output/{slug}/photos/"
```
(Windows: `explorer`, Linux: `xdg-open`)

### 등록된 사진 확인

사용자가 "완료"라고 하면:
1. Glob으로 `photos/` 하위 모든 이미지 파일 탐색
2. 각 사진을 Read로 열어 시각적으로 확인
3. 등록된 소재 목록을 표로 정리:

```markdown
## 등록된 디자인 소재

| # | 폴더 | 파일명 | 미리보기 |
|---|------|--------|---------|
| 1 | products | 슬리핑백_정면.png | ✅ 확인 |
| 2 | products | 착용샷1.jpg | ✅ 확인 |
| 3 | lifestyle | 봄감성.jpg | ✅ 확인 |
| 4 | logo | sundayhug_logo.png | ✅ 확인 |

총 {N}개 소재가 등록되었습니다.

### 채널별 사진 배정 제안
| 채널 | 추천 소재 |
|------|----------|
| 인스타 스토리 | 착용샷1.jpg + 봄감성.jpg |
| 네이버 PC 배너 | 슬리핑백_정면.png + 로고 |
| 카카오톡 | 슬리핑백_정면.png |
| ... |

이 배정으로 진행할까요? 수정하고 싶은 부분이 있으면 알려주세요.
```

### 소재 정보 저장

확정된 소재 정보를 plan.json의 `materials` 필드에 저장합니다:

```json
"materials": {
  "base_dir": "{{WORKSPACE_DIR}}/output/{slug}/photos",
  "photos": [
    {
      "path": "products/슬리핑백_정면.png",
      "category": "products",
      "description": "실키밤부 슬리핑백 정면 누끼",
      "use_in": ["naver-pc", "kakao-single", "insta-event"]
    },
    {
      "path": "lifestyle/착용샷1.jpg",
      "category": "lifestyle",
      "description": "아기 착용 감성샷",
      "use_in": ["insta-story", "jasamol-mobile"]
    },
    {
      "path": "logo/sundayhug_logo.png",
      "category": "logo",
      "description": "썬데이허그 로고",
      "use_in": ["all"]
    }
  ]
}
```

건너뛰기를 선택하면:
```json
"materials": {
  "base_dir": "",
  "photos": []
}
```

## Phase 5: 최종 확정

모든 항목이 확정되면, 표 형태로 정리하여 사용자에게 확인받습니다.

### 요약 형식

```markdown
## 프로모션 기획 요약

| 항목 | 내용 |
|------|------|
| 프로모션명 | {promotion_name} |
| 한줄 컨셉 | {concept} |
| 톤앤매너 | {tone_manner} |
| 목적 | {intent} |
| 타겟 | {target_audience} |
| 기간 | {period} |
| 채널 | {channels} |
| 핵심 메시지 | {key_message} |
| 대상 제품 | {products} |
| 혜택 | {offer} |
| 룩앤필 | {look_and_feel} |
| 레퍼런스 | {visual_references 수}장 등록 |
| 디자인 소재 | {materials.photos 수}장 등록 |
| 예상 산출물 | {deliverables_preview} |

이 내용으로 기획서를 생성할까요?
```

**사용자가 확인하면 Phase 6으로 진행합니다.**

## Phase 6: .pen 기획서 생성

Pencil MCP 도구를 사용하여 시각적 기획서를 생성합니다.

### 레이아웃 참조

`references/plan-template.md`를 Read로 읽어 기획서 레이아웃과 batch_design 골격을 참조합니다.

### 생성 순서

1. `open_document("new")` → 새 .pen 파일 생성
2. `batch_design`으로 기획서 레이아웃 구성:
   - **Header** (1680x56): 브랜드명 + "프로모션 기획서" + 날짜
   - **Hero** (1680x200): 프로모션명(대형 타이포) + 한줄 컨셉 + 베이지 배경
   - **Body** (1680x844): 2단 레이아웃
     - 좌: 기본정보 카드 / 혜택 카드 / 채널 카드
     - 우: 핵심메시지(인용 박스) / 대상 제품 / 산출물 체크리스트
   - **Footer** (1680x48): 안내 문구 + 상태
3. `get_screenshot`으로 결과 확인

### 스타일

| 요소 | 값 |
|------|---|
| 전체 배경 | `#FAFAF7` |
| 헤더 배경 | `#8B7355` (텍스트 흰색) |
| 히어로 배경 | `#F5E6D3` |
| 카드 | 흰색, cornerRadius 12, 가벼운 그림자 |
| 섹션 제목 | 20px bold `#8B7355` |
| 본문 | 14-16px `#666666` |
| 태그 | `#F5E6D3` bg, pill shape |

## Phase 7: .json 데이터 저장

기획서와 동일한 경로에 .json 파일을 저장합니다.

### 출력 경로

```
{{WORKSPACE_DIR}}/output/{slug}/plan.pen
{{WORKSPACE_DIR}}/output/{slug}/plan.json
```

`slug`는 프로모션명을 영문 하이픈 형식으로 변환합니다.
예: "봄 슬리핑백 특가" → `spring-sleeping-bag-sale`

### 폴더 생성

출력 전 프로젝트 폴더가 없으면 Bash로 생성합니다:
```bash
mkdir -p "{{WORKSPACE_DIR}}/output/{slug}"
```

### JSON 스키마

`references/plan-template.md`의 `.json 데이터 스키마` 섹션을 참조합니다.

Write 도구로 JSON 파일을 저장합니다:

```json
{
  "version": "1.0",
  "created_at": "{ISO_DATE}",
  "status": "confirmed",
  "promotion_name": "...",
  "slug": "...",
  "look_and_feel": "부드러운 봄 파스텔 + 미니멀 여백 + 자연광 느낌",
  "visual_references": [
    { "path": "/path/to/ref1.png", "note": "이 색감 참고" },
    { "path": "/path/to/ref2.jpg", "note": "이 레이아웃 느낌" }
  ],
  ...
}
```

## Phase 8: 핸드오프

기획서 생성 완료 후 안내:

```markdown
기획서가 생성되었습니다!

- 프로젝트 폴더: `{{WORKSPACE_DIR}}/output/{slug}/`
- .pen 기획서: `output/{slug}/plan.pen`
- .json 데이터: `output/{slug}/plan.json`

디자인 제작을 시작하려면 `/promo-html` 또는 `/promotion-design`을 실행하세요.
```

## 주의사항

- 사용자가 이미 제공한 정보는 다시 묻지 마세요
- 채널 선택 시 반드시 channel-specs.md의 정확한 사이즈를 안내하세요
- .pen 기획서는 1680x1188 고정 사이즈로 생성합니다
- JSON 데이터는 `/promotion-design` 스킬이 읽어야 하므로 스키마를 정확히 준수하세요
- `copywriting` 스킬의 원칙(명확함 > 창의성, 혜택 > 기능)을 카피에 반영하세요
