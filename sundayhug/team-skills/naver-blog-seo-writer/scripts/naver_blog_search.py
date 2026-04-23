#!/usr/bin/env python3
"""
네이버 블로그 검색 API를 활용한 상위 블로그 분석 스크립트

사용법:
  python naver_blog_search.py \
    --client-id YOUR_CLIENT_ID \
    --client-secret YOUR_CLIENT_SECRET \
    --keyword "신생아 슬리핑백 추천" \
    --display 10 \
    --output blog_analysis.json

네이버 검색 API (openapi.naver.com) 사용
→ https://developers.naver.com 에서 앱 등록 후 Client ID/Secret 발급
"""

import argparse
import json
import sys
import urllib.parse
from datetime import datetime

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests


NAVER_BLOG_SEARCH_URL = "https://openapi.naver.com/v1/search/blog.json"


def search_naver_blogs(client_id: str, client_secret: str, keyword: str, display: int = 10, start: int = 1) -> dict:
    """네이버 블로그 검색"""
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret,
    }
    params = {
        "query": keyword,
        "display": min(display, 100),
        "start": start,
        "sort": "sim",  # 정확도순 (sim: 정확도, date: 최신순)
    }

    response = requests.get(NAVER_BLOG_SEARCH_URL, headers=headers, params=params, timeout=30)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"❌ API 오류: HTTP {response.status_code}")
        print(f"   응답: {response.text[:300]}")
        return {}


def clean_html(text: str) -> str:
    """HTML 태그 및 특수문자 제거"""
    import re
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
    text = text.replace('&quot;', '"').replace('&#39;', "'").replace('&nbsp;', ' ')
    return text.strip()


def analyze_title_pattern(title: str) -> str:
    """제목 패턴 분류"""
    import re
    title = clean_html(title)

    if re.search(r'\d+가지|\d+개|\d+선|\bTOP\s*\d+', title, re.IGNORECASE):
        return "숫자형"
    elif title.endswith('?') or title.endswith('까?') or '어떻게' in title or '뭘까' in title:
        return "질문형"
    elif '후기' in title or '리뷰' in title or '솔직' in title:
        return "후기형"
    elif '추천' in title:
        return "추천형"
    elif '방법' in title or 'HOW' in title.upper() or '하는 법' in title:
        return "방법형"
    elif '비교' in title or 'vs' in title.lower():
        return "비교형"
    elif '총정리' in title or '완벽정리' in title or '정리' in title:
        return "정리형"
    else:
        return "기타"


def estimate_word_count(description: str) -> str:
    """미리보기로 글 길이 추정"""
    desc_len = len(clean_html(description))
    # 미리보기는 보통 150~200자, 실제 글은 10~20배
    estimated = desc_len * 12
    if estimated < 1000:
        return "짧음 (1,000자 미만 추정)"
    elif estimated < 2000:
        return "보통 (1,000~2,000자 추정)"
    elif estimated < 3500:
        return "김 (2,000~3,500자 추정)"
    else:
        return "매우 김 (3,500자 이상 추정)"


def extract_keywords_from_title(title: str, search_keyword: str) -> list:
    """제목에서 추가 키워드 추출"""
    title = clean_html(title)
    # 검색 키워드 단어 분리
    search_words = search_keyword.split()
    # 제목에서 검색 키워드 외 단어 추출 (간단한 방식)
    words = title.split()
    extra = [w for w in words if w not in search_words and len(w) >= 2]
    return extra[:5]


