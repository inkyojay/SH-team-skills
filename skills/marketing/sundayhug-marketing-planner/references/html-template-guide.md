# HTML 출력 템플릿 디자인 가이드

마케팅 플랜 HTML 결과물은 반드시 아래 디자인 시스템을 따른다.

---

## 디자인 원칙

- **에디토리얼 매거진 스타일**: 깔끔하고 고급스러운 느낌. 보라색/원색 UI 금지.
- **Serif + Sans-serif 조합**: 제목은 세리프, 본문은 산세리프
- **크림/잉크 컬러 팔레트**: 따뜻하고 차분한 톤. 원색 강조는 최소한으로.
- **왼쪽 고정 네비게이션**: 탭 UI 대신 사이드바 + 스크롤 기반 섹션 이동
- **넘버링 섹션**: 01, 02, 03... 형태로 섹션 넘버 표시
- **상세한 전략 서술**: 각 섹션에 전략 의도와 실행 방법을 구체적으로 서술

---

## 필수 구조

```
<body>
  <nav class="nav">        <!-- 왼쪽 고정 사이드바 (220px) -->
  <main class="main">      <!-- 오른쪽 메인 콘텐츠 -->
    <div class="hero">      <!-- 히어로 배너 (잉크 배경) -->
    <section id="usp">      <!-- 01 USP -->
    <section id="target">   <!-- 02 타겟 시나리오 -->
    <section id="keywords">  <!-- 03 키워드 -->
    <section id="content-strategy">  <!-- 04 콘텐츠 전략 -->
    <section id="channels">  <!-- 05 채널 플랜 -->
    <section id="mamcafe">   <!-- 06 맘카페 바이럴 -->
    <section id="distribution"> <!-- 07 배포형 블로그 -->
    <section id="comparison"> <!-- 08 비교 콘텐츠 -->
    <section id="action">    <!-- 09 액션플랜 -->
    <section id="kpi">       <!-- 10 KPI -->
  </main>
</body>
```

---

## 컬러 시스템

```css
:root {
  /* 기본 */
  --cream: #F7F4EF;           /* 배경 */
  --warm-white: #FDFBF8;      /* 카드 배경 */
  --ink: #1A1714;              /* 텍스트, 네비게이션 배경 */
  --ink-60: rgba(26,23,20,0.6); /* 보조 텍스트 */
  --ink-30: rgba(26,23,20,0.3);
  --ink-10: rgba(26,23,20,0.07);
  --border: rgba(26,23,20,0.1);

  /* 강조색 */
  --accent: #C4571A;           /* 주 강조색 (번트 오렌지) */
  --accent-light: #F5E8DF;
  --teal: #1B7A6E;             /* 보조 1 */
  --teal-light: #E0F2EF;
  --blue: #1B4E8F;             /* 보조 2 */
  --blue-light: #E5EDF8;
  --amber: #9A6200;            /* 보조 3 */
  --amber-light: #FBF0D8;
  --purple: #5A3FA0;           /* 보조 4 */
  --purple-light: #EDE9FA;
  --green: #2E6B30;            /* 보조 5 */
  --green-light: #E5F4E6;

  /* 폰트 */
  --serif: 'Noto Serif KR', serif;
  --sans: 'Noto Sans KR', sans-serif;
}
```

---

## 타이포그래피

| 요소 | 폰트 | 크기 | 무게 |
|------|------|------|------|
| 히어로 타이틀 | serif | 42px | 700 |
| 섹션 타이틀 | serif | 28px | 700 |
| 섹션 번호 | sans | 11px | 500, uppercase, letter-spacing 0.12em |
| 본문 설명 | sans | 13px | 400 |
| 카드 타이틀 | sans | 15px | 700 |
| 카드 설명 | sans | 12px | 400, color: ink-60 |
| 테이블 헤더 | sans | 9~10px | 700, uppercase, letter-spacing 0.1em |
| 테이블 셀 | sans | 12px | 400 |
| 태그/뱃지 | sans | 9px | 700, uppercase |
| 네비 항목 | sans | 12px | 400 |

---

## 핵심 컴포넌트

### 1. 왼쪽 네비게이션 (nav)
- 폭: 220px, 고정(fixed), 높이 100vh
- 배경: var(--ink), 텍스트: white
- 브랜드명 상단 + 섹션 그룹별 분류
- 각 항목에 컬러 dot (6px 원형) + 섹션명
- 하단 푸터: 브랜드 + 연도 정보
- active 상태: border-left 2px accent + 밝은 텍스트

### 2. 히어로 배너 (hero)
- 배경: var(--ink), 텍스트: white
- 상단 라벨: 10px uppercase, accent 색상
- 제목: serif 42px, 강조 단어에 accent 색상
- 설명: 14px, rgba(255,255,255,0.55)
- 하단 칩: 둥근 테두리 + 반투명 배경
- 장식: ::before, ::after로 큰 원형 보더

### 3. 섹션 헤더
```html
<div class="section-header">
  <span class="section-num">01</span>
  <h2 class="section-title">제목</h2>
</div>
<p class="section-sub">설명 텍스트</p>
```

