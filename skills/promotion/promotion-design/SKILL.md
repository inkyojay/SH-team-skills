---
name: promotion-design
description: 썬데이허그 프로모션 디자인 제작. 6개 채널(라이브/카카오/인스타/스마트스토어/네이버/메타광고) 템플릿으로 HTML → PNG → .pen 디자인 생성.
triggers:
  - "프로모션 디자인"
  - "프로모션 제작"
  - "promotion design"
  - "라이브 페이지 만들어줘"
  - "카카오 메시지 만들어줘"
  - "배너 만들어줘"
  - "인스타 만들어줘"
  - "메타 광고 만들어줘"
  - "광고 소재 만들어줘"
  - "meta ads"
---

# 프로모션 디자인 제작 스킬

6개 채널의 템플릿을 활용하여 HTML 디자인을 생성하고, 사용자와 대화하며 조정한 뒤, 최종본을 섹션별 PNG + .pen 파일로 저장합니다.

## 지원 채널 (6개)

| 채널 | 템플릿 경로 | 구조 |
|------|-----------|------|
| 라이브 프로모션 페이지 | `templates/promotion/live-page/` | 섹션 기반 (31개 섹션, 다수 변형) |
| 카카오 메시지 | `templates/promotion/kakao-messages/` | 타입-변형 기반 (8타입, 23변형) |
| 인스타그램 | `templates/promotion/instagram/` | 타입-변형 기반 (6타입, 18변형) |
| 스마트스토어 배너 | `templates/promotion/smartstore-banners/` | 타입-변형 기반 (5타입, 15변형) |
| 네이버 라이브 배너 | `templates/promotion/naver-live-banners/` | 타입-변형 기반 (5타입, 15변형) |
| 메타 광고 | `templates/promotion/meta-ads/` | 소구점 기반 (10타입, 30변형) |

---

## 두 가지 입력 모드

### 모드 A: JSON 토글 방식 (정밀 제어)

사용자가 template-guide.html에서 토글로 섹션을 선택하고 JSON을 붙여넣는 방식.

### 모드 B: 자유 요청 방식 (AI 추천)

사용자가 프로모션 정보와 사진만 주고 "알아서 만들어줘"라고 요청하는 방식.
JSON 없이도 프로모션 내용을 분석하여 적합한 섹션/변형을 AI가 선택합니다.

**자유 요청 처리 흐름:**
1. 프로모션 정보(제품, 혜택, 기간 등) 파악
2. 채널 확인 (명시 안 하면 질문)
3. 소재 사진 폴더 확인 → 이미지 분석
4. 프로모션 성격에 맞는 섹션/변형 자동 선택
5. 선택한 구성을 사용자에게 제안:

```markdown
## 추천 구성

프로모션 내용을 분석하여 다음 구성을 추천합니다:

| 섹션 | 변형 | 선택 이유 |
|------|------|----------|
| 00 Live Thumbnail | - | 썸네일 필수 |
| 01 Live Hero | D (Photo BG Dark) | 제품 사진 활용 |
| 05 Live Benefits | D (Tiered Pricing) | 다량 구매 할인 강조 |
| 06 Coupon | B (Multi) | 쿠폰 3종 |
| 17 Gift Event | D (Photo Banner) | 사은품 사진 있음 |
| ...

이 구성으로 진행할까요? 수정할 부분이 있으면 알려주세요.
```

6. 확인 후 HTML 조합 진행

---

## Phase 1: 입력 수집

사용자에게 아래를 요청합니다. 이미 제공된 정보는 건너뜁니다.

### 1-1. 프로모션 정보

```markdown
## 프로모션 정보를 알려주세요

| 항목 | 예시 |
|------|------|
| 프로모션명 | 봄 슬리핑백 특가 |
| 대상 제품 | 실키밤부 슬리핑백 |
| 혜택 | 최대 52% 할인 + 사은품 3종 |
| 기간 | 3월 15일 ~ 3월 22일 |
| 핵심 메시지 | 라이브 단독 역대 최저가 |
| 가격 정보 | 정가 89,000원 → 42,800원 |

한 번에 알려주셔도 되고, 하나씩 말씀해주셔도 됩니다.
```

### 1-2. 소재 사진 폴더

```markdown
## 소재 사진 폴더

디자인에 사용할 사진이 들어있는 폴더 경로를 알려주세요.
예: ~/Desktop/photos 또는 ~/Downloads/프로모션소재

폴더 안의 모든 이미지(jpg, png, webp)를 자동으로 스캔합니다.
```

