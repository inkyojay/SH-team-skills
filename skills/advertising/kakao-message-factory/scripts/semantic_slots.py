"""
semantic_slots.py — 시맨틱 키 → 템플릿별 실제 CSS 클래스 매핑

사용자/Claude는 시맨틱 키만 입력 (title, desc, price 등).
팩토리가 각 템플릿의 실제 클래스로 자동 변환.

매핑이 없는 슬롯은 단순 무시 (예: B-lifestyle은 price 슬롯 없음).
"""
from __future__ import annotations

# ─── 시맨틱 텍스트 슬롯 ─────────────────────────────────────────────────────
# 각 템플릿이 어떤 시맨틱 키를 어떤 CSS 클래스로 받는지 정의
# `cls@N`: 같은 클래스가 N번 반복될 때 N번째 매칭만 (0-based)

SEMANTIC_TEXT_SLOTS: dict[str, dict[str, str]] = {
    # ─── 01-image (800×400) ───
    "01-image:A-product": {
        "badge": "km-badge",
        "title": "km-split-text",
    },
    "01-image:B-lifestyle": {
        "brand": "km-strip-brand",
        "info": "km-strip-text",
    },
    "01-image:C-event": {
        "badge": "km-badge",
        "title": "km-center",  # 중앙 텍스트 영역
    },

    # ─── 02-wide-image (800×600) ───
    "02-wide-image:A-product": {
        "title": "km-info-bar-name",
        "desc":  "km-info-bar-desc",
        "discount": "km-info-bar-discount",
        "price": "km-info-bar-price",
        "orig":  "km-info-bar-orig",
    },
    "02-wide-image:B-lifestyle": {
        "brand": "km-lifestyle-brand",
    },
    "02-wide-image:C-event": {
        "badge": "km-badge",
        "title": "km-split-text",
    },

    # ─── 03-wide-list (800×400 + 800×800) ───
    "03-wide-list:A-product": {
        "title": "km-split-text",
        "item1_title": "km-list-item-name@0",
        "item1_desc":  "km-list-item-desc@0",
        "item1_discount": "km-list-item-discount@0",
        "item1_price": "km-list-item-price@0",
        "item1_orig":  "km-list-item-orig@0",
        "item2_title": "km-list-item-name@1",
        "item2_desc":  "km-list-item-desc@1",
        "item2_discount": "km-list-item-discount@1",
        "item2_price": "km-list-item-price@1",
        "item2_orig":  "km-list-item-orig@1",
        "item3_title": "km-list-item-name@2",
        "item3_desc":  "km-list-item-desc@2",
        "item3_discount": "km-list-item-discount@2",
        "item3_price": "km-list-item-price@2",
        "item3_orig":  "km-list-item-orig@2",
    },
    "03-wide-list:B-curated": {
        "label": "km-curated-label",
        "title": "km-curated-title",
        "item1_title": "km-list-item-name@0",
        "item1_desc":  "km-list-item-desc@0",
        "item1_discount": "km-list-item-discount@0",
        "item1_price": "km-list-item-price@0",
        "item1_orig":  "km-list-item-orig@0",
        "item2_title": "km-list-item-name@1",
        "item2_desc":  "km-list-item-desc@1",
        "item2_price": "km-list-item-price@1",
        "item3_title": "km-list-item-name@2",
        "item3_desc":  "km-list-item-desc@2",
        "item3_price": "km-list-item-price@2",
    },

    # ─── 04-carousel-feed (800×600) — 카드별 분리 ───
    "04-carousel-feed:A-product": {
        # cover (card 0) + product (card 1)
        "tag":   "km-cover-tag",
        "title": "km-cover-title",
        "date":  "km-cover-date",
        "product_title": "km-info-bar-name",
        "product_desc":  "km-info-bar-desc",
        "product_discount": "km-info-bar-discount",
        "product_price": "km-info-bar-price",
        "product_orig":  "km-info-bar-orig",
    },
    "04-carousel-feed:B-lifestyle": {
        "brand": "km-strip-brand",
        "info":  "km-strip-text",
    },
    "04-carousel-feed:C-story": {
        "story1_num":   "km-story-num@0",
        "story1_title": "km-story-title@0",
        "story1_body":  "km-story-body@0",
        "story2_num":   "km-story-num@1",
        "story2_title": "km-story-title@1",
        "story2_body":  "km-story-body@1",
    },

    # ─── 04-carousel-feed:D-live-* (1080×1350, 5 카드, 인라인 스타일 위주) ───
    # D-live 템플릿은 클래스가 거의 없고 인라인 스타일 구조 → 별도 처리 (live_carousel.py)
    "04-carousel-feed:D-live-carousel": {},
    "04-carousel-feed:D-live-carousel--abc-bed": {},
    "04-carousel-feed:D-live-carousel--portable-bed": {},

    # ─── 05-carousel-commerce (800×800) ───
    "05-carousel-commerce:A-standard": {
        # cover card 0
        "tag":   "km-cover-tag",
        "title": "km-cover-title",
        "sub":   "km-cover-sub",
        "date":  "km-cover-date",
        # product card 1
        "product_badge":    "km-commerce-badge",
        "product_category": "km-commerce-category",
        "product_title":    "km-commerce-name",
        "product_desc":     "km-commerce-desc",
        "product_discount": "km-commerce-discount",
        "product_price":    "km-commerce-price",
        "product_orig":     "km-commerce-orig",
    },
    "05-carousel-commerce:B-dual": {
        "badge": "km-badge",
        "item1_title": "km-dual-name@0",
        "item1_size":  "km-dual-size@0",
        "item1_discount": "km-dual-discount@0",
        "item1_price": "km-dual-price@0",
        "item1_orig":  "km-dual-orig@0",
        "item2_title": "km-dual-name@1",
        "item2_size":  "km-dual-size@1",
        "item2_discount": "km-dual-discount@1",
        "item2_price": "km-dual-price@1",
        "item2_orig":  "km-dual-orig@1",
    },
    "05-carousel-commerce:C-triple": {
        # cover card 0
        "tag":   "km-cover-tag",
        "title": "km-cover-title",
        "sub":   "km-cover-sub",
        # triple list card 1
        "item1_title": "km-triple-name@0",
        "item1_desc":  "km-triple-desc@0",
        "item1_price": "km-triple-price@0",
        "item2_title": "km-triple-name@1",
        "item2_desc":  "km-triple-desc@1",
        "item2_price": "km-triple-price@1",
        "item3_title": "km-triple-name@2",
        "item3_desc":  "km-triple-desc@2",
        "item3_price": "km-triple-price@2",
    },
    "05-carousel-commerce:D-option": {
        "option_a": "km-option-name@0",
        "option_b": "km-option-name@1",
        "coupon1_label": "km-coupon-label@0",
        "coupon1_amount": "km-coupon-amount@0",
        "coupon2_label": "km-coupon-label@1",
        "coupon2_amount": "km-coupon-amount@1",
    },
    "05-carousel-commerce:E-bundle": {
        "badge": "km-badge",
        "label": "km-bundle-label",
        "title": "km-title",
        "discount": "km-commerce-discount",
        "price": "km-commerce-price",
        "orig":  "km-commerce-orig",
    },

    # ─── 06-commerce (800×600) ───
    "06-commerce:A-standard": {
        "title":    "km-commerce-name",
        "category": "km-commerce-category",
        "desc":     "km-commerce-desc",
        "badge":    "km-commerce-badge",
        "discount": "km-commerce-discount",
        "price":    "km-commerce-price",
        "orig":     "km-commerce-orig",
    },
    "06-commerce:B-premium": {
        "title":    "km-premium-name",
        "label":    "km-premium-label",
        "discount": "km-commerce-discount",
        "price":    "km-commerce-price",
        "orig":     "km-commerce-orig",
    },
    "06-commerce:C-sale": {
        "title": "km-title",
        "tag":   "km-sale-tag",
        "info":  "km-sale-info",
        "price": "km-price",
        "orig":  "km-price-orig",
    },

    # ─── 07/08-alimtalk (지원 중단 — 키만 유지) ───
    "07-alimtalk-image:A-order": {},
    "07-alimtalk-image:B-info": {"info": "km-center"},
    "08-alimtalk-itemlist:A-order-summary": {
        "title": "km-itemlist-title",
        "btn":   "km-alimtalk-btn",
    },
    "08-alimtalk-itemlist:B-recommendation": {
        "title": "km-itemlist-title",
        "btn":   "km-alimtalk-btn",
    },
}


