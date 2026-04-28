# 카카오 메시지 템플릿 맵 — 8타입 × 24베리에이션 사용 가이드

> 본 스킬은 sundayhug-brand 디자인 시스템의 검증된 템플릿(`Synology/스킬/sundayhug-brand/templates/promotion/kakao-messages/types/`)을 placeholder 치환으로 채워 사용합니다. 새로운 디자인을 만들지 않습니다.

---

## 타입 ID 명명 규칙

```
{타입번호}-{타입명}:{베리에이션문자}
       예: 02-wide-image:A
           05-carousel-commerce:B
           07-alimtalk-image:A
```

베리에이션 문자 의미 (전 타입 공통):
- **A** — Product / Standard / Order (제품 사진 중심)
- **B** — Lifestyle / Dual / Curated / Info (감성 또는 2개 비교)
- **C** — Event / Sale / Story / Triple (이벤트/할인/스토리/3개 리스트)
- **D** — Option (캐러셀 전용 — A/B 옵션 비교)
- **E** — Bundle (캐러셀 전용 — 세트 상품)

---

## 24베리에이션 사용 가이드

### 01-image (800×400+, 2:1~3:4 가변)

| ID | 용도 | 추천 상황 |
|---|---|---|
| `01-image:A-product` | 제품 사진 단독 | 신제품 출시 단일 컷 |
| `01-image:B-lifestyle` | 라이프스타일 컷 | 감성 캠페인, 브랜드 무드 강조 |
| `01-image:C-event` | 이벤트 비주얼 | 시즌 프로모션, 콜라보 |

### 02-wide-image (800×600, 4:3) ★ 가장 자주 사용

| ID | 용도 | 추천 상황 |
|---|---|---|
| `02-wide-image:A-product` | 풀블리드 제품 + 하단 정보바 (가격/할인) | 단일 제품 프로모션 |
| `02-wide-image:B-lifestyle` | 라이프스타일 풀샷 + 가격 오버레이 | 신상 출시 |
| `02-wide-image:C-event` | 이벤트 비주얼 + 혜택 정보 | 출산 선물 시즌, 명절 세트 |

### 03-wide-list (800×400 헤더 + 800×800 리스트 3~4개)

| ID | 용도 | 추천 상황 |
|---|---|---|
| `03-wide-list:A-product` | 같은 카테고리 제품 3~4개 리스트 | 신상 라인업 일괄 노출 |
| `03-wide-list:B-curated` | 큐레이션 (사용자 추천형) | "10만 맘이 선택한 BEST" |

### 04-carousel-feed (800×600/카드, 4:3) ★ 스토리텔링용

| ID | 용도 | 추천 상황 |
|---|---|---|
| `04-carousel-feed:A-product` | 제품 다각도/디테일 컷 | 신제품 디테일 프리뷰 |
| `04-carousel-feed:B-lifestyle` | 사용 시나리오 (낮/밤/외출) | 라이프스타일 스토리 |
| `04-carousel-feed:C-story` | 브랜드 스토리/탄생 비하인드 | 브랜드 캠페인 |
| `04-carousel-feed:D-live` | 라이브 방송 사전 노출 | 라이브 커머스 예고 |

### 05-carousel-commerce (800×800/카드, 1:1) ★ 커머스 핵심

| ID | 용도 | 추천 상황 |
|---|---|---|
| `05-carousel-commerce:A-standard` | 인트로 + 단일 제품 카드 N장 | 신제품 라인업 (3~6개) |
| `05-carousel-commerce:B-dual` | 카드당 2개 제품 비교 | 사이즈/색상 선택지 제공 |
| `05-carousel-commerce:C-triple` | 카드당 3개 제품 넘버링 | TOP 3 추천 |
| `05-carousel-commerce:D-option` | 옵션 A/B 비교 + 가격표 + 쿠폰 | 풀세트 vs 단품 |
| `05-carousel-commerce:E-bundle` | 세트 구성 + 합산 가격 | 출산 선물 세트, 가족 패키지 |

### 06-commerce (800×600, 4:3)

| ID | 용도 | 추천 상황 |
|---|---|---|
| `06-commerce:A-standard` | 단일 제품 + 가격 (와이드형보다 정보 풍부) | 베스트셀러 단일 노출 |
| `06-commerce:B-premium` | 프리미엄 라인 강조 (어두운 톤) | VIP/프리미엄 컬렉션 |
| `06-commerce:C-sale` | 세일 강조 (붉은 강조색) | 시즌 오프, 클리어런스 |

