# HTML 리포트 생성 스펙

## 출력 방식 선택

### A) `visualize:show_widget` (대화 내 즉시 표시)
- 1~3개월 짧은 프로모션 플랜
- 빠른 확인/수정 필요 시
- CSS 변수 사용: `var(--color-text-primary)`, `var(--color-background-primary)` 등
- `<style>`, `<div>`, `<script>` 직접 작성

### B) HTML 파일 생성 (다운로드용)
- 3개월+ 장기 플랜 또는 보고서
- 공유/인쇄 목적
- standalone HTML (모든 CSS/JS 인라인)
- `/mnt/user-data/outputs/promotion-plan.html`로 저장 후 `present_files`로 제공

---

## 디자인 시스템

### 컬러 팔레트

```css
/* 브랜드 메인 */
--brand-primary: #1D9E75;
--brand-primary-light: #E1F5EE;
--brand-primary-dark: #0F6E56;

/* 월별 테마 (3개월 기준, 확장 가능) */
--month-1-bg: #E1F5EE;  --month-1-text: #0F6E56;  --month-1-accent: #1D9E75;
--month-2-bg: #FAEEDA;  --month-2-text: #854F0B;  --month-2-accent: #EF9F27;
--month-3-bg: #FAECE7;  --month-3-text: #993C1D;  --month-3-accent: #D85A30;

/* 채널 뱃지 */
.ch-store    { background: #FAEEDA; color: #854F0B; }
.ch-naver    { background: #E6F1FB; color: #185FA5; }
.ch-insta    { background: #FAECE7; color: #993C1D; }
.ch-thread   { background: #EEEDFE; color: #3C3489; }
.ch-mamcafe  { background: #E1F5EE; color: #0F6E56; }
.ch-blog     { background: #F0E6FB; color: #5B2E91; }
.ch-member   { background: #EEEDFE; color: #3C3489; }

/* 프로모션 유형 뱃지 */
.badge-green  { background: #E1F5EE; color: #0F6E56; }
.badge-amber  { background: #FAEEDA; color: #854F0B; }
.badge-coral  { background: #FAECE7; color: #993C1D; }
.badge-blue   { background: #E6F1FB; color: #185FA5; }
.badge-purple { background: #EEEDFE; color: #3C3489; }
```

### 타이포그래피
- 위젯 모드: `var(--font-sans)` 사용
- 파일 모드: Google Fonts `Pretendard` 또는 `Noto Sans KR`
- 섹션 제목: 16px, font-weight: 500
- 본문: 13px, line-height: 1.6
- KPI 숫자: 22px, font-weight: 500
- 뱃지/라벨: 11~12px, font-weight: 500

### 레이아웃
- 최대 너비: 900px
- 카드 간격: 12px
- 카드 패딩: 1rem 1.25rem
- 카드 보더 라디우스: 8px (또는 `var(--border-radius-lg)`)
- 그리드: `repeat(auto-fit, minmax(200px, 1fr))`

---

## 필수 컴포넌트 HTML 구조

### 1. 탭 네비게이션

```html
<div class="tabs">
  <div class="tab active" onclick="show('overview')">전체 개요</div>
  <div class="tab" onclick="show('month1')">N월 — 테마명</div>
  <div class="tab" onclick="show('month2')">N월 — 테마명</div>
  <div class="tab" onclick="show('channel')">채널별 전략</div>
  <div class="tab" onclick="show('kpi')">KPI</div>
</div>
```

스타일:
```css
.tab {
  padding: 7px 16px;
  border-radius: 20px;
  border: 0.5px solid var(--color-border-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all .15s;
}
.tab.active {
  background: #1D9E75;
  border-color: #1D9E75;
  color: #fff;
  font-weight: 500;
}
```

### 2. KPI 서머리 카드

```html
<div class="grid2">
  <div class="card card-accent" style="border-left-color: #1D9E75">
    <div class="kpi-label">라벨</div>
    <div class="kpi-num">수치 또는 텍스트</div>
    <div class="kpi-label">부가 설명</div>
  </div>
</div>
```

### 3. 프로모션 카드

```html
<div class="promo-card">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
    <div class="promo-title">프로모션명</div>
    <span class="badge badge-green">기간</span>
  </div>
  <div class="promo-desc">프로모션 설명 텍스트</div>
  <div class="promo-meta">
    <span class="badge badge-amber">태그1</span>
    <span class="badge badge-coral">태그2</span>
  </div>
</div>
```

### 4. 주차 블록 (접기/펼치기)

```html
<div class="week-block">
  <div class="week-header" onclick="toggleWeek(this)">
    <div class="week-num" style="background:#색상;color:#색상">NW</div>
    <div class="week-theme">주차 테마 텍스트</div>
    <span class="arrow">▼</span>
  </div>
  <div class="week-body">
    <div class="action-row">
      <span class="ch-badge ch-store">스토어</span>
      <span class="action-text">실행 항목 텍스트</span>
    </div>
    <div class="action-row">
      <span class="ch-badge ch-naver">네이버</span>
      <span class="action-text">실행 항목 텍스트</span>
    </div>
    <!-- 채널별 반복 -->
  </div>
</div>
```

### 5. 채널 전략 카드

```html
<div class="card">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">
    <span class="ch-badge ch-insta" style="font-size:13px;padding:5px 12px">인스타그램</span>
    <span style="font-size:12px;color:var(--color-text-tertiary)">감성 + 바이럴</span>
  </div>
  <div style="font-size:13px;color:var(--color-text-secondary);line-height:1.8">
    • 릴스 주 2회 (정보형 숏폼)<br>
    • 피드 주 3회 (라이프스타일)<br>
    • UGC 리포스트 수시
  </div>
</div>
```

---

## JavaScript 필수 함수

### 탭 전환
```javascript
function show(id) {
  document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  event.target.classList.add('active');
}
```

### 주차 접기/펼치기
```javascript
function toggleWeek(el) {
  const body = el.nextElementSibling;
  const arrow = el.querySelector('.arrow');
  if (body.style.display === 'none') {
    body.style.display = 'block';
    arrow.textContent = '▼';
  } else {
    body.style.display = 'none';
    arrow.textContent = '▶';
  }
}
```

---

## 콘텐츠 작성 톤

- **프로모션명**: 짧고 임팩트 있게 (예: "봄맞이 소재 교체 세일", "#썬데이허그꿀잠 UGC 캠페인")
- **설명**: 2~3문장으로 핵심만 (목적 + 방법 + 기대효과)
- **액션 항목**: 한 줄로 구체적 실행 내용 (채널 + 콘텐츠 유형 + 주제/카피)
- **KPI**: 수치 목표 명시 (매출 +N%, 리뷰 N건, 유입 +N%)

---

## 체크리스트 — HTML 생성 전 확인

```
□ 모든 월에 테마/프로모션/주차 액션이 있는가?
□ 6개 채널 모두 커버되었는가?
□ KPI가 구체적 숫자로 명시되었는가?
□ 탭 전환이 정상 작동하는가?
□ 주차 접기/펼치기가 작동하는가?
□ 모바일에서도 깨지지 않는 반응형인가?
□ 브랜드 컬러가 일관되게 적용되었는가?
□ 채널 뱃지 컬러가 정확한가?
```
