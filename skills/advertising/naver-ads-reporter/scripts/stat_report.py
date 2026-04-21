#!/usr/bin/env python3
"""
네이버 검색광고 대용량 보고서(StatReport) 비동기 처리.

Flow:
  1. POST /stat-reports { reportTp, statDt } → reportJobId 수령
  2. GET /stat-reports/{id} 폴링 → status: REGIST → RUNNING → BUILT
  3. BUILT되면 downloadUrl로 TSV 파일 다운로드
  4. pandas DataFrame으로 파싱하여 반환 또는 파일로 저장

사용법 (CLI):
  python stat_report.py \
    --report-tp AD \
    --date-from 2026-04-14 \
    --date-to 2026-04-20 \
    --output /tmp/report_ad.tsv

사용법 (모듈):
  from stat_report import fetch_stat_report
  df = fetch_stat_report(client, report_tp="AD", date_from="2026-04-14", date_to="2026-04-20")
"""

from __future__ import annotations

import argparse
import gzip
import io
import os
import sys
import time
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

try:
    import requests
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "requests", "pandas",
         "--break-system-packages", "-q"]
    )
    import requests
    import pandas as pd

# 같은 폴더의 client import
sys.path.insert(0, str(Path(__file__).parent))
from naver_ads_client import NaverAdsClient, NaverAdsCredentials, NaverAdsAPIError  # noqa: E402


# ───────── 리포트 타입별 예상 컬럼 스키마 ─────────
# 네이버 공식 문서 기준. 실제 다운로드한 TSV의 헤더가 없거나 다를 수 있으므로
# 파싱 시 컬럼 개수로 자동 추론 + 사용자가 override 가능.

REPORT_COLUMNS = {
    "AD": [
        "date", "customer_id", "campaign_id", "adgroup_id", "keyword_id",
        "ad_id", "business_channel_id", "media", "pc_mobile_type",
        "impressions", "clicks", "cost", "avg_rank",
    ],
    "AD_DETAIL": [
        "date", "customer_id", "campaign_id", "adgroup_id", "keyword_id",
        "ad_id", "business_channel_id", "media", "pc_mobile_type",
        "impressions", "clicks", "cost", "avg_rank",
    ],
    "AD_CONVERSION": [
        "date", "customer_id", "campaign_id", "adgroup_id", "keyword_id",
        "ad_id", "business_channel_id", "media", "pc_mobile_type",
        "conv_type", "conversions", "conversion_value",
    ],
    "KEYWORD": [
        "date", "customer_id", "campaign_id", "adgroup_id", "keyword_id",
        "impressions", "clicks", "cost", "avg_rank",
    ],
    "SHOPPING_PRODUCT": [
        "date", "customer_id", "campaign_id", "adgroup_id",
        "product_id_nv_mid", "product_name",
        "media", "pc_mobile_type",
        "impressions", "clicks", "cost",
    ],
    "SHOPPING_PRODUCT_CONVERSION": [
        "date", "customer_id", "campaign_id", "adgroup_id",
        "product_id_nv_mid", "product_name",
        "media", "pc_mobile_type",
        "conv_type", "conversions", "conversion_value",
    ],
    "SHOPPINGBRANDPRODUCT": [
        "date", "customer_id", "campaign_id", "adgroup_id",
        "product_id_nv_mid", "product_name",
        "media", "pc_mobile_type",
        "impressions", "clicks", "cost",
    ],
}

DEFAULT_POLL_INTERVAL = 3
MAX_POLL_INTERVAL = 15
POLL_TIMEOUT = 180  # 초


# ───────── 1. Report job 발급 ─────────

def create_report_job(client: NaverAdsClient, report_tp: str, stat_dt: str) -> str:
    """
    Stat Report 발급 요청.
    stat_dt: 'YYYY-MM-DD' 형식. 하나의 날짜만 가능(API 제약).
    반환: reportJobId (int or str)
    """
    body = {"reportTp": report_tp, "statDt": stat_dt}
    resp = client.request("POST", "/stat-reports", body=body)
    # 응답 형태: {"reportJobId": 12345, "status": "REGIST", ...}
    job_id = resp.get("reportJobId") if isinstance(resp, dict) else None
    if job_id is None:
        raise RuntimeError(f"reportJobId를 받지 못함. 응답: {resp}")
    return str(job_id)


