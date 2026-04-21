#!/usr/bin/env python3
"""
네이버 광고 성과 리포트 End-to-End 오케스트레이션.

전체 플로우를 한 번에 실행:
  1. 크레덴셜 로드
  2. 마스터 데이터 조회 (캠페인/키워드 맵)
  3. AD 리포트 발급 & 다운로드
  4. (선택) SHOPPING_PRODUCT 리포트 발급 & 다운로드
  5. HTML 리포트 생성

사용법:
  python run_report.py \
    --date-from 2026-04-14 \
    --date-to 2026-04-20 \
    --include-shopping

  # 키를 인자로 넘기는 경우
  python run_report.py \
    --customer-id XXX --api-key YYY --secret-key ZZZ \
    --date-from 2026-04-14 --date-to 2026-04-20
"""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from naver_ads_client import NaverAdsClient, NaverAdsCredentials, NaverAdsAPIError  # noqa: E402
from stat_report import fetch_stat_report  # noqa: E402
from html_renderer import render_report  # noqa: E402


# ───────── 날짜 프리셋 ─────────

def resolve_date_preset(preset: str) -> tuple[str, str]:
    """
    프리셋 문자열을 date_from, date_to로 변환.
    """
    today = date.today()
    yesterday = today - timedelta(days=1)

    if preset == "yesterday":
        return yesterday.isoformat(), yesterday.isoformat()
    if preset == "last7":
        return (today - timedelta(days=7)).isoformat(), yesterday.isoformat()
    if preset == "last14":
        return (today - timedelta(days=14)).isoformat(), yesterday.isoformat()
    if preset == "last30":
        return (today - timedelta(days=30)).isoformat(), yesterday.isoformat()
    if preset == "thismonth":
        first = today.replace(day=1)
        return first.isoformat(), yesterday.isoformat()
    if preset == "lastmonth":
        first_this = today.replace(day=1)
        last_prev = first_this - timedelta(days=1)
        first_prev = last_prev.replace(day=1)
        return first_prev.isoformat(), last_prev.isoformat()
    if preset == "lastweek":
        # 지난주 월~일
        dow = today.weekday()  # 월=0
        this_mon = today - timedelta(days=dow)
        last_mon = this_mon - timedelta(days=7)
        last_sun = this_mon - timedelta(days=1)
        return last_mon.isoformat(), last_sun.isoformat()

    raise ValueError(f"알 수 없는 프리셋: {preset}")


# ───────── 마스터 조회 ─────────

def build_maps(client: NaverAdsClient) -> tuple[dict, dict]:
    """
    campaign_id → name, keyword_id → keyword 매핑 빌드.
    키워드는 adgroup별로 순회해야 하므로 시간이 걸림 → 실패해도 진행.
    """
    campaign_map = {}
    keyword_map = {}

    try:
        campaigns = client.list_campaigns()
        for c in campaigns:
            cid = c.get("nccCampaignId")
            if cid:
                campaign_map[cid] = c.get("name", cid)
        print(f"  ✓ 캠페인 {len(campaign_map)}개 매핑")
    except NaverAdsAPIError as e:
        print(f"  ⚠️  캠페인 조회 실패 ({e}) — ID로 표시됩니다.", file=sys.stderr)

    try:
        adgroups = client.list_adgroups()
        print(f"  ✓ 광고그룹 {len(adgroups)}개 발견, 키워드 매핑 중...")
        for ag in adgroups:
            ag_id = ag.get("nccAdgroupId")
            if not ag_id:
                continue
            try:
                kws = client.list_keywords(ag_id)
                for k in kws:
                    kid = k.get("nccKeywordId")
                    if kid:
                        keyword_map[kid] = k.get("keyword", kid)
            except NaverAdsAPIError:
                continue
        print(f"  ✓ 키워드 {len(keyword_map)}개 매핑")
    except NaverAdsAPIError as e:
        print(f"  ⚠️  광고그룹/키워드 조회 실패 ({e})", file=sys.stderr)

    return campaign_map, keyword_map


# ───────── 메인 ─────────

