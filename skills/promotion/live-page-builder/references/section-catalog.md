# 31개 섹션 카탈로그

라이브 페이지 템플릿(SynologyDrive `live-page/sections/`)의 31개 섹션 전수 정리.
프리미엄 프리셋(★) 14개는 기본 활성. 나머지는 캠페인 성격에 따라 추가/제외.

각 섹션은 600px 폭 standalone HTML로 빌드되고, `body.scrollHeight` 측정 기반 PNG 캡처.

## 카탈로그 표

| ID | 섹션 | 필수 | ★ | 주요 슬롯 | 사용 케이스 |
|---|---|---|---|---|---|
| 01-live-hero | Live Hero (라이브 히어로) | ✅ | ★ | host_image, live_title_html, live_benefit, live_sub | 첫 인상 |
| 02-trust-bar | Trust Bar (신뢰 바) | ✅ | ★ | trust_1_main, trust_2_main, trust_3_main | 발송/환불/배송 한 줄 |
| 03-schedule | Schedule (방송 일정) | ✅ | ★ | schedule_date, schedule_time, schedule_channel | 라이브 시작 안내 |
| 04-countdown | Countdown (카운트다운) | ✅ | ★ | countdown_hours/mins/secs, countdown_note | 정적 카운트다운 (애니메이션 없음) |
| 05-live-benefits | Live Benefits (라이브 혜택) | ✅ | ★ | live_benefits[] (4개) | 2×2 카드 그리드 |
| 06-coupon | Coupon (전용 쿠폰) | 🔶 | ★ | coupon_code, coupon_amount, coupon_condition | 쿠폰 있으면 |
| 07-bundle-deals | Bundle Deals (구매 옵션) | ✅ | | bundles[] (2-4개) | 다중 옵션 라이브 |
| 08-price-compare | Price Compare (가격 비교표) | 🔶 | | live_price, original_price, price_online | 정가 대비 강조 |
| 09-set-contents | Set Contents (세트 구성) | 🔶 | | set_items[] | 세트 상품 |
| 10-mid-cta | Mid CTA (중간 구매 유도) | ✅ | ★ | mid_cta_title, mid_cta_sub | 페이지 중간 강조 |
| 11-host-recommendation | Host Recommendation | 🔶 | ★ | host_name, host_role, host_quote_html | 호스트 코멘트 |
| 12-quick-showcase | Quick Showcase (퀵 쇼케이스) | ✅ | ★ | showcases[] (3-4개) | 셀링 포인트 |
| 13-lifestyle | Lifestyle (라이프스타일) | 🔶 | ★ | lifestyle_image, lifestyle_caption | 사용 장면 |
| 14-size-spec | Size & Spec | 🔶 | | size_headers[], size_rows[] | 사이즈 표 |
| 15-review | Review (리뷰) | ✅ | ★ | review_avg_score, review_total_count, reviews[] | 통계 + 샘플 |
| 16-social-proof | Social Proof (SNS 후기) | 🔶 | | social_reviews[] | SNS 인용 |
| 17-gift-event | Gift Event (사은품) | 🔶 | | gifts[] | 사은품 있으면 |
| 18-target-persona | Target Persona | 🔶 | | target_items[] | "이런 분에게 추천" |
| 19-faq | FAQ | 🔶 | ★ | faqs[] (3-5개) | 자주 묻는 질문 |
| 20-shipping | Shipping (배송/교환/반품) | ✅ | | ship_title_*, ship_desc_* | 보통 default 사용 |
| 21-guarantee | Guarantee (구매 보장) | 🔶 | | guarantee_*_title, guarantee_*_desc | 100일 환불 등 |
| 22-cert-badges | Cert Badges (인증 배지) | 🔶 | | cert_items[] | OEKO-TEX 등 |
| 23-brand-quote | Brand Quote | 🔶 | | brand_quote_html, brand_tag | 브랜드 인용문 |
| 24-brand-story | Brand Story | 🔶 | | brand_story_title, brand_story_desc_html, brand_story_image | 브랜드 스토리 |
| 25-final-cta | Final CTA | ✅ | ★ | final_cta_title_html, final_cta_desc, purchase_url | 최종 구매 유도 |
| 26-close | Close (브랜드 클로징) | ✅ | | close_title_html, close_desc_html | 마지막 인사 |
| 27-footer | Footer | ✅ | ★ | (default 사용 — channel_name 등) | 브랜드 푸터 |
| 28-product-banner | Product Banner | 🔶 | | banner_title, banner_desc, banner_cta_text 등 | 다른 제품 안내 |
| 29-product-grid | Product Grid | 🔶 | | products[] | 제품 그리드 |
| 30-collection-banner | Collection Banner | 🔶 | | collection_title, collection_image | 컬렉션 안내 |
| 31-channel-follow | Channel Follow | 🔶 | | channel_name, channel_desc, channel_url | 팔로우 유도 |

✅ = SynologyDrive GUIDE.md 기준 "필수"
★ = `section_catalog.PREMIUM_PRESET` 기본 14개

## 프리미엄 프리셋 (기본 14개) 순서

```
01-live-hero      → 02-trust-bar     → 03-schedule       → 04-countdown
05-live-benefits  → 06-coupon
10-mid-cta
11-host-recommendation → 12-quick-showcase → 13-lifestyle
15-review
19-faq
25-final-cta
27-footer
```

## 캠페인별 추천 추가 섹션

| 캠페인 성격 | 추가 섹션 |
|---|---|
| 신상품 출시 | 24-brand-story, 28-product-banner |
| 세트 상품 | 09-set-contents, 08-price-compare |
| 다중 옵션 | 07-bundle-deals |
| 사은품 강조 | 17-gift-event |
| 사이즈 중요 | 14-size-spec |
| 친환경 강조 | 22-cert-badges, 23-brand-quote |
| SNS 활용 | 16-social-proof, 31-channel-follow |
| 컬렉션 라이브 | 30-collection-banner |

## 자동 제외 규칙

`build_live.py`는 다음 케이스에서 섹션을 자동으로 제외:

1. **배열 슬롯이 비어있음**: `gifts`가 비면 17-gift-event 제외, `bundles`가 비면 07 제외 등
2. **`active_sections`에 없음**: spec에서 명시 안 한 섹션은 빌드 안 함

각 섹션의 자세한 슬롯 사전 → `references/slot-vocabulary.md`
