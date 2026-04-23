# 썬데이허그 스마트스토어 배너 템플릿

네이버 스마트스토어 배너 이미지 제작을 위한 HTML 템플릿 시스템.
HTML → PNG 변환 워크플로우 전용. JavaScript/애니메이션 없음.

## 파일 구조

```
smartstore-banners/
├── _base-styles.css       # 디자인 시스템 (변수, 리셋, 프레임, 컴포넌트)
├── _palettes.css          # 캠페인 컬러 팔레트 12종
├── _guide-chrome.css      # 가이드 페이지 전용 UI 스타일
├── GUIDE.md               # 이 파일
├── template-guide.html    # 전체 미리보기 + 팔레트 스위처
└── types/
    ├── 01-pc-main/        # PC 메인배너 (1920×600)
    │   ├── A-product.html
    │   ├── B-season.html
    │   ├── C-event.html
    │   └── D-lifestyle.html    ← 풀블리드 이미지 + 우측 텍스트
    ├── 02-mobile-main/    # 모바일 메인배너 (720×960, 세로형)
    │   ├── A-product.html
    │   ├── B-season.html
    │   ├── C-event.html
    │   └── D-lifestyle.html    ← 풀블리드 세로 이미지 + 하단 텍스트
    ├── 03-promotion/      # 프로모션 스트립 배너 (720×240)
    │   ├── A-discount.html
    │   ├── B-exhibition.html
    │   └── C-new-product.html
    ├── 04-coupon/         # 쿠폰 배너 (720×360)
    │   ├── A-single.html
    │   ├── B-multi.html
    │   └── C-conditional.html
    └── 05-category/       # 카테고리 배너 (720×360)
        ├── A-collection.html
        ├── B-best.html
        └── C-season.html
```

## 배너 타입 (5종)

| 타입 | 크기 | 용도 |
|------|------|------|
| 01 PC 메인 | 1920×600 | PC 스토어 홈 상단 메인 배너 |
| 02 모바일 메인 | 720×480 | 모바일 스토어 홈 상단 메인 배너 |
| 03 프로모션 | 720×240 | 프로모션 영역 스트립 배너 |
| 04 쿠폰 | 720×360 | 쿠폰 다운로드 유도 배너 |
| 05 카테고리 | 720×360 | 카테고리 상단 배너 |

## 팔레트 (12종)

body 또는 상위 요소에 `data-palette` 속성을 추가하여 적용.

```html
<body data-palette="warm-spring">
```

### 시즌 (4종)
- **warm-spring** — 봄 신상, 출산 선물
- **cool-summer** — 여름 특가, 메쉬 라인
- **cozy-autumn** — 추석 세트, 가을 신상
- **gentle-winter** — 크리스마스, 겨울 슬립백

### 무드 (4종)
- **rose-dawn** — 여아 제품, 블러시 컬렉션
- **fresh-garden** — 친환경, 밤부 라인
- **moonlit-calm** — 수면 캠페인, 야간 라이브
- **blush-touch** — 신생아, 출산 축하

### 스페셜 (4종)
- **slate-mood** — 남아 제품, 프리미엄 라인
- **golden-hour** — 브랜드 대표 (기본값)
- **coral-sunset** — 한정판, 콜라보, 기념일
- **midnight-luxe** — VIP 라이브, 프리미엄 세트 (다크 모드)

## 사용법

1. `types/` 폴더에서 적합한 배너 타입과 변형을 선택
2. HTML 파일을 복사하여 텍스트/이미지 교체
3. 필요 시 `data-palette` 속성으로 캠페인 팔레트 변경
4. HTML → PNG 변환 도구로 이미지 생성

## CSS 클래스 접두사

모든 스마트스토어 배너 클래스는 `.ss-` 접두사를 사용합니다.

- `.ss-frame` — 배너 프레임 컨테이너
- `.ss-title` / `.ss-subtitle` — 타이포그래피
- `.ss-badge` — 라운드 뱃지
- `.ss-price` / `.ss-discount` / `.ss-price-orig` — 가격 정보
- `.ss-label` — 영문 라벨 (uppercase)
- `.ss-hero-img` — 전체 커버 이미지
- `.ss-overlay` — 이미지 위 텍스트 오버레이 (.bottom / .top / .full)
- `.ss-split` / `.ss-split-text` / `.ss-split-img` — 좌우 분할 레이아웃
- `.ss-center` — 중앙 정렬 레이아웃
- `.ss-coupon-card` / `.ss-coupon-amount` — 쿠폰 카드
- `.ss-brand-bar` / `.ss-brand-logo` — 브랜드 바
- `.ss-period` — 이벤트 기간