# ───────── 2. Polling ─────────

def poll_until_built(client: NaverAdsClient, job_id: str, timeout: int = POLL_TIMEOUT) -> dict:
    """
    상태가 BUILT가 될 때까지 폴링.
    반환: 최종 job dict (downloadUrl 포함)
    """
    started = time.time()
    interval = DEFAULT_POLL_INTERVAL
    last_status = None

    while time.time() - started < timeout:
        job = client.request("GET", f"/stat-reports/{job_id}")
        status = job.get("status") if isinstance(job, dict) else None
        if status != last_status:
            print(f"  📡 job {job_id} 상태: {status}")
            last_status = status

        if status == "BUILT":
            return job
        if status in ("FAILED", "EXPIRED", "CANCELED", "NONE"):
            raise RuntimeError(f"Report job 실패: status={status}, detail={job}")

        time.sleep(interval)
        interval = min(interval + 2, MAX_POLL_INTERVAL)

    raise TimeoutError(f"Report {job_id} 폴링 타임아웃 ({timeout}초)")


# ───────── 3. Download ─────────

def download_report(client: NaverAdsClient, job: dict, output_path: Optional[str] = None) -> bytes:
    """
    BUILT 상태 job의 downloadUrl에서 TSV 파일 다운로드.
    downloadUrl은 인증이 필요한 경우와 아닌 경우가 모두 있음 — 우선 인증 없이 시도.
    """
    url = job.get("downloadUrl")
    if not url:
        raise RuntimeError(f"downloadUrl 없음. job={job}")

    # 일부 응답은 직접 URL, 일부는 GET /stat-reports/{id}/download 형태
    for attempt in range(3):
        try:
            headers = {"Authorization": f"Bearer {client.creds.api_key}"}
            # 우선 인증 헤더 없이 시도 (presigned url)
            resp = requests.get(url, timeout=60)
            if resp.status_code == 401 or resp.status_code == 403:
                resp = requests.get(url, headers=headers, timeout=60)
            resp.raise_for_status()
            content = resp.content
            # 일부 리포트는 gzip 압축
            if content[:2] == b"\x1f\x8b":
                content = gzip.decompress(content)
            if output_path:
                Path(output_path).write_bytes(content)
                print(f"  💾 저장: {output_path} ({len(content):,} bytes)")
            return content
        except requests.exceptions.RequestException as e:
            if attempt < 2:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"다운로드 실패: {e}")


# ───────── 4. Parse TSV → DataFrame ─────────

def parse_tsv(content: bytes, report_tp: str) -> pd.DataFrame:
    """
    TSV 바이트를 DataFrame으로 파싱.
    - 헤더가 있으면 그대로 사용
    - 없으면 REPORT_COLUMNS의 기본 스키마 적용
    """
    text = content.decode("utf-8", errors="replace")
    if not text.strip():
        return pd.DataFrame()

    first_line = text.split("\n", 1)[0]
    fields = first_line.split("\t")
    # 헤더 휴리스틱: 첫 줄에 숫자만 있으면 헤더 없음
    has_header = any(not f.strip().replace("-", "").replace(".", "").isdigit()
                     for f in fields if f.strip())
    # 단, 'date' 컬럼은 YYYYMMDD 형태라 숫자로 보일 수 있음 → 첫 필드만 체크
    first_field = fields[0].strip() if fields else ""
    if first_field.isdigit() and len(first_field) == 8:
        has_header = False

    cols = REPORT_COLUMNS.get(report_tp)
    if has_header:
        df = pd.read_csv(io.StringIO(text), sep="\t", dtype=str)
    else:
        df = pd.read_csv(io.StringIO(text), sep="\t", header=None, dtype=str,
                         names=cols if cols else None)

    # 컬럼 개수가 안 맞으면 경고만 내고 진행
    if cols and len(df.columns) != len(cols):
        print(f"  ⚠️  컬럼 개수 불일치 (실제 {len(df.columns)}개 vs 예상 {len(cols)}개). "
              f"스키마를 재확인하세요.", file=sys.stderr)

    # 숫자형 변환
    numeric_cols = ["impressions", "clicks", "cost", "conversions",
                    "conversion_value", "avg_rank"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)

    # date 컬럼 표준화 (YYYYMMDD → YYYY-MM-DD)
    if "date" in df.columns:
        df["date"] = df["date"].astype(str).str.replace(
            r"^(\d{4})(\d{2})(\d{2})$", r"\1-\2-\3", regex=True
        )

    return df