### 07-alimtalk-image (800×400, 2:1) ★ 정보성 전용

| ID | 용도 | 추천 상황 |
|---|---|---|
| `07-alimtalk-image:A-order` | 주문 확인 / 배송 알림 | 주문 완료, 발송 시작 |
| `07-alimtalk-image:B-info` | 일반 정보 안내 | 회원가입 환영, 휴면 해제 |

⚠️ 광고성 카피 절대 금지 — `kakao_validator`가 빌드 단계에서 자동 차단

### 08-alimtalk-itemlist (가변)

| ID | 용도 | 추천 상황 |
|---|---|---|
| `08-alimtalk-itemlist:A-order-summary` | 주문 상세 (아이템 N개) | 결제 완료 후 주문 명세 |
| `08-alimtalk-itemlist:B-recommendation` | 관심 상품 추천 (정보형) | 회원 맞춤 추천 (광고문구 X) |

---

## 캠페인별 추천 조합

### 신제품 출시 (3종 라인업)
1. `02-wide-image:A-product` — 대표 신상 단일 노출 (메인)
2. `05-carousel-commerce:A-standard` — 라인업 3개 캐러셀 (디테일)
3. `04-carousel-feed:A-product` — 디테일 컷 (서브)

### 시즌 프로모션 (출산 선물 시즌)
1. `02-wide-image:C-event` — 시즌 비주얼 (메인)
2. `05-carousel-commerce:E-bundle` — 출산 선물 세트 캐러셀
3. `03-wide-list:B-curated` — "엄마들이 선택한" 큐레이션

### 라이브 커머스 예고
1. `04-carousel-feed:D-live` — 라이브 예고 카드 (사전 알림)
2. `05-carousel-commerce:A-standard` — 라이브 판매 상품 라인업

### 주문 알림 (정보성)
1. `07-alimtalk-image:A-order` — 주문 확인
2. `08-alimtalk-itemlist:A-order-summary` — 주문 상세
3. `07-alimtalk-image:A-order` — 발송 알림 (재발송)

---

## 12개 캠페인 팔레트 (data-palette 속성)

부모 요소에 `data-palette="..."` 추가하면 자동 색상 적용:

| 카테고리 | 팔레트 | 대표색 | 추천 용도 |
|---|---|---|---|
| **시즌** | `golden-hour` | #C8A07C | 브랜드 대표, 기본 (default) |
| | `warm-spring` | #E8C9A8 | 봄 신상, 출산 선물 |
| | `cool-summer` | #B3C5D3 | 여름 특가, 메쉬 라인 |
| | `cozy-autumn` | #D4A574 | 추석 세트, 가을 신상 |
| | `gentle-winter` | #C4B5CB | 크리스마스, 겨울 슬립백 |
| **무드** | `rose-dawn` | #C09B8D | 여아 제품, 블러시 |
| | `fresh-garden` | #7A8F76 | 친환경, 밤부 라인 |
| | `moonlit-calm` | #B0A899 | 수면 캠페인, 야간 라이브 |
| | `blush-touch` | #DEB5A8 | 신생아, 출산 축하 |
| **스페셜** | `slate-mood` | #8A9BB0 | 남아 제품, 프리미엄 |
| | `coral-sunset` | #D4856C | 한정판, 콜라보, 기념일 |
| | `midnight-luxe` | #2C2C3A | VIP, 프리미엄 (다크 모드) |

---

## 템플릿 HTML 내 placeholder 패턴

`scripts/kakao_factory.py`가 자동 치환하는 패턴:

| 패턴 | 설명 | 예시 |
|---|---|---|
| `{{key}}` | 텍스트 치환 | `{{title}}`, `{{price}}`, `{{description}}` |
| `src="..."` | 이미지 경로 치환 (key 매칭) | `src="hero.jpg"` → `images.hero` 키와 매칭 |
| `data-palette="..."` | 팔레트 주입 (자동) | 빈 값 또는 기본값을 config의 palette로 교체 |
| `data-card-index="..."` | 캐러셀 카드 순서 | 0=인트로, 1~N=제품 카드 |

⚠️ 일부 템플릿은 placeholder가 아니라 실제 더미 텍스트로 작성됨. 빌드 전 `kakao_factory.scan_placeholders()`가 24개 베리에이션 전체를 스캔해 매핑 인덱스를 자동 작성합니다.
