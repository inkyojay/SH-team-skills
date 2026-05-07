#!/usr/bin/env python3
"""
naver_shop.py — 네이버 쇼핑 검색 API (참고용)

용도: 키워드 경쟁 강도 / 카테고리 추정 / 상위 노출 제품 네이밍 패턴.
환경변수: NAVER_CLIENT_ID, NAVER_CLIENT_SECRET (DataLab과 공유).
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from typing import Any

try:
    import requests
except ImportError:
    raise SystemExit("[!] requests 필요")


SHOP_URL = "https://openapi.naver.com/v1/search/shop.json"


@dataclass
class ShopItem:
    title: str
    brand: str
    mall: str
    price: int
    category1: str
    category2: str
    category3: str


@dataclass
class ShopSearchResult:
    keyword: str
    total: int
    items: list[ShopItem]


def _strip_b(s: str) -> str:
    return (s or "").replace("<b>", "").replace("</b>", "").strip()


def search_shop(query: str, display: int = 10) -> ShopSearchResult:
    cid = os.environ.get("NAVER_CLIENT_ID")
    sec = os.environ.get("NAVER_CLIENT_SECRET")
    if not cid or not sec:
        raise RuntimeError("환경변수 NAVER_CLIENT_ID / NAVER_CLIENT_SECRET 필요")

    headers = {
        "X-Naver-Client-Id": cid,
        "X-Naver-Client-Secret": sec,
    }
    params = {"query": query, "display": display, "sort": "sim"}
    try:
        resp = requests.get(SHOP_URL, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  ⚠️  쇼핑 검색 실패 '{query}': {e}", file=sys.stderr)
        return ShopSearchResult(keyword=query, total=0, items=[])

    items = []
    for it in data.get("items", []):
        try:
            price = int(str(it.get("lprice") or "0").replace(",", ""))
        except ValueError:
            price = 0
        items.append(
            ShopItem(
                title=_strip_b(it.get("title", "")),
                brand=str(it.get("brand", "")),
                mall=str(it.get("mallName", "")),
                price=price,
                category1=str(it.get("category1", "")),
                category2=str(it.get("category2", "")),
                category3=str(it.get("category3", "")),
            )
        )
    return ShopSearchResult(keyword=query, total=int(data.get("total", 0)), items=items)


if __name__ == "__main__":
    q = sys.argv[1] if len(sys.argv) > 1 else "아기 냉감패드"
    result = search_shop(q, display=5)
    print(f"[Test] query='{q}' total={result.total}")
    for i, it in enumerate(result.items, 1):
        print(f"  {i}. {it.title[:60]} ({it.mall}, {it.price:,}원)")
        print(f"     카테고리: {it.category1} > {it.category2} > {it.category3}")
