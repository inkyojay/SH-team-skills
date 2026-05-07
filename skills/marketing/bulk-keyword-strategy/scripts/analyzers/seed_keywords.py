#!/usr/bin/env python3
"""
seed_keywords.py — 제품 정보 → 시드 키워드 자동 도출

전략:
1. 제품 카테고리 폴더 (sleep-products, sleeping-bags, daily-look 등)에 따라 기본 시드 룰 적용
2. 제품명에서 핵심 명사 추출
3. 소재 / 사이즈 / 시즌 변형 추가
4. 타겟 연령 변형 (아기 / 신생아 / 유아 / 베이비)

출력: 시드 키워드 리스트 (5~10개), 검색광고 API에 hint로 던질 용도
"""

from __future__ import annotations

import re
from typing import Any


# 카테고리별 기본 키워드 풀 (시드)
CATEGORY_BASE: dict[str, list[str]] = {
    "sleep-products": ["아기 침구", "아기 침대 매트", "신생아 침구"],
    "sleeping-bags": [
        "아기 슬립백",
        "신생아 슬립백",
        "베이비 슬립백",
        "수면조끼",
        "유아 슬립백",
    ],
    "newborn": ["신생아 스와들", "신생아 속싸개", "아기 스와들"],
    "daily-look": [
        "아기 바디수트",
        "신생아 바디수트",
        "아기 우주복",
        "신생아 우주복",
    ],
    "outlet": [
        "아기 옷",
        "신생아 옷",
        "아기 파자마",
        "아기 우주복",
    ],
    "abc": ["아기 침대", "휴대용 아기침대", "신생아 침대"],
    "set-products": ["출산 선물 세트", "신생아 선물 세트", "출산 준비물"],
}


# 제품명에서 자주 등장하는 한국어 명사 (시드 후보)
PRODUCT_NOUN_PATTERNS = [
    # 침구류
    ("냉감", ["아기 냉감패드", "신생아 냉감패드"]),
    ("쿨링", ["아기 쿨매트", "신생아 쿨매트"]),
    ("cool", ["아기 쿨매트", "냉감패드"]),
    ("듀얼", ["양면 쿨매트", "양면 패드"]),
    ("dual", ["양면 쿨매트"]),
    ("메쉬", ["메쉬 패드", "에어메쉬 패드"]),
    ("mesh", ["메쉬 패드"]),
    ("듀라론", ["듀라론 패드", "듀라론 쿨매트"]),
    # 슬립백 / 슬립색 (variant spellings)
    ("슬립백", ["아기 슬립백", "신생아 슬립백", "베이비 슬립백", "수면조끼"]),
    ("sleepsack", ["아기 슬립백", "신생아 슬립백", "베이비 슬립백", "수면조끼"]),
    ("sleeping-bag", ["아기 슬립백", "신생아 슬립백"]),
    ("sleep-vest", ["수면조끼", "아기 수면조끼"]),
    # 스와들 / 속싸개
    ("스와들", ["신생아 스와들", "아기 속싸개", "스와들업"]),
    ("swaddle", ["신생아 스와들", "아기 속싸개", "스와들업"]),
    ("속싸개", ["신생아 속싸개", "아기 속싸개"]),
    # 의류
    ("바디수트", ["아기 바디수트", "신생아 바디수트"]),
    ("bodysuit", ["아기 바디수트", "신생아 바디수트"]),
    ("body-mesh", ["아기 바디수트 메쉬", "메쉬 바디수트"]),
    ("우주복", ["아기 우주복", "신생아 우주복"]),
    ("롬퍼", ["아기 롬퍼", "아기 우주복"]),
    ("romper", ["아기 롬퍼", "아기 우주복"]),
    ("longsleeve", ["아기 긴팔", "아기 우주복"]),
    ("파자마", ["아기 파자마", "유아 파자마"]),
    ("pajama", ["아기 파자마", "유아 파자마"]),
    ("후드", ["아기 후드", "아기 후드티"]),
    ("hoodie", ["아기 후드", "아기 후드티"]),
    ("바지", ["아기 바지", "신생아 바지"]),
    ("팬츠", ["아기 팬츠", "아기 조거팬츠"]),
    ("조거", ["아기 조거팬츠"]),
    ("jogger", ["아기 조거팬츠", "아기 바지"]),
    ("나시", ["아기 나시", "신생아 나시"]),
    ("nasi", ["아기 나시"]),
    ("턱받이", ["아기 턱받이"]),
    ("bib", ["아기 턱받이"]),
    ("terry", ["아기 턱받이"]),
    ("flower-bib", ["아기 턱받이", "아기 꽃턱받이"]),
    ("조끼", ["아기 조끼", "유아 조끼"]),
    ("vest", ["아기 조끼", "유아 조끼"]),
    ("indoor-vest", ["아기 실내조끼", "유아 실내조끼"]),
    ("loungewear", ["아기 잠옷", "유아 잠옷"]),
    ("실내복", ["아기 실내복", "유아 실내복"]),
    ("쇼트", ["아기 반팔", "여름 아기옷"]),
    ("short-set", ["아기 반팔세트", "여름 아기 세트"]),
    # 침대 액세서리
    ("암막", ["아기 암막커버", "암막 침대"]),
    ("cover", ["아기 침대 커버"]),
    ("매트리스", ["아기 매트리스", "신생아 매트리스 패드"]),
    ("mattress", ["아기 매트리스 패드"]),
    ("모기장", ["아기 모기장"]),
    ("mosquito", ["아기 모기장"]),
    ("organizer", ["아기 침대 정리함"]),
    ("쿠션", ["아기 쿠션", "역류방지 쿠션"]),
    ("역류방지", ["역류방지 쿠션", "신생아 역류방지"]),
    ("reflux", ["역류방지 쿠션"]),
    ("crib", ["휴대용 아기침대", "신생아 침대"]),
    ("portable", ["휴대용 아기침대"]),
    # 기타
    ("화이트노이즈", ["아기 화이트노이즈", "수면 사운드"]),
    ("white-noise", ["아기 화이트노이즈"]),
    ("휴대용", ["휴대용 아기침대"]),
    # 세트 상품
    ("baby-shower", ["출산 선물 세트", "베이비 샤워"]),
    ("starter", ["출산 준비물", "신생아 출산 준비"]),
    ("newborn", ["신생아 선물 세트", "신생아 출산 준비"]),
    ("toddler", ["유아 선물 세트", "유아 수면용품"]),
    ("travel", ["여행용 아기침대", "휴대용 아기침대"]),
    ("nursery", ["아기방 꾸미기", "신생아 방"]),
    ("milestone", ["100일 선물", "돌 선물"]),
    ("daily-outfit", ["아기옷 세트", "유아옷 세트"]),
]