def analyze_blogs(items: list, keyword: str) -> dict:
    """블로그 검색 결과 분석"""
    analysis = {
        "keyword": keyword,
        "total_results": len(items),
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "title_patterns": {},
        "common_subkeywords": [],
        "blogs": [],
        "seo_insights": {}
    }

    pattern_counts = {}
    all_extra_keywords = []

    for i, item in enumerate(items, 1):
        title = clean_html(item.get("title", ""))
        description = clean_html(item.get("description", ""))
        link = item.get("link", "")
        blog_name = item.get("bloggername", "")
        post_date = item.get("postdate", "")

        # 날짜 포맷
        if post_date and len(post_date) == 8:
            post_date = f"{post_date[:4]}-{post_date[4:6]}-{post_date[6:]}"

        pattern = analyze_title_pattern(title)
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

        extra_kws = extract_keywords_from_title(title, keyword)
        all_extra_keywords.extend(extra_kws)

        analysis["blogs"].append({
            "rank": i,
            "title": title,
            "title_pattern": pattern,
            "blog_name": blog_name,
            "post_date": post_date,
            "description": description,
            "estimated_length": estimate_word_count(description),
            "link": link,
            "extra_keywords": extra_kws,
        })

    analysis["title_patterns"] = pattern_counts

    # 자주 등장한 연관 키워드
    kw_counts = {}
    for kw in all_extra_keywords:
        kw_counts[kw] = kw_counts.get(kw, 0) + 1
    sorted_kws = sorted(kw_counts.items(), key=lambda x: x[1], reverse=True)
    analysis["common_subkeywords"] = [k for k, v in sorted_kws[:15] if v >= 2]

    # SEO 인사이트 도출
    most_common_pattern = max(pattern_counts, key=pattern_counts.get) if pattern_counts else "기타"
    analysis["seo_insights"] = {
        "dominant_title_pattern": most_common_pattern,
        "pattern_distribution": pattern_counts,
        "recommended_title_pattern": most_common_pattern,
        "key_sub_keywords": analysis["common_subkeywords"][:8],
        "competition_level": "높음" if len(items) >= 8 else "중간" if len(items) >= 4 else "낮음",
    }

    return analysis


def print_analysis(analysis: dict):
    """분석 결과 콘솔 출력"""
    print(f"\n{'='*65}")
    print(f"📊 네이버 블로그 경쟁 분석 결과")
    print(f"{'='*65}")
    print(f"키워드: {analysis['keyword']}")
    print(f"분석 건수: {analysis['total_results']}개")
    print(f"\n🎯 제목 패턴 분포:")
    for pattern, count in sorted(analysis['title_patterns'].items(), key=lambda x: x[1], reverse=True):
        bar = "█" * count
        print(f"  {pattern:<8}: {bar} ({count}개)")

    print(f"\n💡 SEO 인사이트:")
    insights = analysis['seo_insights']
    print(f"  지배적 패턴: {insights['dominant_title_pattern']}")
    print(f"  경쟁 강도: {insights['competition_level']}")
    print(f"  핵심 서브 키워드: {', '.join(insights['key_sub_keywords'])}")

    print(f"\n{'─'*65}")
    print(f"{'순위':<5} {'제목':<40} {'패턴':<8} {'날짜'}")
    print(f"{'─'*65}")
    for blog in analysis["blogs"]:
        title_short = blog["title"][:38] + ".." if len(blog["title"]) > 40 else blog["title"]
        print(f"{blog['rank']:<5} {title_short:<40} {blog['title_pattern']:<8} {blog['post_date']}")


def main():
    parser = argparse.ArgumentParser(description="네이버 블로그 상위 노출 분석")
    parser.add_argument("--client-id", required=True, help="네이버 API Client ID")
    parser.add_argument("--client-secret", required=True, help="네이버 API Client Secret")
    parser.add_argument("--keyword", required=True, help="검색 키워드")
    parser.add_argument("--display", type=int, default=10, help="가져올 결과 수 (최대 100)")
    parser.add_argument("--output", default="blog_analysis.json", help="결과 저장 파일명")

    args = parser.parse_args()

    print(f"🔍 [{args.keyword}] 네이버 블로그 검색 중...")

    # API 호출
    raw = search_naver_blogs(
        args.client_id, args.client_secret, args.keyword, args.display
    )

    if not raw or "items" not in raw:
        print("❌ 검색 결과가 없습니다.")
        sys.exit(1)

    items = raw.get("items", [])
    print(f"✅ {len(items)}개 블로그 발견")

    # 분석
    analysis = analyze_blogs(items, args.keyword)
    print_analysis(analysis)

    # JSON 저장
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 전체 결과가 {args.output}에 저장되었습니다.")
    print(f"   이 파일을 Claude에 업로드하시면 블로그 글 작성에 활용합니다.")


if __name__ == "__main__":
    main()
