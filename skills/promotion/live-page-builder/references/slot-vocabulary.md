# 슬롯 사전 (Slot Vocabulary)

31개 섹션이 사용하는 150+ Mustache 슬롯의 의미와 입력 예시. 각 슬롯이 어디서 채워지는지(인터뷰 / default / 자동 계산)를 명시.

## 명명 규칙

- **`*_html` 접미사**: HTML escape 안 함. `<br>`, `<strong>` 등 raw HTML 가능. (`build_live.py`가 자동으로 `{{{var}}}` 처리)
- **단수형 (예: `coupon_code`)**: 단일 값
- **복수형 + `[]` (예: `live_benefits[]`)**: 배열. `{{#배열}}...{{/배열}}` 반복
- **`{{?cond}}` 조건부**: 비표준 mustache. 빌더가 `{{#cond}}`로 자동 변환

## 핵심 라이브 슬롯 (인터뷰 필수)

### 호스트 (01, 11)
| 슬롯 | 타입 | 예시 |
|---|---|---|
| `host_image` | URL/path | `~/Desktop/.../host.jpg` 또는 `https://...` |
| `host_photo` | 동일 | (11번 섹션의 별도 슬롯) |
| `host_name` | 단일 | "사라쌤" |
| `host_role` | 단일 | "수면 코치" |
| `host_quote_html` | HTML | "엄마들이 가장 많이 추천하는<br>실키밤부 슬리핑백" |

### 라이브 타이틀 (01)
| 슬롯 | 타입 | 예시 |
|---|---|---|
| `live_title_html` | HTML | "엄마들의 꿀잠 시크릿<br>실키밤부 라이브 특가" |
| `live_sub` | 단일 | "라이브 시간만 적용, 놓치면 정가 복귀" |
| `live_benefit` | 단일 | "오늘 라이브 한정 30% 할인 + 사은품" |

### 일정 (03, 04)
| 슬롯 | 타입 | 예시 |
|---|---|---|
| `schedule_date` | 단일 | "2026.05.10 (일)" |
| `schedule_time` | 단일 | "오후 8시" |
| `schedule_channel` | 단일 | "네이버 쇼핑라이브" |
| `countdown_hours` | 단일 | "02" (정적, 애니메이션 없음) |
| `countdown_mins` | 단일 | "30" |
| `countdown_secs` | 단일 | "00" |
| `countdown_title` | 단일 | "라이브 시작까지" |
| `countdown_note` | 단일 | "방송 시작 시점 기준" |

### 가격 (06, 08, 10, 25)
| 슬롯 | 타입 | 예시 |
|---|---|---|
| `live_price` | 단일 | "29,900원" |
| `live_price_1` / `live_price_2` | 단일 | (08-price-compare 다중 가격용) |
| `original_price` | 단일 | "39,900원" |
| `original_price_1` / `original_price_2` | 단일 | (08-price-compare용) |
| `price_online` | 단일 | "34,900원" (온라인몰가) |
| `price_regular` | 단일 | (정가, 08용) |
| `price_orig` | 단일 | (취소선 가격) |
| `price_save_amount` | 단일 | "10,000원" |
| `price_live` | 단일 | "29,900원" (07-bundle용) |
| `discount` / `discount_rate` | 단일 | "30%" |
| `discount_rate_1` / `_2` | 단일 | (다중 딜) |

### 쿠폰 (06)
| 슬롯 | 타입 | 예시 |
|---|---|---|
| `coupon_code` | 단일 | "LIVE0510" |
| `coupon_amount` | 단일 | "5,000원" |
| `coupon_condition` | 단일 | "5만원 이상 구매 시" |
| `coupon_label` | 단일 | "라이브 전용" |

