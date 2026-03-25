#!/usr/bin/env python3
"""
네이버 쇼핑 검색 API + 데이터랩 쇼핑인사이트 API 통합 분석 스크립트

5가지 분석 기능:
1. 경쟁사 제품 자동 수집 (쇼핑 검색)
2. 가격대 분석 (쇼핑 검색)
3. 시즌별 수요 트렌드 (데이터랩)
4. 타겟 고객 검증 — 성별/연령별 (데이터랩)
5. 브랜드 점유율 추정 (쇼핑 검색)

사용법:
  # 쇼핑 검색 분석 (기능 1,2,5)
  python naver_shopping_analysis.py search \
    --client-id YOUR_CLIENT_ID \
    --client-secret YOUR_CLIENT_SECRET \
    --query "아기 쿨매트" \
    --total 100 \
    --output shopping_results.json

  # 데이터랩 트렌드 분석 (기능 3,4)
  python naver_shopping_analysis.py trend \
    --client-id YOUR_CLIENT_ID \
    --client-secret YOUR_CLIENT_SECRET \
    --category "50000008" \
    --keywords "아기 쿨매트,아기 냉감패드,아기 여름이불" \
    --start-date "2025-01-01" \
    --end-date "2026-03-01" \
    --output trend_results.json

필요한 인증: 네이버 개발자센터 (developers.naver.com) 애플리케이션의
Client ID / Client Secret (검색광고 API와 별도)
"""

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests


# ============================================================
# PART 1: 쇼핑 검색 API (경쟁사 수집 + 가격 분석 + 브랜드 점유율)
# ============================================================

SEARCH_URL = "https://openapi.naver.com/v1/search/shop.json"


def fetch_shopping_results(client_id: str, client_secret: str, query: str, total: int = 100) -> list:
    """네이버 쇼핑 검색 결과를 페이지네이션으로 수집"""
    all_items = []
    display = 100  # 한 페이지당 최대 100개
    pages = (min(total, 1000) + display - 1) // display

    print(f"\n🛒 '{query}' 쇼핑 검색 중... (최대 {min(total, 1000)}개)")

    for page in range(pages):
        start = page * display + 1
        if start > 1000:
            break

        params = {
            "query": query,
            "display": display,
            "start": start,
            "sort": "sim",  # sim: 정확도순, date: 날짜순, asc: 가격오름, dsc: 가격내림
            "exclude": "used:rental:cbshop"  # 중고/렌탈/해외구매대행 제외
        }

        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

        try:
            url = f"{SEARCH_URL}?{urllib.parse.urlencode(params)}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                items = data.get("items", [])
                all_items.extend(items)
                print(f"  ✅ 페이지 {page+1}/{pages}: {len(items)}개 수집")

                if len(items) < display:
                    break
            else:
                print(f"  ❌ HTTP {response.status_code}: {response.text[:100]}")
                break

        except Exception as e:
            print(f"  ❌ 요청 실패: {e}")
            break

        time.sleep(0.2)

    print(f"  총 {len(all_items)}개 상품 수집 완료")
    return all_items


def clean_html(text: str) -> str:
    """HTML 태그 제거"""
    import re
    return re.sub(r'<[^>]+>', '', text)


