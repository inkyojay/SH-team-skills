#!/usr/bin/env python3
"""
네이버 검색 API 통합 고객 목소리(VOC) 분석 스크립트

동일한 네이버 개발자센터 Client ID/Secret으로 5가지 검색 API를 활용:
1. 카페글 검색 (맘카페 분석) — 실제 부모들의 고민/추천/불만 수집
2. 블로그 검색 (리뷰 분석) — 체험후기, 경쟁사 리뷰 키워드 추출
3. 지식인 검색 (질문 분석) — 구매 전 고민, 미충족 니즈 발견
4. 뉴스 검색 (시장 동향) — 업계 뉴스, 신소재, 경쟁사 보도
5. 데이터랩 검색어 트렌드 — 키워드 검색량 상대 추이

사용법:
  # 전체 VOC 분석 (5가지 전부)
  python naver_voc_analysis.py full \
    --client-id YOUR_ID --client-secret YOUR_SECRET \
    --query "아기 쿨매트" \
    --trend-keywords "아기 쿨매트,아기 냉감패드,아기 여름이불" \
    --output voc_results.json

  # 개별 분석
  python naver_voc_analysis.py cafe --query "아기 쿨매트 추천" ...
  python naver_voc_analysis.py blog --query "아기 쿨매트 후기" ...
  python naver_voc_analysis.py kin  --query "아기 쿨매트" ...
  python naver_voc_analysis.py news --query "아기 냉감 수면용품" ...
  python naver_voc_analysis.py trend --keywords "아기 쿨매트,냉감패드" ...
"""

import argparse
import json
import re
import sys
import time
import urllib.parse
from collections import Counter
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests


SEARCH_BASE = "https://openapi.naver.com/v1/search"
DATALAB_URL = "https://openapi.naver.com/v1/datalab/search"


def clean_html(text: str) -> str:
    return re.sub(r'<[^>]+>', '', text).strip()


def make_headers(client_id: str, client_secret: str, content_type=None) -> dict:
    h = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    if content_type:
        h["Content-Type"] = content_type
    return h


def search_naver(client_id, client_secret, service, query, total=100, sort="sim"):
    """네이버 검색 API 공통 호출 (blog/cafearticle/kin/news)"""
    all_items = []
    display = 100
    pages = (min(total, 1000) + display - 1) // display
    headers = make_headers(client_id, client_secret)

    svc_names = {"blog": "블로그", "cafearticle": "카페글", "kin": "지식인", "news": "뉴스"}
    print(f"\n🔍 {svc_names.get(service, service)} 검색: '{query}' (최대 {min(total,1000)}개)")

    for page in range(pages):
        start = page * display + 1
        if start > 1000:
            break
        params = {"query": query, "display": display, "start": start, "sort": sort}
        try:
            url = f"{SEARCH_BASE}/{service}.json?{urllib.parse.urlencode(params)}"
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                all_items.extend(items)
                total_found = data.get("total", 0)
                print(f"  ✅ 페이지 {page+1}: {len(items)}개 수집 (총 검색결과 {total_found:,}건)")
                if len(items) < display:
                    break
            else:
                print(f"  ❌ HTTP {resp.status_code}: {resp.text[:100]}")
                break
        except Exception as e:
            print(f"  ❌ 요청 실패: {e}")
            break
        time.sleep(0.2)

    print(f"  수집 완료: {len(all_items)}건")
    return all_items


# ============================================================
# 1. 카페글(맘카페) 분석
# ============================================================

