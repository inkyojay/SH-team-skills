"""SUNDAY HUG — 이벤트 메타 광고 5종 (Phase D)

이벤트 페이지(abc-bed-live.html, promo-collection.html) 기반 광고 소재.
기존 제품 광고 초록 팔레트 대신 이벤트 골든 앰버 팔레트 사용.

Run: python3 products/event_ads.py [slug ...]
  - no args → build all 5 event units
  - slug(s)  → build only matching units
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

# 이벤트 팔레트 (today-event.css / abc-bed-live.html CSS 기반)
EVENT_COLORS = {
    "primary": "#C8A07C",   # accent / golden hour
    "secondary": "#F5EADC", # warm ivory
    "accent": "#D4645C",    # danger / live red (urgency)
}

# 긴급성 강조 팔레트 (flash sale 전용)
FLASH_COLORS = {
    "primary": "#D4645C",   # bold red
    "secondary": "#FFF8F0",
    "accent": "#C8A07C",
}

# 웰컴/감성 팔레트 (swaddle pocket 신규 가입)
WELCOME_COLORS = {
    "primary": "#1D9E75",   # brand green (신뢰/환영)
    "secondary": "#F5F0EB",
    "accent": "#C8A07C",
}

DESKTOP = Path("/Users/inkyo/Desktop/상세페이지 local (최종본)")
OUTPUT_BASE = Path("/Users/inkyo/Projects/team-skills/output/광고카피/sundayhug-meta-bulk")
CDN = "https://sundayhugkr.cafe24.com/skin-skin69/pdp"


# ---------------------------------------------------------------------------
# Event Unit 1: ABC 아기침대 4/30 라이브
# ---------------------------------------------------------------------------

ABC_BED_LIVE = ProductConfig(
    brand=BRAND,
    brand_name_ko=BRAND_KO,
    product_name="ABC 접이식 아기침대 · 라이브 단독가",
    product_slug="abc-bed-live",
    category="events",
    colors=EVENT_COLORS,
    images={
        # CDN 검증 경로
        "hero-toddler":    f"{CDN}/abc/abc-v2/images/intro-02-toddler.webp",
        "hero-mosquito":   f"{CDN}/abc/abc-mosquito-net/images/hero-01.webp",
        "hero-organizer":  f"{CDN}/abc/abc-organizer/images/hero-01.webp",
        "lifestyle-sleep": "https://www.sundayhug.kr/skin-skin69/pdp/sleeping-bags/sleepsack/cotton-mesh/images/intro-01.webp",
    },
    tone_image_pools={
        "emotional":     ["hero-toddler", "lifestyle-sleep", "hero-toddler"],
        "informational": ["hero-toddler", "hero-mosquito", "hero-organizer"],
        "urgency":       ["hero-toddler", "hero-mosquito", "hero-toddler"],
    },
    copies={
        # ── emotional: 아이의 첫 공간 · 따뜻한 기억 ──────────────────────────────
        "emotional": [
            CopySet("emotional",
                    "잠드는 순간이\n기억됩니다",
                    "신생아부터 15kg까지 함께 자라는 공간.\n3면 에어 메쉬 · 접이식 · 매트리스 포함.",
                    "라이브 보러가기",
                    badge="4/30 LIVE"),
            CopySet("emotional",
                    "우리 아이의\n첫 번째 안식처",
                    "사방이 메쉬라 언제나 숨 쉬는 침대.\n아이 얼굴 언제든 확인되는 안심 설계.",
                    "자세히 보기"),
            CopySet("emotional",
                    "아이의 잠이\n내일을 만듭니다",
                    "접이식이라 여행도 친정도 어디든 함께.\n라이브에서만 만날 수 있는 가격.",
                    "라이브 일정 보기"),
        ],
        # ── informational: 스펙·가격·세트 구성 ───────────────────────────────────
        "informational": [
            CopySet("informational",
                    "쿠폰 최종가\n160,550원",
                    "정상가 179,000원 → 라이브 169,000원\n라운지 5% 쿠폰 적용 시 총 18,450원 절약.",
                    "쿠폰 받으러 가기",
                    badge="LIVE 단독"),
            CopySet("informational",
                    "데일리케어 풀세트\n223,800원 BEST",
                    "아기침대 + 오거나이저 + 모기장 + 매트리스패드\n정가 246,700원에서 22,900원 저렴.",
                    "세트 구성 보기",
                    badge="BEST SET"),
            CopySet("informational",
                    "KC인증 · 3면 메쉬\n슬라이드 코슬림",
                    "접이식 · 에어 메쉬 · 매트리스 포함 · 무료배송\n4.87★ 233건 실사용 리뷰.",
                    "스펙 확인하기",
                    badge="KC인증"),
        ],
        # ── urgency: D-9 · 11시 1시간 한정 ──────────────────────────────────────
        "urgency": [
            CopySet("urgency",
                    "D-9 · 4/30(목) 11시\n라이브 단독가!",
                    "169,000원 라이브 특가 · 방송 1시간만 적용\n구매인증 시 매트리스 패드 무료 증정.",
                    "알림 신청하기",
                    badge="D-9",
                    urgency_label="4/30 AM 11:00 LIVE"),
            CopySet("urgency",
                    "라이브 끝나면\n179,000원으로!",
                    "오전 11시~11시 59분 단 1시간만 169,000원\n소통왕 스타벅스 · 맘카페 후기 사은품.",
                    "지금 예약하기",
                    badge="1시간 한정",
                    urgency_label="11:00 ~ 11:59 ONLY"),
            CopySet("urgency",
                    '"강.추.육.아.템"\n4.87★ 233건 리뷰',
                    "라이브 당일 선착순 사은품 · 전품목 무료배송\n쿠폰 최종 160,550원 · 지금 예약 필수.",
                    "라이브 입장하기",
                    badge="LIVE 한정",
                    urgency_label="TODAY ONLY"),
        ],
    },
    benefits=[
        Benefit("💸", "18,450원 절약", "쿠폰 최종 160,550원"),
        Benefit("🌬️", "3면 에어 메쉬", "통기성 안심 수면 설계"),
        Benefit("✅", "KC 인증 완료", "안심 소재·견고한 구조"),
        Benefit("🎁", "매트리스 포함", "구매인증 시 패드 추가 증정"),
    ],
    review={
        "text": '"강.추.육.아.템 입니다!! 휴대성, 안정성, 간편성, 견고함 모두 만족스러워요."',
        "name": "jas*** · 4.87★ 실제 구매 리뷰 (233건 중)",
    },
    price_label="169,000원 (라이브 단독가 · 쿠폰 적용 160,550원)",
)


# ---------------------------------------------------------------------------
# Event Unit 2: 플라워 턱받이 990원 선착순
# ---------------------------------------------------------------------------

BIB_FLASH_SALE = ProductConfig(
    brand=BRAND,
    brand_name_ko=BRAND_KO,
    product_name="플라워 턱받이 · 990원 선착순",
    product_slug="bib-flash-sale",
    category="events",
    colors=FLASH_COLORS,
    images={
        # 플라워 턱받이 전용 CDN 경로 불명확 → 나비잠 속싸개 이미지로 대체
        # (같은 신생아 카테고리, 동일 색감·타겟)
        "hero-bamboo":    f"{CDN}/newborn/butterfly-swaddle/silky-bamboo/image/hero-main-bamboo.webp",
        "hero-swaddle":   f"{CDN}/newborn/swaddle-pocket/images/hero-main.webp",
        # 역류방지쿠션 라이프스타일 (신생아 맘 공감)
        "lifestyle-baby": str(DESKTOP / "newborn/dual-reflux-cushion/images/lifestyle-01.webp"),
    },
    tone_image_pools={
        "emotional":     ["lifestyle-baby", "hero-bamboo"],
        "informational": ["hero-bamboo", "hero-swaddle"],
        "urgency":       ["hero-bamboo", "lifestyle-baby", "hero-swaddle"],
    },
    copies={
        "emotional": [
            CopySet("emotional",
                    "아기 첫 턱받이\n990원으로",
                    "신생아 필수템 · 썬데이허그 플라워 턱받이\n4/21 단 하루, 특별한 가격.",
                    "지금 담기"),
            CopySet("emotional",
                    "예쁜 플라워 디자인\n90% 할인",
                    "아이의 첫 식사를 더 사랑스럽게.\n990원 · 선착순 150명 한정.",
                    "이벤트 보기"),
        ],
        "informational": [
            CopySet("informational",
                    "정상가 → 990원\n4/21 선착순 150명",
                    "4.21 오전 10시 · 선착순 150명 한정\n1인 1개 구매 · 당일 10AM 오픈.",
                    "이벤트 확인",
                    badge="선착순 150명"),
            CopySet("informational",
                    "4/21 오전 10시\n딱 150개 한정",
                    "씻기 쉬운 소재 · 신생아 안심 인증\n990원 · 무료배송 적용 조건 확인 필요.",
                    "조건 확인하기",
                    badge="10AM OPEN"),
        ],
        "urgency": [
            CopySet("urgency",
                    "선착순 150명만!\n990원",
                    "4월 21일 오전 10시 · 딱 150개\n한 번 놓치면 정상가로 돌아갑니다.",
                    "바로 담기",
                    badge="선착순 150명",
                    urgency_label="4/21 10:00 AM"),
            CopySet("urgency",
                    "오전 10시 오픈\n놓치면 정가",
                    "플라워 턱받이 990원 · 4/21 한정\n지금 알림 설정하고 먼저 담으세요.",
                    "알림 설정하기",
                    badge="TODAY ONLY",
                    urgency_label="OPEN 10AM"),
            CopySet("urgency",
                    "990원! 오늘만\n신생아 필수템",
                    "선착순 소진 즉시 종료 · 재판매 없음\n4/21 오전 10시 정각에 담아두세요.",
                    "지금 바로 담기",
                    badge="HURRY",
                    urgency_label="LIMITED"),
        ],
    },
    benefits=[
        Benefit("🌸", "플라워 디자인", "예쁘고 사랑스러운 패턴"),
        Benefit("💧", "세탁 간편", "오염에 강한 소재"),
        Benefit("👶", "신생아 적합", "부드럽고 안전한 소재"),
        Benefit("⚡", "990원 한정", "선착순 150명 · 4/21 10AM"),
    ],
    review={
        "text": "이 가격에 이 퀄리티?! 선착순 열리자마자 담았어요. 색감이 너무 예쁘고 세탁도 잘 돼요.",
        "name": "구매자 · 신생아맘",
    },
    price_label="990원 (선착순 150명 · 4/21 10AM)",
)


# ---------------------------------------------------------------------------
# Event Unit 3: 역류방지쿠션 30% 원데이 4/22
# ---------------------------------------------------------------------------

REFLUX_ONEDAY = ProductConfig(
    brand=BRAND,
    brand_name_ko=BRAND_KO,
    product_name="듀얼 역류방지쿠션 · 30% 원데이",
    product_slug="reflux-oneday",
    category="events",
    colors=EVENT_COLORS,
    images={
        # 로컬 이미지 (all_products.py DUAL_REFLUX와 동일 경로)
        "hero-main":         str(DESKTOP / "newborn/dual-reflux-cushion/images/hero-main.webp"),
        "lifestyle-01":      str(DESKTOP / "newborn/dual-reflux-cushion/images/lifestyle-01.webp"),
        "lifestyle-02":      str(DESKTOP / "newborn/dual-reflux-cushion/images/lifestyle-02.webp"),
        "point-dual-angle":  str(DESKTOP / "newborn/dual-reflux-cushion/images/point-01-dual-angle.webp"),
        "point-cover":       str(DESKTOP / "newborn/dual-reflux-cushion/images/point-02-cover-replace.webp"),
        "point-material":    str(DESKTOP / "newborn/dual-reflux-cushion/images/point-03-material.webp"),
        "all-colors":        str(DESKTOP / "newborn/dual-reflux-cushion/images/all-colors.webp"),
    },
    tone_image_pools={
        "emotional":     ["lifestyle-01", "lifestyle-02", "hero-main"],
        "informational": ["point-dual-angle", "point-cover", "point-material", "hero-main"],
        "urgency":       ["hero-main", "all-colors", "lifestyle-02", "point-dual-angle"],
    },
    copies={
        "emotional": [
            CopySet("emotional",
                    "역류 걱정 없는\n편안한 수유 시간",
                    "수유 후 아기를 편안한 각도로.\n듀얼 역류방지쿠션 · 4/22 세트 특가.",
                    "세트 보러가기"),
            CopySet("emotional",
                    "엄마의 안심,\n아기의 편안함",
                    "커버 분리 세탁까지 꼼꼼하게.\n4/22 하루만 30% 세트 할인.",
                    "오늘 구경하기"),
        ],
        "informational": [
            CopySet("informational",
                    "30도+15도\n듀얼 각도 설계",
                    "0~3개월 30도 · 3개월+ 15도\n발달 단계별 역류 방지.",
                    "각도 상세보기",
                    badge="특허 설계"),
            CopySet("informational",
                    "커버 분리형\nKC인증 안심 소재",
                    "무형광 원단 · 세탁기 세탁 가능\n100% 국내 직영공장 생산.",
                    "소재 확인하기",
                    badge="KC인증"),
            CopySet("informational",
                    "4/22 세트 30% 할인\n오늘 단 하루",
                    "단품 구매보다 세트가 훨씬 유리\n쿠션 + 커버 + 수납파우치 세트.",
                    "세트 구성 보기",
                    badge="-30% 4/22"),
        ],
        "urgency": [
            CopySet("urgency",
                    "4/22(수) 단 하루\n세트 30% 할인!",
                    "역류방지쿠션 세트 · 내일 종료\n지금 담아두지 않으면 다시 정가.",
                    "지금 구매하기",
                    badge="D-DAY 4/22",
                    urgency_label="WED ONLY"),
            CopySet("urgency",
                    "재구매율 96%\n오늘뿐 세트 특가",
                    "2,800+ 엄마 선택 · 4.8★ 베스트셀러\n4/22 원데이 세트 30% 한정.",
                    "원데이 세트 담기",
                    badge="TODAY 30%",
                    urgency_label="ONE-DAY"),
            CopySet("urgency",
                    "신생아 수유템 1순위\n내일이면 정상가",
                    "지금 장바구니에 담아두세요\n4/22 자정 이후 정상가 전환.",
                    "세트 담기",
                    badge="HURRY",
                    urgency_label="ENDS TONIGHT"),
        ],
    },
    benefits=[
        Benefit("🎯", "듀얼 각도 설계", "30도/15도 발달 맞춤"),
        Benefit("🧺", "커버 분리 세탁", "세탁기 세탁 가능"),
        Benefit("🇰🇷", "국내 직영 생산", "원단·충전 모두 국내산"),
        Benefit("✅", "KC 인증 완료", "무형광 안심 소재"),
    ],
    review={
        "text": "역류로 힘들어하던 아기가 편해졌어요. 커버 분리돼서 세탁 편하고 국내산이라 안심돼요.",
        "name": "재구매맘 · 실제 구매 리뷰 · 4.8★",
    },
    price_label="4/22 세트 30% 할인 (원데이)",
)


# ---------------------------------------------------------------------------
# Event Unit 4: 스와들 포켓 신규 가입 3,000원 쿠폰
# ---------------------------------------------------------------------------

SWADDLE_POCKET_WELCOME = ProductConfig(
    brand=BRAND,
    brand_name_ko=BRAND_KO,
    product_name="스와들 포켓 · 신규 가입 3,000원",
    product_slug="swaddle-pocket-welcome",
    category="events",
    colors=WELCOME_COLORS,
    images={
        "hero-main":    f"{CDN}/newborn/swaddle-pocket/images/hero-main.webp",
        # 나비잠 속싸개 라이프스타일로 보완
        "hero-bamboo":  f"{CDN}/newborn/butterfly-swaddle/silky-bamboo/image/hero-main-bamboo.webp",
        # 역류쿠션 라이프스타일 (신생아맘 공감대)
        "lifestyle-01": str(DESKTOP / "newborn/dual-reflux-cushion/images/lifestyle-01.webp"),
    },
    tone_image_pools={
        "emotional":     ["lifestyle-01", "hero-main", "hero-bamboo"],
        "informational": ["hero-main", "hero-bamboo", "hero-main"],
        "urgency":       ["hero-main", "lifestyle-01", "hero-bamboo"],
    },
    copies={
        "emotional": [
            CopySet("emotional",
                    "신생아 첫 날\n편안한 품에",
                    "모로반사 걱정 없는 포근한 속싸개.\n스와들 포켓으로 꿀잠 선물하세요.",
                    "자세히 보기"),
            CopySet("emotional",
                    "아기의 첫 잠\n엄마의 첫 안도",
                    "신생아 포대기처럼 안아주는 스와들.\n가입만 해도 3,000원 쿠폰 증정.",
                    "쿠폰 받기"),
            CopySet("emotional",
                    "오늘부터\n썬데이허그 가족",
                    "신규 가입 웰컴 쿠폰 3,000원\n스와들 포켓 14,000원 → 11,000원.",
                    "가입하고 받기"),
        ],
        "informational": [
            CopySet("informational",
                    "모로반사 예방\n스와들 포켓",
                    "지퍼형 속싸개 · 착용 편리 · KC인증\n데일리 크림 1컬러.",
                    "상세 보기",
                    badge="KC인증"),
            CopySet("informational",
                    "14,000원 → 11,000원\n가입 즉시 적용",
                    "신규 가입 쿠폰 3,000원 당일 한정.\n썬데이허그 자사몰 오픈 기념.",
                    "지금 가입하기",
                    badge="3,000원 쿠폰"),
        ],
        "urgency": [
            CopySet("urgency",
                    "신규 가입만 해도\n3,000원 쿠폰!",
                    "당일 한정 웰컴 쿠폰 · 지금 가입 시 즉시 사용\n스와들 포켓 14,000원 → 11,000원.",
                    "지금 가입",
                    badge="당일 한정",
                    urgency_label="TODAY ONLY"),
            CopySet("urgency",
                    "오늘 가입하면\n11,000원!",
                    "3,000원 쿠폰 당일 만료 · 내일 없어요\n지금 바로 가입하고 혜택 챙기세요.",
                    "바로 가입하기",
                    badge="EXPIRES TODAY",
                    urgency_label="LAST CHANCE"),
            CopySet("urgency",
                    "프로모션 기간 한정\n4/21~4/30",
                    "자사몰 오픈 기념 웰컴 쿠폰 종료 전에\n스와들 포켓 할인으로 시작하세요.",
                    "쿠폰 받고 구매",
                    badge="4/30 마감",
                    urgency_label="LIMITED PERIOD"),
        ],
    },
    benefits=[
        Benefit("👶", "모로반사 예방", "지퍼형 간편 속싸개"),
        Benefit("🎁", "3,000원 쿠폰", "신규 가입 당일 한정"),
        Benefit("✅", "KC 인증 완료", "신생아 안심 소재"),
        Benefit("💚", "썬데이허그 멤버", "자사몰 오픈 기념 혜택"),
    ],
    review={
        "text": "스와들이 처음이라 걱정했는데 지퍼형이라 쉬워요. 쿠폰 쓰니 가격도 너무 좋았어요.",
        "name": "초보맘 · 실제 구매 리뷰",
    },
    price_label="14,000원 → 11,000원 (신규 가입 3,000원 쿠폰)",
)


# ---------------------------------------------------------------------------
# Event Unit 5: Spring Promotion BIG 3 브랜드 광고
# ---------------------------------------------------------------------------

SPRING_PROMO = ProductConfig(
    brand=BRAND,
    brand_name_ko=BRAND_KO,
    product_name="Spring Promotion · BIG 3",
    product_slug="spring-promo",
    category="events",
    colors=EVENT_COLORS,
    images={
        # BIG 3 제품 대표 이미지 믹스
        "hero-abc":      f"{CDN}/abc/abc-v2/images/intro-02-toddler.webp",
        "hero-reflux":   str(DESKTOP / "newborn/dual-reflux-cushion/images/hero-main.webp"),
        "hero-swaddle":  f"{CDN}/newborn/swaddle-pocket/images/hero-main.webp",
        "lifestyle-01":  str(DESKTOP / "newborn/dual-reflux-cushion/images/lifestyle-01.webp"),
        "hero-sleepsack": f"https://www.sundayhug.kr/skin-skin69/pdp/sleeping-bags/sleepsack/cotton-mesh/images/intro-01.webp",
    },
    tone_image_pools={
        "emotional":     ["lifestyle-01", "hero-abc", "hero-reflux", "hero-sleepsack"],
        "informational": ["hero-abc", "hero-reflux", "hero-swaddle", "hero-sleepsack"],
        "urgency":       ["hero-abc", "hero-reflux", "hero-swaddle"],
    },
    copies={
        "emotional": [
            CopySet("emotional",
                    "아이의 잠은\n내일의 시작입니다",
                    "썬데이허그가 준비한 봄 프로모션.\n4/21~4/30 · 자사몰 오픈 기념 한정.",
                    "혜택 확인하기"),
            CopySet("emotional",
                    "봄, 새로운 시작\n썬데이허그와 함께",
                    "플라워 턱받이·역류방지쿠션·스와들 포켓\n세 가지 혜택이 동시에.",
                    "프로모션 보기"),
            CopySet("emotional",
                    "신생아부터 24개월\n모두를 위한 봄",
                    "신생아 필수템부터 ABC 침대까지\n기간 한정 썬데이허그 전품목 할인.",
                    "지금 보러가기"),
        ],
        "informational": [
            CopySet("informational",
                    "BIG 3 동시 진행\n4/21~4/30",
                    "① 턱받이 990원(4/21 선착순) ② 역류쿠션 30%(4/22)\n③ 스와들 포켓 3,000원 쿠폰(신규 가입)",
                    "프로모션 상세보기",
                    badge="BIG 3"),
            CopySet("informational",
                    "ABC 침대 라이브\n+ 전품목 특가",
                    "4/30 라이브 단독가 · 무료배송\n선착순 구매인증 매트리스 패드 증정.",
                    "라이브 예약",
                    badge="4/30 LIVE"),
            CopySet("informational",
                    "자사몰 오픈 기념\n한정 특가 모음",
                    "썬데이허그 공식몰 · 오픈 기념\n전품목 할인 + 쿠폰 + 사은품.",
                    "전체 혜택 보기",
                    badge="오픈 기념"),
        ],
        "urgency": [
            CopySet("urgency",
                    "4/30까지만!\n BIG 3 혜택",
                    "990원·30%·3,000원 동시 진행\n자사몰 오픈 기념 · 기간 한정.",
                    "지금 바로 확인",
                    badge="D-DAY 4/30",
                    urgency_label="4/21~4/30"),
            CopySet("urgency",
                    "프로모션 종료 전\n마지막 기회",
                    "4월 30일 자정 이후 모든 혜택 종료\n지금 바로 장바구니에 담으세요.",
                    "혜택 받기",
                    badge="ENDS 4/30",
                    urgency_label="LIMITED"),
            CopySet("urgency",
                    "전품목 할인\n지금 시작",
                    "썬데이허그 자사몰 오픈 기념\n4/21~30 · 기간 한정 프로모션.",
                    "프로모션 입장",
                    badge="Spring Sale",
                    urgency_label="4.21~4.30"),
        ],
    },
    benefits=[
        Benefit("🌸", "BIG 1 · 990원", "플라워 턱받이 선착순 150명 · 4/21"),
        Benefit("🎯", "BIG 2 · 30% 할인", "역류방지쿠션 세트 원데이 · 4/22"),
        Benefit("🎁", "BIG 3 · 3,000원", "스와들 포켓 쿠폰 신규 가입"),
        Benefit("🛒", "ABC 라이브 단독가", "4/30 LIVE · 169,000원"),
    ],
    review={
        "text": "오픈 기념 행사 덕분에 아기용품 필요한 거 다 샀어요. 쿠폰도 많고 혜택이 진짜 좋더라고요.",
        "name": "구매자 · 봄 프로모션 구매 리뷰",
    },
    price_label="BIG 3 · 4/21~4/30 기간 한정",
)


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

ALL_EVENTS = [
    ABC_BED_LIVE,
    BIB_FLASH_SALE,
    REFLUX_ONEDAY,
    SWADDLE_POCKET_WELCOME,
    SPRING_PROMO,
]


def main() -> None:
    slugs = sys.argv[1:]
    targets = (
        [e for e in ALL_EVENTS if e.product_slug in slugs]
        if slugs
        else ALL_EVENTS
    )
    if not targets:
        print(f"❌ 알 수 없는 슬러그: {slugs}")
        sys.exit(1)

    for cfg in targets:
        out_dir = OUTPUT_BASE / "events" / cfg.product_slug
        print(f"🔨 빌드 중: {cfg.product_slug} → {out_dir}")
        specs = build_ads(cfg, out_dir)
        print(f"  ✓ {len(specs)}개 크리에이티브 생성")
        print(f"  📂 미리보기: {out_dir}/previews/preview-grid.html")

    print(f"\n🎉 완료: {len(targets)}개 이벤트 유닛")


if __name__ == "__main__":
    main()