def analyze_products(items: list, query: str) -> dict:
    """수집된 상품 데이터로 3가지 분석 수행"""

    # 데이터 정리
    cleaned = []
    for item in items:
        price = int(item.get("lprice", 0))
        if price <= 0:
            continue
        cleaned.append({
            "title": clean_html(item.get("title", "")),
            "link": item.get("link", ""),
            "image": item.get("image", ""),
            "price": price,
            "hprice": int(item.get("hprice") or 0),
            "mall": item.get("mallName", ""),
            "brand": item.get("brand", ""),
            "maker": item.get("maker", ""),
            "category1": item.get("category1", ""),
            "category2": item.get("category2", ""),
            "category3": item.get("category3", ""),
            "category4": item.get("category4", ""),
        })

    if not cleaned:
        return {"error": "유효한 상품 데이터가 없습니다"}

    # ── 분석 1: 경쟁사 제품 목록 ──
    top_products = sorted(cleaned, key=lambda x: x["price"])[:30]  # 가격순 상위 30개

    # ── 분석 2: 가격대 분석 ──
    prices = [p["price"] for p in cleaned]
    prices.sort()
    n = len(prices)

    price_analysis = {
        "total_products": n,
        "min_price": prices[0],
        "max_price": prices[-1],
        "avg_price": round(sum(prices) / n),
        "median_price": prices[n // 2],
        "q1_price": prices[n // 4],  # 25% 분위
        "q3_price": prices[3 * n // 4],  # 75% 분위
        "price_ranges": {}
    }

    # 가격대별 분포
    ranges = [
        ("1만원 미만", 0, 10000),
        ("1~3만원", 10000, 30000),
        ("3~5만원", 30000, 50000),
        ("5~7만원", 50000, 70000),
        ("7~10만원", 70000, 100000),
        ("10만원 이상", 100000, float("inf"))
    ]
    for label, low, high in ranges:
        count = sum(1 for p in prices if low <= p < high)
        price_analysis["price_ranges"][label] = {
            "count": count,
            "ratio": round(count / n * 100, 1)
        }

    # 프리미엄 가격 기준 (상위 25%)
    premium_threshold = prices[3 * n // 4]
    price_analysis["premium_threshold"] = premium_threshold
    price_analysis["premium_suggestion"] = f"{int(premium_threshold * 0.9):,}원 ~ {int(premium_threshold * 1.2):,}원"

    # ── 분석 5: 브랜드 점유율 ──
    brand_counter = Counter()
    mall_counter = Counter()
    maker_counter = Counter()

    for p in cleaned:
        brand = p["brand"].strip()
        mall = p["mall"].strip()
        maker = p["maker"].strip()
        if brand:
            brand_counter[brand] += 1
        if mall:
            mall_counter[mall] += 1
        if maker:
            maker_counter[maker] += 1

    brand_share = []
    for brand, count in brand_counter.most_common(15):
        brand_share.append({
            "brand": brand,
            "count": count,
            "share": round(count / n * 100, 1)
        })

    mall_share = []
    for mall, count in mall_counter.most_common(10):
        mall_share.append({
            "mall": mall,
            "count": count,
            "share": round(count / n * 100, 1)
        })

    return {
        "query": query,
        "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_products": n,

        # 분석 1: 경쟁사 제품 목록
        "top_products": top_products,

        # 분석 2: 가격대 분석
        "price_analysis": price_analysis,

        # 분석 5: 브랜드 점유율
        "brand_share": brand_share,
        "mall_share": mall_share,

        # 추천 가격 포지셔닝
        "pricing_recommendation": {
            "value_zone": f"{prices[n//4]:,}원 이하",
            "mainstream_zone": f"{prices[n//4]:,}원 ~ {prices[3*n//4]:,}원",
            "premium_zone": f"{prices[3*n//4]:,}원 이상",
            "recommendation": f"프리미엄 포지셔닝 시 {int(premium_threshold * 0.9):,}~{int(premium_threshold * 1.2):,}원 권장"
        }
    }


# ============================================================
# PART 2: 데이터랩 쇼핑인사이트 API (시즌 트렌드 + 타겟 검증)
# ============================================================

DATALAB_BASE = "https://openapi.naver.com/v1/datalab/shopping"


def fetch_category_trend(client_id: str, client_secret: str,
                         category_id: str, category_name: str,
                         start_date: str, end_date: str,
                         time_unit: str = "month") -> dict:
    """카테고리별 검색 클릭 추이 (시즌 분석)"""
    url = f"{DATALAB_BASE}/categories"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "category": [
            {"name": category_name, "param": [category_id]}
        ]
    }

    print(f"\n📈 카테고리 트렌드 조회: {category_name} ({start_date} ~ {end_date})")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 트렌드 데이터 {len(data.get('results', [{}])[0].get('data', []))}개 기간 수집")
            return data
        else:
            print(f"  ❌ HTTP {response.status_code}: {response.text[:200]}")
            return {"error": response.text}
    except Exception as e:
        print(f"  ❌ 요청 실패: {e}")
        return {"error": str(e)}


def fetch_keyword_trend(client_id: str, client_secret: str,
                        category_id: str, category_name: str,
                        keywords: list,
                        start_date: str, end_date: str,
                        time_unit: str = "month") -> dict:
    """키워드별 검색 클릭 추이"""
    url = f"{DATALAB_BASE}/category/keywords"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }

    keyword_groups = []
    for kw in keywords[:5]:  # 최대 5개
        keyword_groups.append({
            "name": kw,
            "param": [kw]
        })

    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "category": category_id,
        "keyword": keyword_groups
    }

    print(f"\n🔑 키워드별 트렌드 조회: {', '.join(keywords[:5])}")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ 키워드 트렌드 데이터 수집 완료")
            return data
        else:
            print(f"  ❌ HTTP {response.status_code}: {response.text[:200]}")
            return {"error": response.text}
    except Exception as e:
        print(f"  ❌ 요청 실패: {e}")
        return {"error": str(e)}


def fetch_gender_trend(client_id: str, client_secret: str,
                       category_id: str, category_name: str,
                       start_date: str, end_date: str) -> dict:
    """성별 검색 클릭 추이"""
    url = f"{DATALAB_BASE}/category/gender"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "month",
        "category": [
            {"name": category_name, "param": [category_id]}
        ]
    }

    print(f"\n👫 성별 트렌드 조회: {category_name}")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ❌ HTTP {response.status_code}")
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}


