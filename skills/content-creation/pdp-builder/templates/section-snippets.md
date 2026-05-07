# SundayHug PDP — Section Snippets (조합 가능한 빌딩 블록)

> 각 섹션은 **HTML 주석 라벨**로 시작한다. 변수는 `{{...}}` 표기. AI가 카피 생성 시 슬롯만 채워 넣으면 된다.
> 모든 스니펫은 `<div class="pdp-absolute">` 내부 직계 자식으로 배치.

## 0. 페이지 셸 (필수)

```html
<meta charset="UTF-8">
<!-- Styles -->
<link rel="stylesheet" href="https://sundayhugkr.cafe24.com/skin-skin69/product/details/styles.css">
<style>
  /* 제품별 추가 클래스만 여기 (스타일 마스터는 절대 수정 금지) */
</style>
<div class="pdp-absolute">
  {{... 섹션들 ...}}
</div>
```

> Cafe24가 아닌 로컬 프리뷰일 경우 `href`를 `./styles.css`로 바꾸면 된다.

---

## 1. HERO (필수)

```html
<!-- HERO -->
<div class="hero">
  <img class="hero-img" src="{{HERO_IMG_URL}}" alt="{{PRODUCT_NAME}}">
  <div class="hero-text">
    <div class="hero-tag">SUNDAY HUG</div>
    <h1>{{HERO_HEADLINE_LINE1}}<br>{{HERO_HEADLINE_LINE2}}</h1>
    <p class="hero-sub">{{HERO_SUB_LINE1}}<br>{{PRODUCT_NAME}}</p>
  </div>
</div>
```

**카피 가이드**: `<h1>`은 **감성 후킹 한 문장**(예: "빛을 차단하면 아기의 잠이 달라져요"). `.hero-sub`는 제품 카테고리 + 정식 상품명.

## 2. TRUST BAR (선택, 강력 추천)

```html
<!-- TRUST BAR -->
<div class="trust-bar">
  <div class="trust-bar-item">{{KEY_POINT_1}}<small>{{SUB_1}}</small></div>
  <div class="trust-bar-item">{{KEY_POINT_2}}<small>{{SUB_2}}</small></div>
  <div class="trust-bar-item">{{KEY_POINT_3}}<small>{{SUB_3}}</small></div>
</div>
```

3개 핵심 USP를 8자 이내로 압축. 영문보다는 한글 단어 추천.

## 3. INTRO (필수) — 사용자 페인 포인트 → 해법 제시

```html
<!-- INTRO -->
<div class="sec v">
  <div class="sec-label">{{ENGLISH_LABEL}}</div>
  <div class="sec-title">"{{PAIN_QUESTION}}"</div>
  <div class="sec-desc">
    {{PAIN_NARRATIVE_HTML}}
    <span class="hl">{{KEY_INSIGHT}}</span>로<br>
    {{BRAND_PRODUCT_NAME}}<br>
    {{CALL_TO_VALUE}}
  </div>
  <div class="fb-img"><img src="{{INTRO_IMG_URL}}" alt="{{INTRO_ALT}}"></div>
</div>

<div class="thin-line"></div>
```

## 4. OVERVIEW (선택)

```html
<!-- OVERVIEW -->
<div class="sec warm v">
  <div class="sec-label tx-center">Overview</div>
  <div class="sec-title tx-center">{{OVERVIEW_HEADLINE}}</div>
  <div class="sec-desc tx-center">
    {{OVERVIEW_BODY_HTML}}
  </div>
  <div class="fb-img"><img src="{{OVERVIEW_IMG_URL}}" alt="{{OVERVIEW_ALT}}"></div>
</div>
```

## 5. BRAND QUOTE (구분/감성 포인트)

```html
<!-- BRAND QUOTE -->
<div class="bq">
  <p>"{{QUOTE_LINE1}}<br>{{QUOTE_LINE2}}"</p>
  <small>SUNDAY HUG</small>
</div>
```

페이지 안에 2~3번 등장 가능. 섹션 사이 호흡용.