폴더를 받으면:
1. Glob으로 `{폴더}/**/*.{jpg,jpeg,png,webp}` 스캔
2. 각 이미지를 Read로 열어 시각적으로 확인
3. 이미지 목록을 표로 보여줌

### 1-3. 채널 선택

```markdown
## 채널 선택

어떤 채널용 디자인을 만들까요? (복수 선택 가능)

| # | 채널 | 가이드 |
|---|------|--------|
| 1 | 라이브 프로모션 페이지 | live-page/template-guide.html |
| 2 | 카카오 메시지 | kakao-messages/template-guide.html |
| 3 | 인스타그램 | instagram/template-guide.html |
| 4 | 스마트스토어 배너 | smartstore-banners/template-guide.html |
| 5 | 네이버 라이브 배너 | naver-live-banners/template-guide.html |
| 6 | 메타 광고 | meta-ads/template-guide.html |
```

### 1-4. 섹션 설정 (모드 A만 — JSON 토글)

```markdown
## 섹션 설정 (JSON)

template-guide.html을 브라우저에서 열고:
1. 원하는 팔레트를 선택하세요
2. 사용할 섹션/변형을 토글로 켜고 끄세요
3. **COPY JSON** 버튼을 클릭하세요
4. 여기에 붙여넣기 해주세요
```

JSON 없이 진행하면 → 모드 B (자유 요청)로 전환.

---

## Phase 2: HTML 조합

### 2-1. 템플릿 소스 로딩

```
프로젝트 루트: templates/promotion/

live-page:
  - _base-styles.css → 섹션 스타일
  - _palettes.css → 팔레트 CSS
  - ../_global-variables.css → 공통 변수
  - template-guide.html → 각 섹션 HTML 소스

kakao-messages / instagram / smartstore-banners / naver-live-banners:
  - _base-styles.css
  - _palettes.css
  - ../_global-variables.css
  - types/{type-id}/{variation}.html → 개별 변형 HTML
```

### 2-2. Live-page 조합 방법

1. template-guide.html에서 풀페이지 프리뷰 모드(`#mode-fullpage`) 안의 섹션 HTML을 추출
2. JSON/AI 선택 기반으로 필요한 섹션만 선택
3. `data-palette` 속성에 선택된 팔레트 적용
4. `<style>` 태그에 _base-styles.css + _palettes.css + _global-variables.css 인라인 삽입
5. 소재 사진 경로를 실제 이미지로 교체
6. 프로모션 정보(제품명, 가격, 혜택 등)를 실제 데이터로 치환

### 2-3. 타입 기반 채널 조합 방법 (카카오/인스타/스마트스토어/네이버)

1. 선택된 타입의 `variations` 배열 확인
2. 해당 `types/{type-id}/{variation}.html` 파일 읽기
3. 각 변형별로 독립 HTML 파일 생성
4. 팔레트 + 스타일 + 실제 데이터 적용

### 2-4. 데이터 치환 규칙

템플릿 HTML의 더미 텍스트를 실제 프로모션 데이터로 교체합니다:

| 더미 텍스트 패턴 | 치환 대상 |
|----------------|----------|
| 제품명 (슬리핑백 등) | `promotion.product` |
| 가격 (42,800원 등) | `promotion.price` |
| 할인율 (52% 등) | `promotion.discount` |
| 정가 (89,000원 등) | `promotion.original_price` |
| 혜택 텍스트 | `promotion.offer` |
| 기간 텍스트 | `promotion.period` |
| 핵심 메시지 | `promotion.key_message` |
| 이미지 src 경로 | 소재 사진 절대경로 |

### 2-5. 출력 파일

조합된 HTML을 임시 파일로 저장:

```
/tmp/promo-preview-{channel}.html
```

---

## Phase 3: 프리뷰 & 조정

### 3-1. 브라우저 프리뷰

```bash
open /tmp/promo-preview-{channel}.html
```

```markdown
## 프리뷰

브라우저에서 결과물을 확인해주세요.
수정이 필요한 부분이 있으면 알려주세요:

- "히어로 텍스트를 '역대 최저가'로 바꿔줘"
- "리뷰 섹션에 별점 4.9로 수정"
- "이미지를 다른 사진으로 바꿔줘"
- "섹션 순서를 바꿔줘"

만족하시면 "완료" 또는 "저장"이라고 말씀해주세요.
```

