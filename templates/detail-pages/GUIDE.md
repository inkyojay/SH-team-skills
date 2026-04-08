# 썬데이허그 상세페이지 템플릿 시스템

> **이 파일을 가장 먼저 읽으세요.** 에이전트가 상세페이지를 생성/수정할 때 필요한 모든 정보가 여기 있습니다.

---

## 개요

이 템플릿 시스템은 썬데이허그 브랜드의 상세페이지를 일관되게 생성하기 위한 모듈식 섹션 라이브러리입니다.
각 섹션은 독립적인 HTML 파일로, 목적·순서·데이터 스펙이 주석으로 문서화되어 있어 에이전트가 바로 조합하여 페이지를 만들 수 있습니다.

---

## 파일 구조

```
templates/detail-pages/
├── GUIDE.md                ← 지금 읽고 있는 파일 (상세페이지 제작 가이드)
├── _base-styles.css        ← 상세페이지 디자인 시스템 CSS
├── _animations.js          ← IntersectionObserver 스크롤 애니메이션
├── template-guide.html     ← 비주얼 가이드 (브라우저에서 확인용)
└── sections/               ← 섹션별 HTML 템플릿 (27개)
    ├── 01-hero.html
    ├── 02-trust-bar.html
    ├── ...
    └── 27-sticky-bar.html
```

### 관련 파일
```
brand/                           ← 브랜드 디자인 자산 (공통)
├── sundayhug-brand-guide.html   ←   비주얼 브랜드 가이드
└── sundayhug-brand-project.md   ←   브랜드 전략/컬러/톤앤매너

projects/detail-pages/           ← 산출물
├── current/                     ←   최종 HTML 파일들
└── archive/                     ←   이전 버전 보관
```

---

## 페이지 조립 방법

### 1단계: 기본 HTML 셸 생성
```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{product_name}} | 썬데이허그</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Noto+Sans+KR:wght@300;400;500;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<style>
/* _base-styles.css 내용을 여기에 삽입 */
</style>
</head>
<body>

<!-- 이 사이에 섹션 템플릿을 순서대로 삽입 -->

<script>
/* _animations.js 내용을 여기에 삽입 */
</script>
</body>
</html>
```

### 2단계: 섹션 조립
아래 **섹션 순서표**를 따라 필수 섹션을 배치하고, 제품 특성에 맞는 선택 섹션을 추가합니다.

### 3단계: 플레이스홀더 치환
각 섹션의 `{{placeholder}}`를 실제 제품 데이터로 치환합니다.

---

## 섹션 순서표

### 흐름 설계 원칙
```
[시선 포착] → [신뢰 확보] → [문제 인식] → [해결책 제시] → [구매 유도]
→ [사회적 증거] → [프로모션] → [상세 정보] → [감성 마무리] → [최종 전환]
```

### 전체 섹션 맵