def main():
    parser = argparse.ArgumentParser(
        description="네이버 광고 성과 리포트 E2E 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 지난 7일
  python run_report.py --preset last7

  # 명시 기간 + 쇼핑검색광고 포함
  python run_report.py --date-from 2026-04-01 --date-to 2026-04-20 --include-shopping

  # 인자로 키 직접 전달
  python run_report.py --customer-id XXX --api-key YYY --secret-key ZZZ --preset yesterday
        """,
    )
    parser.add_argument("--customer-id", default=os.environ.get("NAVER_AD_CUSTOMER_ID"))
    parser.add_argument("--api-key", default=os.environ.get("NAVER_AD_API_KEY"))
    parser.add_argument("--secret-key", default=os.environ.get("NAVER_AD_SECRET_KEY"))
    parser.add_argument("--preset",
                        choices=["yesterday", "last7", "last14", "last30",
                                 "thismonth", "lastmonth", "lastweek"])
    parser.add_argument("--date-from", help="YYYY-MM-DD")
    parser.add_argument("--date-to", help="YYYY-MM-DD")
    parser.add_argument("--include-shopping", action="store_true",
                        help="쇼핑검색광고 상품별 리포트도 조회")
    parser.add_argument("--skip-master", action="store_true",
                        help="캠페인/키워드 매핑 조회 생략 (빠른 실행)")
    parser.add_argument("--output", default=None, help="HTML 저장 경로")
    parser.add_argument("--cache-dir", default="/tmp/naver_ads_cache",
                        help="TSV 캐시 디렉터리")
    args = parser.parse_args()

    # 날짜 확정
    if args.preset:
        date_from, date_to = resolve_date_preset(args.preset)
    elif args.date_from and args.date_to:
        date_from, date_to = args.date_from, args.date_to
    else:
        # 기본값
        date_from, date_to = resolve_date_preset("last7")
    print(f"📅 조회 기간: {date_from} ~ {date_to}")

    # 크레덴셜 확인
    if not (args.customer_id and args.api_key and args.secret_key):
        print("\n❌ 크레덴셜 누락.", file=sys.stderr)
        print("다음 중 하나로 제공하세요:", file=sys.stderr)
        print("  1) 환경변수: NAVER_AD_CUSTOMER_ID, NAVER_AD_API_KEY, NAVER_AD_SECRET_KEY", file=sys.stderr)
        print("  2) CLI 인자: --customer-id, --api-key, --secret-key", file=sys.stderr)
        print("\n값 확인: searchad.naver.com > 도구 > API 사용 관리", file=sys.stderr)
        sys.exit(1)

    creds = NaverAdsCredentials.from_args(args.customer_id, args.api_key, args.secret_key)
    client = NaverAdsClient(creds)

    # 인증 확인 (간단 호출)
    print("\n🔑 인증 확인...")
    try:
        _ = client.list_campaigns()
        print("  ✓ 인증 성공")
    except NaverAdsAPIError as e:
        print(f"\n❌ 인증 실패: {e}", file=sys.stderr)
        print("키 값을 다시 확인해 주세요.", file=sys.stderr)
        sys.exit(1)

    # 마스터 매핑
    campaign_map, keyword_map = {}, {}
    if not args.skip_master:
        print("\n🗂️  마스터 데이터 수집...")
        campaign_map, keyword_map = build_maps(client)

    cache_dir = Path(args.cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)

    # AD 리포트
    print("\n📊 AD 리포트 수집 중...")
    df_ad = fetch_stat_report(
        client,
        report_tp="AD",
        date_from=date_from,
        date_to=date_to,
        output_dir=str(cache_dir / "AD"),
    )

    if df_ad.empty:
        print("\n⚠️  AD 데이터 없음. 리포트 생성 중단.", file=sys.stderr)
        sys.exit(1)

    # Shopping 리포트 (선택)
    df_shop = None
    if args.include_shopping:
        print("\n🛒 SHOPPING_PRODUCT 리포트 수집 중...")
        try:
            df_shop = fetch_stat_report(
                client,
                report_tp="SHOPPING_PRODUCT",
                date_from=date_from,
                date_to=date_to,
                output_dir=str(cache_dir / "SHOPPING_PRODUCT"),
            )
        except Exception as e:
            print(f"  ⚠️  쇼핑검색광고 리포트 실패: {e}", file=sys.stderr)

    # HTML 생성
    print("\n🎨 HTML 리포트 생성 중...")
    output_path = render_report(
        df_ad=df_ad,
        df_shopping=df_shop,
        date_from=date_from,
        date_to=date_to,
        keyword_map=keyword_map if keyword_map else None,
        campaign_map=campaign_map if campaign_map else None,
        output_path=args.output,
    )

    print(f"\n✅ 완료!\n   📄 {output_path}")
    return output_path


if __name__ == "__main__":
    main()
