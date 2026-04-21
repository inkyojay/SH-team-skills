"""All SUNDAY HUG products — meta ad bulk configs.

Run: python3 all_products.py [slug ...]
  - no args → build all
  - slug(s)  → build only matching products
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from meta_ad_builder import Benefit, CopySet, ProductConfig, build_ads


# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

BRAND = "SUNDAY HUG"
BRAND_KO = "썬데이허그"
COLORS = {"primary": "#1D9E75", "secondary": "#F5F0EB", "accent": "#FF6B35"}

DESKTOP = Path("/Users/inkyo/Desktop/상세페이지 local (최종본)")
OUTPUT_BASE = Path("/Users/inkyo/Projects/team-skills/output/광고카피/sundayhug-meta-bulk")
CDN = "https://sundayhugkr.cafe24.com/skin-skin69/pdp"


def base(brand=BRAND, ko=BRAND_KO, colors=None):
    return {
        "brand": brand,
        "brand_name_ko": ko,
        "colors": colors or COLORS,
    }


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------


# === 2. Dual Reflux Cushion (newborn, local images) ===========================
DUAL_REFLUX = ProductConfig(
    **base(),
    product_name="듀얼 역류 쿠션",
    product_slug="dual-reflux-cushion",
    category="newborn",
    images={
        "hero-main": str(DESKTOP / "newborn/dual-reflux-cushion/images/hero-main.webp"),
        "lifestyle-01": str(DESKTOP / "newborn/dual-reflux-cushion/images/lifestyle-01.webp"),
        "lifestyle-02": str(DESKTOP / "newborn/dual-reflux-cushion/images/lifestyle-02.webp"),
        "point-01-dual-angle": str(DESKTOP / "newborn/dual-reflux-cushion/images/point-01-dual-angle.webp"),
        "point-02-cover": str(DESKTOP / "newborn/dual-reflux-cushion/images/point-02-cover-replace.webp"),
        "point-03-material": str(DESKTOP / "newborn/dual-reflux-cushion/images/point-03-material.webp"),
        "color-cream": str(DESKTOP / "newborn/dual-reflux-cushion/images/color-cream.webp"),
        "material-cover": str(DESKTOP / "newborn/dual-reflux-cushion/images/material-cover.webp"),
        "all-colors": str(DESKTOP / "newborn/dual-reflux-cushion/images/all-colors.webp"),
    },
    tone_image_pools={
        "emotional": ["lifestyle-01", "lifestyle-02", "hero-main", "color-cream", "all-colors"],
        "informational": ["point-01-dual-angle", "point-02-cover", "point-03-material", "material-cover", "hero-main"],
        "urgency": ["hero-main", "all-colors", "lifestyle-02", "point-01-dual-angle"],
    },
    copies={
        "emotional": [
            CopySet("emotional", "트림 걱정 없는\n편안한 수유 시간", "수유 후 역류로 고생하는 아기를\n편안한 각도로 안정시켜줍니다.", "지금 만나보기"),
            CopySet("emotional", "우리 아가\n편하게 쉬어요", "신생아 자세를 배려한 듀얼 각도,\n쌔근쌔근 꿀잠을 선물하세요.", "지금 만나보기"),
            CopySet("emotional", "엄마의 안심,\n아기의 편안함", "커버 분리 세탁까지 꼼꼼하게.\n위생과 편안함 모두 챙겼어요.", "자세히 보기"),
            CopySet("emotional", "토하는 아기에게\n꼭 필요한 한 가지", "수유 후 30도 각도가\n역류 걱정을 덜어줍니다.", "브랜드 스토리"),
        ],
        "informational": [
            CopySet("informational", "특허 듀얼 각도\n역류 방지 설계", "0~3개월 30도, 3개월+ 15도\n발달 단계별 맞춤 각도.", "각도 상세보기", badge="특허"),
            CopySet("informational", "커버 분리형\n세탁 편한 위생", "아기가 토해도 커버만 벗겨\n세탁기에 바로 돌릴 수 있어요.", "사용법 보기"),
            CopySet("informational", "100% 국내산\n구슬솜 충전재", "60수 고밀도 원단 + 구슬솜\n국내 직영공장 자체 생산.", "원단 상세보기", badge="Made in Korea"),
            CopySet("informational", "KC 인증 완료\n안심 소재", "무형광 원단, KC 안전기준\n피부에 닿는 모든 부분 안심.", "인증 확인", badge="KC 인증"),
            CopySet("informational", "5가지 컬러\n우리 아가 방에 딱", "데일리 크림·베이비 핑크·\n어반 그레이·올리브·어스브라운.", "컬러 보기"),
        ],
        "urgency": [
            CopySet("urgency", "재구매율 96%\n역류쿠션 BEST", "2,800+ 엄마들의 선택.\n신생아 수유템 1순위.", "지금 구매하기", badge="재구매 96%"),
            CopySet("urgency", "4.8★\n검증된 신뢰", "신생아 수유템 누적 리뷰 2,800+.\n평점 4.8의 베스트셀러.", "리뷰 확인하기", badge="4.8★"),
            CopySet("urgency", "출산 선물 1위\n지금 준비하세요", "예비맘에게 인기 선물.\n받자마자 바로 쓸 수 있어요.", "선물하기", badge="출산선물 1위"),
            CopySet("urgency", "신생아 필수템\n토함·역류 걱정 끝", "수유 후 세우지 않아도 OK\n듀얼 각도가 해결합니다.", "지금 주문", badge="HOT"),
            CopySet("urgency", "한정 컬러\n빠르게 준비하세요", "시즌 인기 컬러는 조기 품절.\n원하는 컬러로 지금 바로.", "지금 구매", badge="HURRY"),
        ],
    },
    benefits=[
        Benefit("🎯", "듀얼 각도 설계", "수유 후 역류 방지"),
        Benefit("🧺", "커버 분리 세탁", "위생적이고 편리"),
        Benefit("🇰🇷", "100% 국내생산", "원단부터 충전까지"),
        Benefit("✅", "KC 인증 완료", "무형광 안심 소재"),
    ],
    review={"text": "역류로 힘들어하던 아기가 편해졌어요. 커버가 분리돼서 세탁도 편하고 국내산이라 안심됩니다.", "name": "재구매맘 · 실제 구매 리뷰"},
)


# === 3-5. Sleepsack series (local + CDN fallback) =============================
def _sleepsack_images_local(variant: str) -> dict:
    """sleepsack/{silky-bamboo|cotton-mesh|triple-bamboo}/images/*.webp

    Each variant has its own file naming convention, so map explicitly.
    """
    d = DESKTOP / f"sleeping-bags/sleepsack/{variant}/images"
    if variant == "silky-bamboo":
        return {
            "hero-01": str(d / "hero-01.webp"),
            "lifestyle-01": str(d / "lifestyle-01.webp"),
            "lifestyle-02": str(d / "lifestyle-02.webp"),
            "fabric": str(d / "fabric-01-silky-bamboo.webp"),
            "color-01": str(d / "color-01-white-cream-copy.webp"),
            "color-02": str(d / "color-02-oat-beige-copy.webp"),
            "brand-story": str(d / "brand-01-story.webp"),
            "intro-01": str(d / "intro-01.webp"),
            "compare-01": str(d / "compare-01-swaddle.webp"),
            "compare-02": str(d / "compare-02-sleeping-bag.webp"),
        }
    if variant == "cotton-mesh":
        return {
            "hero-main": str(d / "hero-main.webp"),
            "lifestyle-02": str(d / "lifestyle-02.webp"),
            "lifestyle-03": str(d / "lifestyle-03.webp"),
            "lifestyle-04": str(d / "lifestyle-04.webp"),
            "fabric": str(d / "fabric-cotton-mesh.webp"),
            "color-01": str(d / "color-01-oat-cream.webp"),
            "color-02": str(d / "color-02-daily-cream.webp"),
            "intro-01": str(d / "intro-01.webp"),
            "overview": str(d / "overview-fabric-properties.webp"),
            "point-01-turn": str(d / "point-01-turn.webp"),
            "compare-swaddle": str(d / "compare-swaddle.webp"),
        }
    if variant == "triple-bamboo":
        return {
            "hero-main": str(d / "hero-main.webp"),
            "lifestyle-01": str(d / "lifestyle-01.webp"),
            "lifestyle-02": str(d / "lifestyle-02.webp"),
            "lifestyle-03": str(d / "lifestyle-03.webp"),
            "fabric": str(d / "fabric-triple-bamboo.webp"),
            "color-01": str(d / "color-01.webp"),
            "color-02": str(d / "color-02.webp"),
            "brand-story": str(d / "brand-story.webp"),
            "overview-01": str(d / "overview-01.webp"),
            "point-01-turn": str(d / "point-01-turn.webp"),
            "point-03-warmth": str(d / "point-03-warmth.webp"),
        }
    return {}


SLEEPSACK_SILKY_BAMBOO = ProductConfig(
    **base(),
    product_name="슬립색 실키밤부",
    product_slug="sleepsack-silky-bamboo",
    category="sleeping-bags",
    images=_sleepsack_images_local("silky-bamboo"),
    # tone pools auto-inferred from image keys
    copies={
        "emotional": [
            CopySet("emotional", "실크처럼 부드러운\n우리 아가 꿀잠", "밤부 100% 원단이 선사하는\n실크 같은 감촉을 경험하세요.", "지금 만나보기"),
            CopySet("emotional", "뒤집기 이후에도\n안심 수면", "이불 걷어차는 우리 아이,\n입는 이불로 밤새 따뜻하게.", "지금 만나보기"),
            CopySet("emotional", "아기와 엄마 모두\n편안한 밤", "포근한 밤부의 감촉이\n통잠을 선물합니다.", "자세히 보기"),
            CopySet("emotional", "사계절 내내\n함께하는 슬립색", "봄·가을·여름까지\n한 벌로 두루 입히세요.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "100% 밤부 레이온\n무형광 안심 소재", "민감한 아기 피부도 안심.\n실크같이 부드러운 촉감.", "원단 상세보기"),
            CopySet("informational", "양방향 투웨이 지퍼\n기저귀 교체 간편", "위·아래 양방향 지퍼로\n밤중에도 빠르게 갈아줘요.", "사용법 보기", badge="Two-Way"),
            CopySet("informational", "팔 자유도 높은\n슬리브리스 설계", "양팔이 자유로워\n뒤집기 이후에도 안전합니다.", "핏 상세"),
            CopySet("informational", "S/M/L 3단계\n6가지 컬러", "70cm·90cm·110cm\n성장 단계별 선택 가능.", "사이즈 확인", badge="3 Size"),
            CopySet("informational", "KC 인증 완료\n100% 국내생산", "봉제부터 검수까지\n직영공장에서 직접.", "품질 보기", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "재구매율 98%\n슬립색 BEST", "누적 리뷰 2,800+\n4.9★ 신뢰받는 베스트셀러.", "지금 구매하기", badge="재구매 98%"),
            CopySet("urgency", "4.9★\n엄마들의 선택", "2,800명+ 엄마가 검증한\n최고의 슬립색.", "리뷰 확인하기", badge="4.9★"),
            CopySet("urgency", "출산 선물 BEST", "예비맘 선물 1순위.\n바로 쓸 수 있는 슬립색.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러\n품절 임박", "인기 컬러는 빠르게 소진.\n원하는 컬러로 지금 바로.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "신생아 수면 필수템", "뒤집기 시작한 우리 아이,\n슬립색으로 안전하게.", "지금 주문", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("🎋", "밤부 100%", "실크 같은 부드러움"),
        Benefit("🤲", "팔 자유", "뒤집기 후에도 안전"),
        Benefit("🔐", "양방향 지퍼", "기저귀 교체 편리"),
        Benefit("🇰🇷", "국내생산", "직영공장 품질관리"),
    ],
    review={"text": "밤부 소재가 정말 부드럽고 쾌적합니다. 양방향 지퍼가 정말 편리해요.", "name": "4.9★ 실제 구매 리뷰"},
)


SLEEPSACK_COTTON_MESH = ProductConfig(
    **base(),
    product_name="슬립색 코튼메쉬",
    product_slug="sleepsack-cotton-mesh",
    category="sleeping-bags",
    images=_sleepsack_images_local("cotton-mesh"),
    # tone pools auto-inferred from image keys
    copies={
        "emotional": [
            CopySet("emotional", "뜨거운 여름밤도\n시원한 꿀잠", "열 많은 우리 아기를 위한\n메쉬 원단의 시원함.", "지금 만나보기"),
            CopySet("emotional", "땀 걱정 없이\n푹 자는 아기", "통풍 좋은 메쉬 슬립색이\n쾌적한 수면을 도와줍니다.", "지금 만나보기"),
            CopySet("emotional", "무더위에도\n이불은 필요해요", "여름밤 냉방병 걱정,\n얇은 메쉬 슬립색으로.", "자세히 보기"),
            CopySet("emotional", "엄마도 아기도\n편안한 열대야", "통기성 좋은 면 100%가\n여름을 가볍게 해줍니다.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "코튼 100% 메쉬\n탁월한 통기성", "일반 원단 대비 3배 통기.\n땀을 빠르게 발산합니다.", "원단 상세보기", badge="통기성 3배"),
            CopySet("informational", "무형광 면 소재\n피부 자극 DOWN", "KC 인증 완료\n민감한 피부도 안심.", "인증 확인", badge="KC 인증"),
            CopySet("informational", "양방향 투웨이 지퍼", "밤중에도 빠르게\n기저귀를 갈 수 있어요.", "사용법 보기"),
            CopySet("informational", "S/M/L 3단계\n6가지 컬러", "70·90·110cm\n신생아부터 영유아까지.", "사이즈 확인"),
            CopySet("informational", "여름·환절기 최적\n26~28도에 딱", "무더위 실내에서도\n쾌적하게 입힐 수 있어요.", "활용 TIP"),
        ],
        "urgency": [
            CopySet("urgency", "여름 필수템\n슬립색 BEST", "열 많은 아기에게 1순위.\n재구매 98% 베스트셀러.", "지금 구매하기", badge="여름 BEST"),
            CopySet("urgency", "4.9★\n2,800+ 리뷰", "통기성 좋다는 엄마들의\n생생한 후기 확인하세요.", "리뷰 확인하기", badge="4.9★"),
            CopySet("urgency", "한정 컬러\n품절 임박", "시즌 한정 사파리 컬러\n인기 빠르게 소진 중.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "여름 선물 BEST", "출산·백일 선물로 인기.\n여름 준비 완료.", "선물하기", badge="BEST"),
            CopySet("urgency", "신생아 땀띠 걱정 끝", "통기성으로 해결하는\n여름 수면 필수템.", "지금 주문", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("🌬️", "통기성 3배", "땀·열 빠르게 발산"),
        Benefit("🌿", "면 100%", "무형광 피부 안심"),
        Benefit("🔐", "양방향 지퍼", "기저귀 교체 편리"),
        Benefit("❄️", "여름 최적", "26~28도 쾌적"),
    ],
    review={"text": "여름에 정말 시원하고 쾌적합니다. 열 많은 우리 아기가 이제 편해졌어요.", "name": "4.9★ 실제 구매 리뷰"},
)


SLEEPSACK_TRIPLE_BAMBOO = ProductConfig(
    **base(),
    product_name="슬립색 트리플밤부",
    product_slug="sleepsack-triple-bamboo",
    category="sleeping-bags",
    images=_sleepsack_images_local("triple-bamboo"),
    # tone pools auto-inferred from image keys
    copies={
        "emotional": [
            CopySet("emotional", "포근한 겨울밤\n우리 아가 꿀잠", "3중 구조 보온으로\n추위 걱정 없는 꿀잠.", "지금 만나보기"),
            CopySet("emotional", "따뜻한 감싸기,\n안심의 무게감", "3겹 밤부가 선사하는\n엄마 품 같은 포근함.", "지금 만나보기"),
            CopySet("emotional", "이불 걷어차도\n걱정 없어요", "입는 이불이니까\n밤새 따뜻하게 감싸줘요.", "자세히 보기"),
            CopySet("emotional", "환절기부터 겨울까지\n한 벌로 충분", "가을·겨울·봄 환절기\n안정적인 체온 유지.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "밤부 3중 구조\n최고의 보온성", "3겹 밤부 레이온으로\n따뜻함을 안정적으로.", "원단 상세보기", badge="3중 구조"),
            CopySet("informational", "무형광 밤부 100%\n민감 피부 안심", "KC 인증 완료\n피부에 닿는 모든 부분 안전.", "인증 확인", badge="KC 인증"),
            CopySet("informational", "양방향 투웨이 지퍼", "밤중에도 빠르게\n기저귀를 갈 수 있어요.", "사용법 보기"),
            CopySet("informational", "S/M/L 3단계", "70·90·110cm\n성장 단계별 선택.", "사이즈 확인"),
            CopySet("informational", "겨울·환절기 최적\n20~24도 딱 좋아요", "추운 계절에도 안심.\n이불 없이도 따뜻함 유지.", "활용 TIP"),
        ],
        "urgency": [
            CopySet("urgency", "겨울 필수템\n슬립색 BEST", "추위 타는 아기에게\n재구매 98% 베스트셀러.", "지금 구매하기", badge="겨울 BEST"),
            CopySet("urgency", "4.9★\n2,800+ 리뷰", "따뜻하고 품질 좋다는\n엄마들의 후기 확인하세요.", "리뷰 확인하기", badge="4.9★"),
            CopySet("urgency", "겨울 선물 BEST", "출산·백일 선물로 인기.\n3중 구조 프리미엄.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러\n품절 임박", "시즌 인기 컬러\n빠르게 소진 중.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "이불 걷어참 걱정 끝", "입는 이불로 해결하는\n겨울 수면 필수템.", "지금 주문", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("🔥", "3중 구조", "보온력 극대화"),
        Benefit("🎋", "밤부 100%", "부드럽고 안심"),
        Benefit("🔐", "양방향 지퍼", "기저귀 교체 편리"),
        Benefit("❄️", "겨울 최적", "20~24도 쾌적"),
    ],
    review={"text": "3중 구조라 정말 따뜻합니다. 겨울에 아기가 편안해보여요.", "name": "4.9★ 실제 구매 리뷰"},
)


# === 6-7. 슬리핑백 구버전 (v1) — 한글 폴더 ====================================
# 단일 config로 묶어서 처리 (메쉬 1종 + 실키/트리플 통합 1종)
def _sleepbag_v1_images(variant: str) -> dict:
    """슬리핑백/{메쉬|실키밤부|트리플밤부}/image/*.webp — 이미지가 많아서 hero/lifestyle 몇 개만 선별"""
    d = DESKTOP / f"sleeping-bags/슬리핑백/{variant}/image"
    # 공통 파일명 가정 (보통 hero, lifestyle 같은 이름 존재)
    candidates = ["hero-main.webp", "hero-01.webp", "lifestyle-01.webp", "lifestyle-02.webp",
                  "point-01.webp", "point-02.webp", "fabric.webp", "overview.webp",
                  "compare.webp", "size-guide.webp"]
    images = {}
    if d.exists():
        available = {f.name for f in d.glob("*.webp")}
        for c in candidates:
            if c in available:
                images[c.replace(".webp", "").replace("-", "_")] = str(d / c)
        # fallback: first 8 webp files
        if not images:
            for i, f in enumerate(sorted(d.glob("*.webp"))[:8]):
                images[f"img_{i}"] = str(f)
    return images


SLEEPBAG_V1_MESH = ProductConfig(
    **base(),
    product_name="슬리핑백 메쉬 (구버전)",
    product_slug="sleepbag-v1-mesh",
    category="sleeping-bags",
    images=_sleepbag_v1_images("메쉬"),
    copies={
        "emotional": [
            CopySet("emotional", "여름 밤을 시원하게\n우리 아가 꿀잠", "메쉬 원단 슬리핑백으로\n땀 걱정 없이 편안하게.", "지금 만나보기"),
            CopySet("emotional", "땀띠 걱정 없는\n포근한 수면", "통기성 좋은 메쉬가\n쾌적한 잠을 선물합니다.", "자세히 보기"),
            CopySet("emotional", "엄마도 안심\n아기도 편안", "입는 이불로\n밤새 잘 자는 아기.", "자세히 보기"),
            CopySet("emotional", "한여름도\n편안한 잠자리", "에어컨 실내에서도\n알맞은 온도 유지.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "메쉬 원단\n탁월한 통기성", "뛰어난 통풍으로\n열·땀을 빠르게 발산.", "원단 상세보기"),
            CopySet("informational", "무형광 소재\nKC 인증 완료", "피부에 닿는 모든 부분\n안전성을 검증했습니다.", "인증 확인", badge="KC 인증"),
            CopySet("informational", "양방향 지퍼\n기저귀 교체 편리", "밤중에도 빠르게\n간편한 갈아입힘.", "사용법 보기"),
            CopySet("informational", "다양한 사이즈\n성장 맞춤", "S·M·L 단계별 선택\n우리 아가에 딱.", "사이즈 확인"),
            CopySet("informational", "100% 국내생산\n직영공장 품질", "원단부터 봉제까지\n직접 관리합니다.", "품질 보기", badge="Made in Korea"),
        ],
        "urgency": [
            CopySet("urgency", "여름 필수템\n서둘러요", "여름 성수기\n빠르게 품절 중.", "지금 구매하기", badge="여름 BEST"),
            CopySet("urgency", "검증된 베스트셀러", "엄마들의 선택으로\n꾸준히 사랑받는 제품.", "리뷰 확인하기", badge="4.8★"),
            CopySet("urgency", "출산 선물 BEST", "여름 출산 선물 1순위.\n받자마자 바로 쓰세요.", "선물하기", badge="BEST"),
            CopySet("urgency", "가격 혜택 중", "시즌 프로모션.\n놓치지 마세요.", "지금 구매", badge="SALE"),
            CopySet("urgency", "HOT 아이템", "시원한 수면 솔루션\n지금 준비하세요.", "지금 주문", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("🌬️", "메쉬 통기성", "땀 걱정 DOWN"),
        Benefit("🌿", "무형광 소재", "KC 인증 안심"),
        Benefit("🔐", "양방향 지퍼", "교체 편리"),
        Benefit("🇰🇷", "국내생산", "직영공장 품질"),
    ],
    review={"text": "여름에 진짜 시원해요. 땀띠 걱정 없어졌어요.", "name": "4.8★ 엄마 리뷰"},
)


SLEEPBAG_V1_BAMBOO = ProductConfig(
    **base(),
    product_name="슬리핑백 실키밤부 (구버전)",
    product_slug="sleepbag-v1-bamboo",
    category="sleeping-bags",
    images={
        **_sleepbag_v1_images("실키밤부"),
        **{"triple_" + k: v for k, v in _sleepbag_v1_images("트리플밤부").items()},
    },
    copies={
        "emotional": [
            CopySet("emotional", "실크처럼 부드러운\n우리 아가 꿀잠", "밤부 원단 슬리핑백으로\n포근한 밤을 선물하세요.", "지금 만나보기"),
            CopySet("emotional", "환절기부터 겨울까지\n한 벌로 충분", "3중 구조 트리플밤부로\n따뜻함을 안정적으로.", "자세히 보기"),
            CopySet("emotional", "엄마와 아기 모두\n편안한 수면", "입는 이불로 이불 걷어참 걱정 끝.\n밤새 따뜻하게.", "자세히 보기"),
            CopySet("emotional", "밤부의 부드러운 감촉", "민감한 피부에도\n부담 없는 실크 같은 촉감.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "밤부 100%\n무형광 안심 소재", "민감 피부에도\n실크 같은 부드러움.", "원단 상세보기"),
            CopySet("informational", "3중 구조 보온\n환절기·겨울 최적", "겹겹이 감싸는 따뜻함\n20~24도에 딱.", "원단 상세보기", badge="3중 구조"),
            CopySet("informational", "양방향 지퍼\n기저귀 교체 편리", "밤중에도 빠르게\n간편한 갈아입힘.", "사용법 보기"),
            CopySet("informational", "다양한 사이즈", "S·M·L 단계별 선택\n성장 맞춤.", "사이즈 확인"),
            CopySet("informational", "KC 인증 완료\n국내 자체 생산", "직영공장에서 직접 관리\n품질 보증.", "품질 보기", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "겨울 필수템", "추위 타는 아기에게\n3중 구조가 딱.", "지금 구매하기", badge="겨울 BEST"),
            CopySet("urgency", "검증된 베스트셀러", "엄마들의 선택으로\n꾸준히 사랑받는 제품.", "리뷰 확인하기", badge="4.8★"),
            CopySet("urgency", "겨울 선물 BEST", "출산·백일 선물 1순위.\n따뜻한 마음을 담아.", "선물하기", badge="BEST"),
            CopySet("urgency", "시즌 한정", "인기 컬러 빠르게 소진.\n지금 준비하세요.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "HOT 아이템", "따뜻한 수면 솔루션\n검증된 품질.", "지금 주문", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("🎋", "밤부 100%", "실크 같은 부드러움"),
        Benefit("🔥", "3중 구조", "보온력 극대화"),
        Benefit("🔐", "양방향 지퍼", "교체 편리"),
        Benefit("✅", "KC 인증", "국내생산 안심"),
    ],
    review={"text": "실키밤부 정말 부드러워요. 트리플밤부는 겨울용으로 딱이에요.", "name": "4.8★ 엄마 리뷰"},
)


# === 8. Butterfly Swaddle Cotton Mesh (newborn, CDN) ==========================
def _bfly_mesh_cdn() -> dict:
    b = f"{CDN}/newborn/butterfly-swaddle/cotton-mesh/image"
    return {
        "hero-main": f"{b}/hero-main.webp",
        "lifestyle-01": f"{b}/lifestyle-mesh-01.webp",
        "lifestyle-02": f"{b}/lifestyle-mesh-02.webp",
        "overview": f"{b}/overview-mesh.webp",
        "point-01": f"{b}/point-01.webp",
        "fabric-cotton-mesh": f"{b}/fabric-02-cotton-mesh.webp",
        "two-way-zipper": f"{b}/two-way-zipper.webp",
        "m-shape-leg": f"{b}/m-shape-leg-design.webp",
        "kc-cert": f"{b}/kc-certified-product.webp",
    }


BUTTERFLY_SWADDLE_MESH = ProductConfig(
    **base(),
    product_name="버터플라이 스와들 코튼메쉬",
    product_slug="butterfly-swaddle-cotton-mesh",
    category="newborn",
    images=_bfly_mesh_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "나비잠 자세로\n깊은 꿀잠", "엄마 뱃속 자세 그대로\n안정감을 선물하세요.", "지금 만나보기"),
            CopySet("emotional", "열 많은 우리 아가\n시원한 수면", "코튼메쉬가 만드는\n땀 걱정 없는 포근함.", "지금 만나보기"),
            CopySet("emotional", "4시간 통잠\n시작은 스와들", "모로반사 완화로\n깊은 수면을 유도합니다.", "자세히 보기"),
            CopySet("emotional", "엄마 마음으로\n만든 스와들", "원단부터 봉제까지\n엄마가 안심할 수 있는 품질.", "브랜드 스토리"),
        ],
        "informational": [
            CopySet("informational", "코튼메쉬 원단\n통기성 극대화", "여름에도 쾌적한 수면.\n열 배출 극대화.", "원단 상세보기", badge="여름 최적"),
            CopySet("informational", "나비잠 W자 설계", "양팔이 자연스럽게 위로,\n엄마 뱃속 자세 재현.", "핏 상세"),
            CopySet("informational", "투웨이 지퍼", "기저귀 교체 시\n속싸개 벗김 없이 간편.", "사용법 보기"),
            CopySet("informational", "M자 다리 설계", "고관절 건강한 발달\n안정적 자세 유도.", "핏 상세"),
            CopySet("informational", "KC 인증 완료", "원단·지퍼·봉제 모두\n안전성 검증.", "인증 확인", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "4.9★\n신생아 BEST", "누적 리뷰 3,200+\n재구매 97% 검증.", "지금 구매하기", badge="4.9★"),
            CopySet("urgency", "여름 필수템\n서둘러요", "통기성 좋은 메쉬\n여름 출산 맘 1순위.", "지금 구매", badge="여름 BEST"),
            CopySet("urgency", "출산 선물 BEST", "예비맘 선물로 인기.\n받자마자 바로 사용.", "선물하기", badge="BEST"),
            CopySet("urgency", "모로반사로 깨는 아기", "연속 4시간+ 숙면\n엄마 후기 3,200+.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "한정 컬러\n품절 임박", "시즌 인기 컬러\n빠르게 소진 중.", "지금 구매", badge="HURRY"),
        ],
    },
    benefits=[
        Benefit("🌬️", "코튼메쉬", "여름 통기성 극대화"),
        Benefit("🦋", "나비잠 W자", "엄마 뱃속 재현"),
        Benefit("🔐", "투웨이 지퍼", "기저귀 교체 편리"),
        Benefit("🦵", "M자 다리", "고관절 발달 배려"),
    ],
    review={"text": "모로반사로 깨던 아기가 4시간 이상 연속으로 자요! 통기성도 최고예요.", "name": "4.9★ 실제 구매 리뷰"},
)


# === 9. Butterfly Swaddle Silky Bamboo (newborn, CDN) =========================
def _bfly_bamboo_cdn() -> dict:
    b = f"{CDN}/newborn/butterfly-swaddle/silky-bamboo/image"
    return {
        "hero-main": f"{b}/hero-main-bamboo.webp",
        "lifestyle-01": f"{b}/lifestyle-bamboo-01.webp",
        "lifestyle-02": f"{b}/lifestyle-bamboo-02.webp",
        "overview": f"{b}/overview-bamboo.webp",
        "point-01": f"{b}/point-01.webp",
        "two-way-zipper": f"{b}/two-way-zipper.webp",
        "point-05": f"{b}/point-05.webp",
        "color-white": f"{b}/color-01-white-cream-silky-bamboo.webp",
        "color-lavender": f"{b}/color-05-bloom-lavender-silky-bamboo.webp",
        "size": f"{b}/size-01.webp",
    }


BUTTERFLY_SWADDLE_BAMBOO = ProductConfig(
    **base(),
    product_name="버터플라이 스와들 실키밤부",
    product_slug="butterfly-swaddle-silky-bamboo",
    category="newborn",
    images=_bfly_bamboo_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "실크처럼 부드러운\n나비잠 스와들", "민감한 피부에도\n실크 같은 감촉.", "지금 만나보기"),
            CopySet("emotional", "사계절 내내\n함께하는 스와들", "여름엔 시원, 겨울엔 포근.\n한 벌로 충분해요.", "자세히 보기"),
            CopySet("emotional", "모로반사 걱정 끝", "깊은 수면으로 가는\n첫 번째 선물.", "자세히 보기"),
            CopySet("emotional", "엄마 마음으로 만든\n프리미엄 스와들", "원단부터 봉제까지\n국내 직영공장에서.", "브랜드 스토리"),
        ],
        "informational": [
            CopySet("informational", "실키 밤부 원단\n항균·탈취", "민감 피부도 안심.\n실크 같은 부드러움.", "원단 상세보기"),
            CopySet("informational", "사계절 활용", "밤부 특성상\n여름·겨울 모두 OK.", "원단 상세보기", badge="사계절"),
            CopySet("informational", "나비잠 W자 설계", "양팔이 자연스럽게 위로,\n엄마 뱃속 자세 재현.", "핏 상세"),
            CopySet("informational", "투웨이 지퍼", "기저귀 교체 편리\n속싸개 벗김 없이.", "사용법 보기"),
            CopySet("informational", "KC 인증 완료", "원단·지퍼·봉제 모두\n안전성 검증.", "인증 확인", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "4.9★\n누적 리뷰 3,200+", "재구매 97% 베스트셀러.\n엄마들의 1순위.", "지금 구매하기", badge="4.9★"),
            CopySet("urgency", "민감 피부 아기 필수템", "실키 밤부 촉감.\n알레르기 걱정 끝.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "출산 선물 BEST", "예비맘 선물로 인기.\n프리미엄 소재.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러\n품절 임박", "블룸 라벤더 등\n시즌 인기 컬러.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "사계절 한 벌로 OK", "여름·겨울 구분 없이\n밤부의 만능 솔루션.", "지금 주문", badge="NEW"),
        ],
    },
    benefits=[
        Benefit("🎋", "실키 밤부", "실크 같은 부드러움"),
        Benefit("🌡️", "사계절 활용", "여름·겨울 OK"),
        Benefit("🦋", "나비잠 W자", "엄마 뱃속 재현"),
        Benefit("✅", "KC 인증", "민감 피부 안심"),
    ],
    review={"text": "실키 밤부 원단이 정말 부드러워요. 아기 피부에 자극이 없어요!", "name": "4.9★ 민감피부 아가맘"},
)


# === 10. Swaddle Pocket (newborn, CDN) ========================================
def _swaddle_pocket_cdn() -> dict:
    b = f"{CDN}/newborn/swaddle-pocket/images"
    return {
        "hero-main": f"{b}/hero-main.webp",
        "lifestyle-01": f"{b}/lifestyle-01.webp",
        "lifestyle-02": f"{b}/lifestyle-02.webp",
        "product-photo-01": f"{b}/product-photo-01.webp",
        "why-you-need": f"{b}/why-you-need.webp",
        "point-02": f"{b}/point-02.webp",
        "point-03": f"{b}/point-03.webp",
        "fabric-closeup": f"{b}/fabric-closeup.webp",
        "trust-korea": f"{b}/trust-point-made-in-korea.webp",
        "product-size": f"{b}/product-size.webp",
    }


SWADDLE_POCKET = ProductConfig(
    **base(),
    product_name="스와들 포켓",
    product_slug="swaddle-pocket",
    category="newborn",
    images=_swaddle_pocket_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "입히기만 해도\n포근한 자궁 속", "복잡한 속싸개 접기 필요 없이\n옷처럼 간단하게.", "지금 만나보기"),
            CopySet("emotional", "출생 직후 ~ 50일\n첫 속싸개", "가장 포근한 신생아 입문.\n엄마도 초보도 쉬워요.", "자세히 보기"),
            CopySet("emotional", "무자극 · 무소음\n완벽한 수면 환경", "지퍼·벨크로 없이\n원단과 봉제만으로.", "자세히 보기"),
            CopySet("emotional", "조리원에서도 칭찬", "조리원 선생님들이\n추천하는 첫 스와들.", "브랜드 스토리"),
        ],
        "informational": [
            CopySet("informational", "지퍼·벨크로 ZERO\n완벽 무자극", "원단과 봉제만으로 만든\n신생아 전용 속싸개.", "상세 보기"),
            CopySet("informational", "옷처럼 간단 착용", "복잡한 싸기 불필요.\n한 번에 입히기만.", "사용법 보기", badge="초보 맘 OK"),
            CopySet("informational", "폴리 60 + 레이온 33 + 엘라스틴 7", "신축성 좋은 3중 블렌드.\n아기 체형에 딱 맞게.", "원단 상세"),
            CopySet("informational", "출생 직후 ~ 50일 전용", "나비잠 스와들로\n자연스럽게 연결.", "활용 TIP"),
            CopySet("informational", "KC 인증 완료\n국내생산", "무형광 원단\n직영공장 품질관리.", "품질 보기", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "출산 직후 필수템", "조리원 입소 전\n꼭 준비하세요.", "지금 구매하기", badge="필수템"),
            CopySet("urgency", "예비맘 선물 BEST", "초보 엄마에게\n가장 도움되는 선물.", "선물하기", badge="BEST"),
            CopySet("urgency", "50일 딱 맞는\n첫 스와들", "너무 어려서 일반 스와들\n못 하는 시기에 딱.", "지금 주문", badge="NEW"),
            CopySet("urgency", "한정 수량", "국내 직영 생산\n시즌 재고 한정.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "모로반사 걱정 끝", "입히자마자 안정되는\n신생아 수면.", "리뷰 확인", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("🤍", "무자극 설계", "지퍼·벨크로 ZERO"),
        Benefit("👕", "옷처럼 간단", "복잡한 싸기 불필요"),
        Benefit("🍼", "~50일 전용", "초신생아 맞춤"),
        Benefit("🇰🇷", "국내생산", "무형광 안심"),
    ],
    review={"text": "조리원에서 추천받아 샀는데 진짜 편해요. 옷처럼 입히기만 하면 돼서 초보 엄마도 쉬워요.", "name": "신생아맘 · 실제 구매 리뷰"},
)


# === 11. Cooling Mesh Dual Pad (sleep-products, CDN) ==========================
def _cooling_cdn() -> dict:
    b = f"{CDN}/sleep-products/cooling-pad/images"
    return {
        "hero-main": f"{b}/hero-main.webp",
        "lifestyle-01": f"{b}/lifestyle-01.webp",
        "lifestyle-02": f"{b}/lifestyle-02.webp",
        "all-colors": f"{b}/color-all.webp",
        "checkpoint": f"{b}/checkpoint.webp",
        "dual-pad": f"{b}/dual-pad.webp",
        "point-01": f"{b}/point-01-main.webp",
        "point-02": f"{b}/point-02-main.webp",
        "size-compare": f"{b}/size-compare.webp",
        "crib-compatible": f"{b}/crib-compatible.webp",
    }


COOLING_PAD = ProductConfig(
    **base(),
    product_name="쿨링메쉬 듀얼 패드",
    product_slug="cooling-mesh-dual-pad",
    category="sleep-products",
    images=_cooling_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "땀 안 차는\n시원한 잠자리", "듀라론 냉감사로\n접촉 순간 시원함.", "지금 만나보기"),
            CopySet("emotional", "열대야도\n포근한 꿀잠", "열 많은 우리 아가\n시원하게 재워주세요.", "자세히 보기"),
            CopySet("emotional", "잠자리 환경의 변화", "아기가 쾌적하면\n엄마도 편해요.", "자세히 보기"),
            CopySet("emotional", "여름 외출에도\n꼭 필요", "유모차·카시트에도\n시원한 쿨링매트.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "듀라론 냉감사\n영구 냉감", "세탁 후에도 유지되는\n지속적 냉감 효과.", "원단 상세보기", badge="영구 냉감"),
            CopySet("informational", "3D 에어메쉬\n양면 사용", "한 면 냉감 + 한 면 메쉬\n상황에 맞게 뒤집어.", "사용법 보기", badge="양면 사용"),
            CopySet("informational", "빠른 건조\n세탁기 OK", "세탁 후 빠르게 건조.\n관리 간편.", "관리법"),
            CopySet("informational", "S·L 2가지 사이즈", "100×70cm / 100×150cm\n침대·크립·유모차 OK.", "사이즈 확인"),
            CopySet("informational", "국내 자체 생산", "원단부터 재단까지\n직영공장 관리.", "품질 보기", badge="Made in Korea"),
        ],
        "urgency": [
            CopySet("urgency", "여름 필수템\nNEW", "신제품 쿨링 솔루션.\n올여름 꼭 준비하세요.", "지금 구매하기", badge="NEW"),
            CopySet("urgency", "열대야 대비 BEST", "에어컨만으론 부족한\n직접 접촉 쿨링.", "지금 구매", badge="여름 BEST"),
            CopySet("urgency", "한정 수량", "시즌 초기 수량 한정.\n빠르게 준비하세요.", "지금 주문", badge="HURRY"),
            CopySet("urgency", "선물 BEST", "예비맘 · 출산 선물\n여름 실용템.", "선물하기", badge="BEST"),
            CopySet("urgency", "HOT 아이템", "검증된 냉감 효과\n지금 만나보세요.", "리뷰 확인", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("❄️", "듀라론 냉감", "세탁 후에도 유지"),
        Benefit("🔄", "양면 사용", "냉감 + 메쉬"),
        Benefit("💨", "3D 에어메쉬", "통기성 극대화"),
        Benefit("🧼", "세탁 편의", "세탁기 OK"),
    ],
    review={"text": "에어컨 켜도 잘 자지 못하던 아이가 이 패드 덕분에 편하게 자요. 시원함이 지속돼서 좋아요.", "name": "열대야 대비맘"},
)


# === 12. Portable Crib (sleep-products, CDN) — 핵심 제품 ======================
def _portable_crib_cdn() -> dict:
    b = f"{CDN}/sleep-products/portable-crib/images"
    return {
        "hero-main": f"{b}/hero-main.webp",
        "lifestyle": f"{b}/portable-crib-lifestyle.webp",
        "stable-frame": f"{b}/stable-frame.webp",
        "overview-01": f"{b}/overview-01.webp",
        "foldable": f"{b}/foldable-structure.webp",
        "mesh-fabric": f"{b}/mesh-fabric.webp",
        "storage-bag": f"{b}/storage-bag.webp",
        "unfolded": f"{b}/unfolded.webp",
        "folded": f"{b}/folded.webp",
        "product-size": f"{b}/product-size.webp",
    }


PORTABLE_CRIB = ProductConfig(
    **base(),
    product_name="꿀잠 ABC 접이식 아기침대",
    product_slug="portable-crib",
    category="sleep-products",
    images=_portable_crib_cdn(),
    tone_image_pools={
        "emotional": ["lifestyle", "hero-main", "unfolded", "overview-01"],
        "informational": ["stable-frame", "foldable", "mesh-fabric", "storage-bag", "product-size"],
        "urgency": ["hero-main", "folded", "lifestyle", "foldable"],
    },
    copies={
        "emotional": [
            CopySet("emotional", "어디서든 친숙한\n아기의 잠자리", "여행 · 외갓집 · 카페에서도\n우리 아가만의 공간.", "지금 만나보기"),
            CopySet("emotional", "귀성길도 걱정 없이", "접어서 가방에 쏙.\n어디서든 안정된 수면.", "자세히 보기"),
            CopySet("emotional", "엄마 품처럼 포근한\n휴대용 침대", "익숙한 잠자리를\n여행지에서도 그대로.", "자세히 보기"),
            CopySet("emotional", "온 가족의 외출\n이제 가볍게", "아기 수면 공간 하나로\n외출이 달라집니다.", "브랜드 스토리"),
        ],
        "informational": [
            CopySet("informational", "접이식 구조\n1초 휴대", "가방에 쏙 들어가는\n초경량 접이식 설계.", "접이 구조 보기", badge="접이식"),
            CopySet("informational", "에어메쉬 원단\n사계절 통기", "안쪽 4면 메쉬로\n열·땀 걱정 없이.", "원단 상세"),
            CopySet("informational", "견고한 프레임\n안정성 보장", "흔들림 최소화\n튼튼한 프레임 구조.", "프레임 상세", badge="안정성"),
            CopySet("informational", "수납 가방 포함\n여행용 세트", "전용 수납 가방으로\n이동이 편리합니다.", "구성품 보기"),
            CopySet("informational", "KC 인증 완료\n국내 자체 생산", "아기 침대 안전기준 충족\n통세탁도 가능.", "인증 확인", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "여행맘 필수템\n귀성 준비", "연휴 귀성길 · 여행\n지금 준비하세요.", "지금 구매하기", badge="여행 BEST"),
            CopySet("urgency", "4.95★ 리뷰", "여행맘들의 극찬.\n검증된 휴대 솔루션.", "리뷰 확인", badge="4.95★"),
            CopySet("urgency", "출산 선물 BEST", "실용성 1위 선물.\n초보 엄마도 편해요.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 수량", "시즌 초기 수량 한정.\n빠르게 준비하세요.", "지금 주문", badge="HURRY"),
            CopySet("urgency", "외출 · 여행 필수템", "카페 · 공원 · 해외\n어디서든 아기 공간.", "지금 구매", badge="HOT"),
        ],
    },
    benefits=[
        Benefit("🎒", "접이식 휴대", "가방 한 번에"),
        Benefit("🌬️", "에어메쉬", "사계절 통기"),
        Benefit("🛡️", "견고 프레임", "흔들림 최소화"),
        Benefit("✅", "KC 인증", "안전기준 충족"),
    ],
    review={"text": "여행 갈 때 진짜 필수템이에요. 아이에게 친숙한 잠자리를 어디서든 제공해주니까 안심이에요. 귀성길에도 접어서 가방에 넣으면 되니까 가볍고 좋아요.", "name": "여행맘 · 4.95★"},
)


# === 13. White Noise (sleep-products, CDN) ====================================
def _white_noise_cdn() -> dict:
    b = f"{CDN}/sleep-products/white-noise/image"
    return {
        "hero-main": f"{b}/hero-main.webp",
        "lifestyle-01": f"{b}/lifestyle-01.webp",
        "lifestyle-02": f"{b}/lifestyle-02.webp",
        "overview-controls": f"{b}/overview-controls.webp",
        "point-01": f"{b}/point-01.webp",
        "point-02": f"{b}/point-02.webp",
        "point-03-timer": f"{b}/point-03-timer.webp",
        "point-04": f"{b}/point-04.webp",
        "point-05": f"{b}/point-05.webp",
        "package": f"{b}/package-contents.webp",
    }


WHITE_NOISE = ProductConfig(
    **base(),
    product_name="꿀잠 백색소음기",
    product_slug="white-noise",
    category="sleep-products",
    images=_white_noise_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "10분 안에\n잠드는 아기", "21종 맞춤 사운드로\n잠투정 끝.", "지금 만나보기"),
            CopySet("emotional", "엄마의 밤이\n편안해져요", "아기가 잘 자면\n엄마의 휴식도 깊어집니다.", "자세히 보기"),
            CopySet("emotional", "무드등 겸용", "수유등 · 포커스 조명까지\n하나로 OK.", "자세히 보기"),
            CopySet("emotional", "작은 사운드가\n만드는 큰 변화", "잠투정 아기에게\n가장 필요한 한 가지.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "21종 사운드\n백색·자연·팬음", "백색음 5 · 팬음 5 · 자연음 11\n우리 아기에 맞게.", "사운드 리스트", badge="21종 사운드"),
            CopySet("informational", "32단계 볼륨\n360도 조절", "섬세한 볼륨 조정으로\n수면 환경 맞춤.", "조작 상세"),
            CopySet("informational", "30/60/90분 타이머", "자동 꺼짐으로\n배터리와 안전까지.", "사용법 보기", badge="타이머"),
            CopySet("informational", "USB-C 충전식\n무선 사용", "코드 걸릴 걱정 없이\n어디서든 안전하게.", "충전 상세"),
            CopySet("informational", "5단계 무드등\n차일드락 · 메모리", "세심한 편의 기능.\n우리 아가 안심.", "기능 상세"),
        ],
        "urgency": [
            CopySet("urgency", "5.0★ 완벽 평점", "잠투정 해결템 1위.\n지금 만나보세요.", "지금 구매하기", badge="5.0★"),
            CopySet("urgency", "잠투정 심한 아기 필수", "10분 안에 잠드는 마법.\n리뷰가 증명.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "선물 BEST", "출산 · 돌잔치 선물\n인기 1순위.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 특가 중", "시즌 프로모션.\n놓치지 마세요.", "지금 구매", badge="SALE"),
            CopySet("urgency", "NEW 모델", "최신 업그레이드\n신제품 메모리 기능.", "지금 주문", badge="NEW"),
        ],
    },
    benefits=[
        Benefit("🎵", "21종 사운드", "아기 맞춤 선택"),
        Benefit("🔊", "32단계 볼륨", "360도 조절"),
        Benefit("⏱️", "타이머", "30/60/90분"),
        Benefit("💡", "무드등 5단계", "수유등 겸용"),
    ],
    review={"text": "잠투정 심했는데 백색소음기 틀어주니 10분 안에 잠들더라고요. 이제 없으면 안 되는 필수템이에요.", "name": "5.0★ 수면 솔루션"},
)


# === 14. Bodysuit Mesh (daily-look, CDN) ======================================
def _bodysuit_mesh_cdn() -> dict:
    b = f"{CDN}/daily-look/bodysuit/bodysuit-mesh"
    return {
        "hero-main": f"{b}/hero-main-mesh.webp",
        "lifestyle-01": f"{b}/lifestyle-01-mesh.webp",
        "lifestyle-02": f"{b}/lifestyle-02-mesh.webp",
        "all-colors": f"{b}/all-colors-mesh.webp",
        "point-01-fabric": f"{b}/point-01-mesh-fabric.webp",
        "point-02-snap": f"{b}/point-02-mesh-snap-button.webp",
        "point-03-activity": f"{b}/point-03-mesh-activity.webp",
        "point-04-fluor-free": f"{b}/point-04-fluorescent-free-mesh.webp",
        "size": f"{b}/product-size-cotton-mesh.webp",
        "trust": f"{b}/trust-point-cotton-mesh.webp",
    }


BODYSUIT_MESH = ProductConfig(
    **base(),
    product_name="코튼메쉬 바디슈트",
    product_slug="bodysuit-mesh",
    category="daily-look",
    images=_bodysuit_mesh_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "땀띠 걱정 없는\n일상 기본템", "통기성 좋은 코튼메쉬로\n매일 가볍게 입혀요.", "지금 만나보기"),
            CopySet("emotional", "외출도 가볍게", "시원하고 활동성 좋은\n여름 데일리 필수.", "자세히 보기"),
            CopySet("emotional", "아기 피부에\n가장 먼저 닿는 옷", "그래서 더 신중하게\n무형광 안심 소재로.", "자세히 보기"),
            CopySet("emotional", "6가지 컬러로\n코디 편안함", "데일리·사파리 컬러\n일상을 예쁘게.", "컬러 보기"),
        ],
        "informational": [
            CopySet("informational", "면 100% 코튼메쉬\n태열 방지", "열 많은 아기를 위한\n통기성 우수 원단.", "원단 상세보기", badge="여름 최적"),
            CopySet("informational", "스냅 버튼\n기저귀 교체 편리", "발 아래 스냅으로\n빠른 교체.", "사용법"),
            CopySet("informational", "여유있는 핏\n활동성 UP", "아기의 움직임을\n방해하지 않는 디자인.", "핏 상세"),
            CopySet("informational", "무형광 스냅\n안심 소재", "KC 인증 완료\n피부에 닿는 모든 부분 안전.", "인증 확인", badge="KC 인증"),
            CopySet("informational", "S/M/L 3사이즈\n6컬러", "40·43·45cm\n데일리 · 사파리 컬러.", "사이즈 확인"),
        ],
        "urgency": [
            CopySet("urgency", "여름 데일리템 BEST", "여름철 필수 아이템.\n지금 준비하세요.", "지금 구매하기", badge="여름 BEST"),
            CopySet("urgency", "출산 선물 BEST", "예비맘 인기 선물.\n6컬러 모두 인기.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러\n품절 임박", "사파리 컬러 인기\n빠르게 소진 중.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "국내생산 HOT", "직영공장 생산\n검증된 품질.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "NEW 컬러 출시", "신규 사파리 컬러\n첫 선보임.", "지금 주문", badge="NEW"),
        ],
    },
    benefits=[
        Benefit("🌬️", "코튼메쉬", "태열 방지 통기성"),
        Benefit("🔘", "스냅 버튼", "기저귀 교체 편리"),
        Benefit("🤸", "여유 핏", "활동성 UP"),
        Benefit("✅", "KC 인증", "무형광 안심"),
    ],
    review={"text": "여름에 진짜 시원해요. 땀띠 걱정 없이 매일 입히고 있어요.", "name": "데일리맘 리뷰"},
)


# === 15. Bodysuit Short (daily-look, CDN) =====================================
def _bodysuit_short_cdn() -> dict:
    b = f"{CDN}/daily-look/bodysuit/bodysuit-bamboo"
    return {
        "hero-main": f"{b}/hero-main-bamboo.webp",
        "lifestyle-02": f"{b}/lifestyle-02-bamboo.webp",
        "all-colors": f"{b}/all-colors-bamboo.webp",
        "point-01-fabric": f"{b}/point-01-bamboo-fabric.webp",
        "point-02-snap": f"{b}/point-02-bamboo-snap-button.webp",
        "point-03-activity": f"{b}/point-03-bamboo-activity.webp",
        "point-04-fluor-free": f"{b}/point-04-fluorescent-free-bamboo.webp",
        "size": f"{b}/product-size-silky-bamboo.webp",
        "trust-bamboo": f"{b}/trust-point-bamboo.webp",
        "trust-snap": f"{b}/trust-point-snap-design.webp",
    }


BODYSUIT_SHORT = ProductConfig(
    **base(),
    product_name="코튼밤부 반팔 바디슈트",
    product_slug="bodysuit-short",
    category="daily-look",
    images=_bodysuit_short_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "실크처럼 부드러운\n데일리 기본템", "밤부 60% 혼방\n실크 같은 감촉.", "지금 만나보기"),
            CopySet("emotional", "사계절 포근하게", "여름·환절기·초겨울\n한 벌로 충분해요.", "자세히 보기"),
            CopySet("emotional", "민감한 피부에도 안심", "그래서 더 신중하게\n무형광 소재.", "자세히 보기"),
            CopySet("emotional", "4가지 컬러로\n코디 편안함", "데일리 + 포인트 컬러.\n매일 입기 좋아요.", "컬러 보기"),
        ],
        "informational": [
            CopySet("informational", "밤부 60% + 코튼 40%\n실크 촉감", "실크처럼 부드럽고\n흡수성 우수.", "원단 상세보기", badge="실크 촉감"),
            CopySet("informational", "스냅 디자인\n기저귀 교체 편리", "발 아래 스냅.\n빠른 교체 OK.", "사용법"),
            CopySet("informational", "여유있는 활동성", "아기 움직임\n방해하지 않는 핏.", "핏 상세"),
            CopySet("informational", "무형광 스냅", "KC 인증 완료\n피부 안심.", "인증 확인", badge="KC 인증"),
            CopySet("informational", "S/M/L 3사이즈\n4컬러", "40·43·45cm\n데일리+포인트 컬러.", "사이즈 확인"),
        ],
        "urgency": [
            CopySet("urgency", "사계절 데일리 BEST", "봄·여름·가을·초겨울\n계절 상관없이.", "지금 구매하기", badge="사계절 BEST"),
            CopySet("urgency", "출산 선물 BEST", "고급 밤부 소재\n선물로 인기.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러", "제이드 · 라이트 코랄\n시즌 인기 컬러.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "국내생산", "직영공장 품질\n무형광 검증.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "NEW 컬러", "신규 포인트 컬러\n첫 선보임.", "지금 주문", badge="NEW"),
        ],
    },
    benefits=[
        Benefit("🎋", "밤부 60%", "실크 같은 부드러움"),
        Benefit("🔘", "스냅 디자인", "기저귀 교체 편리"),
        Benefit("🌡️", "사계절 OK", "환절기 포근함"),
        Benefit("✅", "KC 인증", "무형광 안심"),
    ],
    review={"text": "밤부 소재라 정말 부드럽고 피부 트러블 없어요. 사계절 입히고 있어요.", "name": "사계절 데일리맘"},
)


# === 16. Jogger Pants (daily-look, CDN) =======================================
def _jogger_cdn() -> dict:
    b = f"{CDN}/daily-look/jogger-pants/images"
    return {
        "hero-main": f"{b}/hero-main-pants.webp",
        "lifestyle-01": f"{b}/lifestyle-pants-01.webp",
        "lifestyle-02": f"{b}/lifestyle-pants-02.webp",
        "all-colors": f"{b}/all-colors-jogger.webp",
        "point-01-fabric": f"{b}/point-01-bamboo-fabric.webp",
        "point-02-fit": f"{b}/point-02-relaxed-fit.webp",
        "point-03-ankle": f"{b}/point-03-ankle-band.webp",
        "point-04-korea": f"{b}/point-04-made-in-korea-bamboo.webp",
        "size": f"{b}/jogger-pants-size.webp",
        "trust": f"{b}/trust-point-bamboo.webp",
    }


JOGGER_PANTS = ProductConfig(
    **base(),
    product_name="배앓이 방지 배기 조거팬츠",
    product_slug="jogger-pants",
    category="daily-look",
    images=_jogger_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "허리 안 조이는\n편안한 일상", "배앓이 걱정 없이\n우리 아가 편하게.", "지금 만나보기"),
            CopySet("emotional", "기저귀 위에도\n부담 없이", "여유있는 배기핏으로\n하루 종일 편안.", "자세히 보기"),
            CopySet("emotional", "아기도 엄마도 편한\n국민 팬츠", "입자마자 바로 편해요.\n한 번 사면 반복 구매.", "자세히 보기"),
            CopySet("emotional", "4가지 컬러\n데일리 코디", "어떤 상의와도\n잘 어울려요.", "컬러 보기"),
        ],
        "informational": [
            CopySet("informational", "배앓이 방지 밴딩", "엘라스틴+밤부 소재가\n허리를 조이지 않아요.", "상세 보기", badge="배앓이 방지"),
            CopySet("informational", "밤부 60% + 코튼 40%", "부드럽고 흡습성 우수.\n민감 피부 안심.", "원단 상세보기"),
            CopySet("informational", "여유있는 배기핏", "기저귀 위에도\n부담 없이 입어요.", "핏 상세"),
            CopySet("informational", "부드러운 발목밴드", "너무 조이지 않게\n활동성 최적화.", "활용 TIP"),
            CopySet("informational", "KC 인증\n국내 자체 생산", "직영공장에서 직접.\n무형광 안심.", "품질 보기", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "국민 팬츠 BEST", "재구매 많은 인기 팬츠.\n지금 준비하세요.", "지금 구매하기", badge="BEST"),
            CopySet("urgency", "출산 선물 BEST", "실용성 1위 선물.\n한 번 쓰면 계속.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러\n품절 임박", "제이드 · 라이트 코랄\n시즌 인기.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "HOT 아이템", "배앓이 걱정\n해결하는 팬츠.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "NEW 사이즈 추가", "신규 L 사이즈\n보행기 맘 OK.", "지금 주문", badge="NEW"),
        ],
    },
    benefits=[
        Benefit("🤰", "배앓이 방지", "밴딩 안 조임"),
        Benefit("🎋", "밤부 혼방", "부드러움 + 흡습"),
        Benefit("🤸", "배기핏", "활동성 UP"),
        Benefit("🦶", "부드러운 발목밴드", "조이지 않음"),
    ],
    review={"text": "허리 안 조이고 배 편한 팬츠라 아기가 좋아해요. 계속 재구매 중이에요.", "name": "재구매맘"},
)


# === 17. Longsleeve Romper (daily-look, CDN) ==================================
def _romper_cdn() -> dict:
    b = f"{CDN}/daily-look/longsleeve-romper/images"
    return {
        "hero-main": f"{b}/hero-main.webp",
        "lifestyle-01": f"{b}/lifestyle-01.webp",
        "lifestyle-02": f"{b}/lifestyle-02.webp",
        "lifestyle-03": f"{b}/lifestyle-03-final.webp",
        "lineup": f"{b}/lineup-all.webp",
        "point-01-snap": f"{b}/point-01-front-snap.webp",
        "point-02-fullbody": f"{b}/point-02-fullbody-cover.webp",
        "point-03-band": f"{b}/point-03-band-finish.webp",
        "point-04-fabric": f"{b}/point-04-cotton-bamboo.webp",
        "size": f"{b}/size-info.webp",
    }


LONGSLEEVE_ROMPER = ProductConfig(
    **base(),
    product_name="긴팔 코튼밤부 우주복",
    product_slug="longsleeve-romper",
    category="daily-look",
    images=_romper_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "머리부터 발끝까지\n포근하게", "올인원 우주복으로\n체온 유지 걱정 끝.", "지금 만나보기"),
            CopySet("emotional", "환절기부터 겨울까지", "한 벌로 한 계절.\n편리하고 따뜻해요.", "자세히 보기"),
            CopySet("emotional", "배 드러남 걱정 끝", "올인원이라 이불\n밖으로 나와도 안심.", "자세히 보기"),
            CopySet("emotional", "앞트임 스냅으로\n기저귀 교체 편리", "누운 상태 그대로\n빠른 교체 OK.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "앞트임 스냅", "누운 상태로 바로\n기저귀를 갈 수 있어요.", "사용법", badge="앞트임"),
            CopySet("informational", "올인원 풀바디 커버", "머리 아래부터 발끝까지\n배 드러남 방지.", "핏 상세"),
            CopySet("informational", "밤부 60% + 코튼 40%", "부드럽고 흡습성 좋은\n사계절 혼방.", "원단 상세보기"),
            CopySet("informational", "손목 · 발목 밴드", "너무 조이지 않는\n부드러운 마무리.", "활용 TIP"),
            CopySet("informational", "KC 인증\n국내 자체 생산", "직영공장 품질\n무형광 안심.", "품질 보기", badge="KC 인증"),
        ],
        "urgency": [
            CopySet("urgency", "환절기 필수템", "일교차 클 때 최고.\n지금 준비하세요.", "지금 구매하기", badge="환절기"),
            CopySet("urgency", "출산 선물 BEST", "실용성 1위 선물.\n예비맘 인기.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러", "데일리·오트 2컬러\n시즌 인기.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "HOT 아이템", "배 드러남 걱정\n해결하는 우주복.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "NEW 출시", "신규 라인업\n첫 선보임.", "지금 주문", badge="NEW"),
        ],
    },
    benefits=[
        Benefit("🔘", "앞트임 스냅", "기저귀 교체 편리"),
        Benefit("🤱", "올인원", "배 드러남 방지"),
        Benefit("🎋", "밤부 60%", "부드러움 + 흡습"),
        Benefit("🧦", "부드러운 밴드", "손목·발목 마무리"),
    ],
    review={"text": "올인원이라 자면서 배 드러날 걱정 없어요. 앞트임 스냅이 진짜 편해요.", "name": "환절기 준비맘"},
)


# === 18. Terry Bib (daily-look, CDN) — bonus ==================================
def _terry_bib_cdn() -> dict:
    b = f"{CDN}/daily-look/terry-bib/images"
    return {
        "hero-main": f"{b}/hero-main.webp",
        "lifestyle-01": f"{b}/lifestyle-01.webp",
        "lifestyle-02": f"{b}/lifestyle-02.webp",
        "all-colors": f"{b}/all-colors.webp",
        "point-01": f"{b}/point-01.webp",
        "point-02": f"{b}/point-02.webp",
        "point-03-wet": f"{b}/point-03-wet-demo.webp",
        "point-04": f"{b}/point-04.webp",
        "color-cream": f"{b}/color-daily-cream.webp",
        "artboard": f"{b}/artboard-01.webp",
    }


TERRY_BIB = ProductConfig(
    **base(),
    product_name="리버서블 테리 턱받이",
    product_slug="terry-bib",
    category="daily-look",
    images=_terry_bib_cdn(),
    copies={
        "emotional": [
            CopySet("emotional", "침 · 분유 · 이유식\n완벽 흡수", "프리미엄 테리 원단으로\n옷 걱정 끝.", "지금 만나보기"),
            CopySet("emotional", "양면 사용 가능한\n리버서블 디자인", "한 장으로 두 가지 스타일.\n일상도 사진도 OK.", "자세히 보기"),
            CopySet("emotional", "8가지 컬러로\n코디 편안함", "데일리 4 · 무드 4\n어떤 옷에도 잘 어울려요.", "컬러 보기"),
            CopySet("emotional", "아기 턱도 안심", "부드러운 테리 원단\n민감한 피부도 OK.", "자세히 보기"),
        ],
        "informational": [
            CopySet("informational", "프리미엄 테리 원단\n흡수력 극대화", "침·분유·이유식 모두\n빠르게 흡수.", "원단 상세보기", badge="흡수력"),
            CopySet("informational", "리버서블 양면 사용", "한 장으로 두 스타일.\n상황에 맞게 뒤집어.", "사용법", badge="양면"),
            CopySet("informational", "넉넉한 FREE 사이즈", "30×26cm\n목부터 가슴까지 완벽 커버.", "사이즈 확인"),
            CopySet("informational", "무형광 소재", "KC 인증 완료\n피부 안심.", "인증 확인", badge="KC 인증"),
            CopySet("informational", "8컬러\n데일리 + 무드", "데일리 4컬러 + 무드 4컬러\n다양한 활용.", "컬러 보기"),
        ],
        "urgency": [
            CopySet("urgency", "수유 · 이유식기 필수", "지금 꼭 준비하세요.\n여러 장 필수.", "지금 구매하기", badge="필수템"),
            CopySet("urgency", "출산 선물 BEST", "실용성 1위 선물.\n8컬러 모두 인기.", "선물하기", badge="BEST"),
            CopySet("urgency", "한정 컬러\n품절 임박", "무드 컬러 4종\n빠르게 소진 중.", "지금 구매", badge="HURRY"),
            CopySet("urgency", "HOT 아이템", "침·이유식 걱정 끝\n리버서블 신기.", "리뷰 확인", badge="HOT"),
            CopySet("urgency", "NEW 컬러", "신규 어스브라운 · 블룸라벤더\n첫 선보임.", "지금 주문", badge="NEW"),
        ],
    },
    benefits=[
        Benefit("💦", "프리미엄 테리", "흡수력 극대화"),
        Benefit("🔄", "리버서블", "양면 사용"),
        Benefit("📏", "FREE 사이즈", "목~가슴 커버"),
        Benefit("🎨", "8가지 컬러", "데일리 + 무드"),
    ],
    review={"text": "흡수력 진짜 좋고 양면 쓸 수 있어서 세탁 빈도도 줄었어요. 컬러가 다양해서 옷에 맞춰 쓰기 좋아요.", "name": "이유식기맘"},
)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ALL_PRODUCTS: list[ProductConfig] = [
    DUAL_REFLUX,
    SLEEPSACK_SILKY_BAMBOO,
    SLEEPSACK_COTTON_MESH,
    SLEEPSACK_TRIPLE_BAMBOO,
    # v1 sleeping bags skipped — only page screenshots available, not usable as ad assets
    BUTTERFLY_SWADDLE_MESH,
    BUTTERFLY_SWADDLE_BAMBOO,
    SWADDLE_POCKET,
    COOLING_PAD,
    PORTABLE_CRIB,
    WHITE_NOISE,
    BODYSUIT_MESH,
    BODYSUIT_SHORT,
    JOGGER_PANTS,
    LONGSLEEVE_ROMPER,
    TERRY_BIB,
]


def main(argv: list[str]) -> None:
    targets = argv[1:] if len(argv) > 1 else None
    results = []
    for cfg in ALL_PRODUCTS:
        if targets and cfg.product_slug not in targets:
            continue
        out_dir = OUTPUT_BASE / cfg.category / cfg.product_slug
        try:
            specs = build_ads(cfg, out_dir)
            results.append((cfg.product_slug, len(specs), "OK", None))
            print(f"  ✓ {cfg.product_slug:<40} {len(specs):>3} creatives")
        except Exception as e:
            results.append((cfg.product_slug, 0, "FAIL", str(e)))
            print(f"  ✗ {cfg.product_slug:<40} FAILED — {e}")

    print()
    ok = sum(1 for _, _, s, _ in results if s == "OK")
    total_creatives = sum(n for _, n, _, _ in results)
    print(f"✓ Done: {ok}/{len(results)} products, {total_creatives} creatives total")


if __name__ == "__main__":
    main(sys.argv)
