"""
portable_crib_v3_sample.py — ABC 휴대용 아기침대 v3 캠페인 (시각적 다양성 데모)

v3 신규: 시맨틱 슬롯 + 다양성 레시피 → 같은 입력으로 시각적으로 다른 결과물.

레시피 적용:
- wide-mix-5: 5종 와이드 (풀블리드/라이프/이벤트/커머스/세일) — 5가지 다른 레이아웃
- carousel-mix-5: 5세트 캐러셀 (단일/듀얼/TOP3/옵션/세트)
- live-carousel: 1080×1350 5카드 (휴대용+냉감패드 라이브)

실행:
    cd skills/advertising/kakao-message-factory/scripts
    python3 kakao_factory.py build products/portable_crib_v3_sample.py
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from kakao_factory import CampaignV3, SemanticData, build_campaign_v3  # noqa: E402

# ─── 이미지 경로 ────────────────────────────────────────────────────────────
IMG = Path.home() / "Desktop" / "상세페이지 local (최종본)/sleep-products/portable-crib/images_jpg"


# ─── 시맨틱 데이터 (한 번만 채움 — 모든 템플릿에 자동 매핑) ────────────────
data = SemanticData(
    title="ABC 휴대용 아기침대",
    desc="5초 펴고 접고 · 크림/제이드/베이비핑크",
    badge="BEST",
    category="PORTABLE CRIB",
    discount=35,
    price=119000,
    orig=184000,
    label="PREMIUM",
    tag="BEST DEAL",
    info="휴대용 · 신생아부터",
    brand="SUNDAY HUG",
    sub="크림 · 제이드 · 베이비핑크 3컬러",
    date="2026.04.28(화) — 05.05(화)",

    images={
        "hero": str(IMG / "cream-lifestyle-01.jpg"),
        "product": str(IMG / "cream-product.jpg"),
        # 카루셀 아이템 이미지
        "item1": str(IMG / "cream-product.jpg"),
        "item2": str(IMG / "jade-green-product.jpg"),
        "item3": str(IMG / "baby-pink-product.jpg"),
        # D-live alt 매칭용
        "휴대용 아기침대": str(IMG / "cream-product.jpg"),
        "데일리 크림": str(IMG / "cream-product.jpg"),
        "베이비 핑크": str(IMG / "baby-pink-product.jpg"),
        "제이드그린": str(IMG / "jade-green-product.jpg"),
    },

    # 캐러셀의 카드별/아이템별 데이터 (B-dual은 2개, C-triple은 3개 사용)
    items=[
        {"title": "크림", "desc": "베이지 톤", "price": 119000, "orig": 184000, "discount": 35,
         "image": str(IMG / "cream-product.jpg"), "category": "PORTABLE CRIB"},
        {"title": "제이드", "desc": "그린 톤", "price": 119000, "orig": 184000, "discount": 35,
         "image": str(IMG / "jade-green-product.jpg"), "category": "PORTABLE CRIB"},
        {"title": "베이비핑크", "desc": "핑크 톤", "price": 119000, "orig": 184000, "discount": 35,
         "image": str(IMG / "baby-pink-product.jpg"), "category": "PORTABLE CRIB"},
    ],

    # 톤별 카피 오버라이드 (Claude가 인터뷰에서 작성)
    tone_overrides={
        "emotional": {
            "title": "엄마 옆자리, 우리 아기 잠자리",
            "desc": "5초만에 펼치는 부드러운 휴대용 아기침대",
        },
        "informational": {
            "title": "ABC 휴대용 아기침대",
            "desc": "5초 펴고 접고 · 크림/제이드/베이비핑크 3컬러",
        },
        "urgency": {
            "title": "ABC 침대 35% OFF",
            "desc": "오늘만 이 가격 · 곧 마감",
        },
        "premium": {
            "title": "ABC PORTABLE CRIB",
            "desc": "Premium portable bed for your little one",
        },
        "soft": {
            "title": "꿀잠 휴대용 아기침대",
            "desc": "어디든 함께, 우리 아기의 작은 잠자리",
        },
    },
)


# ─── 캠페인 — 3개 레시피 동시 적용 ──────────────────────────────────────────
CAMPAIGN = CampaignV3(
    brand="sundayhug",
    campaign_slug="portable-crib_v3",
    recipes=[
        "wide-mix-5",       # 5개 다른 레이아웃의 와이드
        "carousel-mix-5",   # 5세트 다른 패턴 캐러셀
        "live-carousel",    # 1080×1350 라이브 5카드
    ],
    data=data,
    live_template_hint="portable-bed",  # D-live-carousel--portable-bed 자동 선택
    live_data={
        "images": data.images,
    },
)


if __name__ == "__main__":
    build_campaign_v3(CAMPAIGN)