# 소재 키워드 (연관 키워드용, 메인은 아님)
MATERIAL_KEYWORDS = {
    "밤부": ["대나무 패드"],
    "코튼": [],
    "실키": ["실키 슬립백"],
    "삼중": ["삼중 거즈"],
    "거즈": ["거즈 슬립백"],
    "방수": ["방수 패드"],
    "텐셀": ["텐셀 슬립백"],
}


# 시즌 키워드 매핑
SEASON_KEYWORDS = {
    "여름": ["여름 아기 이불", "여름 아기 침구"],
    "겨울": ["겨울 슬립백", "겨울 아기 침구"],
    "봄가을": ["사계절 아기 침구"],
    "사계절": ["사계절 아기 침구"],
}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


# 본문에서 명사 토큰을 뽑을 때 무시할 stopwords (시드로 가치 없음)
_STOPWORDS = {
    "엄마", "아빠", "부모", "가족", "마음", "사용", "경우", "방법", "필요",
    "모든", "함께", "그리고", "하지만", "따라", "같이", "이런", "저런", "저희",
    "권장", "주의", "추천", "느낌", "환경", "공간", "순간", "모습", "디자인",
    "감각", "분위기", "스타일", "테스트", "제품", "기능", "효과", "케어", "관리",
    "그대로", "조심", "이상", "이하", "정도", "많이", "조금",
    "여러", "다양", "선택", "확인", "참고",
    "원단", "소재", "디자이너", "마감", "원사",
}


def _extract_nouns_from_text(text: str, min_len: int = 2, max_len: int = 6) -> list[str]:
    """긴 문장에서 한글 명사 후보 추출 (간단 룰 기반)."""
    if not text:
        return []
    # 한글 2~6자 연속, 영문 3~12자 연속
    tokens = re.findall(r"[가-힣]{" + str(min_len) + r"," + str(max_len) + r"}", text)
    out = []
    for t in tokens:
        if t in _STOPWORDS:
            continue
        if t in out:
            continue
        out.append(t)
    return out


