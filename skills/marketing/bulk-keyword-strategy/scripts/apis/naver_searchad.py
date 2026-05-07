#!/usr/bin/env python3
"""
naver_searchad.py — 네이버 검색광고 키워드도구 (keywordstool) 호출

기존 naver-ads-reporter의 NaverAdsClient를 재사용.
시드 키워드 5개씩 묶어 keywordstool API 호출 → 연관 키워드 + 검색량.

응답 키 (네이버 공식):
  relKeyword            : 연관 키워드 (str)
  monthlyPcQcCnt        : 월간 PC 검색수 (int 또는 "< 10")
  monthlyMobileQcCnt    : 월간 모바일 검색수
  monthlyAvePcClkCnt    : 월간 평균 PC 클릭수
  monthlyAveMobileClkCnt: 월간 평균 모바일 클릭수
  monthlyAvePcCtr       : 월간 평균 PC CTR
  compIdx               : 경쟁 정도 ("높음"/"중간"/"낮음")
  plAvgDepth            : 평균 광고 노출 위치
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# 기존 naver-ads-reporter 클라이언트 재사용
# scripts/apis/naver_searchad.py → parents[4] = skills/
_AD_REPORTER_DIR = Path(__file__).resolve().parents[4] / "advertising/naver-ads-reporter/scripts"
sys.path.insert(0, str(_AD_REPORTER_DIR))

try:
    from naver_ads_client import NaverAdsCredentials, NaverAdsClient  # type: ignore
except ImportError as e:
    raise SystemExit(
        f"[!] naver-ads-reporter 모듈을 찾을 수 없습니다: {_AD_REPORTER_DIR}\n원인: {e}"
    )


def _to_int(value: Any) -> int:
    """'< 10' 같은 응답을 0으로, 그 외 숫자로 변환."""
    if value is None:
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    s = str(value).strip()
    if s.startswith("<"):
        return 0
    try:
        return int(s.replace(",", ""))
    except ValueError:
        return 0


@dataclass
class KeywordStat:
    keyword: str
    pc_search: int
    mobile_search: int
    pc_click: float
    mobile_click: float
    competition: str  # 높음 / 중간 / 낮음
    avg_depth: float

    @property
    def total_search(self) -> int:
        return self.pc_search + self.mobile_search

    @property
    def total_click(self) -> float:
        return self.pc_click + self.mobile_click


class KeywordtoolClient:
    """keywordstool API 단순 래퍼."""

    def __init__(self) -> None:
        self.creds = NaverAdsCredentials.from_env()
        self.client = NaverAdsClient(self.creds)

    def lookup(self, hint_keywords: list[str]) -> list[KeywordStat]:
        """
        시드 키워드 (최대 5개) → 연관 키워드 + 검색량 리스트.

        주의: 한 번 호출로 최대 5개 hint, 응답은 ~1000개 키워드까지.
        """
        if not hint_keywords:
            return []
        # 네이버는 최대 5개까지만 받음
        # hintKeywords는 띄어쓰기 없이 보내야 함 (그렇지 않으면 11001 BAD_REQUEST)
        hints = ",".join(k.replace(" ", "").strip() for k in hint_keywords[:5] if k.strip())
        if not hints:
            return []

        params = {
            "hintKeywords": hints,
            "showDetail": 1,
            "includeHintKeywords": 1,
        }
        resp = self.client.request("GET", "/keywordstool", params=params)
        if not resp or not isinstance(resp, dict):
            return []
        items = resp.get("keywordList", []) or []
        results: list[KeywordStat] = []
        for it in items:
            results.append(
                KeywordStat(
                    keyword=str(it.get("relKeyword", "")).strip(),
                    pc_search=_to_int(it.get("monthlyPcQcCnt")),
                    mobile_search=_to_int(it.get("monthlyMobileQcCnt")),
                    pc_click=float(it.get("monthlyAvePcClkCnt") or 0),
                    mobile_click=float(it.get("monthlyAveMobileClkCnt") or 0),
                    competition=str(it.get("compIdx") or "").strip(),
                    avg_depth=float(it.get("plAvgDepth") or 0),
                )
            )
        return results

    def lookup_batched(self, all_seeds: list[str]) -> list[KeywordStat]:
        """5개 묶음으로 분할 호출 후 dedup."""
        seen: dict[str, KeywordStat] = {}
        for i in range(0, len(all_seeds), 5):
            chunk = all_seeds[i : i + 5]
            for stat in self.lookup(chunk):
                if not stat.keyword:
                    continue
                # 같은 키워드가 다른 시드 호출에서도 나오면 더 큰 검색량 기준 유지
                if stat.keyword not in seen or stat.total_search > seen[stat.keyword].total_search:
                    seen[stat.keyword] = stat
        return list(seen.values())


if __name__ == "__main__":
    # CLI 시범 호출
    seeds = sys.argv[1:] or ["아기 냉감패드", "아기 쿨매트"]
    print(f"[Test] hint keywords: {seeds}")
    client = KeywordtoolClient()
    results = client.lookup(seeds)
    print(f"[Result] {len(results)}개 키워드 받음. TOP 10 (검색량 기준):")
    for r in sorted(results, key=lambda x: x.total_search, reverse=True)[:10]:
        print(f"  {r.keyword:<30} PC {r.pc_search:>6}  Mobile {r.mobile_search:>6}  경쟁 {r.competition}")