def analyze_cafe(items: list, query: str) -> dict:
    """카페글에서 고객 목소리 추출"""
    cleaned = []
    cafe_counter = Counter()
    keyword_counter = Counter()

    # 자주 등장하는 의미 있는 단어 추출용 불용어
    stopwords = set("아기 아이 우리 좀 이 그 저 것 거 수 때 더 잘 좋 해 하 은 는 이 가 을 를 에 의 로 와 과 도 만 나 한 된 안 건 번 걸 볼".split())

    for item in items:
        title = clean_html(item.get("title", ""))
        desc = clean_html(item.get("description", ""))
        link = item.get("link", "")
        cafe = item.get("cafename", "")

        cleaned.append({
            "title": title,
            "description": desc[:200],
            "link": link,
            "cafe": cafe,
            "date": item.get("postdate", "")
        })

        if cafe:
            cafe_counter[cafe] += 1

        # 제목+설명에서 키워드 추출
        text = f"{title} {desc}"
        words = re.findall(r'[가-힣]{2,}', text)
        for w in words:
            if w not in stopwords and len(w) >= 2:
                keyword_counter[w] += 1

    # 고민/추천/불만 패턴 분류
    patterns = {
        "고민/질문": ["추천", "뭐가 좋", "어떤 거", "골라", "비교", "뭐 써", "뭐 사", "알려", "궁금"],
        "불만/단점": ["별로", "실망", "후회", "안 좋", "안좋", "단점", "보풀", "미끄", "더워", "안 시원", "뜨거"],
        "만족/장점": ["좋아", "만족", "추천합", "최고", "시원", "잘 자", "꿀잠", "대박", "강추"],
        "구매/가격": ["가격", "할인", "세일", "쿠폰", "공구", "공동구매", "얼마", "저렴"]
    }

    pattern_results = {}
    for category, keywords in patterns.items():
        count = 0
        examples = []
        for item in cleaned:
            text = f"{item['title']} {item['description']}"
            if any(kw in text for kw in keywords):
                count += 1
                if len(examples) < 3:
                    examples.append(item["title"][:60])
        pattern_results[category] = {"count": count, "ratio": round(count/max(len(cleaned),1)*100, 1), "examples": examples}

    return {
        "source": "카페글(맘카페)",
        "query": query,
        "total_collected": len(cleaned),
        "top_cafes": [{"name": k, "count": v, "share": round(v/max(len(cleaned),1)*100,1)} for k, v in cafe_counter.most_common(10)],
        "top_keywords": [{"word": k, "count": v} for k, v in keyword_counter.most_common(30)],
        "voice_patterns": pattern_results,
        "sample_posts": cleaned[:20],
    }


# ============================================================
# 2. 블로그 리뷰 분석
# ============================================================

def analyze_blog(items: list, query: str) -> dict:
    """블로그에서 리뷰/체험단 패턴 분석"""
    cleaned = []
    blogger_counter = Counter()
    keyword_counter = Counter()
    stopwords = set("아기 아이 우리 좀 이 그 저 것 수 때 더 잘 좋 해 은 는 가 을 를 에 의 로 와 과 도 만 나 한 된 안 건 번 걸 볼 후기 리뷰 추천".split())

    for item in items:
        title = clean_html(item.get("title", ""))
        desc = clean_html(item.get("description", ""))
        cleaned.append({
            "title": title,
            "description": desc[:200],
            "link": item.get("link", ""),
            "blogger": item.get("bloggername", ""),
            "date": item.get("postdate", "")
        })
        if item.get("bloggername"):
            blogger_counter[item["bloggername"]] += 1
        text = f"{title} {desc}"
        words = re.findall(r'[가-힣]{2,}', text)
        for w in words:
            if w not in stopwords and len(w) >= 2:
                keyword_counter[w] += 1

    # 체험단/광고 vs 진성 리뷰 추정
    ad_keywords = ["협찬", "제공", "체험단", "원고료", "소정", "지원받", "광고"]
    genuine_keywords = ["직접 구매", "내돈내산", "자비", "솔직"]
    ad_count = sum(1 for item in cleaned if any(kw in f"{item['title']} {item['description']}" for kw in ad_keywords))
    genuine_count = sum(1 for item in cleaned if any(kw in f"{item['title']} {item['description']}" for kw in genuine_keywords))

    # 브랜드 언급 빈도
    brand_counter = Counter()
    for item in cleaned:
        text = f"{item['title']} {item['description']}"
        words = re.findall(r'[가-힣a-zA-Z]{2,}', text)
        for w in words:
            if w not in stopwords:
                brand_counter[w] += 1

    return {
        "source": "블로그 리뷰",
        "query": query,
        "total_collected": len(cleaned),
        "review_type": {
            "sponsored_estimated": ad_count,
            "genuine_estimated": genuine_count,
            "unknown": len(cleaned) - ad_count - genuine_count,
            "sponsored_ratio": round(ad_count/max(len(cleaned),1)*100, 1)
        },
        "top_keywords": [{"word": k, "count": v} for k, v in keyword_counter.most_common(30)],
        "active_bloggers": [{"name": k, "posts": v} for k, v in blogger_counter.most_common(10)],
        "sample_reviews": cleaned[:15],
    }


