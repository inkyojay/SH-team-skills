# plan.json → HTML 변수 매핑 가이드

> plan.json 필드에서 HTML에 삽입할 변수를 추출·생성하는 규칙

## 직접 매핑 변수

| 변수명 | plan.json 경로 | 예시값 |
|--------|---------------|--------|
| `BRAND_NAME` | 고정값 | `SUNDAYHUG` |
| `BRAND_NAME_KO` | 고정값 | `썬데이허그` |
| `PROMOTION_NAME` | `promotion_name` | `봄 슬리핑백 특가` |
| `CONCEPT` | `concept` | `봄맞이 슬리핑백 전 라인업 20% 특가` |
| `KEY_MESSAGE` | `key_message` | `우리 아기 첫 봄잠, 썬데이허그 슬리핑백과 함께` |
| `TONE_MANNER` | `tone_manner` | `따뜻하고 설레는 봄 느낌` |
| `PERIOD` | `period.start` ~ `period.end` | `3/1 ~ 3/15` |
| `PERIOD_START` | `period.start` | `3월 1일` |
| `PERIOD_END` | `period.end` | `3월 15일` |
| `OFFER_TYPE` | `offer.type` | `discount` |
| `OFFER_VALUE` | `offer.value` | `20%` |
| `OFFER_DESC` | `offer.description` | `슬리핑백 전 라인업 20% 할인` |
| `OFFER_ADDITIONAL` | `offer.additional` | `5만원 이상 무료배송` |
| `CTA_TEXT` | `cta` 또는 기본값 | `지금 구매하기` |

## 제품 변수 (반복)

products 배열의 각 항목에서 추출 (N은 0부터):

| 변수명 | plan.json 경로 | 예시값 |
|--------|---------------|--------|
| `PRODUCT_NAME_N` | `products[N].name` | `코지 슬리핑백` |
| `PRODUCT_PRICE_N` | `products[N].price` (포맷팅) | `89,000원` |
| `PRODUCT_SALE_PRICE_N` | `products[N].discount_price` (포맷팅) | `71,200원` |
| `PRODUCT_IMAGE_N` | `products[N].image` | `/path/to/image.png` |
| `PRODUCT_DISCOUNT_RATE_N` | 계산: `(price - discount_price) / price` | `20%` |

### 가격 포맷팅 규칙
- 천 단위 콤마 삽입: `89000` → `89,000`
- "원" 접미사 추가: `89,000원`
- 할인율 계산: `Math.round((1 - discount_price/price) * 100)` + `%`

## Claude가 생성하는 변수

plan.json의 `tone_manner` + `key_message` + `concept`를 기반으로 채널 특성에 맞게 생성:

| 변수명 | 설명 | 생성 기준 |
|--------|------|----------|
| `HEADLINE` | 채널 최적화 메인 카피 | key_message를 채널에 맞게 변형 |
| `SUBHEAD` | 보조 카피 | concept + offer 요약 |
| `BADGE_TEXT` | 뱃지 텍스트 | offer.type에 따라 결정 |
| `FOOTER_TEXT` | 하단 유의사항 | 기간 + 조건 |

### BADGE_TEXT 생성 규칙

| offer.type | BADGE_TEXT |
|-----------|-----------|
| `discount` | `{OFFER_VALUE} OFF` 또는 `{OFFER_VALUE} 할인` |
| `gift` | `사은품 증정` |
| `coupon` | `쿠폰 {OFFER_VALUE}` |
| `bundle` | `세트 특가` |
| `restock` | `RESTOCK` |
| `new` | `NEW` |

### 채널별 HEADLINE 스타일

| 채널 | 카피 스타일 | 글자수 |
|------|-----------|--------|
| 인스타그램 스토리 | 감성적, 짧고 임팩트 | 15자 이내 |
| 인스타그램 피드 | 정보+감성 밸런스 | 20자 이내 |
| 네이버 브랜드홈 카드 | 제품명 또는 2-3단어 | 8자 이내 |
| 네이버 배너 | 혜택 중심, 명확 | 25자 이내 |
| 자사몰 배너 | 브랜드 감성, 라이프스타일 | 25자 이내 |
| 카카오톡 | 핵심 정보, 직접적 | 20자 이내 |
| 라이브 페이지 | 혜택 나열, 간결 | 10자 이내 |

## 매핑 프로세스

### Step 1: 직접 매핑
plan.json에서 위 테이블의 변수를 추출합니다.

### Step 2: 가격 포맷팅
products 배열을 순회하며 가격 변수를 포맷팅합니다.

### Step 3: 카피 생성
각 채널별로 HEADLINE, SUBHEAD, BADGE_TEXT, FOOTER_TEXT를 생성합니다.
- tone_manner를 반영한 어투
- key_message의 핵심 키워드 활용
- offer 정보를 자연스럽게 통합

### Step 4: 에이전트 전달
각 채널 에이전트에 해당 채널의 변수 세트를 전달합니다:
```
공통 변수: BRAND_NAME, PROMOTION_NAME, PERIOD, OFFER_VALUE, ...
제품 변수: PRODUCT_NAME_0, PRODUCT_PRICE_0, ...
생성 변수: HEADLINE, SUBHEAD, BADGE_TEXT, FOOTER_TEXT
```
