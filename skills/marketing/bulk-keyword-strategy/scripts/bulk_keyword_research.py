#!/usr/bin/env python3
"""
bulk_keyword_research.py — 전제품 일괄 네이버 SEO 키워드 전략 생성 (메인)

Usage:
    # 전체 폴더 처리
    python3 bulk_keyword_research.py \
        --pdp-folder "~/Desktop/상세페이지 (절대경로)" \
        --output ~/Desktop/team-skills/리포트/keyword-strategy/

    # 단일 제품 시범
    python3 bulk_keyword_research.py \
        --single sleep-products/cooling-pad/cooling-mesh-dual-pad.html

환경변수 (모두 필수):
    NAVER_CUSTOMER_ID / NAVER_API_KEY / NAVER_SECRET_KEY  — 검색광고 API
    NAVER_CLIENT_ID / NAVER_CLIENT_SECRET                  — DataLab + 쇼핑 API
"""

from __future__ import annotations

import argparse
import sys
import time
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any

# Local imports
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from parsers.pdp_parser import (
    ProductInfo,
    parse_folder,
    parse_pdp,
    discover_pdps,
    dedup_by_slug,
)
from analyzers.seed_keywords import derive_seeds, derive_seeds_from_product
from analyzers.grader import (
    grade,
    select_main_and_subs,
    select_tags,
    GradedKeyword,
)
from analyzers.name_generator import generate as generate_name
from exporters.xlsx_writer import write_xlsx
from apis.naver_searchad import KeywordtoolClient, KeywordStat
from apis.naver_datalab import DataLabClient, KeywordTrend


def _short_material(raw: str) -> str:
    """소재 텍스트를 짧게 (상품명용 — 2~3 단어)."""
    if not raw:
        return ""
    # 자주 보이는 소재 추출
    keys = [
        "듀라론", "메쉬", "에어메쉬", "코튼", "밤부", "거즈", "텐셀",
        "실키", "오가닉", "삼중", "방수", "100%면", "100수",
    ]
    raw_lower = raw.lower()
    found = [k for k in keys if k.lower() in raw_lower]
    return " ".join(found[:3]) if found else ""


def _detect_season(usp: str, sub_title: str) -> str:
    text = f"{usp} {sub_title}".lower()
    if "여름" in text or "쿨" in text or "냉감" in text or "통기" in text or "메쉬" in text:
        return "여름"
    if "겨울" in text or "보온" in text or "삼중" in text:
        return "겨울"
    if "봄가을" in text or "사계절" in text:
        return "사계절"
    return ""


def _detect_target_age(usp: str, sub_title: str) -> str:
    text = f"{usp} {sub_title}"
    if "신생아" in text or "newborn" in text.lower():
        return "신생아"
    if "유아" in text or "toddler" in text.lower():
        return "유아"
    return "아기"


