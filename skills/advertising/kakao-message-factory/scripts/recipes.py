"""
recipes.py — 다양성 레시피

같은 사이즈 안에서도 레이아웃 자체가 다른 템플릿을 섞어
"진짜 시각적으로 다른" 5변형을 자동 생성.

각 레시피는 (template_id, palette, tone) 튜플 리스트.
"""
from __future__ import annotations

# ─── 다양성 레시피 ──────────────────────────────────────────────────────────
RECIPES: dict[str, dict] = {

    # ═══ Wide Image 800×600 — 5종 (시각적으로 완전 다름) ═══
    "wide-mix-5": {
        "type": "messages",
        "label": "와이드 5종 (스타일 다양: 풀블리드/라이프/이벤트/커머스/세일)",
        "size_label": "800×600",
        "variants": [
            ("02-wide-image:A-product",   "warm-spring",   "informational"),
            ("02-wide-image:B-lifestyle", "rose-dawn",     "emotional"),
            ("02-wide-image:C-event",     "coral-sunset",  "urgency"),
            ("06-commerce:A-standard",    "cool-summer",   "informational"),
            ("06-commerce:C-sale",        "golden-hour",   "urgency"),
        ],
    },

    "wide-premium-5": {
        "type": "messages",
        "label": "프리미엄 와이드 5종 (다크/럭셔리 톤)",
        "size_label": "800×600",
        "variants": [
            ("02-wide-image:A-product",   "midnight-luxe", "premium"),
            ("02-wide-image:B-lifestyle", "slate-mood",    "premium"),
            ("06-commerce:A-standard",    "moonlit-calm",  "premium"),
            ("06-commerce:B-premium",     "midnight-luxe", "premium"),
            ("06-commerce:B-premium",     "slate-mood",    "premium"),
        ],
    },

    "wide-soft-3": {
        "type": "messages",
        "label": "감성 와이드 3종 (출산 선물/신생아 톤)",
        "size_label": "800×600",
        "variants": [
            ("02-wide-image:A-product",   "blush-touch",   "soft"),
            ("02-wide-image:B-lifestyle", "rose-dawn",     "emotional"),
            ("06-commerce:A-standard",    "warm-spring",   "soft"),
        ],
    },

    # ═══ Carousel Commerce 800×800 — 5세트 (구성 다름) ═══
    "carousel-mix-5": {
        "type": "carousels",
        "label": "캐러셀 5세트 (단일/듀얼/TOP3/옵션/세트)",
        "size_label": "800×800",
        "variants": [
            ("05-carousel-commerce:A-standard", "warm-spring",   "단일 제품 라인업"),
            ("05-carousel-commerce:B-dual",     "rose-dawn",     "2개 비교"),
            ("05-carousel-commerce:C-triple",   "cool-summer",   "TOP 3 추천"),
            ("05-carousel-commerce:D-option",   "coral-sunset",  "옵션 비교 + 쿠폰"),
            ("05-carousel-commerce:E-bundle",   "midnight-luxe", "세트 구성"),
        ],
    },

    "carousel-product-3": {
        "type": "carousels",
        "label": "캐러셀 제품 중심 3종 (단일/듀얼/TOP3)",
        "size_label": "800×800",
        "variants": [
            ("05-carousel-commerce:A-standard", "warm-spring",  "단일 라인업"),
            ("05-carousel-commerce:B-dual",     "cool-summer",  "2개 비교"),
            ("05-carousel-commerce:C-triple",   "rose-dawn",    "TOP 3"),
        ],
    },

    # ═══ Carousel Feed 800×600 — 3종 (스토리텔링) ═══
    "feed-mix-3": {
        "type": "carousels",
        "label": "카루셀 피드 3종 (제품 디테일/라이프스타일/브랜드 스토리)",
        "size_label": "800×600",
        "variants": [
            ("04-carousel-feed:A-product",   "warm-spring",  "제품 디테일"),
            ("04-carousel-feed:B-lifestyle", "rose-dawn",    "라이프스타일"),
            ("04-carousel-feed:C-story",     "moonlit-calm", "브랜드 스토리"),
        ],
    },

    # ═══ Live Carousel 1080×1350 ═══
    "live-carousel": {
        "type": "live_carousel",
        "label": "라이브 캐러셀 (1080×1350, 5카드 라이브 방송 홍보)",
        "size_label": "1080×1350",
        "templates": [
            "04-carousel-feed:D-live-carousel--portable-bed",  # 휴대용+냉감패드 라이브 (듀얼 제품)
            "04-carousel-feed:D-live-carousel--abc-bed",       # ABC 침대 단독 라이브 (세트 중심)
            "04-carousel-feed:D-live-carousel",                # 일반 라이브
        ],
        # Claude가 인터뷰에서 가장 가까운 1개 자동 선택
    },
}


# ─── 톤별 카피 자동 변형 (Claude가 미작성 시 fallback) ─────────────────────
TONE_TRANSFORMS = {
    "informational": {
        # 그대로 사용
        "title_prefix": "",
        "title_suffix": "",
        "desc_template": "{desc}",
    },
    "emotional": {
        "title_prefix": "",  # 사용자 입력 그대로 — 원래 감성 톤 권장
        "desc_template": "{desc}",
        "_hint": "엄마/아기/포근/꿈 같은 단어 활용",
    },
    "urgency": {
        "title_prefix": "",
        "title_suffix": "",
        "desc_template": "오늘만 · {desc}",
        "_hint": "한정/마감 어휘 활용",
    },
    "premium": {
        "title_prefix": "",
        "title_suffix": "",
        "desc_template": "{desc}",
        "_hint": "영문 라벨, 절제된 어휘",
    },
    "soft": {
        "title_prefix": "꿀잠 ",
        "desc_template": "{desc}",
        "_hint": "포근/부드럽/조용히 같은 단어 활용",
    },
}


def list_recipes() -> list[tuple[str, str]]:
    """(name, label) 리스트."""
    return [(k, v["label"]) for k, v in RECIPES.items()]


def get_recipe(name: str) -> dict:
    if name not in RECIPES:
        raise KeyError(f"Unknown recipe '{name}'. Available: {list(RECIPES.keys())}")
    return RECIPES[name]


def expand_recipe(name: str) -> list[tuple[str, str, str]]:
    """레시피 → variants 튜플 리스트. live-carousel은 templates 사용."""
    r = get_recipe(name)
    if r["type"] == "live_carousel":
        return [(t, "cool-summer", "informational") for t in r["templates"]]
    return r["variants"]


def apply_tone_transform(tone: str, base_text: str, slot_key: str = "desc") -> str:
    """톤별 카피 변형 적용 (간단 fallback). Claude가 직접 작성한 카피가 있으면 우선."""
    if tone not in TONE_TRANSFORMS:
        return base_text
    transform = TONE_TRANSFORMS[tone]
    if slot_key == "title":
        prefix = transform.get("title_prefix", "")
        suffix = transform.get("title_suffix", "")
        return f"{prefix}{base_text}{suffix}".strip()
    if slot_key == "desc":
        template = transform.get("desc_template", "{desc}")
        return template.format(desc=base_text)
    return base_text
