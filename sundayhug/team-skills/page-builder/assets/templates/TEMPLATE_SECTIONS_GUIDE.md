# 상세페이지 섹션별 템플릿 가이드

> **브랜드:** 썬데이허그 (SUNDAYHUG)
> **버전:** v4
> **용도:** 유아용품 상세페이지 제작 시 섹션별 템플릿 참고용

---

## 목차

1. [공통 스타일 변수](#1-공통-스타일-변수)
2. [Hero 섹션](#2-hero-섹션)
3. [Review 섹션](#3-review-섹션)
4. [When (사용시기) 섹션](#4-when-사용시기-섹션)
5. [Brand Story 섹션](#5-brand-story-섹션)
6. [Material Guide 섹션](#6-material-guide-섹션)
7. [Check Point 섹션](#7-check-point-섹션)
8. [Development Story 섹션](#8-development-story-섹션)
9. [Color Option 섹션](#9-color-option-섹션)
10. [Size Design 섹션](#10-size-design-섹션)
11. [How to Wear 섹션](#11-how-to-wear-섹션)
12. [Size Guide 섹션](#12-size-guide-섹션)
13. [Product Info 섹션](#13-product-info-섹션)
14. [Care Guide 섹션](#14-care-guide-섹션)
15. [Footer CTA 섹션](#15-footer-cta-섹션)

---

## 1. 공통 스타일 변수

### 컬러 팔레트
```css
:root {
    --cream: #FAF8F5;           /* 배경용 크림색 */
    --warm-white: #FFFFFF;       /* 기본 흰색 */
    --sand: #E8E2DA;             /* 모래색 */
    --gold: #C9A227;             /* 포인트 골드 */
    --gold-light: #E8D5A3;       /* 연한 골드 */
    --deep-navy: #1C2632;        /* 다크 배경 (밤하늘) */
    --charcoal: #2D2D2D;         /* 차콜 */
    --text-primary: #1A1A1A;     /* 본문 기본 */
    --text-secondary: #4A4A4A;   /* 본문 보조 */
    --text-muted: #888888;       /* 흐린 텍스트 */
    --border: #E5E5E5;           /* 테두리 */
    --coral: #D4907E;            /* 코랄 (여름용) */
    --soft-green: #7A9E7E;       /* 연두색 */
}
```

### 폰트
```css
font-family: 'Noto Sans KR', -apple-system, sans-serif;  /* 본문 */
font-family: 'Gowun Batang', 'Playfair Display', serif;  /* 제목 (세리프) */
font-family: 'Playfair Display', serif;                   /* 영문 포인트 */
font-family: 'Caveat', cursive;                           /* 필기체 */
```

### 공통 섹션 헤더
```html
<p class="section-label">SECTION LABEL</p>
<h2 class="section-title">섹션 제목</h2>
<p class="section-desc">섹션 설명 텍스트</p>
```

---

## 2. Hero 섹션

### 용도
- 상세페이지 최상단 메인 비주얼
- 브랜드 로고, 제품명, 핵심 포인트 3개 노출

### 특징
- 배경 이미지 사용 가능 (`background-image`)
- 글래스모피즘 카드 디자인
- 아이콘 + 텍스트 포인트 카드

### HTML 템플릿
```html
<section class="hero-section">
    <!-- 브랜드 로고 -->
    <div class="hero-logo">
        <div class="logo-placeholder">
            <span>BRAND_NAME</span>
        </div>
    </div>

    <!-- 서브 카피 -->
    <p class="sub-copy">
        서브 카피 라인 1<br>
        서브 카피 라인 2
    </p>

    <!-- 메인 카피 (제품명) -->
    <h2 class="main-copy">제품 메인 타이틀</h2>

    <!-- 포인트 카드 영역 -->
    <div class="hero-points-wrapper">
        <div class="hero-points-box">
            <p class="hero-points-title">Different Point</p>
            <div class="hero-points">
                <div class="hero-point">
                    <span class="point-icon">
                        <img src="icon1.png" alt="아이콘1">
                    </span>
                    <div class="point-text">
                        <p class="num">✦ point 1</p>
                        <p>포인트 설명<br>두 줄로</p>
                    </div>
                </div>
                <!-- point 2, 3 반복 -->
            </div>
        </div>
    </div>
</section>
```

### 커스터마이징 포인트
| 항목 | 위치 | 설명 |
|------|------|------|
| 배경 이미지 | `.hero-section` | `background-image: url('파일명.png')` |
| 배경 색상 | `.hero-section` | `background-color: #색상코드` |
| 포인트 개수 | `.hero-points` | 2~4개 조절 가능 |
| 아이콘 | `.point-icon img` | 60x60px 권장 |

---

## 3. Review 섹션

### 용도
- 고객 리뷰/후기 하이라이트
- 신뢰도 및 구매 전환율 향상

### 특징
- 세로형 카드 레이아웃 (원형 이미지 + 상세 후기)
- 별점 + 한줄 요약 + 상세 후기
- 하이라이트 텍스트 강조

### HTML 템플릿
```html
<section class="review-highlight">
    <p class="section-label">Real Review</p>
    <h2 class="section-title">고객님들의 <span class="highlight-text">핵심키워드</span> 후기</h2>
    <p class="section-desc">설명 텍스트</p>

    <div class="review-cards">
        <div class="review-card">
            <div class="review-image">리뷰 이미지</div>
            <div class="review-card-content">
                <p class="stars">★★★★★</p>
                <p>"<span class="review-highlight-bg">강조 키워드</span> 한줄 요약!"</p>
                <p class="reviewer">김** · 6개월 아기</p>
                <p class="review-detail">상세 후기 내용...</p>
            </div>
        </div>
        <!-- 카드 반복 (권장 3개) -->
    </div>
</section>
```

### 커스터마이징 포인트
| 항목 | 클래스 | 설명 |
|------|--------|------|
| 강조 텍스트 | `.review-highlight-bg` | 노란색 하이라이트 효과 |
| 리뷰 이미지 | `.review-image` | 120x120px 원형 |
| 카드 개수 | `.review-cards` | 2~4개 권장 |

---

## 4. When (사용시기) 섹션

### 용도
- 제품 사용 시기/단계 가이드
- 성장 단계별 제품 추천

### 특징
- 가이드북 스타일 디자인 (노트 바인딩 효과)
- STEP 단계별 레이아웃
- 추천 제품 하이라이트 (`.featured`)
- 메모지 스타일 주의사항

### HTML 템플릿
```html
<section class="when-section">
    <p class="section-label">Sleep Solution Guide</p>
    <h2 class="section-title">제품명, 이럴 때 추천해요!</h2>
    <p class="section-desc">설명 텍스트</p>

    <!-- 가이드북 -->
    <div class="guidebook">
        <div class="guidebook-header">
            <h3>GUIDE TITLE</h3>
            <p>가이드 부제목</p>
        </div>

        <!-- STEP 1 -->
        <div class="guide-page">
            <div class="guide-left">
                <p class="guide-step">STEP 1</p>
                <div class="guide-image">제품 이미지</div>
            </div>
            <div class="guide-content">
                <div class="guide-title-row">
                    <h4 class="guide-title">제품명</h4>
                    <p class="guide-desc">한줄 설명 뱃지</p>
                </div>
                <p class="guide-detail">상세 설명...</p>
                <p class="guide-tags">#해시태그1 #해시태그2</p>
            </div>
        </div>

        <!-- STEP 2 (추천 제품) -->
        <div class="guide-page featured">
            <!-- featured 클래스: 골드 테두리 + 추천 뱃지 -->
        </div>

        <!-- STEP 3 -->
        <div class="guide-page">...</div>
    </div>

    <!-- 메모 주의사항 -->
    <div class="memo-notice">
        <div class="memo-tape memo-tape-left"></div>
        <div class="memo-content">
            <h5>⚠ 주의사항 제목</h5>
            <p>주의사항 내용<br><span class="red-pencil-underline">밑줄 강조</span></p>
            <p class="footnote">*각주 설명</p>
        </div>
    </div>
</section>
```

### 커스터마이징 포인트
| 항목 | 클래스 | 설명 |
|------|--------|------|
| 추천 강조 | `.guide-page.featured` | 골드 테두리 + 추천 뱃지 |
| 뱃지 텍스트 | `.guide-page.featured::after` | CSS에서 `content:` 수정 |
| 밑줄 강조 | `.red-pencil-underline` | 빨간 밑줄 효과 |

---

## 5. Brand Story 섹션

### 용도
- 브랜드 소개 및 철학
- 감성적 스토리텔링

### 특징
- 밤하늘 테마 (딥네이비 배경)
- 별/달 장식 요소
- 세리프 폰트 사용

### HTML 템플릿
```html
<section class="brand-story">
    <!-- 별 장식 (20개) -->
    <span class="star-dot dot-1"></span>
    <!-- ... dot-2 ~ dot-20 -->

    <p class="section-label">Brand Story</p>
    <h2 class="section-title">브랜드 슬로건</h2>
    <p>
        <span class="brand-intro">브랜드 한줄 소개</span><br><br>
        브랜드 스토리 본문...
    </p>
    <p class="brand-ending">마무리 문구</p>
</section>
```

### 커스터마이징 포인트
| 항목 | 설명 |
|------|------|
| 별 개수 | `dot-1` ~ `dot-20` (CSS에서 위치 조정) |
| 배경색 | `--deep-navy` (#1C2632) |
| 엔딩 강조 | `.brand-ending` (골드 컬러) |

---

## 6. Material Guide 섹션

### 용도
- 소재/원단 비교 가이드
- 시즌별/용도별 제품 선택 도움

### 특징
- 소재 비교 테이블
- 빈티지 노트북 스타일
- 원단 칩 이미지 영역

### HTML 템플릿
```html
<section class="material-guide">
    <p class="section-label">Material Guide</p>
    <h2 class="section-title">소재별 쇼핑 가이드</h2>

    <!-- 소재 비교 테이블 -->
    <div class="material-compare-new">
        <table class="material-table">
            <thead>
                <tr>
                    <th class="category-col"></th>
                    <th>특징</th>
                    <th>소재구성</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="category-label">소재명<br><span class="season-tag gold">사계절</span></td>
                    <td>특징 설명</td>
                    <td>소재 구성</td>
                </tr>
                <!-- 행 반복 -->
            </tbody>
        </table>
    </div>

    <a href="#" class="material-link-btn">다른 소재 보러가기 →</a>

    <!-- 노트북 스타일 상세 -->
    <div class="vintage-notebook">
        <div class="notebook-page">
            <div class="paper-holes">
                <div class="paper-hole"></div>
                <!-- 8개 반복 -->
            </div>
            <div class="notebook-header">
                <span class="notebook-date">Material Note</span>
                <h3 class="notebook-title">소재명</h3>
            </div>
            <div class="fabric-swatch-area">
                <div class="fabric-swatch">
                    <div class="swatch-image">원단 칩</div>
                    <div class="swatch-pin"></div>
                </div>
                <div class="swatch-memo">
                    <p class="memo-text">"소재 설명"</p>
                </div>
            </div>
            <div class="notebook-content">
                <div class="note-item">
                    <span class="note-bullet">✦</span>
                    <div class="note-text">
                        <strong>특징 제목</strong>
                        <p>특징 설명 <span class="red-underline">강조</span></p>
                    </div>
                </div>
                <!-- 항목 반복 -->
            </div>
        </div>
    </div>
</section>
```

### 시즌 태그 종류
```html
<span class="season-tag gold">사계절</span>   <!-- 골드 -->
<span class="season-tag coral">여름용</span>   <!-- 코랄 -->
<span class="season-tag blue">겨울용</span>    <!-- 블루 -->
```

---

## 7. Check Point 섹션

### 용도
- 제품 특장점/기능 상세 소개
- 핵심 셀링 포인트 강조

### 특징
- 밤하늘 테마 배경
- 반달 형태 헤더
- 4개 그룹화된 포인트 레이아웃

### 구조 개요
```
Check Point 섹션
├── checkpoint-header (반달 배경 + 제목)
├── checkpoint-body
│   ├── POINT 01: detail-section (이미지 3개 교차 레이아웃)
│   ├── POINT 02: checkpoint-centered (중앙 배치)
│   ├── POINT 03: checkpoint-point3 (세로+가로 이미지)
│   └── POINT 04: checkpoint-point4 (가로 이미지 3개)
```

### HTML 템플릿 - 헤더
```html
<section class="checkpoint-section">
    <div class="checkpoint-header">
        <div class="checkpoint-moon-wrapper">
            <div class="checkpoint-moon">
                <!-- 별 장식 -->
                <div class="night-sky-stars">
                    <span class="star star-1">✦</span>
                    <!-- ... -->
                </div>
                <p class="moon-section-label">Check Point</p>
                <h2 class="moon-section-title">제품 포인트 제목</h2>
                <p class="moon-section-desc">설명 텍스트</p>
            </div>
        </div>
    </div>
```

### POINT 01 템플릿 (이미지 3개 교차)
```html
<div class="detail-section">
    <p class="checkpoint-num">✦ POINT 01</p>
    <h3 class="section-title">포인트 제목</h3>

    <!-- 아이템 (좌 이미지 - 우 텍스트) -->
    <div class="detail-item">
        <div class="detail-image">
            <div class="detail-image-placeholder">이미지</div>
        </div>
        <div class="detail-content">
            <p class="detail-num">01</p>
            <h4>소제목</h4>
            <p>설명...</p>
        </div>
    </div>

    <!-- 아이템 (우 이미지 - 좌 텍스트) -->
    <div class="detail-item reverse">...</div>
</div>
```

### POINT 02 템플릿 (중앙 배치)
```html
<div class="checkpoint-centered">
    <p class="checkpoint-num">✦ POINT 02</p>
    <h3>포인트 제목</h3>
    <div class="centered-image">이미지</div>
    <div class="centered-details">
        <div class="centered-detail-item">
            <h4>소제목 1</h4>
            <p>설명...</p>
        </div>
        <div class="centered-detail-item">
            <h4>소제목 2</h4>
            <p>설명...</p>
        </div>
    </div>
</div>
```

### POINT 03 템플릿 (세로+가로 이미지)
```html
<div class="checkpoint-point3">
    <p class="checkpoint-num">✦ POINT 03</p>
    <h3>포인트 제목</h3>
    <div class="main-vertical-image">메인 이미지</div>
    <div class="small-images-row">
        <div class="small-horizontal-image">이미지 1</div>
        <div class="small-horizontal-image">이미지 2</div>
    </div>
    <div class="point3-details">
        <div class="point3-detail-item">
            <h4>소제목</h4>
            <p>설명...</p>
        </div>
        <!-- 반복 -->
    </div>
</div>
```

### POINT 04 템플릿 (가로 이미지 3개)
```html
<div class="checkpoint-point4">
    <div class="point4-header">
        <p class="checkpoint-num">✦ POINT 04</p>
        <h3>포인트 제목</h3>
    </div>
    <div class="point4-item">
        <div class="point4-image">이미지</div>
        <div class="point4-content">
            <h4>소제목</h4>
            <p>설명...</p>
        </div>
    </div>
    <!-- 아이템 반복 -->
</div>
```

---

## 8. Development Story 섹션

### 용도
- 제품 개발 스토리
- 전문가 협업/인증 강조

### HTML 템플릿
```html
<section class="dev-story">
    <p class="section-label">Development Story</p>
    <h2 class="section-title">전문가와 함께 개발했습니다</h2>

    <div class="dev-content">
        <p class="dev-quote">인용구/핵심 메시지</p>

        <div class="dev-profile">
            <div class="photo">프로필 사진</div>
            <div class="dev-profile-info">
                <h4>직함 <span class="award-icon">★</span>수상내역</h4>
                <p>이름/소속</p>
            </div>
        </div>

        <div class="dev-text">
            <p>개발 스토리 본문...</p>
        </div>
    </div>
</section>
```

---

## 9. Color Option 섹션

### 용도
- 컬러 옵션 소개
- 시각적 컬러 팔레트

### HTML 템플릿
```html
<section class="color-section">
    <p class="section-label">Color Option</p>
    <h2 class="section-title">컬러 옵션 제목</h2>
    <p class="section-desc">설명...</p>

    <div class="color-grid">
        <div class="color-item">
            <div class="color-swatch" style="background: #F5F0E8;"></div>
            <p>컬러명</p>
        </div>
        <!-- 컬러 반복 -->
    </div>

    <div class="img-placeholder large">컬러별 제품 이미지</div>
</section>
```

---

## 10. Size Design 섹션

### 용도
- 사이즈별 디자인 차이점
- 성장 단계별 사이즈 추천

### HTML 템플릿
```html
<section class="size-section">
    <p class="section-label">Size Design</p>
    <h2 class="section-title">사이즈별 맞춤 디자인</h2>
    <p class="section-desc">설명...</p>

    <div class="size-compare">
        <div class="size-card">
            <div class="size-card-header">
                <h4>STEP 1</h4>
                <p>S size (~8M)</p>
            </div>
            <div class="size-card-image">도식화 이미지</div>
            <div class="size-features">
                <span class="size-feature">기능태그1</span>
                <span class="size-feature">기능태그2</span>
            </div>
        </div>
        <!-- 사이즈 카드 반복 -->
    </div>
</section>
```

---

## 11. How to Wear 섹션

### 용도
- 착용/사용 방법 안내
- 단계별 가이드

### HTML 템플릿
```html
<section class="howto-section">
    <p class="section-label">How to Wear</p>
    <h2 class="section-title">손쉬운 착용방법</h2>

    <div class="howto-steps">
        <div class="howto-step">
            <div class="step-image">STEP 1 이미지</div>
            <p class="step-num">STEP 1</p>
            <p>설명...</p>
        </div>
        <!-- STEP 반복 -->
    </div>

    <p style="text-align: center; color: var(--text-muted);">
        ※ 추가 안내사항
    </p>
</section>
```

---

## 12. Size Guide 섹션

### 용도
- 사이즈 상세 정보 테이블
- 사이즈 선택 가이드

### HTML 템플릿
```html
<section class="size-guide-section">
    <p class="section-label">Size Info</p>
    <h2 class="section-title">사이즈 선택하기</h2>
    <p class="section-desc">설명...</p>

    <table class="size-table">
        <thead>
            <tr>
                <th>사이즈</th>
                <th>권장 월령</th>
                <th>권장 키</th>
                <th>총 길이</th>
                <th>가슴 둘레</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>S</strong></td>
                <td>3~9개월</td>
                <td>60~70cm</td>
                <td>64cm</td>
                <td>38cm</td>
            </tr>
            <!-- 행 반복 -->
        </tbody>
    </table>
</section>
```

---

## 13. Product Info 섹션

### 용도
- 제품 상세 정보 (법적 필수 표기)
- 스펙 정보

### HTML 템플릿
```html
<section class="info-section">
    <p class="section-label">Product Info</p>
    <h2 class="section-title">상품 정보</h2>

    <table class="info-table">
        <tr>
            <th>제품명</th>
            <td>제품 이름</td>
        </tr>
        <tr>
            <th>소재</th>
            <td>소재 구성</td>
        </tr>
        <tr>
            <th>컬러</th>
            <td>컬러 목록</td>
        </tr>
        <tr>
            <th>사이즈</th>
            <td>사이즈 정보</td>
        </tr>
        <tr>
            <th>제조국</th>
            <td>대한민국</td>
        </tr>
        <tr>
            <th>KC 인증</th>
            <td>인증 정보</td>
        </tr>
        <tr>
            <th>제조사</th>
            <td>제조사명</td>
        </tr>
    </table>
</section>
```

---

## 14. Care Guide 섹션

### 용도
- 세탁/관리 방법 안내
- 아이콘 기반 가이드

### HTML 템플릿
```html
<section class="care-section">
    <p class="section-label">Care Guide</p>
    <h2 class="section-title">세탁 및 관리 방법</h2>

    <div class="care-grid">
        <div class="care-item">
            <div class="care-icon">
                <svg><!-- 아이콘 SVG --></svg>
            </div>
            <p>30°C 이하<br>미온수 세탁</p>
        </div>
        <!-- 아이콘 반복 (4개 권장) -->
    </div>
</section>
```

### 기본 아이콘 종류
- 온도계 (세탁 온도)
- 세탁망 (세탁 방법)
- 태양/그늘 (건조 방법)
- 금지 (표백제 금지)

---

## 15. Footer CTA 섹션

### 용도
- 다른 제품 연결
- 교차 판매 유도

### HTML 템플릿
```html
<section class="footer-cta">
    <!-- 밤하늘 장식 -->
    <div class="footer-dots">
        <span class="footer-dot fd-1"></span>
        <!-- fd-1 ~ fd-16 -->
    </div>

    <h2>다른 제품 보러가기</h2>
    <p>브랜드의 다양한 제품을 만나보세요</p>

    <div class="other-products">
        <a href="URL" class="product-link">
            <div class="product-thumb">제품 이미지</div>
            <p>제품명</p>
        </a>
        <!-- 제품 반복 (2~4개) -->
    </div>
</section>

<footer>
    <div class="footer-inner">
        <p class="footer-logo">BRAND_NAME</p>
        <p class="footer-tagline">브랜드 태그라인</p>
        <p class="footer-copy">© 2025 BRAND. All rights reserved.</p>
    </div>
</footer>
```

---

## 섹션 조합 가이드

### 필수 섹션
1. Hero
2. Product Info
3. Footer

### 권장 순서
```
1. Hero (메인 비주얼)
2. Review (신뢰 구축)
3. When (사용 시기 가이드)
4. Brand Story (브랜드 소개)
5. Material (소재 설명)
6. Check Point (특장점)
7. Development (개발 스토리)
8. Color (컬러 옵션)
9. Size (사이즈)
10. How to (사용법)
11. Size Guide (사이즈표)
12. Product Info (제품 정보)
13. Care (세탁 관리)
14. Footer CTA (교차 판매)
```

### 제품 유형별 추천 조합

#### 의류/패션 제품
Hero → Review → Material → Check Point → Color → Size → How to → Size Guide → Care → Product Info → Footer

#### 기능성 제품
Hero → Review → When → Check Point → Development → Material → Size → Product Info → Care → Footer

#### 단순 제품
Hero → Review → Check Point → Color → Size Guide → Product Info → Care → Footer

---

## 파일 구조

```
/template/
├── template_guide_v1.html      # 전체 템플릿 (v4 기준)
├── TEMPLATE_SECTIONS_GUIDE.md  # 이 가이드 문서
└── assets/                     # 이미지 폴더
    ├── hero_baby.png
    ├── checkpoint_baby.png
    └── ...
```

---

## 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| v4 | 2025-02 | 사이드바 제거, Check Point 4그룹화, Hero 글래스모피즘 |
| v1 | 2025-01 | 초기 버전 |