def fetch_age_trend(client_id: str, client_secret: str,
                    category_id: str, category_name: str,
                    start_date: str, end_date: str) -> dict:
    """연령별 검색 클릭 추이"""
    url = f"{DATALAB_BASE}/category/age"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "month",
        "category": [
            {"name": category_name, "param": [category_id]}
        ]
    }

    print(f"\n👶 연령별 트렌드 조회: {category_name}")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ❌ HTTP {response.status_code}")
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}


def fetch_device_trend(client_id: str, client_secret: str,
                       category_id: str, category_name: str,
                       start_date: str, end_date: str) -> dict:
    """기기별(PC/모바일) 검색 클릭 추이"""
    url = f"{DATALAB_BASE}/category/device"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
        "Content-Type": "application/json"
    }
    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": "month",
        "category": [
            {"name": category_name, "param": [category_id]}
        ]
    }

    print(f"\n📱 기기별 트렌드 조회: {category_name}")

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"  ❌ HTTP {response.status_code}")
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# 출력 & 메인
# ============================================================

def print_search_summary(results: dict):
    """쇼핑 검색 분석 결과 요약 출력"""
    print(f"\n{'='*60}")
    print(f"🛒 네이버 쇼핑 분석 결과: '{results['query']}'")
    print(f"{'='*60}")
    print(f"분석일시: {results['analysis_date']}")
    print(f"수집 상품: {results['total_products']}개\n")

    # 가격 분석
    pa = results["price_analysis"]
    print(f"💰 가격대 분석")
    print(f"  최저가: {pa['min_price']:,}원")
    print(f"  최고가: {pa['max_price']:,}원")
    print(f"  평균가: {pa['avg_price']:,}원")
    print(f"  중앙값: {pa['median_price']:,}원")
    print(f"  하위25%: {pa['q1_price']:,}원")
    print(f"  상위25%: {pa['q3_price']:,}원")
    print(f"\n  가격대별 분포:")
    for label, info in pa["price_ranges"].items():
        bar = "█" * int(info["ratio"] / 2)
        print(f"    {label:12} {bar:20} {info['count']:3}개 ({info['ratio']}%)")

    # 브랜드 점유율
    print(f"\n🏷️ 브랜드 점유율 TOP 10")
    for b in results["brand_share"][:10]:
        bar = "█" * int(b["share"])
        print(f"  {b['brand']:15} {bar:20} {b['count']:3}개 ({b['share']}%)")

    # 추천 가격
    pr = results["pricing_recommendation"]
    print(f"\n🎯 가격 포지셔닝 추천")
    print(f"  가성비 구간: {pr['value_zone']}")
    print(f"  주류 구간:   {pr['mainstream_zone']}")
    print(f"  프리미엄:    {pr['premium_zone']}")
    print(f"  → {pr['recommendation']}")

    # 상위 제품
    print(f"\n📦 주요 경쟁 제품 (가격순 상위 10개)")
    for i, p in enumerate(results["top_products"][:10], 1):
        print(f"  {i:2}. {p['title'][:40]:42} {p['price']:>8,}원  [{p['brand'] or p['mall']}]")


def print_trend_summary(trend_data: dict, gender_data: dict, age_data: dict, device_data: dict):
    """트렌드 분석 결과 요약 출력"""
    print(f"\n{'='*60}")
    print(f"📈 네이버 쇼핑인사이트 트렌드 분석")
    print(f"{'='*60}")

    # 시즌 트렌드
    if "results" in trend_data:
        for result in trend_data["results"]:
            print(f"\n📅 시즌별 수요 추이: {result.get('title', '')}")
            data_points = result.get("data", [])
            if data_points:
                max_val = max(d["ratio"] for d in data_points)
                for d in data_points:
                    period = d["period"]
                    ratio = d["ratio"]
                    bar_len = int(ratio / max_val * 30) if max_val > 0 else 0
                    bar = "█" * bar_len
                    peak = " ← 피크!" if ratio == max_val and ratio > 0 else ""
                    print(f"  {period} {bar:30} {ratio:6.1f}{peak}")

    # 성별
    if "results" in gender_data:
        print(f"\n👫 성별 검색 비율")
        for result in gender_data["results"]:
            title = result.get("title", "")
            data_points = result.get("data", [])
            if data_points:
                latest = data_points[-1]
                print(f"  {title}: {latest.get('group', '')} — 비율 {latest.get('ratio', 0):.1f}")

    # 연령별
    if "results" in age_data:
        print(f"\n👶 연령별 검색 비율")
        for result in age_data["results"]:
            title = result.get("title", "")
            data_points = result.get("data", [])
            if data_points:
                latest = data_points[-1]
                print(f"  {title}: {latest.get('group', '')} — 비율 {latest.get('ratio', 0):.1f}")


