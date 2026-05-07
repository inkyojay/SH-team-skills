#!/usr/bin/env python3
"""
name_generator.py — 네이버 스마트스토어 상품명 자동 생성 (50자 이내)

공식:
  [브랜드] [시리즈명] [메인키워드] [보조키워드 1~3개] [소재] [타겟연령] [시즌]

규칙 (네이버 SEO 공식):
  - 50자 이내 (필수)
  - 수식어 / 자극 / 과장 표현 금지
  - 띄어쓰기로 키워드 분리
  - 핵심 키워드 앞쪽 배치
  - 같은 단어 반복 금지

브랜드 가이드 금기어 (V-02 / V-03):
  - 자극: !!, 대박, 미친, 역대급, 초특가, 베스트, 강력
  - 과장: 최고, 1위, 독보적, 유일, 절대, 100%, 완벽
  - 의료: 치료, 효능
  - 가격: 할인, OFF (단독 강조)
"""

from __future__ import annotations

import re
from typing import Optional


BRAND = "썬데이허그"
SERIES_DEFAULT = "꿀잠"  # 디폴트 시리즈명 (수면 라인은 거의 다 공유)

# 카테고리별 시리즈명 (제품 카테고리에 따라 매핑)
CATEGORY_SERIES = {
    "sleep-products": "꿀잠",
    "sleeping-bags": "꿀잠",
    "newborn": "꿀잠",
    "abc": "ABC",
    "daily-look": "데일리",
    "outlet": "꿀잠",
    "set-products": "꿀잠",
}


# 브랜드 가이드 금기어
FORBIDDEN_PATTERNS = [
    r"!{2,}",
    r"대박",
    r"미친",
    r"역대급",
    r"초특가",
    r"베스트(셀러)?",
    r"강력",
    r"최고",
    r"1\s*위",
    r"독보적",
    r"유일(한|함)?",
    r"절대",
    r"100\s*%",
    r"완벽",
    r"치료",
    r"효능",
    r"할인",
    r"\bOFF\b",
]

FORBIDDEN_RE = re.compile("|".join(FORBIDDEN_PATTERNS), re.IGNORECASE)


def is_forbidden(text: str) -> tuple[bool, list[str]]:
    """금기어 포함 여부 + 매칭 리스트."""
    matches = FORBIDDEN_RE.findall(text)
    return (len(matches) > 0, [m if isinstance(m, str) else "/".join(m) for m in matches])


def _korean_len(text: str) -> int:
    """네이버 글자수 = 모든 문자 (한글/영문/숫자/공백) 1자 == len()."""
    return len(text)


def generate(
    main_keyword: str,
    sub_keywords: list[str],
    category: str = "",
    material_short: str = "",
    season: str = "",
    target_age: str = "",
    max_chars: int = 50,
) -> tuple[str, list[str]]:
    """
    네이버 상품명 1안 생성.

    Returns:
        (product_name, warnings)
    """
    warnings: list[str] = []
    series = CATEGORY_SERIES.get(category, SERIES_DEFAULT)

    # 토큰 우선순위: 브랜드 → 시리즈 → 메인 → 보조1 → 소재 → 보조2 → 보조3 → 타겟 → 시즌
    tokens: list[str] = [BRAND, series, main_keyword.strip()]
    if sub_keywords:
        tokens.append(sub_keywords[0].strip())
    if material_short:
        tokens.append(material_short.strip())
    if len(sub_keywords) >= 2:
        tokens.append(sub_keywords[1].strip())
    if len(sub_keywords) >= 3:
        tokens.append(sub_keywords[2].strip())
    if target_age:
        tokens.append(target_age.strip())
    if season:
        tokens.append(season.strip())

    # 빈 / 중복 제거 (단어 단위)
    seen_words: set[str] = set()
    cleaned_tokens: list[str] = []
    for tok in tokens:
        if not tok:
            continue
        # 토큰이 띄어쓰기로 다시 나뉠 수 있음 (예: "아기 냉감패드")
        words = tok.split()
        new_words = []
        for w in words:
            if w not in seen_words:
                seen_words.add(w)
                new_words.append(w)
        if new_words:
            cleaned_tokens.append(" ".join(new_words))

    # 50자 한도 안에서 토큰 추가
    name = ""
    for tok in cleaned_tokens:
        candidate = (name + " " + tok).strip() if name else tok
        if _korean_len(candidate) > max_chars:
            warnings.append(f"제외 (길이 초과): {tok}")
            continue
        name = candidate

    # 금기어 검증
    has_forbidden, matches = is_forbidden(name)
    if has_forbidden:
        warnings.append(f"⚠️ 금기어 포함: {matches}")

    if _korean_len(name) > max_chars:
        warnings.append(f"⚠️ 길이 초과: {_korean_len(name)}자")

    return name.strip(), warnings


if __name__ == "__main__":
    cases = [
        {
            "main_keyword": "아기 냉감패드",
            "sub_keywords": ["아기 쿨매트", "신생아 냉감패드", "양면 쿨매트", "듀라론 패드"],
            "category": "sleep-products",
            "material_short": "듀라론 메쉬",
            "season": "여름",
            "target_age": "신생아",
        },
        {
            "main_keyword": "아기 슬립백",
            "sub_keywords": ["신생아 슬립백", "베이비 슬립백", "여름 슬립백"],
            "category": "sleeping-bags",
            "material_short": "코튼 메쉬",
            "season": "여름",
            "target_age": "신생아",
        },
        {
            "main_keyword": "아기 바디수트",
            "sub_keywords": ["신생아 우주복", "베이비 옷"],
            "category": "daily-look",
            "material_short": "오가닉 코튼",
            "season": "",
            "target_age": "신생아",
        },
    ]
    for c in cases:
        name, warns = generate(**c)
        print(f"입력 메인: {c['main_keyword']}")
        print(f"  → 상품명 ({len(name)}자): {name}")
        for w in warns:
            print(f"    {w}")
        print()