def process_one(
    product: ProductInfo,
    keyword_client: KeywordtoolClient | None,
    datalab_client: DataLabClient | None,
    skip_apis: bool = False,
) -> dict[str, Any]:
    """단일 제품 처리 → record dict."""
    rec: dict[str, Any] = {
        "slug": product.slug,
        "category": product.category,
        "title": product.sub_title or product.title,
        "usp_short": product.usp_short,
        "material": product.material,
        "size": product.size,
        "color": product.color,
        "multi_categories": product.extra_specs.get("__multi_categories__", ""),
        "warnings": list(product.parsing_warnings),
    }

    # NEW: PDP 본문 highlights / sec_titles / trust_items / faq 활용
    seeds, body_tokens = derive_seeds_from_product(product)
    rec["seeds"] = seeds

    if skip_apis or not keyword_client:
        rec["warnings"].append("API 호출 스킵 (시드만)")
        # 더미 채움
        rec.update(
            product_name=f"썬데이허그 꿀잠 {seeds[0] if seeds else '아기 용품'}",
            main_keyword=seeds[0] if seeds else "",
            main_search=0,
            main_grade="-",
            main_competition="",
            sub_keywords=seeds[1:5] if len(seeds) > 1 else [],
            tags=seeds[:10],
            peak_month="",
            current_vs_peak="",
        )
        return rec

    # 1. 검색광고 API
    try:
        stats = keyword_client.lookup_batched(seeds)
    except Exception as e:
        rec["warnings"].append(f"검색광고 API 실패: {e}")
        stats = []

    # 2. DataLab (시드 5개만)
    trends_map: dict[str, KeywordTrend] = {}
    if datalab_client and seeds:
        try:
            trends = datalab_client.keyword_trends(seeds[:5])
            for t in trends:
                trends_map[t.keyword] = t
        except Exception as e:
            rec["warnings"].append(f"DataLab 실패: {e}")

    current_month = date.today().month

    # 3. 등급 매기기
    graded: list[GradedKeyword] = []
    for s in stats:
        # 트렌드는 시드 키워드에 대해서만 있음 → 보조 키워드는 시즌 체크 X
        peak = None
        seasonal = False
        for tkw, trend in trends_map.items():
            if tkw == s.keyword:
                peak = trend.peak_month
                seasonal = trend.is_seasonal
                break
        graded.append(
            grade(
                keyword=s.keyword,
                pc_search=s.pc_search,
                mobile_search=s.mobile_search,
                competition=s.competition,
                peak_month=peak,
                seasonal=seasonal,
                current_month=current_month,
            )
        )

    # 4. 메인 + 보조 + 태그 선정
    # 블록리스트: 호환 침대명 + 경쟁 브랜드 + 무관 캐릭터/박람회/일반어
    blocklist = [
        # 침대 호환 모델
        "리안드림콧", "크리미드림", "베어블리", "쿠시노", "드림콧", "호환",
        # 경쟁/무관 브랜드
        "트립트랩", "스토케", "이케아", "아프리콧스튜디오", "유니클로",
        "시나모롤", "산리오", "포켓몬", "디즈니", "겨울왕국", "티니핑",
        "구름베이비", "마더가든", "코코블린", "리틀빅", "마이리틀데이지",
        "코코하니", "리미떼두두", "베베니즈", "꽃축제",
        "부가부", "드래곤플라이", "니스툴그로우", "밍크뮤", "나비잠",
        "머미쿨쿨", "맘쿨쿨", "엔젤하임", "타이니러브", "차일드유",
        # 박람회/이벤트/상권
        "베이비페어", "박람회", "남대문", "아동복도매",
        "어린이날선물", "레터링케이크", "꽃다발",
        # 너무 일반적이라 우리 SKU와 매칭 약한 것
        "원목침대", "패밀리침대", "침대프레임", "범퍼침대", "벙커침대",
        "유아책상", "유아의자", "원목책상", "유아침대가드", "아기2층침대",
        "LED침대", "침대LED", "led침대",
        # 의류 — 우리 라인 아닌 사이즈/카테고리
        "7부", "5부", "3부", "9부",  # 부분 길이는 모두 매칭됨 (정확한 단어 단위가 아님 주의)
        "100일옷", "50일옷", "100일선물", "백일선물",
        "경량패딩", "롱패딩", "다운점퍼",
        "내복", "잠옷세트",
        # 무관 / 카테고리 외 (가전/식품/주얼리)
        "선풍기", "에어컨", "공기청정기", "가습기", "제습기",
        "돌반지", "돌상", "백일상", "돌선물",
        "분유포트", "양배추", "흑염소진액", "젖병", "노리개젖꼭지",
        "체온계", "브라운체온계",
        # 일반 매트/이불 (우리 SKU와 매칭 약함)
        "돗자리", "캠핑매트", "에어매트리스", "에어매트", "발매트",
        "POE매트", "층간소음매트", "거실매트", "바닥매트", "놀이매트",
        "이불세트", "차렵이불",
        # 기타 무관
        "카페", "유아원", "유아원복", "유치원가방",
        "제철과일", "선물세트가성비", "돌드레스",
        "장난감", "교구", "원목장난감",
        "출산선물",  # 단독 — "출산선물세트"는 OK이지만 "출산선물"만은 약함
    ]

    # 시드 어휘 토큰 (메인/태그 적합도 부스트용)
    # body_tokens에 이미 highlights/sec_titles/trust_items/faq 명사 모두 포함됨
    from analyzers.grader import _extract_tokens
    seed_tokens: set[str] = set(body_tokens)
    for s in seeds:
        seed_tokens |= _extract_tokens(s)
    # 제품명 / USP 명사도 추가 (이중 보강)
    seed_tokens |= _extract_tokens(product.sub_title)
    seed_tokens |= _extract_tokens(product.usp_short)

    main, subs = select_main_and_subs(
        graded,
        blocklist_substrings=blocklist,
        n_sub=4,
        seed_tokens=seed_tokens,
        relevance_boost=5.0,  # 시드 어휘 매칭 강한 부스트
    )
    tags = select_tags(
        graded,
        blocklist_substrings=blocklist,
        n=10,
        seed_tokens=seed_tokens,
    )

    # 5. 상품명 생성
    if main:
        season = _detect_season(product.usp_short, product.sub_title)
        target = _detect_target_age(product.usp_short, product.sub_title)
        material_short = _short_material(product.material)
        product_name, name_warns = generate_name(
            main_keyword=main.keyword,
            sub_keywords=[s.keyword for s in subs],
            category=product.category,
            material_short=material_short,
            season=season,
            target_age=target,
        )
        if name_warns:
            rec["warnings"].extend(name_warns)
    else:
        product_name = f"썬데이허그 꿀잠 {seeds[0] if seeds else '아기 용품'}"
        rec["warnings"].append("메인 키워드 도출 실패 (검색량 0)")

    # 6. 시즌 정보
    main_trend = trends_map.get(main.keyword) if main else None
    if main_trend:
        peak_month = main_trend.peak_month
        cvp = f"{main_trend.current_vs_peak:.1f}%"
    else:
        peak_month = ""
        cvp = ""

    rec.update(
        product_name=product_name,
        main_keyword=main.keyword if main else "",
        main_search=main.total_search if main else 0,
        main_grade=main.grade if main else "-",
        main_competition=main.competition if main else "",
        sub_keywords=[s.keyword for s in subs],
        tags=[t.keyword.replace(" ", "") for t in tags],  # 태그는 띄어쓰기 제거
        peak_month=peak_month,
        current_vs_peak=cvp,
    )
    return rec