| 순서 | 파일명 | 섹션명 | 필수 | 배경 | 목적 카테고리 |
|------|--------|--------|------|------|---------------|
| 01 | 01-hero.html | Hero | ✅ | warm | 시선 포착 |
| 02 | 02-trust-bar.html | Trust Bar | ✅ | dark | 신뢰 확보 |
| 03 | 03-intro.html | Intro | ✅ | white | 문제 인식 |
| -- | (thin-line) | 구분선 | - | - | - |
| 04 | 04-safety.html | Safety | 선택 | white | 문제 인식 |
| -- | (thin-line) | 구분선 | - | - | - |
| 05 | 05-key-features.html | Key Features | ✅ | white | 해결책 제시 |
| 06 | 06-mid-cta.html | Mid CTA | ✅ | gradient | 구매 유도 |
| 07 | 07-review.html | Review | ✅ | warm | 사회적 증거 |
| 08 | 08-event.html | Event | 선택 | white | 프로모션 |
| 09 | 09-lifestyle-image.html | Lifestyle Image | 선택 | - | 시각 휴식 |
| 10 | 10-product-guide.html | Product Guide | 선택 | warm | 상세 정보 |
| 10a | 10a-expert-card.html | Expert Card | 선택 | warm톤 | 사회적 증거 |
| 09 | 09-lifestyle-image.html | Lifestyle Image | 선택 | - | 시각 휴식 |
| 11 | 11-material.html | Material | 선택 | white | 상세 정보 |
| 12 | 12-feature-points.html | Feature Points | ✅ | 교차 | 상세 정보 |
| 12a | 12a-feature-overlay.html | Feature Overlay | 선택 | img | 상세 정보 |
| 13 | 13-product-detail.html | Product Detail | ✅ | warm | 상세 정보 |
| 14 | 14-color-variation.html | Color Variation | ✅ | white | 상세 정보 |
| 15 | 15-size-design.html | Size Design | 선택 | warm | 상세 정보 |
| 16 | 16-how-to-wear.html | How to Wear | 선택 | white | 상세 정보 |
| 17 | 17-size-info.html | Size Info | ✅ | warm | 상세 정보 |
| 18 | 18-care.html | Care | ✅ | white | 상세 정보 |
| 19 | 19-shipping.html | Shipping | ✅ | warm | 신뢰 확보 |
| 20 | 20-other-products.html | Other Products | 선택 | white | 크로스셀 |
| 21 | 21-product-info.html | Product Info | ✅ | warm | 상세 정보 |
| 22 | 22-brand-quote.html | Brand Quote | ✅ | dark | 감성 마무리 |
| 23 | 23-brand-story.html | Brand Story | ✅ | warm | 감성 마무리 |
| 24 | 24-final-cta.html | Final CTA | ✅ | dark | 최종 전환 |
| 25 | 25-close.html | Close | ✅ | warm | 감성 마무리 |
| 26 | 26-footer.html | Footer | ✅ | dark | 마무리 |
| 27 | 27-sticky-bar.html | Sticky Bar | ✅ | white | 상시 전환 |

> **배경 교차 규칙**: white → warm → white → warm 순서로 교차. dark 섹션은 Brand Quote, Final CTA, Footer에만 사용. 연속된 같은 배경을 피할 것.

---

## 필수 vs 선택 섹션 가이드

### 항상 필수인 섹션 (15개)
Hero, Trust Bar, Intro, Key Features, Mid CTA, Review, Feature Points, Product Detail, Color Variation, Size Info, Care, Shipping, Product Info, Brand Quote, Brand Story, Final CTA, Close, Footer, Sticky Bar

### 제품 유형별 선택 섹션

| 섹션 | 언제 사용 | 예시 |
|------|-----------|------|
| Safety | 안전 이슈가 있는 제품 | 슬리핑백(질식 위험), 카시트 |
| Event | 프로모션 진행 중일 때 | 사은품 증정, 한정 할인 |
| Lifestyle Image | 시각적 브레이크 필요 시 | 긴 상세페이지 중간중간 |
| Product Guide | 시리즈/연계 제품이 있을 때 | 수면 솔루션 가이드 |
| Material | 소재 비교가 중요할 때 | 밤부/코튼/메쉬 비교 |
| Size Design | 사이즈별 기능 차이가 있을 때 | S=스냅버튼, M/L=풀집업 |
| How to Wear | 착용/사용법 설명 필요 시 | 슬리핑백, 힙시트 |
| Other Products | 관련 제품 크로스셀 | 같은 카테고리 제품 |
| Expert Card | 전문가 추천으로 신뢰도 높일 때 | 수면컨설턴트 추천, 통계 포함 |
| Feature Overlay | 이미지 임팩트를 극대화할 때 | 풀 이미지 위 텍스트 오버레이 |

---

## 플레이스홀더 규칙

### 문법
- `{{변수명}}` — 단순 텍스트 치환
- `{{변수명_html}}` — HTML 포함 가능 (줄바꿈은 `<br>`)
- `{{#반복블록}}...{{/반복블록}}` — 반복 데이터 (리뷰, 컬러, 사은품 등)
- `{{?조건블록}}...{{/조건블록}}` — 조건부 표시

