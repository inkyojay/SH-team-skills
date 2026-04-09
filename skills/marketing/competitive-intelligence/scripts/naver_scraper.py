#!/usr/bin/env python3
"""
네이버 쇼핑 데이터 가공 유틸리티
Claude의 web_search/web_fetch로 수집한 원시 데이터를 구조화하고 분석한다.

Usage:
  # JSON 데이터 파일을 분석
  python3 naver_scraper.py --mode analyze --data collected_data.json
  
  # 감성 분석만 실행
  python3 naver_scraper.py --mode sentiment --data reviews.json
"""

import argparse
import json
import re
import sys


def analyze_products(products):
    """제품 목록 통계 분석"""
    if not products:
        return {"error": "No products found", "total_products": 0}

    prices = [p["price"] for p in products if p.get("price", 0) > 0]
    reviews = [p["review_count"] for p in products if p.get("review_count", 0) > 0]
    sorted_by_reviews = sorted(products, key=lambda x: x.get("review_count", 0), reverse=True)

    analysis = {
        "total_products": len(products),
        "price_stats": {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0,
            "avg": round(sum(prices) / len(prices)) if prices else 0,
            "median": sorted(prices)[len(prices) // 2] if prices else 0,
        },
        "review_stats": {
            "total_reviews": sum(reviews),
            "avg_reviews": round(sum(reviews) / len(reviews)) if reviews else 0,
        },
        "best_sellers": sorted_by_reviews[:10],
        "price_distribution": {},
        "free_shipping_ratio": 0,
        "categories": {},
    }

    for p in prices:
        bracket = f"{(p // 10000) * 10000:,}~{((p // 10000) + 1) * 10000:,}원"
        analysis["price_distribution"][bracket] = analysis["price_distribution"].get(bracket, 0) + 1

    free_count = sum(1 for p in products if p.get("free_shipping"))
    if products:
        analysis["free_shipping_ratio"] = round(free_count / len(products) * 100, 1)

    for p in products:
        cat = p.get("category", "기타")
        analysis["categories"][cat] = analysis["categories"].get(cat, 0) + 1

    return analysis


def analyze_sentiment(texts):
    """키워드 기반 감성 분석"""
    positive_kw = [
        "따뜻", "잘자", "편해", "추천", "재구매", "부드러", "고급", "좋아", "만족",
        "예뻐", "디자인", "넉넉", "가벼", "세탁잘", "빨리", "퀄리티",
    ]
    negative_kw = [
        "비싸", "불편", "사이즈", "세탁", "배송", "품질", "환불", "올풀", "땀",
        "작아", "얇아", "냄새", "뜯어", "별로", "실망", "하자",
    ]

    pos_count = neg_count = neu_count = 0
    pos_keywords = {}
    neg_keywords = {}

    for text in texts:
        if not isinstance(text, str):
            text = str(text)
        matched_pos = matched_neg = False
        for kw in positive_kw:
            if kw in text:
                pos_keywords[kw] = pos_keywords.get(kw, 0) + 1
                matched_pos = True
        for kw in negative_kw:
            if kw in text:
                neg_keywords[kw] = neg_keywords.get(kw, 0) + 1
                matched_neg = True
        if matched_pos and not matched_neg:
            pos_count += 1
        elif matched_neg and not matched_pos:
            neg_count += 1
        else:
            neu_count += 1

    total = pos_count + neg_count + neu_count or 1
    return {
        "positive": {"count": pos_count, "ratio": round(pos_count / total * 100, 1)},
        "negative": {"count": neg_count, "ratio": round(neg_count / total * 100, 1)},
        "neutral": {"count": neu_count, "ratio": round(neu_count / total * 100, 1)},
        "top_positive_keywords": sorted(pos_keywords.items(), key=lambda x: -x[1])[:10],
        "top_negative_keywords": sorted(neg_keywords.items(), key=lambda x: -x[1])[:10],
    }


def extract_promo_keywords(texts):
    """프로모션 키워드 감지"""
    promo_kw = [
        "할인", "세일", "SALE", "특가", "무료배송", "사은품", "증정",
        "1+1", "공구", "체험단", "공동구매", "기획전", "한정", "쿠폰",
        "적립금", "포인트", "오픈기념", "런칭", "이벤트",
    ]
    detected = {}
    for text in texts:
        if not isinstance(text, str):
            continue
        for kw in promo_kw:
            if kw.lower() in text.lower():
                detected[kw] = detected.get(kw, 0) + 1
    return sorted(detected.items(), key=lambda x: -x[1])


def main():
    parser = argparse.ArgumentParser(description="네이버 쇼핑 데이터 분석 유틸리티")
    parser.add_argument("--mode", choices=["analyze", "sentiment", "promo"], required=True)
    parser.add_argument("--data", required=True, help="입력 JSON 파일")
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    result = {}
    if args.mode == "analyze":
        result = analyze_products(data if isinstance(data, list) else data.get("products", []))
    elif args.mode == "sentiment":
        texts = data if isinstance(data, list) else [r.get("text", r.get("summary", "")) for r in data.get("reviews", data)]
        result = analyze_sentiment(texts)
    elif args.mode == "promo":
        texts = data if isinstance(data, list) else [p.get("text", "") for p in data]
        result = {"detected_promos": extract_promo_keywords(texts)}

    out = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
    else:
        print(out)


if __name__ == "__main__":
    main()
