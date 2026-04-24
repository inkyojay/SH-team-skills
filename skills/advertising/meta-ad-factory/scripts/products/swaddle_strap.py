"""Swaddle Strap (SUNDAY HUG) — meta ad bulk builder."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from meta_ad_builder import (
    Benefit,
    CopySet,
    ProductConfig,
    build_ads,
)


IMAGES_DIR = Path.home() / "Desktop" / "상세페이지 local (최종본)" / "newborn" / "swaddle-strap" / "images"


CFG = ProductConfig(
    brand="SUNDAY HUG",
    brand_name_ko="썬데이허그",
    product_name="스와들 스트랩",
    product_slug="swaddle-strap",
    category="newborn",
    colors={
        "primary": "#1D9E75",
        "secondary": "#F5F0EB",
        "accent": "#FF6B35",
    },
    # Full image pool (9 images)
    images={
        "hero-main": str(IMAGES_DIR / "hero-main.webp"),
        "lifestyle-01": str(IMAGES_DIR / "lifestyle-01.webp"),
        "lifestyle-02": str(IMAGES_DIR / "lifestyle-02.webp"),
        "velcro-closeup": str(IMAGES_DIR / "point-02-velcro-closeup.webp"),
        "velcro-detail": str(IMAGES_DIR / "point-02-velcro-detail.webp"),
        "tight-fit": str(IMAGES_DIR / "point-01-tight-fit.webp"),
        "overview": str(IMAGES_DIR / "overview.webp"),
        "compare-strap": str(IMAGES_DIR / "compare-swaddle-strap.webp"),
        "made-in-korea": str(IMAGES_DIR / "point-04-made-in-korea.webp"),
    },
    # Explicit tone → image pool mapping (for maximum variety per tone)
    tone_image_pools={
        "emotional": [
            "lifestyle-01",
            "hero-main",
            "lifestyle-02",
            "overview",
            "tight-fit",
        ],
        "informational": [
            "velcro-closeup",
            "tight-fit",
            "velcro-detail",
            "overview",
            "made-in-korea",
            "compare-strap",
        ],
        "urgency": [
            "hero-main",
            "compare-strap",
            "lifestyle-02",
            "velcro-closeup",
            "overview",
            "lifestyle-01",
        ],
    },
    copies={
        "emotional": [
            CopySet(
                tone="emotional",
                headline="소리 없이 지켜주는\n첫 번째 선물",
                subtext="밤새 깨지 않고 푹 자는 아기의 모습,\n무소음 벨크로가 만들어줍니다.",
                cta="지금 만나보기",
            ),
            CopySet(
                tone="emotional",
                headline="포근한 꿀잠을\n선물하세요",
                subtext="에어메쉬로 시원하게,\n타이트 핏으로 안전하게 감싸요.",
                cta="지금 만나보기",
            ),
            CopySet(
                tone="emotional",
                headline="우리 아가 첫 수면,\n썬데이허그와 함께",
                subtext="모로반사로 깨는 신생아를\n부드럽게 감싸는 스와들 스트랩.",
                cta="자세히 보기",
            ),
            CopySet(
                tone="emotional",
                headline="밤잠 잘 자는 아기의 시작",
                subtext="자궁 속 포근함이 그리운 신생아에게\n엄마 품 같은 안정감을 선물하세요.",
                cta="지금 만나보기",
            ),
            CopySet(
                tone="emotional",
                headline="엄마 마음으로 만든\n스와들 스트랩",
                subtext="원단 한 장부터 봉제까지,\n엄마가 안심할 수 있는 품질로.",
                cta="브랜드 스토리",
            ),
        ],
        "informational": [
            CopySet(
                tone="informational",
                headline="무소음 벨크로\n+ 에어메쉬 원단",
                subtext="밤중 기저귀 교체에도\n아기가 깨지 않는 무소음 설계.",
                cta="상세 스펙 확인",
            ),
            CopySet(
                tone="informational",
                headline="100% 국내생산\nKC 인증 완료",
                subtext="원단 선별부터 봉제까지\n직영공장에서 직접 관리합니다.",
                cta="자세히 보기",
                badge="KC 인증",
            ),
            CopySet(
                tone="informational",
                headline="타이트 핏으로\n올라가지 않아요",
                subtext="상체는 안정감 있게,\n하체는 고관절 발달을 위해 자유롭게.",
                cta="핏 구조 보기",
            ),
            CopySet(
                tone="informational",
                headline="에어메쉬 통기성\n태열 걱정 DOWN",
                subtext="특수 개발 에어메쉬가\n체온·습도를 빠르게 조절합니다.",
                cta="원단 상세보기",
                badge="태열 케어",
            ),
            CopySet(
                tone="informational",
                headline="한 손으로 간편한\n벨크로 여닫이",
                subtext="밤중에도 한 손으로 빠르게,\n넉넉한 접착 면적으로 튼튼하게.",
                cta="사용법 보기",
            ),
            CopySet(
                tone="informational",
                headline="FREE 사이즈\n권장 0~3개월",
                subtext="60cm × 30cm · 신생아부터 3개월까지\n뒤집기 시작 전 필수.",
                cta="사이즈 확인",
                badge="FREE",
            ),
        ],
        "urgency": [
            CopySet(
                tone="urgency",
                headline="재구매율 96%\n스와들 스트랩",
                subtext="2,800+ 리뷰가 증명한\n신생아 수면 필수템.",
                cta="지금 구매하기",
                badge="재구매 96%",
            ),
            CopySet(
                tone="urgency",
                headline="신생아 필수템\n놓치지 마세요",
                subtext="출산 전 미리 준비하는\n엄마들의 첫 번째 선택.",
                cta="지금 구매하기",
                badge="BEST",
            ),
            CopySet(
                tone="urgency",
                headline="4.8★ 평점\n신뢰받는 브랜드",
                subtext="엄마 2,800명이 선택한\n썬데이허그 스와들 스트랩.",
                cta="리뷰 확인하기",
                badge="4.8★",
            ),
            CopySet(
                tone="urgency",
                headline="출산 선물 BEST\n지금 준비하세요",
                subtext="예비맘 선물로 1순위.\n받자마자 바로 쓸 수 있어요.",
                cta="선물하기",
                badge="출산선물 1위",
            ),
            CopySet(
                tone="urgency",
                headline="한 번 쓰면 못 버리는\n수면 아이템",
                subtext="밤중 기저귀 교체에도 안 깨는\n무소음의 편안함을 경험하세요.",
                cta="지금 주문",
                badge="HOT",
            ),
            CopySet(
                tone="urgency",
                headline="2,800+ 엄마의 선택\n당신도 함께해요",
                subtext="누적 리뷰 2,800+, 재구매 96%\n검증된 신생아 속싸개.",
                cta="지금 구매하기",
                badge="NEW",
            ),
        ],
    },
    benefits=[
        Benefit(icon="🔇", title="무소음 벨크로", desc="밤중 기저귀 교체도 조용히"),
        Benefit(icon="🌬️", title="에어메쉬 원단", desc="태열 걱정 없는 통기성"),
        Benefit(icon="🤱", title="타이트 핏 설계", desc="올라가지 않는 안정감"),
        Benefit(icon="🇰🇷", title="100% 국내생산", desc="직영공장 품질 관리"),
    ],
    review={
        "text": "무소음 벨크로라 기저귀 갈 때 아기가 안 깨요! 에어메쉬라 땀도 안 차요.",
        "name": "yujin_mom22 · 실제 구매 리뷰",
    },
    price_label="",
)


def main() -> None:
    output_dir = (
        Path.home() / "Desktop" / "team-skills" / "광고카피" / "sundayhug-meta-bulk" / "newborn" / "swaddle-strap"
    )
    specs = build_ads(CFG, output_dir)
    print(f"✓ Generated {len(specs)} creatives")
    print(f"  Output: {output_dir}")
    print(f"  Preview: {output_dir / 'previews' / 'preview-grid.html'}")


if __name__ == "__main__":
    main()