### 공통 변수 (모든 페이지에서 사용)
```
{{brand_tag}}        — 브랜드 태그 (예: "SUNDAY HUG")
{{product_name}}     — 제품명 (예: "꿀잠 슬리핑백 실키밤부")
{{product_name_short}} — 짧은 제품명 (예: "꿀잠 슬리핑백")
{{purchase_url}}     — 구매 링크 URL
{{brand_quote}}      — 브랜드 인용문
```

### 이미지 규격
| 위치 | 권장 크기 | 비율 |
|------|-----------|------|
| Hero | 600×540 | - |
| Lifestyle (풀블리드) | 600×360 | 5:3 |
| Feature 좌우교차 | 280×320 | 7:8 |
| Feature 센터 | 600×400 | 3:2 |
| Sub-point | 280×220 | 14:11 |
| Detail grid | 270×200 | 4:3 |
| Color variation | 270×340 | 약 4:5 |
| Review strip | 200×200 | 1:1 |
| Other products | 180×180 | 1:1 |
| Feature Overlay | 600×800+ | 3:4 이상 |
| Expert avatar | 96×96 | 1:1 원형 |
| Color grid item | 270×360 | 3:4 |

---

## 배경 교차 패턴

시각적 리듬과 가독성을 위해 섹션 배경색을 교차 배치합니다:

```
white  → Hero + Trust Bar (hero는 warm이지만 이미지가 덮음)
white  → Intro
white  → Safety (선택)
white  → Key Features
gradient → Mid CTA
warm   → Review
white  → Event (선택)
(풀블리드 이미지)
warm   → Product Guide (선택)
(풀블리드 이미지)
white  → Material (선택)
교차   → Feature Points (white ↔ warm 반복)
warm   → Product Detail
white  → Color Variation
warm   → Size Design (선택)
white  → How to Wear (선택)
warm   → Size Info
white  → Care
warm   → Shipping
white  → Other Products (선택)
warm   → Product Info
dark   → Brand Quote
warm   → Brand Story
dark   → Final CTA
warm   → Close
dark   → Footer
white  → Sticky Bar (fixed)
```

---

## 디자인 시스템 요약

### 컬러 토큰
```css
--bg: #FFFFFF          /* 기본 배경 */
--bg-warm: #FAF7F4     /* 따뜻한 배경 */
--bg-warm2: #F5F0EB    /* 진한 따뜻한 배경 */
--dark: #1A1A1A        /* 다크 텍스트 */
--dark2: #2C2C3A       /* 다크 섹션 배경 */
--accent: #C8A07C      /* 포인트 컬러 (골드) */
--accent-light: #F0E6DA /* 연한 포인트 */
--danger: #D4645C      /* 경고/위험 */
--safe: #7C9A72        /* 안전/긍정 */
```

### 타이포그래피
```
디스플레이: Cormorant Garamond (브랜드 인용, 로고)
본문: Noto Sans KR (한글 콘텐츠 전체)
영문 라벨: DM Sans (섹션 라벨, 메타)
```

### 레이아웃
```
최대폭: 600px (모바일 중심)
좌우 패딩: 30px
섹션 상하 패딩: 52px
```

---

## 에이전트 작업 체크리스트

상세페이지를 만들 때 아래 순서를 따르세요:

1. ☐ 이 GUIDE.md를 읽는다
2. ☐ 제품 정보를 확인한다 (제품명, 특징, 이미지, 가격 등)
3. ☐ 필수 섹션 + 해당 제품에 필요한 선택 섹션을 결정한다
4. ☐ `_base-styles.css` 내용을 `<style>` 태그에 삽입한다
5. ☐ 섹션 순서표에 따라 섹션 템플릿을 순서대로 조립한다
6. ☐ 각 섹션의 `{{placeholder}}`를 제품 데이터로 치환한다
7. ☐ `_animations.js` 내용을 `<script>` 태그에 삽입한다
8. ☐ 배경 교차 패턴이 지켜지는지 확인한다
9. ☐ thin-line 구분선이 필요한 곳에 `<div class="thin-line"></div>` 추가
10. ☐ 최종 HTML 파일을 저장한다