# ============================================================
# 3. 지식인 질문 분석
# ============================================================

def analyze_kin(items: list, query: str) -> dict:
    """지식인에서 구매 전 질문 패턴 분석"""
    cleaned = []
    question_patterns = Counter()

    pattern_map = {
        "추천 요청": ["추천", "뭐가 좋", "어떤 게", "골라", "알려"],
        "비교 질문": ["vs", "차이", "비교", "뭐가 나", "다른 점"],
        "안전성 우려": ["안전", "유해", "괜찮", "위험", "안심"],
        "사용 시기": ["언제부터", "몇 개월", "신생아", "돌아기"],
        "소재 질문": ["소재", "원단", "듀라론", "인견", "메쉬", "냉감"],
        "가격 질문": ["가격", "얼마", "비싸", "저렴", "가성비"],
        "사용 방법": ["어떻게", "사용법", "세탁", "관리", "빨래"],
    }

    for item in items:
        title = clean_html(item.get("title", ""))
        desc = clean_html(item.get("description", ""))
        cleaned.append({
            "title": title,
            "description": desc[:200],
            "link": item.get("link", ""),
            "date": item.get("postdate", "")
        })
        text = f"{title} {desc}"
        for pattern_name, keywords in pattern_map.items():
            if any(kw in text for kw in keywords):
                question_patterns[pattern_name] += 1

    # 롱테일 키워드 후보 추출 (질문 제목에서)
    longtail_candidates = []
    for item in cleaned[:50]:
        title = item["title"]
        # 자연어 질문 패턴에서 키워드 추출
        if any(q in title for q in ["추천", "뭐", "어떤", "언제", "어떻게", "vs", "비교"]):
            longtail_candidates.append(title[:50])

    return {
        "source": "지식인 질문",
        "query": query,
        "total_collected": len(cleaned),
        "question_patterns": {k: {"count": v, "ratio": round(v/max(len(cleaned),1)*100,1)} for k, v in question_patterns.most_common()},
        "longtail_candidates": longtail_candidates[:20],
        "sample_questions": cleaned[:15],
    }


# ============================================================
# 4. 뉴스 동향 수집
# ============================================================

def analyze_news(items: list, query: str) -> dict:
    """뉴스에서 시장 동향 추출"""
    cleaned = []
    source_counter = Counter()

    for item in items:
        title = clean_html(item.get("title", ""))
        desc = clean_html(item.get("description", ""))
        cleaned.append({
            "title": title,
            "description": desc[:200],
            "link": item.get("originallink", item.get("link", "")),
            "date": item.get("pubDate", "")
        })

    return {
        "source": "뉴스 동향",
        "query": query,
        "total_collected": len(cleaned),
        "recent_news": cleaned[:20],
    }


# ============================================================
# 5. 데이터랩 검색어 트렌드
# ============================================================