## 6. WHY {FEATURE} — 핵심 가치 설명

```html
<!-- WHY {FEATURE_KEYWORD} -->
<div class="sec cool v">
  <div class="sec-label">Why {{FEATURE_EN}}?</div>
  <div class="sec-title">{{FEATURE_KOREAN_TITLE}}</div>
  <div class="sec-desc">
    <span class="hl">{{HOOK_SENTENCE}}</span><br><br>
    {{BODY_PARA_1}}<br><br>
    {{BODY_PARA_2}}
  </div>
</div>
```

배경 변형 자유: `cool` / `warm` / `cream` / `sage` 중 선택해 시각적 리듬 만들기.

## 7. KEY FEATURE 01/02/03 (제품별 인라인 스타일 필요)

> `.feat-hz` 클래스는 마스터 CSS에 없음. HTML 상단 인라인 `<style>`에서 정의 (`abc-cover.html` 참고).

```html
<!-- FEAT 01 -- {{FEATURE_NAME}} -->
<div class="feat v">
  <div class="feat-hz">
    <div class="feat-hz-img"><img src="{{FEAT_IMG_URL}}" alt="{{FEAT_ALT}}"></div>
    <div class="feat-hz-body">
      <div class="feat-num">KEY FEATURE 01</div>
      <div class="feat-title">{{FEAT_TITLE}}</div>
      <div class="feat-desc">
        {{FEAT_BODY_HTML}}
      </div>
    </div>
  </div>
</div>
```

번호 짝수 (`02`, `04`)에는 `<div class="feat-hz rev">` 로 좌우 반전 → 시각적 리듬.

## 8. SUB 2-COL (디테일 컷 2장)

```html
<div class="sub-2col">
  <div class="sub-2col-item v">
    <img src="{{IMG_1}}" alt="{{ALT_1}}" style="border-radius:6px;margin-bottom:12px;">
    <h4>{{TITLE_1}}</h4>
    <p>{{DESC_1}}</p>
  </div>
  <div class="sub-2col-item v">
    <img src="{{IMG_2}}" alt="{{ALT_2}}" style="border-radius:6px;margin-bottom:12px;">
    <h4>{{TITLE_2}}</h4>
    <p>{{DESC_2}}</p>
  </div>
</div>
```

## 9. USE CASE / STEP LIST

```html
<!-- USE CASE -->
<div class="sec v">
  <div class="sec-label">Use Case</div>
  <div class="sec-title">{{USECASE_HEADLINE}}</div>
  <div class="sec-desc">{{USECASE_INTRO}}</div>

  <div class="step-list">
    <div class="step-item v">
      <div class="step-num">CASE 01</div>
      <div class="step-title">{{CASE_1_TITLE}}</div>
      <div class="step-desc">{{CASE_1_BODY_HTML}}</div>
    </div>
    <!-- CASE 02, 03 ... -->
  </div>
</div>
```

## 10. FAQ

```html
<!-- FAQ -->
<div class="sec warm v">
  <div class="sec-label">FAQ</div>
  <div class="sec-title">자주 묻는 질문</div>

  <div style="margin-top:24px;">
    <div class="faq-item">
      <div class="faq-q">Q1. {{QUESTION_1}}</div>
      <div class="faq-a">{{ANSWER_1}}</div>
    </div>
    <!-- Q2, Q3, ... -->
  </div>
</div>
```

질문은 5개 권장. 실제 CS 문의 빈도순으로 배치.

## 11. SPECS / INFO TABLE (제품별 인라인 스타일)

> `.info-tbl`도 인라인 스타일 (`abc-cover.html` 참고).

```html
<!-- SPECS -->
<div class="sec v">
  <div class="sec-label">Specifications</div>
  <div class="sec-title">제품 사양</div>
  <table class="info-tbl">
    <tr><th>{{LABEL_1}}</th><td>{{VALUE_1}}</td></tr>
    <tr><th>{{LABEL_2}}</th><td>{{VALUE_2}}</td></tr>
    <tr><th>{{LABEL_3}}</th><td>{{VALUE_3}}</td></tr>
  </table>
</div>
```

