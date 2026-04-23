---
name: page-builder
description: 상세페이지 제작
triggers:
  - "상세페이지 만들어줘"
  - "제품 페이지 작성"
  - "브랜드 스타일로"
  - "URL 분석해서 리뉴얼"
  - "경쟁사 페이지 참고해서"
---

# 상세페이지 빌더 (멀티 브랜드 지원)

## 🎯 스킬 목적

**브랜드별 컬러 시스템**을 기반으로 **제품 상세페이지**를 생성합니다.
- 브랜드별 CSS 컬러 변수 적용 (`assets/brands/` 폴더)
- 기존 CSS 클래스만 사용 (추가 CSS 작성 금지)
- 더미 이미지는 `https://dummyimage.com/` 사용
- 기승전결 스토리텔링 구조

---

## 🎨 브랜드 컬러 시스템

### 브랜드 CSS 파일 위치
```
assets/brands/
├── sundayhug-colors.css     # 썬데이허그 (기본) ✅ 생성됨
└── [브랜드명]-colors.css    # 커스텀 브랜드 (필요시 추가)
```

### 브랜드 지정 방법

**사용자 요청 예시:**
- "썬데이허그 스타일로 상세페이지 만들어줘" → `sundayhug-colors.css`
- "모던블루 브랜드로 작업해줘" → `modern-blue-colors.css`
- "mybrand로 상세페이지 만들어줘" → `mybrand-colors.css`

**브랜드 미지정 시:** 기본값 `sundayhug-colors.css` 사용

### 새 브랜드 추가 방법

1. `assets/brands/sundayhug-colors.css` 파일 복사
2. 브랜드명에 맞게 파일명 변경 (예: `mybrand-colors.css`)
3. CSS 변수 값을 브랜드 컬러로 수정
4. `assets/brands/` 폴더에 저장

### CSS 변수 구조
```css
:root {
    --brand-primary: #A38068;       /* 메인 브랜드 컬러 */
    --brand-primary-dark: #8b6b56;  /* 메인 컬러 어두운 버전 */
    --brand-secondary: #2d2420;     /* 보조 컬러 (다크) */
    --brand-accent: #ff8605;        /* 강조 컬러 */
    --brand-accent-dark: #ff6b35;   /* 강조 컬러 어두운 버전 */
    --bg-cream: #FFFBF5;            /* 배경 크림 */
    --bg-oat: #EAE2D5;              /* 배경 오트 */
    /* ... */
}
```

---

## 📋 워크플로우 (4단계)

### Step 1: 입력 수집 & 분석

**입력 유형:**
- URL 제공 → 크롤링 후 분석
- 제품 정보 직접 제공 → 바로 분석
- 경쟁사 URL 참고 → 구조 분석 후 개선안 제시

**분석 항목:**
```
□ 제품명, 카테고리
□ 주요 특징 (3~5개)
□ 타겟 고객 (신생아/영아/유아)
□ 컬러 옵션 유무
□ 가격 정보
□ 안전 인증
□ 사이즈 스펙
□ ⭐ 이미지 URL (가능한 모두 추출)
```

**⭐ 이미지 URL 처리 (우선순위):**

1. **사용자 제공 URL 사용**
   - 사용자가 제품 이미지 URL을 직접 제공한 경우 우선 사용

2. **크롤링으로 추출 시도**
   - 페이지 내 모든 제품 이미지 URL 추출
   - 이미지 URL 패턴:
     - `https://www.sundayhug.kr/web/product/big/...`
     - `https://www.sundayhug.kr/web/product/medium/...`
     - CDN 이미지 URL 등

3. **사용자에게 요청**
   - JS 렌더링 페이지라 추출 실패 시
   - "이미지 URL을 제공해주세요" 요청

4. **더미 이미지 (최후 수단)**
   - 위 방법 모두 불가 시에만 더미 이미지 사용
   - `https://dummyimage.com/{width}x{height}/{bg}/{text}`

### Step 2: 구조 제안 (사용자 확인 필수)

