# 레이아웃 템플릿 가이드

각 레이아웃의 HTML/CSS 구조를 정의한다. 모든 템플릿은 다음 변수를 치환하여 사용:

- `{{WIDTH}}`, `{{HEIGHT}}` — 사이즈 (px)
- `{{IMAGE_BASE64}}` — 제품 이미지 base64 데이터
- `{{HEADLINE}}` — 헤드라인 텍스트
- `{{SUBTEXT}}` — 서브 카피
- `{{CTA}}` — CTA 버튼 텍스트
- `{{PRICE}}` — 가격 (선택)
- `{{DISCOUNT}}` — 할인 정보 (선택)
- `{{BRAND_PRIMARY}}` — 브랜드 메인 컬러
- `{{BRAND_SECONDARY}}` — 브랜드 보조 컬러
- `{{BRAND_ACCENT}}` — 액센트 컬러
- `{{BRAND_NAME}}` — 브랜드명
- `{{LOGO_BASE64}}` — 로고 이미지 (선택)

## 공통 CSS 베이스

```css
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }

.ad-container {
  width: {{WIDTH}}px;
  height: {{HEIGHT}}px;
  position: relative;
  overflow: hidden;
  font-family: 'Noto Sans KR', sans-serif;
  background: {{BRAND_SECONDARY}};
}

.ad-container img.product {
  object-fit: cover;
  width: 100%;
  height: 100%;
}
```

---

## 1. hero-image (이미지 풀 + 텍스트 오버레이)

가장 범용적. 강한 제품 이미지가 있을 때 최적.

**구조:**
- 이미지가 전체 배경
- 하단 그라데이션 오버레이 위에 텍스트
- 선택적 상단 배지 (할인/이벤트)

```html
<div class="ad-container">
  <img class="product" src="data:image/jpeg;base64,{{IMAGE_BASE64}}" alt="product">
  
  <!-- 하단 그라데이션 -->
  <div style="position:absolute; bottom:0; left:0; right:0; height:55%;
    background: linear-gradient(transparent, rgba(0,0,0,0.75)); z-index:1;">
  </div>
  
  <!-- 텍스트 영역 -->
  <div style="position:absolute; bottom:0; left:0; right:0; padding:8%; z-index:2; color:#fff;">
    <p style="font-size:{{SUBTEXT_SIZE}}px; opacity:0.9; margin-bottom:8px; line-height:1.4;">
      {{SUBTEXT}}
    </p>
    <h2 style="font-size:{{HEADLINE_SIZE}}px; font-weight:900; line-height:1.2; margin-bottom:16px;">
      {{HEADLINE}}
    </h2>
    <div style="display:inline-block; background:{{BRAND_PRIMARY}}; color:#fff;
      padding:12px 32px; border-radius:8px; font-weight:700; font-size:{{CTA_SIZE}}px;">
      {{CTA}}
    </div>
  </div>
  
  <!-- 할인 배지 (선택) -->
  {{#DISCOUNT}}
  <div style="position:absolute; top:5%; right:5%; background:{{BRAND_ACCENT}};
    color:#fff; padding:10px 20px; border-radius:50px; font-weight:900;
    font-size:{{BADGE_SIZE}}px; z-index:2;">
    {{DISCOUNT}}
  </div>
  {{/DISCOUNT}}
  
  <!-- 브랜드 로고 (선택) -->
  {{#LOGO_BASE64}}
  <div style="position:absolute; top:5%; left:5%; z-index:2;">
    <img src="data:image/png;base64,{{LOGO_BASE64}}" style="height:40px; opacity:0.9;">
  </div>
  {{/LOGO_BASE64}}
</div>
```

**사이즈별 폰트 조정:**
| 사이즈 | HEADLINE_SIZE | SUBTEXT_SIZE | CTA_SIZE | BADGE_SIZE |
|--------|--------------|-------------|----------|-----------|
| 1080×1080 | 42 | 20 | 18 | 22 |
| 1080×1350 | 48 | 22 | 20 | 24 |
| 1080×1920 | 52 | 24 | 22 | 26 |

---

## 2. split-horizontal (좌우 분할)

제품 이미지와 텍스트를 균형있게 보여줄 때.

**구조:**
- 좌: 제품 이미지 (50~55%)
- 우: 텍스트 + CTA (45~50%)