### 4. USP 카드 그리드
- 3열 그리드
- warm-white 배경 + border 1px
- 상단 태그: 9px uppercase pill (각 USP마다 다른 색상)
- 제목: 15px bold
- 설명: 12px ink-60

### 5. 키워드 테이블
- 의도별 섹션 타이틀로 분류 (kw-section-title)
- 테이블 헤더: 9px uppercase, warm-white 배경
- 키워드 텍스트: kw-word 클래스 (bold, ink 색상)
- 의도 pill: p-buy(teal), p-info(blue), p-cmp(amber), p-prob(accent)
- 경쟁도 pill: p-h(purple), p-m(green), p-l(ink-10)
- hover 시 배경: cream

### 6. 콘텐츠 우선순위 블록 (priority-block)
- border-left: 3px solid [color]
- border-radius: 0 10px 10px 0
- warm-white 배경
- 구성: pb-label(9px) → pb-title(15px bold) → pb-kw(11px) → pb-desc(12px)
- 하단 tag-row: 관련 채널 태그들

### 7. 채널 카드 그리드
- 2열 그리드
- 카드 헤더: dot + 채널명 + 빈도 (ch-freq)
- 카드 바디: ch-row별 구분 (strong 제목 + 설명)
- 채널별 dot 색상: 네이버(green), 인스타(pink), 스레드(purple), 맘카페(amber)

### 8. 맘카페 전략
- 경고 박스 (warn-box): 노란 배경, 핵심 원칙 강조
- 4장 카드 그리드 (cafe-grid 2열)
- 카드 상단 border-top: 3px solid [각기 다른 색]
- 타겟 카페 목록: 그리드 형태 테이블

### 9. 배포형 블로그 전략
- 4가지 타입 카드 (dist-grid 2열)
- 예산 가이드: budget-row 3열 그리드 (budget-box)
- 각 박스: 큰 숫자(22px, accent) + 라벨(11px)

### 10. 비교 콘텐츠
- 비교표 (cmp-table): 우리 제품 셀에 .win 클래스 (teal bold)
- 6가지 비교 유형 서술

### 11. 액션플랜
- 월 탭: m-tab 버튼 (ink 배경 active)
- 월 배너: month-banner (ink 배경 + 테마 + 키워드 칩)
- 주차 블록: week-block 접기/펼치기
  - week-header: 주차명 + 부제 + 화살표
  - week-body: action-row (채널 뱃지 + 상세 액션)
  - 채널 뱃지: a-n(green), a-i(pink), a-t(purple), a-c(amber), a-p(blue)

### 12. KPI
- kpi-grid 4열
- kpi-box: 큰 숫자(26px, light weight) + 라벨(11px)
- 마일스톤: milestone-row (월 뱃지 + 기준 텍스트)
- 예산 테이블: 월별 항목 + 합계행

---

## 반응형 / 인쇄

```css
@media print {
  .nav { display: none; }
  .main { margin-left: 0; }
  .section { padding: 40px; page-break-inside: avoid; }
}
```

모바일 대응은 현재 필수 아님 (데스크톱 우선 문서).

---

## 인터랙션

### JavaScript 필수 기능
1. **네비게이션 active 상태**: 스크롤 위치에 따라 현재 섹션의 nav-item에 active 클래스
2. **월 탭 전환**: m-tab 클릭 시 해당 month-content 표시
3. **주차 접기/펼치기**: week-header 클릭 시 week-body 토글 + 화살표 회전

```javascript
// 네비게이션 스크롤 추적
const sections = document.querySelectorAll('section[id]');
const navItems = document.querySelectorAll('.nav-item');
window.addEventListener('scroll', () => {
  let current = '';
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 100) current = s.id;
  });
  navItems.forEach(a => {
    a.classList.remove('active');
    if (a.getAttribute('href') === '#' + current) a.classList.add('active');
  });
});

// 월 탭 전환
document.querySelectorAll('.m-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.m-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.month-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById(tab.dataset.month).classList.add('active');
  });
});

// 주차 접기/펼치기
document.querySelectorAll('.week-header').forEach(h => {
  h.addEventListener('click', () => h.parentElement.classList.toggle('open'));
});
```

---

## 콘텐츠 작성 원칙

1. **각 섹션에 section-sub 설명문 필수**: 해당 섹션이 왜 중요한지, 어떤 전략 의도인지 1~2줄로 서술
2. **priority-block에 전략 서술 필수**: 단순 키워드 나열이 아니라, 왜 이 키워드 묶음이 중요한지, 어떤 메시지를 반복할지 구체적으로
3. **채널 카드에 실행 가이드 포함**: "월 4회 발행" 같은 빈도 + 구체적 콘텐츠 형태 + 주의사항
4. **액션플랜 action-row에 키워드 인라인 태그**: kw-inline 클래스로 해당 주차 타겟 키워드 표시
5. **맘카페 warn-box 필수**: 브랜드 직접 참여 금지 원칙 강조
6. **비교 콘텐츠에 .win 클래스**: 비교표에서 썬데이허그 우위 항목 강조

---

## 파일 저장 위치

결과물은 항상 `~/Desktop/team-skills/` 디렉토리에 저장 (각 팀원 로컬 Desktop):
```
~/Desktop/team-skills/{제품명}-마케팅플랜.html
```