### 3-2. 수정 반영

사용자 피드백에 따라:
1. HTML 파일을 Edit 도구로 수정
2. 브라우저 새로고침 안내
3. 반복

---

## Phase 4: 최종 저장 (HTML + PNG)

### 4-1. 저장 폴더 생성

```bash
mkdir -p ~/Desktop/output/{프로모션명-slug}
```

`slug`는 프로모션명을 안전한 폴더명으로 변환:
- "봄 슬리핑백 특가" → `봄-슬리핑백-특가`
- 기존에 `~/Desktop/output/` 폴더가 있으면 그대로 사용

### 4-2. 최종 HTML 저장

```bash
cp /tmp/promo-preview-{channel}.html ~/Desktop/output/{slug}/{channel}.html
```

### 4-3. 섹션별 PNG 캡처

`/capture-sections` 스킬을 사용하여 섹션별 이미지를 생성합니다.

```
/capture-sections ~/Desktop/output/{slug}/{channel}.html
```

이 스킬이 자동으로:
- 전체 페이지 캡처
- 각 섹션별 개별 PNG 생성
- 같은 폴더에 `{파일명}_sections/` 하위로 저장

---

## Phase 5: .pen 파일 생성

HTML 확인이 완료되면, 동일한 디자인을 Pencil .pen 파일로도 생성합니다.

### 5-1. .pen 생성 방법

1. `open_document("new")` → 새 .pen 파일 생성
2. HTML에 적용된 사진, 텍스트, 레이아웃을 그대로 .pen으로 재현
3. `batch_design`으로 구성:
   - 각 섹션을 프레임으로 생성
   - 실제 소재 사진을 이미지 fill로 적용 (절대경로)
   - 텍스트/색상/레이아웃을 HTML과 동일하게
4. `get_screenshot`으로 결과 확인
5. 사용자 확인 후 저장

### 5-2. 저장 경로

```
~/Desktop/output/{slug}/
├── {channel}.html          ← 최종 HTML
├── {channel}.pen           ← Pencil 디자인 파일
├── 00_full-page.png        ← 전체 페이지
├── 01_live-thumb.png       ← 섹션별 PNG
├── 02_trust-bar.png
└── ...
```

### 5-3. .pen 생성 시 주의사항

- HTML에 사용된 이미지를 그대로 .pen에도 적용 (같은 절대경로)
- 팔레트 색상을 .pen 변수로 등록
- 각 섹션은 별도 프레임으로 구분
- live-page는 width 600px 기준
- 카카오 메시지는 800px, 인스타그램은 1080px 기준

---

## Phase 6: 완료 안내

```markdown
## 프로모션 디자인 완료!

**{프로모션명}** 디자인이 저장되었습니다.

📁 저장 위치: `~/Desktop/output/{slug}/`

| # | 파일 | 설명 |
|---|------|------|
| 1 | {channel}.html | 최종 HTML |
| 2 | {channel}.pen | Pencil 디자인 파일 |
| 3 | 00_full-page.png | 전체 페이지 |
| 4 | 01_live-thumb.png | 섹션별 PNG |
| ... | ... | ... |

Finder에서 폴더를 열까요?
```

```bash
open ~/Desktop/output/{slug}/
```

---

## 주의사항

- 이미지 경로는 반드시 절대경로로 변환하여 HTML에 삽입 (file:// 프로토콜에서 상대경로 깨짐 방지)
- 팔레트 CSS는 `[data-palette="{name}"]` 셀렉터로 적용
- live-page는 `max-width:600px` 모바일 뷰로 생성 (body에 적용)
- 카카오 메시지는 원본 사이즈(800px) 그대로 생성
- 인스타그램은 원본 사이즈(1080px) 그대로 생성
- 스마트스토어/네이버 배너는 각 타입별 원본 사이즈 유지
- 메타 광고는 소구점 타입별 3가지 포맷(1080×1080, 1080×1350, 1080×1920)으로 생성
- 소재 사진이 부족하면 기존 템플릿의 더미 이미지 유지하고 사용자에게 안내
- CSS는 외부 링크가 아닌 `<style>` 태그로 인라인 삽입 (독립 파일로 동작하도록)
- 구글 폰트 `<link>` 태그는 유지 (온라인 환경 가정)
- .pen 파일 생성 시 HTML과 동일한 소재 사진을 사용하여 일관성 유지