```html
<div class="ad-container" style="display:flex;">
  <!-- 이미지 영역 -->
  <div style="width:55%; position:relative; overflow:hidden;">
    <img class="product" src="data:image/jpeg;base64,{{IMAGE_BASE64}}" 
      style="width:100%; height:100%; object-fit:cover;">
  </div>
  
  <!-- 텍스트 영역 -->
  <div style="width:45%; display:flex; flex-direction:column; justify-content:center;
    padding:8%; background:{{BRAND_SECONDARY}};">
    
    <div style="font-size:13px; color:{{BRAND_PRIMARY}}; font-weight:700;
      text-transform:uppercase; letter-spacing:2px; margin-bottom:12px;">
      {{BRAND_NAME}}
    </div>
    
    <h2 style="font-size:{{HEADLINE_SIZE}}px; font-weight:900; color:#1a1a1a;
      line-height:1.2; margin-bottom:16px;">
      {{HEADLINE}}
    </h2>
    
    <p style="font-size:{{SUBTEXT_SIZE}}px; color:#555; line-height:1.5; margin-bottom:24px;">
      {{SUBTEXT}}
    </p>
    
    {{#PRICE}}
    <div style="font-size:28px; font-weight:900; color:{{BRAND_PRIMARY}}; margin-bottom:20px;">
      {{PRICE}}
    </div>
    {{/PRICE}}
    
    <div style="display:inline-block; background:{{BRAND_PRIMARY}}; color:#fff;
      padding:14px 32px; border-radius:8px; font-weight:700; font-size:{{CTA_SIZE}}px;
      text-align:center;">
      {{CTA}}
    </div>
  </div>
</div>
```

**사이즈별 폰트:**
| 사이즈 | HEADLINE_SIZE | SUBTEXT_SIZE | CTA_SIZE |
|--------|--------------|-------------|----------|
| 1080×1080 | 32 | 16 | 16 |
| 1080×1350 | 36 | 18 | 18 |
| 1080×1920 | 40 | 20 | 20 |

---

## 3. split-vertical (상하 분할)

세로 포맷(4:5, 9:16)에 최적.

**구조:**
- 상: 제품 이미지 (55~60%)
- 하: 텍스트 + CTA (40~45%)

```html
<div class="ad-container" style="display:flex; flex-direction:column;">
  <!-- 이미지 영역 -->
  <div style="flex:6; position:relative; overflow:hidden;">
    <img class="product" src="data:image/jpeg;base64,{{IMAGE_BASE64}}"
      style="width:100%; height:100%; object-fit:cover;">
    {{#DISCOUNT}}
    <div style="position:absolute; top:6%; right:6%; background:{{BRAND_ACCENT}};
      color:#fff; padding:10px 22px; border-radius:50px; font-weight:900;
      font-size:{{BADGE_SIZE}}px;">
      {{DISCOUNT}}
    </div>
    {{/DISCOUNT}}
  </div>
  
  <!-- 텍스트 영역 -->
  <div style="flex:4; display:flex; flex-direction:column; justify-content:center;
    align-items:center; padding:6% 8%; background:{{BRAND_SECONDARY}}; text-align:center;">
    
    <h2 style="font-size:{{HEADLINE_SIZE}}px; font-weight:900; color:#1a1a1a;
      line-height:1.2; margin-bottom:12px;">
      {{HEADLINE}}
    </h2>
    
    <p style="font-size:{{SUBTEXT_SIZE}}px; color:#555; line-height:1.5; margin-bottom:20px;">
      {{SUBTEXT}}
    </p>
    
    <div style="background:{{BRAND_PRIMARY}}; color:#fff; padding:14px 40px;
      border-radius:8px; font-weight:700; font-size:{{CTA_SIZE}}px;">
      {{CTA}}
    </div>
  </div>
</div>
```

---

## 4. benefit-stack (USP 나열형)

다수의 장점을 빠르게 전달할 때.

**구조:**
- 상단: 제품 이미지 (40%)
- 하단: USP 3~4개를 아이콘+텍스트로 나열

```html
<div class="ad-container" style="display:flex; flex-direction:column; background:{{BRAND_SECONDARY}};">
  <!-- 이미지 -->
  <div style="flex:4; position:relative; overflow:hidden;">
    <img class="product" src="data:image/jpeg;base64,{{IMAGE_BASE64}}"
      style="width:100%; height:100%; object-fit:cover;">
  </div>
  
  <!-- 베네핏 영역 -->
  <div style="flex:6; padding:6% 8%; display:flex; flex-direction:column; justify-content:center;">
    <h2 style="font-size:{{HEADLINE_SIZE}}px; font-weight:900; color:#1a1a1a;
      text-align:center; margin-bottom:24px;">
      {{HEADLINE}}
    </h2>
    
    <!-- 베네핏 리스트 -->
    <div style="display:flex; flex-direction:column; gap:16px; margin-bottom:24px;">
      {{#BENEFITS}}
      <div style="display:flex; align-items:center; gap:16px;">
        <div style="width:48px; height:48px; background:{{BRAND_PRIMARY}}; border-radius:50%;
          display:flex; align-items:center; justify-content:center; flex-shrink:0;">
          <span style="color:#fff; font-size:22px;">{{ICON}}</span>
        </div>
        <div>
          <div style="font-weight:700; font-size:17px; color:#1a1a1a;">{{BENEFIT_TITLE}}</div>
          <div style="font-size:14px; color:#777;">{{BENEFIT_DESC}}</div>
        </div>
      </div>
      {{/BENEFITS}}
    </div>
    
    <div style="background:{{BRAND_PRIMARY}}; color:#fff; padding:14px 32px;
      border-radius:8px; font-weight:700; font-size:{{CTA_SIZE}}px; text-align:center;">
      {{CTA}}
    </div>
  </div>
</div>
```