# ─── 시맨틱 이미지 슬롯 ─────────────────────────────────────────────────────
# 어떤 시맨틱 이미지 키가 어떤 클래스/alt와 매칭되는지

SEMANTIC_IMAGE_SLOTS: dict[str, dict[str, str]] = {
    # 01
    "01-image:A-product": {"hero": "km-split-img"},
    "01-image:B-lifestyle": {"hero": "km-hero-img"},
    "01-image:C-event": {"hero": "km-center"},  # background

    # 02
    "02-wide-image:A-product": {"hero": "km-hero-img"},
    "02-wide-image:B-lifestyle": {"hero": "km-hero-img"},
    "02-wide-image:C-event": {"hero": "km-split-img"},

    # 03
    "03-wide-list:A-product": {
        "hero": "km-split-img",
        "item1": "km-list-item-img@0",
        "item2": "km-list-item-img@1",
        "item3": "km-list-item-img@2",
    },
    "03-wide-list:B-curated": {
        "item1": "km-list-item-img@0",
        "item2": "km-list-item-img@1",
        "item3": "km-list-item-img@2",
    },

    # 04 carousel-feed (cover + product)
    "04-carousel-feed:A-product": {
        "hero": "km-hero-img@0",      # cover
        "product": "km-hero-img@1",   # product
    },
    "04-carousel-feed:B-lifestyle": {
        "hero": "km-hero-img@0",
        "product": "km-hero-img@1",
    },
    "04-carousel-feed:C-story": {
        "story1_img": "km-hero-img@0",
        "story2_img": "km-hero-img@1",
    },

    # D-live: alt 매칭 사용 (semantic key = alt text)
    "04-carousel-feed:D-live-carousel": {},
    "04-carousel-feed:D-live-carousel--abc-bed": {},
    "04-carousel-feed:D-live-carousel--portable-bed": {},

    # 05 carousel-commerce
    "05-carousel-commerce:A-standard": {
        "hero": "km-hero-img",       # cover
        "product": "km-commerce-img",# product card
    },
    "05-carousel-commerce:B-dual": {
        "item1": "km-dual-img@0",
        "item2": "km-dual-img@1",
    },
    "05-carousel-commerce:C-triple": {
        "hero": "km-hero-img",
        "item1": "km-triple-img@0",
        "item2": "km-triple-img@1",
        "item3": "km-triple-img@2",
    },
    "05-carousel-commerce:D-option": {
        "option_a_img": "km-option-img@0",
        "option_b_img": "km-option-img@1",
    },
    "05-carousel-commerce:E-bundle": {
        "hero": "km-bundle-hero",
    },

    # 06
    "06-commerce:A-standard": {"hero": "km-top-img"},
    "06-commerce:B-premium": {"hero": "km-top-img"},
    "06-commerce:C-sale": {"hero": "km-hero-img"},
}


