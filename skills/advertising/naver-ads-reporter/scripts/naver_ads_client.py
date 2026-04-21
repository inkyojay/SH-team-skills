#!/usr/bin/env python3
"""
네이버 검색광고 API 공통 클라이언트.

HMAC-SHA256 서명 생성, 헤더 구성, GET/POST 요청 유틸리티를 제공한다.
다른 스크립트에서 import하여 사용한다.

환경변수:
  NAVER_CUSTOMER_ID  (광고주 번호)
  NAVER_API_KEY      (액세스라이선스)
  NAVER_SECRET_KEY   (비밀키)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any, Optional

try:
    import requests
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages", "-q"])
    import requests


API_BASE = "https://api.searchad.naver.com"
DEFAULT_TIMEOUT = 30


@dataclass
class NaverAdsCredentials:
    customer_id: str
    api_key: str
    secret_key: str

    @classmethod
    def from_env(cls) -> "NaverAdsCredentials":
        """환경변수에서 크레덴셜 로드."""
        missing = []
        cid = os.environ.get("NAVER_CUSTOMER_ID")
        key = os.environ.get("NAVER_API_KEY")
        sec = os.environ.get("NAVER_SECRET_KEY")
        if not cid: missing.append("NAVER_CUSTOMER_ID")
        if not key: missing.append("NAVER_API_KEY")
        if not sec: missing.append("NAVER_SECRET_KEY")
        if missing:
            raise RuntimeError(
                f"환경변수 누락: {', '.join(missing)}\n"
                f"searchad.naver.com > 도구 > API 사용 관리에서 값을 확인한 뒤 설정하세요."
            )
        return cls(customer_id=cid, api_key=key, secret_key=sec)

    @classmethod
    def from_args(cls, customer_id: str, api_key: str, secret_key: str) -> "NaverAdsCredentials":
        return cls(customer_id=str(customer_id), api_key=api_key, secret_key=secret_key)


def _generate_signature(timestamp: str, method: str, path: str, secret_key: str) -> str:
    """
    HMAC-SHA256 서명 생성.
    네이버 검색광고 API 공식 규격:
      message = {timestamp}.{METHOD}.{path}
      HMAC-SHA256(secret_key.encode("utf-8"), message.encode("utf-8"))
      → hexdigest() 반환
    ref: searchad.naver.com developer guide
    """
    message = f"{timestamp}.{method}.{path}"
    return hmac.new(
        secret_key.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()


def _build_headers(creds: NaverAdsCredentials, method: str, path: str) -> dict:
    timestamp = str(int(time.time() * 1000))
    signature = _generate_signature(timestamp, method, path, creds.secret_key)
    return {
        "X-Timestamp": timestamp,
        "X-API-KEY": creds.api_key,
        "X-Customer": creds.customer_id,
        "X-Signature": signature,
        "Content-Type": "application/json; charset=UTF-8",
    }


class NaverAdsClient:
    """검색광고 API 호출 래퍼."""

    def __init__(self, creds: NaverAdsCredentials, base_url: str = API_BASE):
        self.creds = creds
        self.base_url = base_url
        self.session = requests.Session()

    # ───────── Low-level ─────────

    def request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        body: Optional[dict] = None,
        timeout: int = DEFAULT_TIMEOUT,
        max_retries: int = 3,
    ) -> Any:
        """
        공통 요청 메서드.
        429/5xx는 exponential backoff로 재시도.
        """
        method = method.upper()
        url = f"{self.base_url}{path}"

        for attempt in range(max_retries):
            headers = _build_headers(self.creds, method, path)
            try:
                if method == "GET":
                    resp = self.session.get(url, headers=headers, params=params, timeout=timeout)
                elif method == "POST":
                    resp = self.session.post(
                        url,
                        headers=headers,
                        params=params,
                        data=json.dumps(body or {}, ensure_ascii=False).encode("utf-8"),
                        timeout=timeout,
                    )
                elif method == "DELETE":
                    resp = self.session.delete(url, headers=headers, params=params, timeout=timeout)
                elif method == "PUT":
                    resp = self.session.put(
                        url,
                        headers=headers,
                        params=params,
                        data=json.dumps(body or {}, ensure_ascii=False).encode("utf-8"),
                        timeout=timeout,
                    )
                else:
                    raise ValueError(f"지원하지 않는 HTTP method: {method}")
            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait = 2 ** attempt
                    print(f"  ⚠️  네트워크 오류 ({e}), {wait}초 후 재시도...", file=sys.stderr)
                    time.sleep(wait)
                    continue
                raise

            # 2xx
            if 200 <= resp.status_code < 300:
                if not resp.content:
                    return None
                try:
                    return resp.json()
                except ValueError:
                    return resp.text

            # 429 rate limit
            if resp.status_code == 429:
                wait = 2 ** (attempt + 1) * 10  # 20s → 40s → 80s
                print(f"  ⚠️  Rate limit (429), {wait}초 대기...", file=sys.stderr)
                time.sleep(wait)
                continue

            # 5xx
            if 500 <= resp.status_code < 600 and attempt < max_retries - 1:
                wait = 2 ** attempt
                print(f"  ⚠️  서버 오류 ({resp.status_code}), {wait}초 후 재시도...", file=sys.stderr)
                time.sleep(wait)
                continue

            # 4xx (non-429) — 즉시 실패
            raise NaverAdsAPIError(
                status_code=resp.status_code,
                path=path,
                body=resp.text[:500],
            )

        raise NaverAdsAPIError(
            status_code=-1,
            path=path,
            body=f"최대 재시도 {max_retries}회 초과",
        )

    # ───────── High-level wrappers ─────────

    def list_campaigns(self) -> list[dict]:
        """전체 캠페인 목록 조회."""
        return self.request("GET", "/ncc/campaigns") or []

    def list_adgroups(self, campaign_id: Optional[str] = None) -> list[dict]:
        """광고그룹 목록 조회 (선택적으로 캠페인 필터)."""
        params = {"nccCampaignId": campaign_id} if campaign_id else None
        return self.request("GET", "/ncc/adgroups", params=params) or []

    def list_keywords(self, adgroup_id: str) -> list[dict]:
        """특정 광고그룹의 키워드 목록."""
        params = {"nccAdgroupId": adgroup_id}
        return self.request("GET", "/ncc/keywords", params=params) or []

    def list_ads(self, adgroup_id: str) -> list[dict]:
        """특정 광고그룹의 소재 목록."""
        params = {"nccAdgroupId": adgroup_id}
        return self.request("GET", "/ncc/ads", params=params) or []

    def get_realtime_stats(self, ids: list[str], fields: list[str], timerange: str) -> Any:
        """
        /stats 실시간 통계 (제한적).
        timerange: JSON string, e.g. '{"since":"2026-04-20","until":"2026-04-21"}'
        fields: ['impCnt', 'clkCnt', 'salesAmt', ...]
        """
        params = {
            "ids": ",".join(ids),
            "fields": json.dumps(fields),
            "timeRange": timerange,
        }
        return self.request("GET", "/stats", params=params)


class NaverAdsAPIError(Exception):
    def __init__(self, status_code: int, path: str, body: str):
        self.status_code = status_code
        self.path = path
        self.body = body
        super().__init__(f"[{status_code}] {path} → {body}")


# ───────── CLI 테스트 진입점 ─────────

def _cli():
    """
    인증 테스트용 CLI.
    python naver_ads_client.py --test
    → 캠페인 목록 조회하여 인증 정상 여부 확인.
    """
    import argparse
    parser = argparse.ArgumentParser(description="네이버 검색광고 API 클라이언트 테스트")
    parser.add_argument("--customer-id", default=os.environ.get("NAVER_CUSTOMER_ID"))
    parser.add_argument("--api-key", default=os.environ.get("NAVER_API_KEY"))
    parser.add_argument("--secret-key", default=os.environ.get("NAVER_SECRET_KEY"))
    parser.add_argument("--test", action="store_true", help="캠페인 목록 조회로 인증 테스트")
    args = parser.parse_args()

    if not (args.customer_id and args.api_key and args.secret_key):
        print("❌ 크레덴셜 3종 모두 필요합니다. (인자 or 환경변수)", file=sys.stderr)
        sys.exit(1)

    creds = NaverAdsCredentials.from_args(args.customer_id, args.api_key, args.secret_key)
    client = NaverAdsClient(creds)

    if args.test:
        print("🔑 인증 테스트 중...")
        try:
            campaigns = client.list_campaigns()
            print(f"✅ 인증 성공. 캠페인 {len(campaigns)}개 조회됨.\n")
            for c in campaigns[:10]:
                print(f"  - [{c.get('nccCampaignId')}] {c.get('name')} "
                      f"(type={c.get('campaignTp')}, status={c.get('status')})")
            if len(campaigns) > 10:
                print(f"  ... 외 {len(campaigns) - 10}개")
        except NaverAdsAPIError as e:
            print(f"❌ API 오류: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    _cli()