**베네핏 아이콘:** 이모지 활용 — ✅ 🌿 💤 🛡️ ⭐ 🎁 💰 등

---

## 5. social-proof (리뷰/별점 강조)

신뢰도 구축. 리타겟팅에 효과적.

**구조:**
- 상단: 별점 + 리뷰 인용문
- 중앙: 제품 이미지
- 하단: CTA

```html
<div class="ad-container" style="display:flex; flex-direction:column; background:{{BRAND_SECONDARY}};
  padding:8%;">
  
  <!-- 리뷰 영역 -->
  <div style="text-align:center; margin-bottom:24px;">
    <div style="font-size:28px; margin-bottom:8px;">⭐⭐⭐⭐⭐</div>
    <p style="font-size:{{SUBTEXT_SIZE}}px; color:#333; font-style:italic; line-height:1.5;
      max-width:80%; margin:0 auto;">
      "{{REVIEW_TEXT}}"
    </p>
    <p style="font-size:14px; color:#999; margin-top:8px;">— {{REVIEWER_NAME}}</p>
  </div>
  
  <!-- 이미지 -->
  <div style="flex:1; position:relative; overflow:hidden; border-radius:16px; margin-bottom:24px;">
    <img class="product" src="data:image/jpeg;base64,{{IMAGE_BASE64}}"
      style="width:100%; height:100%; object-fit:cover;">
  </div>
  
  <!-- CTA -->
  <div style="text-align:center;">
    <h2 style="font-size:{{HEADLINE_SIZE}}px; font-weight:900; color:#1a1a1a; margin-bottom:16px;">
      {{HEADLINE}}
    </h2>
    <div style="display:inline-block; background:{{BRAND_PRIMARY}}; color:#fff;
      padding:14px 40px; border-radius:8px; font-weight:700; font-size:{{CTA_SIZE}}px;">
      {{CTA}}
    </div>
  </div>
</div>
```

---

## 6. urgency (긴급/한정)

전환 극대화. 세일, 타임특가, 한정수량에 사용.

**구조:**
- 강렬한 컬러 배경
- 대형 할인율/혜택 표시
- 제품 이미지 + 긴급 카피

```html
<div class="ad-container" style="background:{{BRAND_PRIMARY}}; display:flex; flex-direction:column;
  align-items:center; justify-content:center; padding:8%; text-align:center; color:#fff;">
  
  <!-- 긴급 배지 -->
  <div style="background:{{BRAND_ACCENT}}; padding:8px 24px; border-radius:50px;
    font-weight:900; font-size:16px; margin-bottom:20px; letter-spacing:1px;">
    {{URGENCY_LABEL}}
  </div>
  
  <!-- 할인/혜택 대형 표시 -->
  <div style="font-size:72px; font-weight:900; line-height:1; margin-bottom:16px;">
    {{DISCOUNT}}
  </div>
  
  <!-- 제품 이미지 (원형 또는 카드) -->
  <div style="width:60%; aspect-ratio:1; border-radius:20px; overflow:hidden;
    margin-bottom:24px; box-shadow:0 10px 40px rgba(0,0,0,0.3);">
    <img class="product" src="data:image/jpeg;base64,{{IMAGE_BASE64}}"
      style="width:100%; height:100%; object-fit:cover;">
  </div>
  
  <h2 style="font-size:{{HEADLINE_SIZE}}px; font-weight:900; margin-bottom:12px;">
    {{HEADLINE}}
  </h2>
  
  <p style="font-size:{{SUBTEXT_SIZE}}px; opacity:0.9; margin-bottom:24px;">
    {{SUBTEXT}}
  </p>
  
  <div style="background:#fff; color:{{BRAND_PRIMARY}}; padding:16px 48px;
    border-radius:8px; font-weight:900; font-size:{{CTA_SIZE}}px;">
    {{CTA}}
  </div>
</div>
```

---

## 미리보기 그리드 (preview-grid.html) 생성 가이드

모든 개별 HTML 소재를 한 화면에서 확인할 수 있는 그리드 뷰를 생성한다.

**구성:**
- 상단: 필터 바 (사이즈, 레이아웃, 톤)
- 그리드: 각 소재를 축소 미리보기로 표시
- 각 소재 카드: 썸네일 + 파일명 + 메타 정보(사이즈, 레이아웃, 톤)
- 소재 클릭 시 실제 사이즈 모달 팝업

**구현 방식:**
- 각 소재 HTML의 내용을 inline으로 포함 (iframe 또는 scaled div)
- JavaScript로 필터링/모달 기능
- 반응형 그리드 (CSS Grid)
- 모든 CSS/JS inline (독립 실행 가능)