def run(
    pdp_folder: Path,
    output_dir: Path,
    single_relpath: str | None = None,
    skip_apis: bool = False,
) -> Path:
    pdp_folder = pdp_folder.expanduser()
    output_dir = output_dir.expanduser()

    # 1. PDP 파싱
    print(f"📂 PDP 폴더: {pdp_folder}")
    if single_relpath:
        files = [pdp_folder / single_relpath]
        products = [parse_pdp(f, pdp_folder) for f in files]
    else:
        products = parse_folder(pdp_folder)
        print(f"   {len(products)}개 HTML 파싱")
        products = dedup_by_slug(products)
        print(f"   {len(products)}개 (dedup 후)")

    # 2. API 클라이언트 초기화
    keyword_client = None
    datalab_client = None
    if not skip_apis:
        try:
            keyword_client = KeywordtoolClient()
            print("   ✅ 검색광고 API 인증 OK")
        except Exception as e:
            print(f"   ⚠️  검색광고 API 인증 실패: {e}")
            print("       → API 호출 스킵 (시드만으로 진행)")
            skip_apis = True
        try:
            datalab_client = DataLabClient()
            print("   ✅ DataLab API 인증 OK")
        except Exception as e:
            print(f"   ⚠️  DataLab API 인증 실패: {e}")
            datalab_client = None

    # 3. 처리
    records: list[dict[str, Any]] = []
    for i, product in enumerate(products, 1):
        print(f"  [{i}/{len(products)}] {product.slug}", flush=True)
        rec = process_one(product, keyword_client, datalab_client, skip_apis=skip_apis)
        records.append(rec)
        # API rate limit 고려 (검색광고 0.5s)
        if not skip_apis:
            time.sleep(0.5)

    # 4. xlsx 출력
    today = date.today().strftime("%Y-%m-%d")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"SundayHug-전제품-키워드-전략_{today}.xlsx"
    write_xlsx(records, out_path)

    # 5. 요약 출력
    print()
    print("=" * 60)
    print(f"  총 {len(records)}개 제품 처리")
    grades = {"S": 0, "A": 0, "B": 0, "C": 0, "D": 0, "-": 0}
    for r in records:
        g = r.get("main_grade", "-")
        grades[g] = grades.get(g, 0) + 1
    print(f"  등급 분포: S={grades.get('S',0)} A={grades.get('A',0)} B={grades.get('B',0)} C={grades.get('C',0)} D={grades.get('D',0)} -={grades.get('-',0)}")
    warned = sum(1 for r in records if r.get("warnings"))
    print(f"  경고 있는 제품: {warned}개")
    print(f"  📊 결과: {out_path}")
    print("=" * 60)
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="SundayHug 전제품 네이버 SEO 일괄 분석")
    ap.add_argument(
        "--pdp-folder",
        default="~/Desktop/상세페이지 (절대경로)",
        help="PDP HTML 폴더 (기본값: ~/Desktop/상세페이지 (절대경로))",
    )
    ap.add_argument(
        "--output",
        default="~/Desktop/team-skills/리포트/keyword-strategy",
        help="결과 xlsx 저장 폴더",
    )
    ap.add_argument(
        "--single",
        default=None,
        help="단일 제품 상대경로 (예: sleep-products/cooling-pad/cooling-mesh-dual-pad.html)",
    )
    ap.add_argument(
        "--skip-apis",
        action="store_true",
        help="API 호출 스킵 (파싱+시드만, 디버깅용)",
    )
    args = ap.parse_args()

    run(
        pdp_folder=Path(args.pdp_folder),
        output_dir=Path(args.output),
        single_relpath=args.single,
        skip_apis=args.skip_apis,
    )


if __name__ == "__main__":
    main()