### 라이브 혜택 (05)
```python
"live_benefits": [
  {"icon": "🎁", "title": "라이브 한정 30%", "desc": "라이브 시간 동안만 적용", "tag": "TODAY"},
  {"icon": "🚚", "title": "오늘 발송", "desc": "평일 14시 이전 결제", "tag": "FAST"},
  {"icon": "💝", "title": "사은품 증정", "desc": "구매 고객 전원", "tag": "GIFT"},
  {"icon": "🔄", "title": "100일 환불", "desc": "조건 없이 가능", "tag": "TRUST"},
]
```

각 항목 슬롯: `icon`, `title`, `desc`, `tag`

## 신뢰/배송 슬롯 (default 제공)

### Trust Bar (02) — 거의 항상 default 사용
| 슬롯 | Default |
|---|---|
| `trust_1_main` | "오늘 발송" |
| `trust_1_sub` | "평일 14시 이전" |
| `trust_2_main` | "100일 환불" |
| `trust_2_sub` | "조건 없이" |
| `trust_3_main` | "무료 배송" |
| `trust_3_sub` | "5만원 이상" |

### Shipping (20) — 거의 항상 default
| 슬롯 | Default |
|---|---|
| `ship_title_1`/`ship_desc_1` | "배송" / "평일 14시 이전 주문 시 당일 발송" |
| `ship_title_2`/`ship_desc_2` | "교환" / "수령 후 7일 이내" |
| `ship_title_3`/`ship_desc_3` | "환불" / "수령 후 100일 이내, 조건 없이" |
| `ship_title_4`/`ship_desc_4` | "고객센터" / "카카오톡 @sundayhug" |

### Guarantee (21) — default
| 슬롯 | Default |
|---|---|
| `guarantee_1_title` | "100일 환불 보장" |
| `guarantee_1_desc` | "사용 후에도 마음에 들지 않으면 조건 없이 환불" |
| `guarantee_2_title` | "유해물질 ZERO" |
| `guarantee_2_desc` | "OEKO-TEX 인증 원단만 사용" |

### Footer (27) — default
| 슬롯 | Default |
|---|---|
| `channel_name` | "Sunday Hug" |
| `channel_url` | "https://sundayhug.kr" |

## 배열 슬롯 (선택, 비면 섹션 제외)

| 배열 | 항목 슬롯 | 권장 개수 |
|---|---|---|
| `live_benefits` | icon, title, desc, tag | 4 |
| `bundles` | name, qty, price_live, original_price, discount, featured(bool) | 2-4 |
| `set_items` | name, qty | 5-10 |
| `gifts` | gift_title_html, gift_desc, gift_note, image | 1-3 |
| `showcases` | image, title, desc, warm(bool), rev(bool) | 3-4 |
| `reviews` | username, quote_html, tag | 3 |
| `social_reviews` | username, quote, image | 3-6 |
| `target_items` | text | 4-6 |
| `faqs` | question, answer_html | 3-5 |
| `cert_items` | name, image, desc | 2-4 |
| `material_rows` | name, composition, condition | 4 |
| `size_headers` | text | 컬럼 헤더들 |
| `size_rows` | cells (배열) | 사이즈별 행 |

## 기타 슬롯

### Mid CTA (10)
- `mid_cta_title`, `mid_cta_sub`

### Final CTA (25)
- `final_cta_title_html`, `final_cta_desc`, `final_cta_note`, `purchase_url`

### Close (26)
- `close_title_html`, `close_desc_html`

### Brand Story (24)
- `brand_story_title`, `brand_story_desc_html`, `brand_story_image`

### Brand Quote (23)
- `brand_quote_html`, `brand_tag`

### Lifestyle (13)
- `lifestyle_image`, `lifestyle_caption`, `lifestyle_alt`

### Section Title (15-review)
- `section_title` (예: "실제 구매 후기"), `review_avg_score`, `review_total_count`, `review_repurchase`

### Banner (28-product-banner)
- `banner_title`, `banner_desc`, `banner_cta_text`, `banner_label`, `banner_price_live`, `banner_price_original`, `image`/`product_image`

### Collection (30-collection-banner)
- `collection_title`, `collection_sub`, `collection_image`, `collection_link_text`, `collection_url`
