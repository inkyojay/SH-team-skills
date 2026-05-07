---
name: pdp-builder
description: |
  SundayHug 자사몰(Cafe24) 상세페이지(PDP)를 사용자와의 대화 + 타사 레퍼런스 + 네이버 키워드 SEO로 자동 생성하는 스킬.
  기존 12개 PDP가 공유하는 마스터 `styles.css`와 톤앤매너를 그대로 따라 새로운 제품 상세페이지 HTML을 만든다.

  진행 순서:
  ① 사용자와 대화로 제품 정보 수집 (카테고리/타겟/USP/이미지 URL)
  ② 타사 레퍼런스 분석 (스마트스토어/쿠팡/소셜 URL, 캡처 이미지, 텍스트 설명 모두 가능)
  ③ keyword-optimizer 스킬 호출하여 네이버 키워드 SEO 카피 발굴
  ④ 섹션 구성안을 사용자에게 확인받고
  ⑤ assets/styles.css + 인라인 스타일을 적용해 HTML 렌더
  ⑥ ~/Desktop/team-skills/상세페이지/sundayhug/{slug}/ 에 저장

  다음 상황에서 이 스킬을 사용한다:
  - "상세페이지 만들어줘", "PDP 만들기", "자사몰 상세페이지"
  - "신제품 상세페이지", "Cafe24 상세페이지 생성"
  - "썬데이허그 상세페이지 디자인"
  - 사용자가 신제품 정보 + 타사 레퍼런스를 함께 던질 때

  사용하지 않아야 하는 상황:
  - 광고 카피만 필요할 때 → keyword-optimizer / meta-ad-factory
  - 이미 만들어진 상세페이지를 캡처/분할만 → pdp-capture-prep, pdp-section-capture
  - 네이버 블로그/스레드 글 → naver-blog-seo-writer, marketing-content-factory
triggers:
  - "상세페이지 만들어줘"
  - "상세페이지 생성"
  - "PDP 만들기"
  - "자사몰 상세페이지"
  - "신제품 상세페이지"
  - "Cafe24 상세페이지"
  - "썬데이허그 상세페이지"
  - "sundayhug PDP"
  - "detail page builder"
  - "product detail page 생성"
---

# pdp-builder — SundayHug 자사몰 상세페이지 자동 생성

## 무엇을 만드는가

신제품 정보 + 타사 레퍼런스 → 기존 SundayHug 톤앤매너에 맞는 PDP HTML.

결과물:
```
~/Desktop/team-skills/상세페이지/sundayhug/{product-slug}/
├── index.html          # 완성된 PDP (Cafe24 업로드 가능)
├── styles.css          # 마스터 스타일 사본 (assets/styles.css 그대로)
└── references.json     # 분석에 사용된 레퍼런스 + 키워드 결과 (트레이스용)
```

## 핵심 자료 (이 스킬 폴더 안)

- `assets/styles.css` — **공통 마스터 CSS, 절대 수정 금지** (12개 페이지 공유)
- `assets/examples/` — 톤 가이드용 5개 PDP (abc-cover / nasi-cotton-mesh / bodysuit-short / swaddle_pocket / pajama-sweetdream). 매번 1~2개 읽어서 톤을 잡는다
- `templates/design-tokens.md` — 컬러·폰트·컨테이너 토큰 요약 (매 호출마다 읽기)
- `templates/section-snippets.md` — 섹션별 HTML 스니펫 카탈로그 (필요 섹션 골라 조립)
- `scripts/analyze_references.py` — URL/소셜/이미지/텍스트 입력 → JSON
- `scripts/render_pdp.py` — 데이터 + 카피 → 최종 HTML

## 워크플로우

### Step 1. 톤·구조 학습 (자동, 매번 수행)

스킬 발동 직후 다음 파일을 Read:
1. `templates/design-tokens.md` (전체)
2. `templates/section-snippets.md` (전체)
3. `assets/examples/` 중 사용자 제품 카테고리에 가까운 2개 선택해 read
   - 수면용품 → `abc-cover.html` + `swaddle_pocket.html`
   - 의류 → `bodysuit-short.html` + `pajama-sweetdream.html`
   - 침구/블랭킷 → `nasi-cotton-mesh.html` + `swaddle_pocket.html`

### Step 2. 제품 정보 수집

대화 또는 AskUserQuestion으로 다음을 수집:

| 항목 | 필수 | 비고 |
|---|---|---|
| 제품 정식명 | ✅ | 예: "썬데이허그 ABC 아기 블랭킷" |
| 제품 슬러그 (영문) | ✅ | 예: "abc-blanket" → 폴더명·이미지 경로에 사용 |
| 카테고리 | ✅ | abc / sleeping-bags / daily-look / newborn / outlet 중 |
| 타겟 연령/사용 시기 | ✅ | 예: "0~24개월" |
| 핵심 USP 3개 | ✅ | trust-bar에 들어감 |
| 이미지 URL 베이스 | ✅ | `https://sundayhugkr.cafe24.com/skin-skin69/pdp/{cat}/{slug}/images` |
| 색상/사이즈/치수 | ✅ | final-cta-note에 들어감 |
| 가격 | ⭕ | 명시 안 해도 페이지 자체에는 안 들어감 |

미흡 시 **AskUserQuestion**으로 보완.

### Step 3. 레퍼런스 분석