**반드시 사용자에게 확인받을 것:**
```markdown
## 📝 상세페이지 구조 제안

**제품:** [제품명]
**컨셉:** [한 줄 컨셉]

### 섹션 구성
1. 인트로 - [메인 카피]
2. 후킹 멘트 - [스토리 방향]
3. 포인트 01~03 - [각 특징]
4. [추가 섹션들...]
5. 사이즈 가이드
6. 브랜드 비전

이 구조로 진행할까요? 수정할 부분이 있으면 말씀해 주세요.
```

**⚠️ 사용자 승인 없이 코드 작성 금지**

### Step 3: HTML 코드 생성

**필수 준수사항:**
1. `references/css-classes.md` 클래스 우선 사용
2. `references/section-templates.md` 섹션 구조 따르기
3. `references/inline-patterns.md` 인라인 패턴 참조 (오버레이 카드, 말풍선 등)
4. 더미 이미지: `https://dummyimage.com/{width}x{height}/{bg색상}/{텍스트색상}`
5. **⭐ 인라인(Standalone) HTML로 출력** - CSS/JS 모두 포함된 완전한 HTML

**💡 인라인 스타일 가이드:**
- 오버레이 카드, 뱃지, 말풍선, 그리드 등 복잡한 UI → `inline-patterns.md` 패턴 사용
- 기본 레이아웃, 타이포그래피, 배경색 → CSS 클래스 사용
- 섹션 간격 조정(margin/padding) → 인라인 스타일 허용

**코드 구조 (인라인 방식):**
```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>제품명 - 썬데이허그</title>

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700&family=Noto+Serif+KR:wght@300;400;500;600;700&display=swap" rel="stylesheet">

    <!-- Swiper CSS (컬러스와이프 사용 시) -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.css">

    <style>
    /* assets/userCSS.css 내용 전체 포함 */
    </style>
</head>
<body>
    <!-- 섹션들... -->

    <!-- jQuery & Swiper JS -->
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/swiper@8/swiper-bundle.min.js"></script>
    <script>
    /* 필요한 JS 기능만 포함 */
    </script>
</body>
</html>
```

**⚠️ 주의:** 생성된 HTML 파일은 브라우저에서 바로 열어 미리보기 가능해야 함

### Step 4: 최종 출력

- HTML 파일로 저장
- 다운로드 링크 제공
- 이미지 교체 가이드 안내

---

## 📁 참조 파일

| 파일 | 용도 |
|------|------|
| `references/css-classes.md` | 사용 가능한 CSS 클래스 목록 |
| `references/section-templates.md` | 14종 섹션 HTML 템플릿 |
| `references/inline-patterns.md` | ⭐ 인라인 스타일 패턴 (오버레이 카드, 말풍선, 뱃지 등) |
| `references/alignment-system.md` | ⭐ 정렬 시스템 가이드 (텍스트 정렬, 위치 클래스, 섹션별 권장 정렬) |
| `design-system-guide.html` | ⭐ **비주얼 가이드** - 브라우저에서 모든 디자인 요소 미리보기 |
| `assets/userCSS.css` | 상세페이지 전용 CSS (인라인용) |
| `assets/userJS.js` | 인터랙션 JS (인라인용) |
| `assets/brands/sundayhug-colors.css` | 썬데이허그 브랜드 컬러 변수 |
| `agents/page-improver.md` | ⭐ **기존 페이지 개선 에이전트** - 리뉴얼/수정 작업용 |

---

## 🎨 브랜드 가이드

### 컬러 팔레트
| 이름 | HEX | 용도 |
|------|-----|------|
| 다크 브라운 | `#A38068` | 메인 포인트, 뱃지 |
| 데일리 크림 | `#FFFBF5` | 밝은 배경 |
| 오트 | `#EAE2D5` | 중간 배경 |
| 오렌지 | `#ff8605` | CTA, 강조 |
| 코랄 | `#eaccca` | 서브 배경 |
| 제이드 그린 | `#d7eae4` | 서브 배경 |

### 더미 이미지 규격
```
메인 비주얼: https://dummyimage.com/600x400/EAE2D5/A38068
정사각형:    https://dummyimage.com/600x600/FFFBF5/A38068
컬러칩:      https://dummyimage.com/100x100/FFB6C1/000000
프로필:      https://dummyimage.com/150x150/EAE2D5/A38068
```

---

## ✅ 체크리스트

