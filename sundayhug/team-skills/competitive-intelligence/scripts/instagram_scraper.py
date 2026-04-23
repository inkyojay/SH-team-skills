#!/usr/bin/env python3
"""
인스타그램 공개 프로필 분석 (web 기반)
Usage:
  python3 instagram_scraper.py --username "계정명"
  python3 instagram_scraper.py --hashtag "해시태그"

Note: 인스타그램 직접 스크래핑은 제한이 많아 web_search 폴백을 권장.
이 스크립트는 보조 도구로, SKILL.md의 web_search 기반 분석이 주력 방법.
"""

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "ko-KR,ko;q=0.9",
}


def fetch_url(url, timeout=15):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return None


def analyze_instagram_via_search(brand_name):
    """web search를 통한 인스타그램 정보 수집 (폴백 방법)"""
    results = {
        "brand": brand_name,
        "method": "web_search_fallback",
        "note": "인스타그램 직접 접근 제한으로 검색 기반 수집. Claude의 web_search 도구 사용 권장.",
        "suggested_searches": [
            f"{brand_name} 인스타그램 팔로워",
            f"site:instagram.com {brand_name}",
            f"{brand_name} 인스타 마케팅",
            f"{brand_name} 인플루언서 협찬",
            f"{brand_name} 인스타 이벤트",
        ],
        "analysis_template": {
            "followers": None,
            "posting_frequency": None,
            "content_types": {
                "product_shots": 0,
                "lifestyle": 0,
                "ugc": 0,
                "event": 0,
                "reels": 0,
            },
            "avg_likes": None,
            "avg_comments": None,
            "top_hashtags": [],
            "sponsored_ratio": None,
        }
    }
    return results


def main():
    parser = argparse.ArgumentParser(description="인스타그램 분석")
    parser.add_argument("--brand", required=True, help="브랜드명")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    result = analyze_instagram_via_search(args.brand)
    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