사용자가 던진 레퍼런스를 4가지 형태로 분류:
- **URL** (스마트스토어/쿠팡/자사몰): `analyze_references.py`로 og:meta + 본문 카피 추출
- **소셜 URL** (인스타/페북): og:meta만 (로그인 우회 X)
- **이미지 파일** (PDP 캡처): Claude Code가 직접 Read 툴로 분석 (Vision)
- **텍스트 설명**: 그대로 키워드 후보로

```bash
python3 skills/content-creation/pdp-builder/scripts/analyze_references.py \
  --input /tmp/refs.json \
  --output /tmp/references.json
```

이미지 캡처가 있으면 Read 툴로 직접 보고 다음을 추출:
- 섹션 구성 순서
- 카피 후킹 패턴
- 비주얼 톤 (색감, 레이아웃)

### Step 4. 키워드 SEO 리서치

기존 [keyword-optimizer](../../marketing/keyword-optimizer/SKILL.md) 스킬을 호출. 프롬프트 예:
> "{제품명}에 대해 네이버 키워드 최적화 분석 진행. 카테고리 {카테고리}, 타겟 {연령}. 상품명 후보 + S~A등급 키워드 + 상품태그 10개를 JSON으로 출력해줘."

결과 JSON에서:
- **상품명 후보 1개**를 선택해 `<h1>` 헤드라인 베이스로 활용
- **S/A등급 키워드 5~8개**를 자연스럽게 본문 카피에 분산
- **태그 10개**는 references.json에 기록 (스마트스토어 등록용)

### Step 5. 섹션 구성안 도출

`templates/section-snippets.md`의 "권장 섹션 구성" 표 참고하여 제품 유형별로 섹션 리스트 도출.

**최소 필수**: HERO + INTRO + WHY × 1 + FINAL CTA + SPECS

도출 후 사용자에게 AskUserQuestion으로 확인:
- "이 순서로 가도 될까요?"
- "추가/삭제할 섹션 있나요?"

### Step 6. 카피 작성 + 데이터 JSON 조립

`render_pdp.py` 입력 형식 (`pdp_data.json`)에 맞춰 채운다. 작성 원칙:

1. **한글 본문 + 영문 라벨/eyebrow 혼용** — `.sec-label` 영문, `.sec-title` 한글
2. **카피는 짧고 감성적** — 한 줄 12자 이내, `<br>`로 행갈이
3. **`.hl` 활용** — 핵심 키워드 1~2개를 본문 안에 강조
4. **레퍼런스 카피 그대로 베끼지 말 것** — 구조·접근만 참고하고 표현은 SundayHug 톤으로 재작성
5. **이미지 파일명 규칙**: `hero-01.webp`, `intro-01.webp`, `feature-01.webp`, `feature-01-01-{usp}.webp` 등

### Step 7. 렌더 + 저장

```bash
python3 skills/content-creation/pdp-builder/scripts/render_pdp.py \
  --input /tmp/pdp_data.json \
  --output ~/Desktop/team-skills/상세페이지/sundayhug/{slug}/
```

`render_pdp.py`가 자동으로:
- `assets/styles.css`를 출력 폴더에 복사
- HTML 렌더 (인라인 스타일 + 모든 섹션)
- references.json 동봉 (`pdp_data.json`에 references 키가 있으면)

### Step 8. 후속 안내

생성 완료 후 사용자에게 안내:

1. 결과 폴더 경로 + index.html 열기
2. 이미지 URL 확인 (Cafe24에 업로드 안 된 상태면 placeholder 보임)
3. 캡처 이미지 시리즈가 필요하면:
   - `pdp-capture-prep` → `pdp-section-capture` 순서로 실행
4. 카탈로그/검색 등록용으로 키워드 결과의 **상품태그 10개** 따로 보여주기

## 결정 사항 / 제약

- ❌ `assets/styles.css` 절대 수정 금지 (12개 페이지 공유 마스터)
- ❌ 이미지 자동 생성 X (별도 스킬 — 미제공 시 URL placeholder + TODO 주석)
- ❌ 인스타/페북 비공개 콘텐츠 스크래이핑 X (사용자에게 캡처 이미지로 다시 요청)
- ✅ 제품별 차이는 HTML 상단 인라인 `<style>` 블록에만 추가
- ✅ Cafe24 절대 URL 사용 (`sundayhugkr.cafe24.com/skin-skin69/pdp/...`)
- ✅ 모든 결과물은 `~/Desktop/team-skills/상세페이지/sundayhug/`에 저장 (CLAUDE.md 규칙)

## 연계 스킬

| 단계 | 스킬 |
|---|---|
| 키워드 SEO | [keyword-optimizer](../../marketing/keyword-optimizer/SKILL.md) |
| 제품 USP 추출 | [product-analyzer](../../brand/product-analyzer/SKILL.md) |
| 캡처 전처리 | [pdp-capture-prep](../../tools/pdp-capture-prep/SKILL.md) |
| 섹션별 PNG 분할 | [pdp-section-capture](../../tools/pdp-section-capture/SKILL.md) |

## 다음 작업 시 참고

- 새 제품 패턴이 나오면 `assets/examples/`에 1개 추가
- 신규 섹션 패턴은 `templates/section-snippets.md`에 항목 추가
- 마스터 CSS 변경이 발생하면 원본(`/Users/inkyo/Desktop/상세페이지 (절대경로)/product/details/styles.css`)을 다시 복사