전형 라벨: 사이즈, 중량, 소재, 인증, 제조사, 원산지, A/S.

## 12. BRAND STORY

```html
<!-- BRAND STORY -->
<div class="sec warm v">
  <div class="sec-label tx-center">Our Story</div>
  <div class="sec-title tx-center">가족의 행복한 일상,<br>썬데이허그</div>
  <div class="sec-desc tx-center">
    우리는 가족 구성원 각자가<br>
    다양한 역할과 책임으로<br>
    분주한 일상을 보내고 있음을<br>
    잘 알고 있습니다.<br><br>
    이러한 일상 속에서도,<br>
    우리 브랜드를 통해<br>
    가족 모두가 함께<br>
    소중한 순간을 만들고<br>
    일상의 행복을<br>
    누릴 수 있기를 바랍니다.
  </div>
  <div class="fb-img"><img src="{{BRAND_STORY_IMG}}" alt="브랜드 스토리"></div>
</div>
```

본문은 SundayHug 공통 카피 — **변경하지 말 것**.

## 13. FINAL CTA (필수)

```html
<!-- FINAL CTA -->
<div class="final-cta v">
  <div class="final-cta-label">SUNDAY HUG</div>
  <h2>{{CTA_HEADLINE_LINE1}}<br>{{CTA_HEADLINE_LINE2}}<br>{{CTA_HEADLINE_LINE3}}</h2>
  <p>{{KEY_BENEFITS_SLASHED}}</p>
  <div class="final-cta-note">{{COLOR}} / {{SIZE}} / {{DIMENSIONS}}</div>
</div>
```

## 14. WASH & CARE (선택, 의류/패브릭 제품 권장)

```html
<!-- WASH & CARE -->
<div class="sec v">
  <div class="sec-label">How To Care</div>
  <div class="sec-title">세탁 및 관리 방법</div>

  <div class="note-card v">
    <div class="note-hd">
      <h3>Wash Guide</h3>
      <span>CARE NOTE</span>
    </div>
    <div class="note-item">
      <strong>Wash</strong>
      <p>{{WASH_INSTRUCTION_HTML}}</p>
    </div>
    <div class="note-item">
      <strong>Separate</strong>
      <p>{{SEPARATE_INSTRUCTION_HTML}}</p>
    </div>
    <div class="note-item">
      <strong>Dry</strong>
      <p>{{DRY_INSTRUCTION}}</p>
    </div>
    <div class="note-item">
      <strong>Caution</strong>
      <p>{{CAUTION_HTML}}</p>
    </div>
  </div>
</div>
```

---

## 권장 섹션 구성 (제품 유형별)

| 제품 유형 | 추천 섹션 순서 |
|---|---|
| **수면 용품** (sleeping bag, swaddle, 암막커버) | HERO → TRUST BAR → INTRO → OVERVIEW → BQ → WHY × 2 → FEAT × 3 → SUB-2COL → USE CASE → FAQ → BQ → BRAND STORY → FINAL CTA → WASH & CARE → SPECS |
| **데일리 의류** (bodysuit, pajama) | HERO → TRUST BAR → INTRO → OVERVIEW → FEAT × 2~3 → SUB-2COL → COLOR/SIZE 가변 → FAQ → FINAL CTA → WASH & CARE → SPECS |
| **세트/패키지** (pajama-set 등) | HERO → COMP-GRID (구성품 그리드) → TRUST BAR → INTRO → FEAT × 2 → USE CASE → FAQ → FINAL CTA → SPECS |
| **유아침대 본체** (abc 메인) | HERO → TRUST BAR → INTRO → OVERVIEW → BQ → WHY × 2 → FEAT × 4~5 → SUB-2COL × N → USE CASE → COMPARISON GRID → FAQ → BRAND STORY → FINAL CTA → SPECS |

**최소 필수 섹션**: HERO + INTRO + WHY × 1 + FINAL CTA + SPECS
