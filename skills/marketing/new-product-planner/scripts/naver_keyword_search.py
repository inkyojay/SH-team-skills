#!/usr/bin/env python3
"""
네이버 검색광고 API를 활용한 키워드 검색량 조회 스크립트

사용법:
  python naver_keyword_search.py \
    --api-key YOUR_API_KEY \
    --secret-key YOUR_SECRET_KEY \
    --customer-id YOUR_CUSTOMER_ID \
    --keywords "키워드1,키워드2,키워드3" \
    --output results.json

키워드는 쉼표로 구분하며, 5개씩 배치로 API를 호출합니다.
"""

import argparse
import base64
import hashlib
import hmac
import json
import sys
import time
import urllib.parse
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests


API_URL = "https://api.searchad.naver.com"
KEYWORD_TOOL_PATH = "/keywordstool"


def generate_signature(timestamp: str, method: str, path: str, secret_key: str) -> str:
    """HMAC-SHA256 서명 생성 (base64 인코딩)"""
    message = f"{timestamp}.{method}.{path}"
    sign = hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    return base64.b64encode(sign).decode("utf-8")


def get_headers(api_key: str, secret_key: str, customer_id: str, method: str = "GET", path: str = KEYWORD_TOOL_PATH) -> dict:
    """API 요청 헤더 생성"""
    timestamp = str(int(time.time() * 1000))
    signature = generate_signature(timestamp, method, path, secret_key)
    return {
        "X-Timestamp": timestamp,
        "X-API-KEY": api_key,
        "X-Customer": customer_id,
        "X-Signature": signature,
        "Content-Type": "application/json"
    }


def fetch_keywords(api_key: str, secret_key: str, customer_id: str, keywords: list, show_detail: int = 1) -> list:
    """
    키워드 검색량 조회
    - 키워드를 5개씩 묶어서 배치 호출
    - API rate limit 고려하여 호출 간 0.5초 대기
    """
    all_results = []
    batches = [keywords[i:i+5] for i in range(0, len(keywords), 5)]
    
    print(f"\n📊 총 {len(keywords)}개 키워드를 {len(batches)}개 배치로 조회합니다...\n")
    
    for batch_idx, batch in enumerate(batches):
        hint = ",".join(batch)
        params = {
            "hintKeywords": hint,
            "showDetail": show_detail
        }
        
        headers = get_headers(api_key, secret_key, customer_id)
        url = f"{API_URL}{KEYWORD_TOOL_PATH}"
        
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                keyword_list = data.get("keywordList", [])
                all_results.extend(keyword_list)
                print(f"  ✅ 배치 {batch_idx + 1}/{len(batches)}: {len(keyword_list)}개 결과 ({', '.join(batch)})")
            else:
                print(f"  ❌ 배치 {batch_idx + 1}/{len(batches)}: HTTP {response.status_code}")
                print(f"     응답: {response.text[:200]}")
                
        except requests.exceptions.RequestException as e:
            print(f"  ❌ 배치 {batch_idx + 1}/{len(batches)}: 요청 실패 - {e}")
        
        # Rate limit 방지
        if batch_idx < len(batches) - 1:
            time.sleep(0.5)
    
    return all_results


def classify_keyword(total_search: int, comp_idx: str) -> str:
    """키워드 등급 분류"""
    if total_search >= 10000:
        return "빅"
    elif total_search >= 1000 and comp_idx in ["낮음", "low"]:
        return "골든"
    elif total_search >= 1000:
        return "성장"
    elif total_search >= 100:
        return "성장" if comp_idx in ["낮음", "low", "중간", "medium"] else "니치"
    else:
        return "니치"


def parse_search_count(value) -> int:
    """검색량 값 파싱 (< 10 같은 문자열 처리)"""
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        cleaned = value.replace("<", "").replace(",", "").strip()
        try:
            return int(cleaned)
        except ValueError:
            return 0
    return 0


