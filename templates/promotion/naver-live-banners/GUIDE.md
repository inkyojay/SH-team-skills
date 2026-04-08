# 썬데이허그 네이버 쇼핑라이브 배너 템플릿

네이버 쇼핑라이브 배너 이미지 제작을 위한 HTML 템플릿 시스템.
HTML → PNG 변환 워크플로우 전용. JavaScript/애니메이션 없음.

## 파일 구조

```
naver-live-banners/
├── _base-styles.css       # 디자인 시스템 (변수, 리셋, 프레임, 컴포넌트)
├── _palettes.css          # 캠페인 컬러 팔레트 12종
├── _guide-chrome.css      # 가이드 페이지 전용 UI 스타일
├── GUIDE.md               # 이 파일
├── template-guide.html    # 전체 미리보기 + 팔레트 스위처
└── types/
    ├── 01-live-main/      # 라이브 메인 (1080×1080)
    │   ├── A-product.html
    │   ├── B-host.html
    │   └── C-event.html
    ├── 02-wide-banner/    # 와이드 배너 (1200×628)
    │   ├── A-product.html
    │   ├── B-benefit.html
    │   └── C-timesale.html
    ├── 03-benefit/        # 혜택 배너 (720×360)
    │   ├── A-coupon.html
    │   ├── B-gift.html
    │   └── C-limited.html
    ├── 04-product-card/   # 상품 카드 (720×720)
    │   ├── A-single.html
    │   ├── B-dual.html
    │   └── C-triple.html
    └── 05-notification/   # 알림 배너 (720×240)
        ├── A-preview.html
        ├── B-live-now.html
        └── C-replay.html
```

## 배너 타입 (5종)

| 타입 | 크기 | 용도 |
|------|------|------|
| 01 라이브 메인 | 1080×1080 | 쇼핑라이브 메인 썸네일 |
| 02 와이드 배너 | 1200×628 | 쇼핑라이브 와이드 배너 |
| 03 혜택 배너 | 720×360 | 라이브 혜택 안내 배너 |
| 04 상품 카드 | 720×720 | 라이브 상품 카드 |
| 05 알림 배너 | 720×240 | 라이브 알림 스트립 |

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

모든 네이버 라이브 배너 클래스는 `.nlb-` 접두사를 사용합니다.

- `.nlb-frame` — 배너 프레임 컨테이너
- `.nlb-title` / `.nlb-subtitle` — 타이포그래피
- `.nlb-badge` — 라운드 뱃지
- `.nlb-price` / `.nlb-discount` / `.nlb-price-orig` — 가격 정보
- `.nlb-label` — 영문 라벨 (uppercase)
- `.nlb-live-badge` — LIVE 뱃지 (빨간색, 정적)
- `.nlb-host-circle` — 진행자 원형 사진
- `.nlb-countdown` — 카운트다운 표시 (정적)
- `.nlb-hero-img` — 전체 커버 이미지
- `.nlb-overlay` — 이미지 위 텍스트 오버레이 (.bottom / .top / .full)
- `.nlb-split` / `.nlb-split-text` / `.nlb-split-img` — 좌우 분할 레이아웃
- `.nlb-center` — 중앙 정렬 레이아웃
- `.nlb-benefit-card` / `.nlb-benefit-amount` — 혜택 카드
- `.nlb-product-card` / `.nlb-product-name` / `.nlb-product-price` — 상품 카드
- `.nlb-brand-bar` / `.nlb-brand-logo` — 브랜드 바
- `.nlb-strip` — 하단 정보 스트립