def main():
    parser = argparse.ArgumentParser(description="네이버 쇼핑 통합 분석")
    subparsers = parser.add_subparsers(dest="command")

    # 쇼핑 검색 분석
    search_parser = subparsers.add_parser("search", help="쇼핑 검색 분석 (경쟁사/가격/점유율)")
    search_parser.add_argument("--client-id", required=True)
    search_parser.add_argument("--client-secret", required=True)
    search_parser.add_argument("--query", required=True, help="검색 키워드")
    search_parser.add_argument("--total", type=int, default=100, help="수집할 상품 수 (최대 1000)")
    search_parser.add_argument("--output", default="shopping_analysis.json")

    # 트렌드 분석
    trend_parser = subparsers.add_parser("trend", help="트렌드 분석 (시즌/성별/연령)")
    trend_parser.add_argument("--client-id", required=True)
    trend_parser.add_argument("--client-secret", required=True)
    trend_parser.add_argument("--category", required=True, help="네이버 쇼핑 카테고리 ID")
    trend_parser.add_argument("--category-name", default="분석 카테고리")
    trend_parser.add_argument("--keywords", default="", help="쉼표 구분 키워드 (최대 5개)")
    trend_parser.add_argument("--start-date", default="2025-01-01")
    trend_parser.add_argument("--end-date", default="2026-03-01")
    trend_parser.add_argument("--output", default="trend_analysis.json")

    # 통합 분석
    full_parser = subparsers.add_parser("full", help="전체 통합 분석")
    full_parser.add_argument("--client-id", required=True)
    full_parser.add_argument("--client-secret", required=True)
    full_parser.add_argument("--query", required=True)
    full_parser.add_argument("--category", required=True)
    full_parser.add_argument("--category-name", default="분석 카테고리")
    full_parser.add_argument("--keywords", default="")
    full_parser.add_argument("--start-date", default="2025-01-01")
    full_parser.add_argument("--end-date", default="2026-03-01")
    full_parser.add_argument("--total", type=int, default=100)
    full_parser.add_argument("--output", default="full_analysis.json")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "search":
        items = fetch_shopping_results(args.client_id, args.client_secret, args.query, args.total)
        results = analyze_products(items, args.query)
        print_search_summary(results)

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 결과 저장: {args.output}")

    elif args.command == "trend":
        trend = fetch_category_trend(args.client_id, args.client_secret,
                                     args.category, args.category_name,
                                     args.start_date, args.end_date)
        gender = fetch_gender_trend(args.client_id, args.client_secret,
                                    args.category, args.category_name,
                                    args.start_date, args.end_date)
        age = fetch_age_trend(args.client_id, args.client_secret,
                              args.category, args.category_name,
                              args.start_date, args.end_date)
        device = fetch_device_trend(args.client_id, args.client_secret,
                                    args.category, args.category_name,
                                    args.start_date, args.end_date)

        keyword_trend = {}
        if args.keywords:
            kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
            keyword_trend = fetch_keyword_trend(args.client_id, args.client_secret,
                                                args.category, args.category_name,
                                                kws, args.start_date, args.end_date)

        results = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category_trend": trend,
            "gender_trend": gender,
            "age_trend": age,
            "device_trend": device,
            "keyword_trend": keyword_trend
        }

        print_trend_summary(trend, gender, age, device)

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 결과 저장: {args.output}")

    elif args.command == "full":
        print("🚀 전체 통합 분석 시작\n")

        # 쇼핑 검색
        items = fetch_shopping_results(args.client_id, args.client_secret, args.query, args.total)
        search_results = analyze_products(items, args.query)

        # 트렌드
        trend = fetch_category_trend(args.client_id, args.client_secret,
                                     args.category, args.category_name,
                                     args.start_date, args.end_date)
        gender = fetch_gender_trend(args.client_id, args.client_secret,
                                    args.category, args.category_name,
                                    args.start_date, args.end_date)
        age = fetch_age_trend(args.client_id, args.client_secret,
                              args.category, args.category_name,
                              args.start_date, args.end_date)
        device = fetch_device_trend(args.client_id, args.client_secret,
                                    args.category, args.category_name,
                                    args.start_date, args.end_date)

        keyword_trend = {}
        if args.keywords:
            kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
            keyword_trend = fetch_keyword_trend(args.client_id, args.client_secret,
                                                args.category, args.category_name,
                                                kws, args.start_date, args.end_date)

        full_results = {
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "query": args.query,
            "shopping_analysis": search_results,
            "trend_analysis": {
                "category_trend": trend,
                "gender_trend": gender,
                "age_trend": age,
                "device_trend": device,
                "keyword_trend": keyword_trend
            }
        }

        print_search_summary(search_results)
        print_trend_summary(trend, gender, age, device)

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(full_results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 전체 결과 저장: {args.output}")


if __name__ == "__main__":
    main()