def process_results(raw_results: list, target_keywords: list) -> dict:
    """
    결과 가공:
    - 입력 키워드에 대한 결과만 필터링 (연관 키워드도 포함 옵션)
    - 등급 분류
    - 정렬
    """
    target_set = set(k.strip().lower() for k in target_keywords)
    
    processed = []
    related_keywords = []
    
    for item in raw_results:
        keyword = item.get("relKeyword", "")
        pc = parse_search_count(item.get("monthlyPcQcCnt", 0))
        mobile = parse_search_count(item.get("monthlyMobileQcCnt", 0))
        total = pc + mobile
        
        comp_idx = item.get("compIdx", "")
        avg_pc_click = item.get("monthlyAvePcClkCnt", 0)
        avg_mobile_click = item.get("monthlyAveMobileClkCnt", 0)
        avg_pc_ctr = item.get("monthlyAvePcCtr", 0)
        avg_mobile_ctr = item.get("monthlyAveMobileCtr", 0)
        ad_depth = item.get("plAvgDepth", 0)
        
        grade = classify_keyword(total, comp_idx)
        mobile_ratio = round(mobile / total * 100, 1) if total > 0 else 0
        
        entry = {
            "keyword": keyword,
            "pc_search": pc,
            "mobile_search": mobile,
            "total_search": total,
            "competition": comp_idx,
            "avg_pc_click": avg_pc_click,
            "avg_mobile_click": avg_mobile_click,
            "avg_pc_ctr": avg_pc_ctr,
            "avg_mobile_ctr": avg_mobile_ctr,
            "ad_depth": ad_depth,
            "grade": grade,
            "mobile_ratio": mobile_ratio
        }
        
        if keyword.strip().lower() in target_set:
            processed.append(entry)
        else:
            related_keywords.append(entry)
    
    # 총 검색량 기준 내림차순 정렬
    processed.sort(key=lambda x: x["total_search"], reverse=True)
    related_keywords.sort(key=lambda x: x["total_search"], reverse=True)
    
    # 등급별 분류
    golden = [k for k in processed if k["grade"] == "골든"]
    growth = [k for k in processed if k["grade"] == "성장"]
    big = [k for k in processed if k["grade"] == "빅"]
    niche = [k for k in processed if k["grade"] == "니치"]
    
    return {
        "query_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_queried": len(target_keywords),
        "total_results": len(processed),
        "total_related": len(related_keywords),
        "summary": {
            "golden_count": len(golden),
            "growth_count": len(growth),
            "big_count": len(big),
            "niche_count": len(niche)
        },
        "keywords": processed,
        "related_keywords": related_keywords[:30],  # 상위 30개만
        "by_grade": {
            "golden": golden,
            "growth": growth,
            "big": big,
            "niche": niche
        }
    }


def print_summary(results: dict):
    """콘솔에 결과 요약 출력"""
    print(f"\n{'='*60}")
    print(f"📊 네이버 키워드 검색량 조회 결과")
    print(f"{'='*60}")
    print(f"조회일시: {results['query_date']}")
    print(f"입력 키워드: {results['total_queried']}개")
    print(f"매칭 결과: {results['total_results']}개")
    print(f"연관 키워드: {results['total_related']}개")
    print(f"\n등급 분포:")
    print(f"  🏆 골든 (최우선 공략): {results['summary']['golden_count']}개")
    print(f"  📈 성장 (선점 기회):   {results['summary']['growth_count']}개")
    print(f"  🔥 빅 (참고용):       {results['summary']['big_count']}개")
    print(f"  🔹 니치 (보조):       {results['summary']['niche_count']}개")
    
    print(f"\n{'─'*60}")
    print(f"{'키워드':<25} {'총검색량':>8} {'경쟁도':>6} {'등급':>4}")
    print(f"{'─'*60}")
    
    for kw in results["keywords"][:20]:
        print(f"{kw['keyword']:<25} {kw['total_search']:>8,} {kw['competition']:>6} {kw['grade']:>4}")
    
    if len(results["keywords"]) > 20:
        print(f"\n  ... 외 {len(results['keywords']) - 20}개 (전체 결과는 JSON 파일 참조)")
    
    if results["related_keywords"]:
        print(f"\n{'─'*60}")
        print(f"💡 추가 발견된 연관 키워드 TOP 10:")
        print(f"{'─'*60}")
        for kw in results["related_keywords"][:10]:
            print(f"  {kw['keyword']:<25} {kw['total_search']:>8,} {kw['competition']:>6}")


def main():
    parser = argparse.ArgumentParser(description="네이버 키워드 검색량 조회")
    parser.add_argument("--api-key", required=True, help="네이버 API 키")
    parser.add_argument("--secret-key", required=True, help="네이버 시크릿 키")
    parser.add_argument("--customer-id", required=True, help="네이버 고객 ID")
    parser.add_argument("--keywords", required=True, help="쉼표로 구분된 키워드 목록")
    parser.add_argument("--output", default="keyword_results.json", help="결과 저장 파일명")
    parser.add_argument("--include-related", action="store_true", help="연관 키워드도 포함")
    
    args = parser.parse_args()
    
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    
    if not keywords:
        print("❌ 키워드가 없습니다.")
        sys.exit(1)
    
    # API 호출
    raw_results = fetch_keywords(
        args.api_key, args.secret_key, args.customer_id, keywords
    )
    
    if not raw_results:
        print("❌ API 결과가 없습니다. 인증 정보를 확인해주세요.")
        sys.exit(1)
    
    # 결과 가공
    results = process_results(raw_results, keywords)
    
    # 결과 출력
    print_summary(results)
    
    # JSON 저장
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 전체 결과가 {args.output}에 저장되었습니다.")
    
    return results


if __name__ == "__main__":
    main()
