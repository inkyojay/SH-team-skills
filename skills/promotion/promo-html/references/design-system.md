# 썬데이허그 HTML 디자인 시스템

> 모든 프로모션 HTML 산출물에 적용되는 브랜드 디자인 시스템

## 폰트

```css
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
```

---

## 브랜드 컬러

### Primary
| 이름 | HEX | CSS 변수 | 용도 |
|------|-----|----------|------|
| 썬데이 베이지 | `#F5E6D3` | `--sunday-beige` | 주 배경, 강조 영역, 태그 |
| 허그 브라운 | `#8B7355` | `--hug-brown` | 헤드라인, 아이콘, CTA 버튼 |

### Secondary
| 이름 | HEX | CSS 변수 | 용도 |
|------|-----|----------|------|
| 크림 | `#FAFAF7` | `--cream` | 전체 배경, 카드 내부 |
| 소프트 그레이 | `#E8E4DE` | `--soft-gray` | 구분선, 비활성, footer |
| 웜 화이트 | `#FFFFFF` | `--warm-white` | 카드 배경, 텍스트 영역 |

### Text
| 이름 | HEX | CSS 변수 | 용도 |
|------|-----|----------|------|
| 딥 브라운 | `#8B7355` | `--text-deep` | 헤드라인, 강조 텍스트 |
| 다크 그레이 | `#333333` | `--text-dark` | 제목, 중요 본문 |
| 미디엄 그레이 | `#666666` | `--text-mid` | 일반 본문 |
| 라이트 그레이 | `#999999` | `--text-light` | 보조 텍스트, 캡션 |

### Accent (프로모션용)
| 이름 | HEX | CSS 변수 | 용도 |
|------|-----|----------|------|
| 세일 레드 | `#D4534A` | `--sale-red` | 할인 강조, SALE 태그 |
| 소프트 핑크 | `#F2D4C4` | `--soft-pink` | 포인트 배경, 하이라이트 |
| 미스티 그린 | `#C5D5C5` | `--misty-green` | 봄/자연 테마 포인트 |

### CSS 변수 블록 (모든 HTML에 삽입)

```css
:root {
  /* Primary */
  --sunday-beige: #F5E6D3;
  --hug-brown: #8B7355;
  /* Secondary */
  --cream: #FAFAF7;
  --soft-gray: #E8E4DE;
  --warm-white: #FFFFFF;
  /* Text */
  --text-deep: #8B7355;
  --text-dark: #333333;
  --text-mid: #666666;
  --text-light: #999999;
  /* Accent */
  --sale-red: #D4534A;
  --soft-pink: #F2D4C4;
  --misty-green: #C5D5C5;
}
```

---

## 타이포그래피

### 계층 구조

| 레벨 | 용도 | CSS |
|------|------|-----|
| H1 | 프로모션명, 메인 카피 | `font-size: 48px; font-weight: 700; color: var(--hug-brown); letter-spacing: -0.5px;` |
| H2 | 섹션 제목, 보조 카피 | `font-size: 28px; font-weight: 700; color: var(--text-dark);` |
| Body | 설명, 상세 정보 | `font-size: 16px; font-weight: 400; color: var(--text-mid); line-height: 1.6;` |
| Caption | 유의사항, 부가 정보 | `font-size: 12px; font-weight: 400; color: var(--text-light);` |
| CTA | 버튼 텍스트 | `font-size: 16px; font-weight: 700; color: #FFFFFF;` |
| Price | 할인 가격 | `font-size: 32px; font-weight: 700; color: var(--sale-red);` |

### 채널별 폰트 사이즈 스케일링

캔버스 크기에 따라 비례 조정:
- **대형** (1920px 이상): H1 64px, H2 36px, Body 18px
- **중형** (1080px): H1 48px, H2 28px, Body 16px (기본)
- **소형** (400px 이하): H1 24px, H2 18px, Body 12px
- **극소형** (240px): H1 16px, H2 12px, Body 10px

---

## 레이아웃 원칙

### 여백
- **외부 여백**: 캔버스 너비의 5~8%
- **섹션 간 여백**: 24-32px
- **카드 내부 패딩**: 20-24px
- **요소 간 간격**: 8-16px

### 정렬
- **텍스트**: 좌측 정렬 기본, 중앙 정렬은 히어로/CTA에만
- **이미지**: 중앙 정렬, 또는 텍스트와 좌우 배치
- **카드**: 그리드 정렬, 균등 간격

### Border Radius
| 요소 | radius |
|------|--------|
| 카드 | 12-16px |
| 버튼 | 8-12px |
| 태그/뱃지 | 16-20px (pill) |
| 이미지 | 8-12px |

### 그림자
```css
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
```
- 카드와 버튼에만 가볍게 적용

---

## 컴포넌트 패턴 (HTML)

### 프로모션 뱃지
```html
<div style="display:inline-block; background:var(--sale-red); padding:6px 16px; border-radius:16px;">
  <span style="font-size:14px; font-weight:700; color:#FFFFFF;">20% OFF</span>
</div>
```

### 제품 카드
```html
<div style="background:#FFFFFF; border-radius:12px; padding:16px; box-shadow:0 2px 8px rgba(0,0,0,0.06);">
  <div style="width:100%; aspect-ratio:1; border-radius:8px; background:var(--sunday-beige); overflow:hidden;">
    <img src="{PRODUCT_IMAGE}" style="width:100%; height:100%; object-fit:cover;" alt="">
  </div>
  <p style="margin-top:12px; font-size:16px; font-weight:700; color:var(--text-dark);">{PRODUCT_NAME}</p>
  <p style="font-size:14px; color:var(--text-light); text-decoration:line-through;">{PRICE}원</p>
  <p style="font-size:20px; font-weight:700; color:var(--sale-red);">{DISCOUNT_PRICE}원</p>
</div>
```

### CTA 버튼
```html
<div style="display:inline-block; background:var(--hug-brown); padding:14px 32px; border-radius:8px; text-align:center;">
  <span style="font-size:16px; font-weight:700; color:#FFFFFF;">{CTA_TEXT}</span>
</div>
```

### 정보 행
```html
<div style="display:flex; gap:8px; align-items:center;">
  <span style="font-size:14px; color:var(--text-light); width:80px;">{LABEL}</span>
  <span style="font-size:14px; color:var(--text-dark);">{VALUE}</span>
</div>
```

### 인용 박스 (핵심 메시지)
```html
<div style="background:var(--sunday-beige); padding:24px; border-radius:12px; border-left:4px solid var(--hug-brown);">
  <span style="font-size:48px; color:var(--hug-brown); opacity:0.3; line-height:1;">"</span>
  <p style="font-size:20px; color:var(--hug-brown); font-weight:500;">{MESSAGE}</p>
</div>
```

---

## 금지 사항

- 원색(빨강 #FF0000, 파랑 #0000FF, 초록 #00FF00) 대면적 사용 금지
- 과도한 그라디언트 금지
- H1/H2/Body/Caption 4단계 외 폰트 사이즈 혼재 금지
- 5px 이하의 작은 텍스트 금지
- 검정(#000000) 배경 금지
- 형광색/네온 컬러 사용 금지
- 브랜드 컬러 팔레트 외 색상 사용 금지
