#!/usr/bin/env python3
"""
grader.py — 키워드 등급 (S/A/B/C/D) 스코어링

기준:
  S: 검색량 ≥ 10,000 + 경쟁도 중하 + 시즌 일치 (피크 ±2개월)
  A: 검색량 ≥ 5,000
  B: 검색량 ≥ 1,000
  C: 검색량 ≥ 100
  D: 검색량 < 100 또는 무관

추가:
  - 경쟁도 (높음/중간/낮음) 가중치
  - 시즌성 (현재가 피크 ±2개월이면 부스트)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class GradedKeyword:
    keyword: str
    total_search: int
    competition: str
    grade: str  # S/A/B/C/D
    score: float  # 정렬용 종합 점수
    reasons: list[str]


COMP_WEIGHT = {
    "낮음": 1.2,
    "중간": 1.0,
    "높음": 0.7,
    "": 1.0,
}


def grade(
    keyword: str,
    pc_search: int,
    mobile_search: int,
    competition: str = "",
    peak_month: Optional[int] = None,
    seasonal: bool = False,
    current_month: Optional[int] = None,
) -> GradedKeyword:
    total = (pc_search or 0) + (mobile_search or 0)
    reasons: list[str] = []

    # 1. 기본 등급 (검색량)
    if total >= 10000:
        base_grade = "S"
    elif total >= 5000:
        base_grade = "A"
    elif total >= 1000:
        base_grade = "B"
    elif total >= 100:
        base_grade = "C"
    else:
        base_grade = "D"
    reasons.append(f"검색량 {total:,} → {base_grade}")

    # 2. 경쟁도 가중치
    comp_w = COMP_WEIGHT.get(competition, 1.0)
    score = total * comp_w
    if comp_w != 1.0:
        reasons.append(f"경쟁도 {competition} ({comp_w}x)")

    # 3. 시즌 보정
    if seasonal and peak_month is not None and current_month is not None:
        diff = abs(peak_month - current_month)
        if diff <= 2 or diff >= 10:  # peak ±2개월 (10/11/12/1/2/3 같은 wrap 포함)
            score *= 1.3
            reasons.append("시즌 일치 (1.3x)")
            # S 조건 (모두 충족)
            if base_grade in {"A", "B"} and competition in {"낮음", "중간"}:
                base_grade = "S"
                reasons.append("시즌+경쟁도 충족 → S 승격")

    return GradedKeyword(
        keyword=keyword,
        total_search=total,
        competition=competition,
        grade=base_grade,
        score=score,
        reasons=reasons,
    )


def _extract_tokens(text: str) -> set[str]:
    """한국어 명사 토큰 추출 (2자 이상)."""
    import re
    tokens = re.findall(r"[가-힣]{2,}|[a-zA-Z]{3,}", text or "")
    return set(tokens)


def select_main_and_subs(
    graded: list[GradedKeyword],
    blocklist_substrings: Optional[list[str]] = None,
    n_sub: int = 4,
    seed_tokens: Optional[set[str]] = None,
    relevance_boost: float = 2.0,
) -> tuple[Optional[GradedKeyword], list[GradedKeyword]]:
    """
    메인 키워드 1개 + 보조 N개 선정.
    blocklist에 매칭되는 키워드는 제외.
    seed_tokens가 주어지면, 시드와 어휘가 겹치는 키워드에 score × relevance_boost.
    """
    blocklist = blocklist_substrings or []
    seed_tokens = seed_tokens or set()

    def allowed(k: str) -> bool:
        return not any(b in k for b in blocklist)

    def score_with_relevance(g: GradedKeyword) -> float:
        if not seed_tokens:
            return g.score
        kw_tokens = _extract_tokens(g.keyword)
        # 시드 토큰과의 교집합 = 의미적 적합도
        overlap = len(kw_tokens & seed_tokens)
        # 1개 이상 겹치면 강한 부스트 (overlap 1 → 5배, 2 → 25배 ...)
        if overlap >= 1:
            return g.score * (relevance_boost ** overlap)
        # 시드와 전혀 안 겹치는 키워드 = 의미 무관 추정 → 강한 페널티
        return g.score * 0.05

    sorted_g = sorted(
        [g for g in graded if allowed(g.keyword)],
        key=score_with_relevance,
        reverse=True,
    )
    if not sorted_g:
        return None, []
    main = sorted_g[0]
    subs = sorted_g[1 : 1 + n_sub]
    return main, subs


def select_tags(
    graded: list[GradedKeyword],
    blocklist_substrings: Optional[list[str]] = None,
    n: int = 10,
    seed_tokens: Optional[set[str]] = None,
) -> list[GradedKeyword]:
    """상품태그 N개 선정 (S/A 우선 + 시드 어휘 매칭 우선)."""
    blocklist = blocklist_substrings or []
    seed_tokens = seed_tokens or set()

    def allowed(k: str) -> bool:
        if any(b in k for b in blocklist):
            return False
        return True

    grade_priority = {"S": 5, "A": 4, "B": 3, "C": 2, "D": 1}

    def relevance_overlap(g: GradedKeyword) -> int:
        if not seed_tokens:
            return 0
        return len(_extract_tokens(g.keyword) & seed_tokens)

    sorted_g = sorted(
        [g for g in graded if allowed(g.keyword)],
        key=lambda x: (relevance_overlap(x), grade_priority.get(x.grade, 0), x.score),
        reverse=True,
    )
    return sorted_g[:n]


if __name__ == "__main__":
    # 시범
    samples = [
        ("아기 냉감패드", 8000, 12000, "중간"),
        ("아기 쿨매트", 15000, 25000, "높음"),
        ("듀라론 패드", 50, 80, "낮음"),
        ("신생아 냉감패드", 1500, 2500, "중간"),
        ("양면 쿨매트", 200, 400, "낮음"),
    ]
    today_month = date.today().month
    graded = [
        grade(kw, pc, mb, comp, peak_month=6, seasonal=True, current_month=today_month)
        for kw, pc, mb, comp in samples
    ]
    print(f"Current month: {today_month} (Peak month: 6)\n")
    for g in graded:
        print(f"  {g.grade}  {g.keyword:<20} {g.total_search:>6}  {g.competition:<5}  score={g.score:>7.0f}")
        for r in g.reasons:
            print(f"      - {r}")
        print()

    main, subs = select_main_and_subs(graded)
    print(f"\n메인: {main.keyword if main else '없음'}")
    print("보조:")
    for s in subs:
        print(f"  - {s.keyword}")
