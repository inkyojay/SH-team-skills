# 프리미엄 프리셋 (기본 14 섹션)

`section_catalog.PREMIUM_PRESET`에 정의된 라이브 페이지 기본 추천 섹션. 사용자가 별도로 활성 섹션을 명시하지 않으면 이 14개가 기본 활성.

## 14개 순서 + 역할

| # | 섹션 | 역할 |
|---|---|---|
| 1 | `01-live-hero` | 첫 인상 — 호스트 + 라이브 타이틀 + 메인 혜택 |
| 2 | `02-trust-bar` | 발송/환불/배송 안심 한 줄 |
| 3 | `03-schedule` | "언제 어디서 보세요" 일정 안내 |
| 4 | `04-countdown` | 정적 카운트다운 (애니메이션 없음, 시각 강조용) |
| 5 | `05-live-benefits` | 2×2 라이브 혜택 카드 — 핵심 혜택 4개 |
| 6 | `06-coupon` | 라이브 전용 쿠폰 코드/금액/조건 |
| 7 | `10-mid-cta` | 페이지 중간 구매 유도 — "지금 사면 이런 혜택" |
| 8 | `11-host-recommendation` | 호스트 코멘트 — 신뢰 빌딩 |
| 9 | `12-quick-showcase` | 셀링 포인트 3-4개 — 제품 특징 |
| 10 | `13-lifestyle` | 라이프스타일 이미지 + 캡션 — 사용 장면 |
| 11 | `15-review` | 리뷰 통계(평점/개수/재구매율) + 샘플 |
| 12 | `19-faq` | 자주 묻는 질문 (3-5개) |
| 13 | `25-final-cta` | 최종 구매 유도 — "라이브 종료 전 결제" |
| 14 | `27-footer` | 브랜드 푸터 |

## 왜 이 14개인가

### 빠진 섹션이 빠진 이유

| 섹션 | 왜 기본 제외 |
|---|---|
| 07-bundle-deals | 다중 옵션 라이브에만 필요 |
| 08-price-compare | 정가 비교 강조 안 하는 케이스 많음 |
| 09-set-contents | 세트 상품 전용 |
| 14-size-spec | 의류성 제품 한정 |
| 16-social-proof | SNS 후기 데이터 별도 수집 필요 |
| 17-gift-event | 사은품 없는 라이브 많음 |
| 18-target-persona | 타겟 명시 안 해도 무방 |
| 20-shipping | 02-trust-bar로 갈음. 자세한 배송 정책은 나중 단계 |
| 21-guarantee | 02 + 19에서 다룸 |
| 22-cert-badges | 친환경/유아 안전 강조 시만 |
| 23-brand-quote | 24-brand-story와 중복 가능 |
| 24-brand-story | 스토리텔링 강조 라이브에만 |
| 26-close | 27-footer로 갈음 가능 |
| 28-product-banner | 다른 제품 안내 — 라이브 본 제품 외 추가 강조 시 |
| 29-product-grid | 제품 그리드 — 컬렉션 라이브용 |
| 30-collection-banner | 컬렉션 라이브 |
| 31-channel-follow | 팔로우 유도 — 보조 |

### 추가하면 좋은 케이스별 추천

| 라이브 성격 | 추가할 섹션 |
|---|---|
| 사은품 강조 | + 17-gift-event |
| 신상품 출시 | + 24-brand-story, + 28-product-banner |
| 의류성 제품 | + 14-size-spec, + 22-cert-badges |
| 컬렉션 라이브 | + 30-collection-banner, + 29-product-grid |
| 가격 비교 강조 | + 08-price-compare |
| 다중 옵션 | + 07-bundle-deals |
| SNS 후기 강조 | + 16-social-proof, + 31-channel-follow |
| 친환경/안전 강조 | + 22-cert-badges, + 23-brand-quote |
| 세트 상품 | + 09-set-contents |

## 변경 방법

`spec.json`에서 `active_sections` 직접 명시:

```json
{
  "campaign_slug": "...",
  "active_sections": [
    "01-live-hero",
    "02-trust-bar",
    "03-schedule",
    "05-live-benefits",
    "07-bundle-deals",
    "10-mid-cta",
    "12-quick-showcase",
    "14-size-spec",
    "15-review",
    "17-gift-event",
    "19-faq",
    "22-cert-badges",
    "25-final-cta",
    "27-footer"
  ],
  ...
}
```

또는 인터뷰 마지막에 "추가 섹션 더 넣을까요?" 물을 때 사용자가 선택하면 add.

## 확정 후 흐름

```bash
build_live.py --spec spec.json    # → previews/{14 HTMLs} + preview-grid.html
export_png.py --campaign <slug>   # → final/{14 PNGs}
open ~/Desktop/output/상세페이지/라이브/<slug>/previews/preview-grid.html
```

미리보기에서 섹션별 PNG 다운로드.