def fetch_search_trend(client_id, client_secret, keywords, start_date, end_date, time_unit="month"):
    """네이버 통합검색 키워드 트렌드 (상대값 0~100)"""
    headers = make_headers(client_id, client_secret, "application/json")

    keyword_groups = []
    for kw in keywords[:5]:
        keyword_groups.append({"groupName": kw, "keywords": [kw]})

    payload = {
        "startDate": start_date,
        "endDate": end_date,
        "timeUnit": time_unit,
        "keywordGroups": keyword_groups
    }

    print(f"\n📈 검색어 트렌드 조회: {', '.join(keywords[:5])}")

    try:
        resp = requests.post(DATALAB_URL, headers=headers, data=json.dumps(payload), timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            results = data.get("results", [])
            print(f"  ✅ {len(results)}개 키워드 트렌드 수집")

            trend_summary = []
            for r in results:
                title = r.get("title", "")
                data_points = r.get("data", [])
                if data_points:
                    values = [d["ratio"] for d in data_points]
                    peak_idx = values.index(max(values))
                    peak_period = data_points[peak_idx]["period"]
                    recent = values[-1] if values else 0
                    avg = round(sum(values)/len(values), 1)
                    trend_summary.append({
                        "keyword": title,
                        "avg_ratio": avg,
                        "peak_ratio": max(values),
                        "peak_period": peak_period,
                        "recent_ratio": recent,
                        "trend": "상승" if len(values) >= 3 and values[-1] > values[-3] else "하락" if len(values) >= 3 and values[-1] < values[-3] else "유지",
                        "data": data_points
                    })
            return {"raw": data, "summary": trend_summary}
        else:
            print(f"  ❌ HTTP {resp.status_code}: {resp.text[:200]}")
            return {"error": resp.text}
    except Exception as e:
        print(f"  ❌ 요청 실패: {e}")
        return {"error": str(e)}


# ============================================================
# 출력 & 메인
# ============================================================

def print_summary(results: dict):
    """전체 분석 결과 요약"""
    print(f"\n{'='*60}")
    print(f"📊 네이버 고객 목소리(VOC) 통합 분석 결과")
    print(f"{'='*60}")
    print(f"분석일시: {results.get('analysis_date', '')}")
    print(f"검색어: {results.get('query', '')}\n")

    # 카페 분석
    if "cafe" in results:
        c = results["cafe"]
        print(f"☕ 카페글(맘카페): {c['total_collected']}건 수집")
        if c.get("top_cafes"):
            print(f"  주요 카페: {', '.join(x['name'] for x in c['top_cafes'][:5])}")
        if c.get("voice_patterns"):
            for cat, info in c["voice_patterns"].items():
                print(f"  {cat}: {info['count']}건 ({info['ratio']}%)")
        print()

    # 블로그 분석
    if "blog" in results:
        b = results["blog"]
        print(f"📝 블로그 리뷰: {b['total_collected']}건 수집")
        rt = b.get("review_type", {})
        print(f"  체험단/협찬 추정: {rt.get('sponsored_estimated',0)}건 ({rt.get('sponsored_ratio',0)}%)")
        print(f"  진성 리뷰 추정: {rt.get('genuine_estimated',0)}건")
        print()

    # 지식인 분석
    if "kin" in results:
        k = results["kin"]
        print(f"❓ 지식인 질문: {k['total_collected']}건 수집")
        if k.get("question_patterns"):
            for cat, info in k["question_patterns"].items():
                print(f"  {cat}: {info['count']}건 ({info['ratio']}%)")
        if k.get("longtail_candidates"):
            print(f"  롱테일 후보: {len(k['longtail_candidates'])}개 발견")
        print()

    # 뉴스
    if "news" in results:
        n = results["news"]
        print(f"📰 뉴스 동향: {n['total_collected']}건 수집")
        for item in n.get("recent_news", [])[:5]:
            print(f"  · {item['title'][:50]}")
        print()

    # 트렌드
    if "trend" in results and "summary" in results["trend"]:
        print(f"📈 검색어 트렌드:")
        for t in results["trend"]["summary"]:
            arrow = "↗️" if t["trend"] == "상승" else "↘️" if t["trend"] == "하락" else "→"
            print(f"  {t['keyword']:20} 평균:{t['avg_ratio']:5.1f}  피크:{t['peak_ratio']:5.1f} ({t['peak_period']})  {arrow} {t['trend']}")


def main():
    parser = argparse.ArgumentParser(description="네이버 VOC 통합 분석")
    subparsers = parser.add_subparsers(dest="command")

    # 공통 인자
    for name in ["cafe", "blog", "kin", "news"]:
        sp = subparsers.add_parser(name)
        sp.add_argument("--client-id", required=True)
        sp.add_argument("--client-secret", required=True)
        sp.add_argument("--query", required=True)
        sp.add_argument("--total", type=int, default=100)
        sp.add_argument("--output", default=f"{name}_results.json")

    # 트렌드
    tp = subparsers.add_parser("trend")
    tp.add_argument("--client-id", required=True)
    tp.add_argument("--client-secret", required=True)
    tp.add_argument("--keywords", required=True, help="쉼표 구분")
    tp.add_argument("--start-date", default="2025-01-01")
    tp.add_argument("--end-date", default="2026-03-01")
    tp.add_argument("--output", default="trend_results.json")

    # 전체 통합
    fp = subparsers.add_parser("full", help="전체 VOC 통합 분석")
    fp.add_argument("--client-id", required=True)
    fp.add_argument("--client-secret", required=True)
    fp.add_argument("--query", required=True)
    fp.add_argument("--total", type=int, default=100)
    fp.add_argument("--trend-keywords", default="", help="쉼표 구분 트렌드 키워드")
    fp.add_argument("--start-date", default="2025-01-01")
    fp.add_argument("--end-date", default="2026-03-01")
    fp.add_argument("--output", default="voc_full_results.json")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    service_map = {"cafe": "cafearticle", "blog": "blog", "kin": "kin", "news": "news"}
    analyzer_map = {"cafe": analyze_cafe, "blog": analyze_blog, "kin": analyze_kin, "news": analyze_news}

    if args.command in service_map:
        items = search_naver(args.client_id, args.client_secret, service_map[args.command], args.query, args.total)
        results = analyzer_map[args.command](items, args.query)
        results["analysis_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 저장 완료: {args.output}")

    elif args.command == "trend":
        kws = [k.strip() for k in args.keywords.split(",") if k.strip()]
        results = fetch_search_trend(args.client_id, args.client_secret, kws, args.start_date, args.end_date)
        results["analysis_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 저장 완료: {args.output}")

    elif args.command == "full":
        print("🚀 전체 VOC 통합 분석 시작\n")
        full = {"analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M"), "query": args.query}

        # 카페
        items = search_naver(args.client_id, args.client_secret, "cafearticle", f"{args.query} 추천", args.total)
        full["cafe"] = analyze_cafe(items, args.query)

        # 블로그
        items = search_naver(args.client_id, args.client_secret, "blog", f"{args.query} 후기 리뷰", args.total)
        full["blog"] = analyze_blog(items, args.query)

        # 지식인
        items = search_naver(args.client_id, args.client_secret, "kin", args.query, min(args.total, 50))
        full["kin"] = analyze_kin(items, args.query)

        # 뉴스
        items = search_naver(args.client_id, args.client_secret, "news", args.query, min(args.total, 30))
        full["news"] = analyze_news(items, args.query)

        # 트렌드
        if args.trend_keywords:
            kws = [k.strip() for k in args.trend_keywords.split(",") if k.strip()]
        else:
            kws = [args.query]
        full["trend"] = fetch_search_trend(args.client_id, args.client_secret, kws, args.start_date, args.end_date)

        print_summary(full)

        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(full, f, ensure_ascii=False, indent=2)
        print(f"\n✅ 전체 결과 저장: {args.output}")


if __name__ == "__main__":
    main()