# ───────── 5. 통합 Fetch 함수 ─────────

def fetch_stat_report(
    client: NaverAdsClient,
    report_tp: str,
    date_from: str,
    date_to: str,
    output_dir: Optional[str] = None,
) -> pd.DataFrame:
    """
    기간 내 일자별로 순회하며 각 날짜의 Stat Report를 발급·다운로드·병합.
    반환: 전체 기간 통합 DataFrame.
    """
    d_from = datetime.strptime(date_from, "%Y-%m-%d").date()
    d_to = datetime.strptime(date_to, "%Y-%m-%d").date()
    if d_from > d_to:
        raise ValueError("date_from이 date_to보다 나중입니다.")

    output_dir = Path(output_dir) if output_dir else None
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    current = d_from
    while current <= d_to:
        stat_dt = current.strftime("%Y-%m-%d")
        print(f"\n📊 [{stat_dt}] {report_tp} 리포트 발급...")
        try:
            job_id = create_report_job(client, report_tp, stat_dt)
            print(f"  ✓ reportJobId: {job_id}")
            job = poll_until_built(client, job_id)
            print(f"  ✓ BUILT (downloadUrl 수령)")
            content = download_report(
                client, job,
                output_path=str(output_dir / f"{report_tp}_{stat_dt}.tsv") if output_dir else None
            )
            df = parse_tsv(content, report_tp)
            if len(df):
                frames.append(df)
                print(f"  ✓ {len(df):,} rows 파싱")
            else:
                print(f"  ⚠️  데이터 없음 (해당 일자 집행 없음)")
        except (NaverAdsAPIError, RuntimeError, TimeoutError) as e:
            print(f"  ❌ [{stat_dt}] 실패: {e}", file=sys.stderr)
        current += timedelta(days=1)

    if not frames:
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    print(f"\n✅ 전체 기간 병합: {len(combined):,} rows")
    return combined


# ───────── CLI ─────────

def _cli():
    parser = argparse.ArgumentParser(description="네이버 검색광고 Stat Report 다운로더")
    parser.add_argument("--customer-id", default=os.environ.get("NAVER_CUSTOMER_ID"))
    parser.add_argument("--api-key", default=os.environ.get("NAVER_API_KEY"))
    parser.add_argument("--secret-key", default=os.environ.get("NAVER_SECRET_KEY"))
    parser.add_argument("--report-tp", required=True,
                        choices=list(REPORT_COLUMNS.keys()),
                        help="리포트 타입")
    parser.add_argument("--date-from", required=True, help="YYYY-MM-DD")
    parser.add_argument("--date-to", required=True, help="YYYY-MM-DD")
    parser.add_argument("--output", default=None, help="병합 TSV 저장 경로 (선택)")
    parser.add_argument("--output-dir", default=None, help="일자별 TSV 저장 디렉터리 (선택)")
    args = parser.parse_args()

    if not (args.customer_id and args.api_key and args.secret_key):
        print("❌ 크레덴셜 3종이 모두 필요합니다.", file=sys.stderr)
        sys.exit(1)

    creds = NaverAdsCredentials.from_args(args.customer_id, args.api_key, args.secret_key)
    client = NaverAdsClient(creds)

    df = fetch_stat_report(
        client,
        report_tp=args.report_tp,
        date_from=args.date_from,
        date_to=args.date_to,
        output_dir=args.output_dir,
    )

    if args.output and len(df):
        df.to_csv(args.output, sep="\t", index=False)
        print(f"\n💾 병합본 저장: {args.output}")

    if len(df):
        print(f"\n📋 샘플 (상위 5행):")
        print(df.head().to_string())
    else:
        print("\n⚠️  수집된 데이터 없음")


if __name__ == "__main__":
    _cli()