# ─── 헬퍼 함수 ──────────────────────────────────────────────────────────────
def map_semantic_to_classes(
    template_id: str,
    semantic_data: dict,
) -> dict[str, str]:
    """
    시맨틱 dict {"title": "...", "price": 119000} → 클래스 dict {"km-info-bar-name": "...", ...}.
    템플릿이 갖지 않는 슬롯은 무시.
    """
    text_slots = SEMANTIC_TEXT_SLOTS.get(template_id, {})
    result = {}
    for sem_key, value in semantic_data.items():
        if value in (None, "", 0) and not isinstance(value, (int, float)):
            continue
        cls = text_slots.get(sem_key)
        if cls:
            result[cls] = value
    return result


def map_semantic_images(
    template_id: str,
    image_data: dict,
) -> dict[str, str]:
    """시맨틱 이미지 dict {"hero": "/path"} → 클래스 dict {"km-hero-img": "/path"}."""
    img_slots = SEMANTIC_IMAGE_SLOTS.get(template_id, {})
    result = {}
    for sem_key, path in image_data.items():
        if not path:
            continue
        cls = img_slots.get(sem_key)
        if cls:
            result[cls] = path
    return result


def supported_slots(template_id: str) -> list[str]:
    """이 템플릿이 지원하는 시맨틱 키 리스트 (디버깅용)."""
    text = list(SEMANTIC_TEXT_SLOTS.get(template_id, {}).keys())
    images = list(SEMANTIC_IMAGE_SLOTS.get(template_id, {}).keys())
    return sorted(set(text + [f"img:{k}" for k in images]))