### 코드 작성 전
- [ ] 제품 정보 충분히 파악
- [ ] 섹션 구조 사용자 승인 받음
- [ ] 컬러 옵션 유무 확인
- [ ] `design-system-guide.html` 참조하여 사용할 패턴 선정

### 코드 작성 중
- [ ] 레이아웃 선언 포함
- [ ] CSS 클래스 우선 사용 (`css-classes.md`)
- [ ] 복잡한 UI는 인라인 패턴 사용 (`inline-patterns.md`)
- [ ] 더미 이미지 URL 형식 준수
- [ ] 섹션 순서 논리적

### 코드 작성 후
- [ ] HTML 유효성 확인
- [ ] 닫는 태그 누락 없음
- [ ] 이미지 교체 가이드 제공

---

## 💡 섹션 선택 가이드

### 필수 섹션 (모든 제품)
1. 레이아웃 선언
2. 인트로
3. 후킹 멘트
4. 포인트 섹션 (최소 3개)
5. 사이즈 가이드
6. 브랜드 비전

### 제품 유형별 추가 섹션

**의류 (슬리핑백, 속싸개)**
- 컬러 라인업 + 컬러 스와이프
- 원단 정보 탭
- HOW TO (세탁법)

**침대/가구 (아기침대, 바운서)**
- 성장 단계 (Stage)
- 경고/안전 섹션
- 추가 구성상품

**프로모션 진행 시**
- 프로모션 섹션
- 사은품 섹션

**신뢰 강화 필요 시**
- 전문가 프로필
- FAQ

---

## 🚫 금지 사항

1. **새로운 CSS 클래스 작성 금지** - `css-classes.md`의 기존 클래스만 사용
2. **문서화되지 않은 인라인 스타일 금지** - `inline-patterns.md` 패턴만 사용
3. **외부 이미지 직접 링크 금지** - 더미 이미지 또는 제공된 URL 사용
4. **사용자 승인 없이 진행 금지** - Step 2 필수
5. **JS 수정 금지** - 기존 userJS.js 그대로 사용

## ✅ 허용 사항

1. **인라인 패턴 사용** - `inline-patterns.md`에 문서화된 패턴은 그대로 복사하여 사용
2. **섹션 간격 조정** - margin, padding 값 조정
3. **색상 값 변경** - 브랜드 컬러 CSS 변수 또는 hex 값으로 교체
4. **텍스트 크기 미세 조정** - font-size 값 조정

---

## 📝 사용 예시

### 신규 페이지 생성

**사용자:** "ABC 아기침대 상세페이지 만들어줘"

**Claude:**
1. 제품 정보 요청 (특징, 컬러, 가격 등)
2. 섹션 구조 제안 → 사용자 확인
3. HTML 코드 생성
4. 파일 제공 + 이미지 교체 안내

### 기존 페이지 개선 (page-improver 에이전트)

**사용자:** "이 상세페이지 개선해줘" / "리뉴얼해줘" / "디자인 수정해줘"

**Claude:** (`agents/page-improver.md` 워크플로우 참조)
1. 기존 페이지 분석 리포트 출력
2. 개선 방향 제안 → 사용자 확인 (정렬 시스템 선택 포함)
3. 디자인 시스템 참조하여 HTML 리빌딩
4. 완성된 파일 + 변경 사항 요약 제공

**⚠️ 기존 이미지 URL은 그대로 유지됩니다.**

---

## 🖼️ 비주얼 가이드 사용법

**`design-system-guide.html`** 파일을 브라우저에서 열면 모든 디자인 요소를 미리보기할 수 있습니다.

**포함된 내용:**
- 브랜드 컬러 팔레트
- 타이포그래피 (제목, 본문)
- 형광펜 하이라이트
- 뱃지 & 태그
- 버튼 스타일
- 이미지 오버레이 카드
- 고민/말풍선 섹션
- 알림/주의사항 박스
- 그리드 레이아웃
- FAQ 아이템
- 섹션 템플릿 예시

**활용 방법:**
1. 브라우저에서 `design-system-guide.html` 열기
2. 사이드바에서 원하는 카테고리 선택
3. 마음에 드는 패턴 확인
4. 해당 패턴의 코드를 `references/` 문서에서 복사하여 사용