def _combine_compound_keywords(nouns: list[str], product_category: str) -> list[str]:
    """
    명사 토큰들을 의미 있는 복합 키워드로 조합.

    예:
      ['듀라론', '냉감', '메쉬'] + sleep-products → ['아기 냉감패드', '듀라론 패드', '메쉬 패드']
      ['모로반사', '깊은숙면'] + newborn → ['신생아 속싸개', '모로반사 방지']
    """
    keywords = []
    text = " ".join(nouns).lower()

    # 의미적 매핑 (본문 명사 → 검색 키워드)
    semantic_map = [
        # 수면 / 침구
        (["냉감", "쿨링", "쿨"], ["아기 냉감패드", "아기 쿨매트", "신생아 냉감패드"]),
        (["듀라론"], ["듀라론 패드", "듀라론 쿨매트"]),
        (["메쉬", "에어메쉬", "에어 메쉬"], ["메쉬 패드", "에어메쉬 패드", "메쉬 슬립백"]),
        (["듀얼", "양면"], ["양면 쿨매트", "양면 패드"]),
        (["통기"], ["통기성 패드", "통기성 슬립백"]),
        (["흡습", "속건"], ["흡습속건 패드"]),
        # 스와들 / 속싸개
        (["스와들", "속싸개"], ["신생아 속싸개", "스와들업", "아기 스와들"]),
        (["모로반사"], ["신생아 속싸개", "모로반사 방지"]),
        (["깊은", "숙면", "수면"], ["신생아 수면", "아기 수면용품"]),
        # 의류
        (["바디수트"], ["아기 바디수트", "신생아 바디수트"]),
        (["우주복", "롬퍼"], ["아기 우주복", "신생아 우주복"]),
        (["조거", "팬츠", "바지"], ["아기 조거팬츠", "아기 바지"]),
        (["실내복", "loungewear"], ["아기 실내복", "유아 실내복"]),
        (["나시"], ["아기 나시"]),
        (["턱받이"], ["아기 턱받이"]),
        (["수면조끼", "조끼", "베스트"], ["아기 수면조끼", "유아 수면조끼"]),
        (["슬리핑백", "슬립백", "슬립색"], ["아기 슬립백", "신생아 슬립백", "수면조끼"]),
        (["코튼밤부", "밤부코튼"], ["대나무 코튼", "밤부 면"]),
        (["밤부"], ["대나무 면", "대나무 슬립백"]),
        (["코튼"], ["코튼 100%", "면 100%"]),
        (["삼중", "트리플", "거즈"], ["삼중 거즈", "거즈 슬립백"]),
        (["실키", "silky"], ["실키 슬립백"]),
        # 침대 액세서리
        (["암막", "차광"], ["아기 암막커버"]),
        (["매트리스"], ["아기 매트리스 패드"]),
        (["모기장"], ["아기 모기장"]),
        (["역류방지", "역류"], ["역류방지 쿠션"]),
        (["휴대용", "포터블"], ["휴대용 아기침대"]),
        (["화이트노이즈", "백색소음"], ["아기 화이트노이즈", "수면 사운드"]),
        # 인증 / 안전
        (["저자극", "피부자극"], ["저자극 아기옷"]),
        (["국내생산", "국산"], ["국내생산 아기"]),
    ]

    for triggers, kws in semantic_map:
        if any(t.lower() in text for t in triggers):
            keywords.extend(kws)

    return keywords


