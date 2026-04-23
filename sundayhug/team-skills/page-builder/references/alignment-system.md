# 정렬 시스템 레퍼런스

상세페이지에서 사용하는 정렬 클래스와 패턴입니다.

---

## 1. 텍스트 정렬 클래스

| 클래스 | 정렬 | 패딩 |
|--------|------|------|
| `.txtleft` | 왼쪽 | padding-left: 15px |
| `.txtcenter` | 가운데 | 없음 |
| `.txtright` | 오른쪽 | padding-right: 15px |

### 사용 예시
```html
<div class="title font-w700 txtleft">왼쪽 정렬 제목</div>
<div class="title font-w700 txtcenter">가운데 정렬 제목</div>
<div class="title font-w700 txtright">오른쪽 정렬 제목</div>
```

---

## 2. 섹션 헤더 정렬

### 기본 (가운데 정렬)
```html
<div class="detail_section">
    <div class="sub_title font-w600 txtcenter color_dark_brown">서브 타이틀</div>
    <div class="feature_title font-w600 txtcenter">메인 타이틀</div>
    <div class="desc_small font-w500 txtcenter">설명 텍스트</div>
</div>
```

### 왼쪽 정렬
```html
<div class="detail_section">
    <div class="sub_title font-w700 txtleft">
        <span class="desc_btn" style="background: #000000;">TAG</span>
    </div>
    <div class="title font-w700 txtleft" style="font-size: 26px; margin: 15px 0;">
        왼쪽 정렬 제목
    </div>
    <div class="desc_small txtleft" style="line-height: 1.9;">
        왼쪽 정렬 설명 텍스트
    </div>
</div>
```

---

## 3. Flex 컨테이너 정렬

### 수평 정렬 (justify-content)
```css
justify-content: flex-start;   /* 왼쪽 */
justify-content: center;       /* 가운데 */
justify-content: flex-end;     /* 오른쪽 */
justify-content: space-between;/* 균등 배치 */
justify-content: space-around; /* 균등 간격 */
```

### 수직 정렬 (align-items)
```css
align-items: flex-start;  /* 상단 */
align-items: center;      /* 중앙 */
align-items: flex-end;    /* 하단 */
```

### 인라인 패턴
```html
<!-- 가운데 정렬 flex 컨테이너 -->
<div style="display: flex; justify-content: center; align-items: center; gap: 15px;">
    <div>아이템 1</div>
    <div>아이템 2</div>
</div>

<!-- 균등 배치 -->
<div style="display: flex; justify-content: space-between; align-items: center;">
    <div>왼쪽</div>
    <div>오른쪽</div>
</div>
```

---

## 4. 이미지 컨테이너 위치 클래스

이미지 위에 텍스트를 오버레이할 때 사용합니다.

| 클래스 | 위치 |
|--------|------|
| `.top-left` | 좌상단 |
| `.top-center` | 상단 중앙 |
| `.top-right` | 우상단 |
| `.middle-left` | 좌측 중앙 |
| `.center` | 정중앙 |
| `.middle-right` | 우측 중앙 |
| `.bottom-left` | 좌하단 |
| `.bottom-center` | 하단 중앙 |
| `.bottom-right` | 우하단 |

### 사용 예시
```html
<div class="image-container">
    <img src="IMAGE_URL" alt="이미지">
    <div class="title bottom-left">좌하단 텍스트</div>
</div>
```

---

## 5. 섹션별 정렬 가이드

### 가운데 정렬 권장 섹션
- **인트로 섹션**: 브랜드/제품 첫인상, 감성적 호소
- **POINT 섹션**: 핵심 특징 강조
- **브랜드 비전**: 브랜드 철학 전달
- **최종 확신 카피**: 구매 유도 마무리
- **CTA 배너**: 클릭 유도 버튼

### 왼쪽 정렬 권장 섹션
- **ABC 스타일 섹션**: A, B, C 포인트 나열
- **FAQ 섹션**: 질문-답변 형식
- **사이즈 가이드**: 정보 전달 중심
- **구성품/상품정보**: 상세 스펙

### 혼합 정렬 권장 섹션
- **고민/말풍선 섹션**: 좌우 번갈아 배치
- **비교 섹션**: 좌우 대비 레이아웃
- **전문가 프로필**: 이미지 + 텍스트 조합

---

## 6. 정렬 조합 패턴

### 패턴 A: 중앙 집중형 (감성/브랜딩)
```
인트로: 가운데
POINT 01~03: 가운데
브랜드 비전: 가운데
```
- **특징**: 일관된 중앙 정렬로 고급스럽고 정제된 느낌
- **적합**: 프리미엄 제품, 감성 마케팅

### 패턴 B: 왼쪽 기조형 (정보 전달)
```
인트로: 가운데
ABC 섹션: 왼쪽
FAQ: 왼쪽
사이즈: 왼쪽
```
- **특징**: 가독성 중심, 정보 전달에 최적화
- **적합**: 기능성 제품, 상세 스펙 중요한 제품

### 패턴 C: 혼합형 (스토리텔링)
```
인트로: 가운데
고민 섹션: 좌우 번갈아
POINT 01: 가운데
POINT 02: 왼쪽 + 이미지 오른쪽
POINT 03: 가운데
브랜드 비전: 가운데
```
- **특징**: 시각적 리듬감, 지루함 방지
- **적합**: 스토리 중심 상세페이지

---

## 7. 인라인 정렬 조정

### 텍스트 정렬 (text-align)
```html
<div style="text-align: left;">왼쪽</div>
<div style="text-align: center;">가운데</div>
<div style="text-align: right;">오른쪽</div>
```

### 마진으로 정렬
```html
<!-- 왼쪽 정렬 -->
<div style="margin-right: auto;">왼쪽 배치</div>

<!-- 가운데 정렬 -->
<div style="margin: 0 auto;">가운데 배치</div>

<!-- 오른쪽 정렬 -->
<div style="margin-left: auto;">오른쪽 배치</div>
```

### 절대 위치 정렬
```html
<!-- 이미지 위 좌하단 텍스트 -->
<div style="position: absolute; bottom: 20px; left: 20px;">
    좌하단 텍스트
</div>

<!-- 이미지 위 우하단 텍스트 -->
<div style="position: absolute; bottom: 20px; right: 20px;">
    우하단 텍스트
</div>

<!-- 이미지 위 하단 중앙 텍스트 -->
<div style="position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);">
    하단 중앙 텍스트
</div>
```

---

## 8. 정렬 변경 시 체크리스트

- [ ] 같은 섹션 내 요소들의 정렬 일관성 확인
- [ ] 모바일에서 가독성 확인 (왼쪽 정렬 권장)
- [ ] 이미지와 텍스트 간 시각적 균형 확인
- [ ] 전체 페이지 흐름에서 자연스러운지 확인
