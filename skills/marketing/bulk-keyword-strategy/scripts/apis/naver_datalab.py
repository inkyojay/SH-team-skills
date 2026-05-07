#!/usr/bin/env python3
"""
naver_datalab.py — 네이버 DataLab 쇼핑인사이트 키워드 트렌드

사용처: 키워드의 12개월 검색 트렌드 → 시즌성 / 피크 월 판정

환경변수:
  NAVER_CLIENT_ID
  NAVER_CLIENT_SECRET

엔드포인트: https://openapi.naver.com/v1/datalab/shopping/category/keywords
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any

try:
    import requests
except ImportError:
    raise SystemExit("[!] requests 필요: pip install requests")


DATALAB_URL = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
TIMEOUT = 30


@dataclass
class DataLabCredentials:
    client_id: str
    client_secret: str

    @classmethod
    def from_env(cls) -> "DataLabCredentials":
        cid = os.environ.get("NAVER_CLIENT_ID")
        sec = os.environ.get("NAVER_CLIENT_SECRET")
        if not cid or not sec:
            raise RuntimeError(
                "환경변수 누락: NAVER_CLIENT_ID / NAVER_CLIENT_SECRET\n"
                "developers.naver.com에서 애플리케이션 등록 후 발급받으세요."
            )
        return cls(client_id=cid, client_secret=sec)


@dataclass
class TrendPoint:
    period: str  # YYYY-MM-DD
    ratio: float


@dataclass
class KeywordTrend:
    keyword: str
    points: list[TrendPoint]

    @property
    def peak_month(self) -> int | None:
        """검색량 피크 달 (1~12). None = 데이터 없음."""
        if not self.points:
            return None
        peak = max(self.points, key=lambda p: p.ratio)
        try:
            return int(peak.period.split("-")[1])
        except (IndexError, ValueError):
            return None

    @property
    def peak_ratio(self) -> float:
        return max((p.ratio for p in self.points), default=0.0)

    @property
    def current_vs_peak(self) -> float:
        """현재(가장 최근) ratio가 피크 대비 몇 % 인지."""
        if not self.points or self.peak_ratio == 0:
            return 0.0
        latest = self.points[-1].ratio
        return (latest / self.peak_ratio) * 100.0

    @property
    def is_seasonal(self) -> bool:
        """시즌성 여부 (피크 vs 평균이 2배 이상이면 시즌성)."""
        if len(self.points) < 6:
            return False
        avg = sum(p.ratio for p in self.points) / len(self.points)
        if avg == 0:
            return False
        return (self.peak_ratio / avg) >= 2.0


# 출산/육아 카테고리 코드 (네이버 쇼핑인사이트 기본)
DEFAULT_BABY_CATEGORY = "50000005"


class DataLabClient:
    def __init__(self) -> None:
        self.creds = DataLabCredentials.from_env()
        self.session = requests.Session()

    def keyword_trends(
        self,
        keywords: list[str],
        category: str = DEFAULT_BABY_CATEGORY,
        months: int = 12,
        time_unit: str = "month",
    ) -> list[KeywordTrend]:
        """
        지정 키워드의 카테고리 내 검색 트렌드 (지난 N개월).

        주의: API는 한 번에 최대 5개 키워드 그룹까지만.
        """
        if not keywords:
            return []
        end = date.today()
        start = end - timedelta(days=months * 31)

        results: list[KeywordTrend] = []
        for i in range(0, len(keywords), 5):
            chunk = keywords[i : i + 5]
            body = {
                "startDate": start.strftime("%Y-%m-%d"),
                "endDate": end.strftime("%Y-%m-%d"),
                "timeUnit": time_unit,
                "category": category,
                "keyword": [{"name": k, "param": [k]} for k in chunk],
            }
            headers = {
                "X-Naver-Client-Id": self.creds.client_id,
                "X-Naver-Client-Secret": self.creds.client_secret,
                "Content-Type": "application/json",
            }
            try:
                resp = self.session.post(
                    DATALAB_URL,
                    headers=headers,
                    data=json.dumps(body),
                    timeout=TIMEOUT,
                )
                resp.raise_for_status()
                data = resp.json()
            except Exception as e:
                print(f"  ⚠️  DataLab 호출 실패 ({chunk}): {e}", file=sys.stderr)
                continue

            for entry in data.get("results", []):
                points = [
                    TrendPoint(period=p["period"], ratio=float(p["ratio"]))
                    for p in entry.get("data", [])
                ]
                results.append(KeywordTrend(keyword=entry.get("title", ""), points=points))
        return results


if __name__ == "__main__":
    keywords = sys.argv[1:] or ["아기 냉감패드", "아기 쿨매트"]
    print(f"[Test] keywords: {keywords}")
    client = DataLabClient()
    trends = client.keyword_trends(keywords)
    for t in trends:
        print(f"\n  📈 {t.keyword}")
        print(f"     peak_month: {t.peak_month}")
        print(f"     peak_ratio: {t.peak_ratio:.2f}")
        print(f"     current vs peak: {t.current_vs_peak:.1f}%")
        print(f"     seasonal: {t.is_seasonal}")