def derive_seeds_from_product(product: Any) -> tuple[list[str], set[str]]:
    """
    NEW 버전: ProductInfo 객체 (또는 dict)에서 시드 + 적합도 토큰 도출.

    Returns:
        seeds: 검색광고 API hint용 (5~10개)
        relevance_tokens: 점수 가중치용 모든 명사 토큰 set
    """
    # ProductInfo이든 dict이든 동일하게 접근
    def get(key: str, default: Any = "") -> Any:
        if hasattr(product, key):
            return getattr(product, key)
        if isinstance(product, dict):
            return product.get(key, default)
        return default

    category = str(get("category", ""))
    sub_title = _normalize(str(get("sub_title", "")))
    usp_short = _normalize(str(get("usp_short", "")))
    material = _normalize(str(get("material", "")))
    slug = str(get("slug", ""))

    # NEW 필드 (PDP 본문)
    highlights: list[str] = list(get("highlights", []) or [])
    sec_titles: list[str] = list(get("sec_titles", []) or [])
    trust_items: list[str] = list(get("trust_items", []) or [])
    section_comments: list[str] = list(get("section_comments", []) or [])
    faq_questions: list[str] = list(get("faq_questions", []) or [])

    # ── 시드 도출 ──
    seeds: list[str] = []
    seeds.extend(CATEGORY_BASE.get(category, []))

    # 1차: 슬러그 + 제품명 + USP 패턴 매칭 (기존 룰)
    haystack = f"{sub_title} {usp_short} {slug}".lower()
    for noun, keywords in PRODUCT_NOUN_PATTERNS:
        if noun.lower() in haystack:
            seeds.extend(keywords)

    # 2차: 본문 명사에서 의미 매핑 (NEW)
    body_nouns: list[str] = []
    for src in highlights + trust_items + sec_titles + section_comments:
        body_nouns.extend(_extract_nouns_from_text(src))
    body_compounds = _combine_compound_keywords(body_nouns, category)
    seeds.extend(body_compounds)

    # 3차: 시즌 / 소재 변형 (기존)
    for season, kws in SEASON_KEYWORDS.items():
        if season.lower() in haystack or any(season in s for s in sec_titles):
            seeds.extend(kws)
    for mat, kws in MATERIAL_KEYWORDS.items():
        if mat.lower() in material.lower() or mat.lower() in haystack:
            seeds.extend(kws)

    # dedup, preserve order
    seen = set()
    deduped: list[str] = []
    for s in seeds:
        s = _normalize(s)
        if s and s not in seen:
            seen.add(s)
            deduped.append(s)
    if not deduped:
        deduped = CATEGORY_BASE.get(category, ["아기 용품"])

    # ── 적합도 토큰 (grader 가중치용) ──
    # 시드 어휘 + 본문 명사 + USP/제품명 명사 + 슬러그 명사 모두 합집합
    relevance_tokens: set[str] = set(body_nouns)
    relevance_tokens |= set(_extract_nouns_from_text(sub_title))
    relevance_tokens |= set(_extract_nouns_from_text(usp_short))
    relevance_tokens |= set(_extract_nouns_from_text(material))
    for s in deduped:
        relevance_tokens |= set(_extract_nouns_from_text(s))
    # 슬러그 영문도 토큰으로 (대소문자 무관 매칭은 grader에서 처리)
    for slug_token in re.findall(r"[a-zA-Z]{3,}", slug):
        relevance_tokens.add(slug_token.lower())

    return deduped[:12], relevance_tokens


def derive_seeds(product: dict[str, Any]) -> list[str]:
    """
    Args:
        product: ProductInfo의 dict 형태 (slug, category, sub_title, usp_short, material)

    Returns:
        시드 키워드 리스트 (5~10개, 중복 제거)
    """
    seeds: list[str] = []
    category = product.get("category", "")
    sub_title = _normalize(product.get("sub_title", ""))
    usp_short = _normalize(product.get("usp_short", ""))
    material = _normalize(product.get("material", ""))
    slug = product.get("slug", "")

    # 1. 카테고리 기본 시드
    seeds.extend(CATEGORY_BASE.get(category, []))

    # 2. 제품명에서 명사 패턴 매칭
    haystack = f"{sub_title} {usp_short} {slug}".lower()
    for noun, keywords in PRODUCT_NOUN_PATTERNS:
        if noun.lower() in haystack:
            seeds.extend(keywords)

    # 3. 소재 변형 (보조)
    for mat, keywords in MATERIAL_KEYWORDS.items():
        if mat.lower() in material.lower() or mat.lower() in haystack:
            seeds.extend(keywords)

    # 4. 시즌 변형
    for season, keywords in SEASON_KEYWORDS.items():
        if season.lower() in haystack:
            seeds.extend(keywords)

    # dedup, preserve order
    seen = set()
    deduped = []
    for s in seeds:
        s = _normalize(s)
        if s and s not in seen:
            seen.add(s)
            deduped.append(s)

    # 시드가 너무 적으면 카테고리 기본만으로도 보완
    if not deduped:
        deduped = CATEGORY_BASE.get(category, ["아기 용품"])

    # 최대 10개 (검색광고 API 5개씩 2번이면 충분)
    return deduped[:10]


if __name__ == "__main__":
    # CLI 시범
    sample = {
        "slug": "cooling-mesh-dual-pad",
        "category": "sleep-products",
        "sub_title": "쿨링 메쉬 듀얼패드",
        "usp_short": "듀라론 냉감 × 메쉬 통기성",
        "material": "듀라론 / 3D 에어메쉬",
    }
    print("Sample:")
    for k, v in sample.items():
        print(f"  {k}: {v}")
    print("\nSeeds:")
    for s in derive_seeds(sample):
        print(f"  - {s}")
