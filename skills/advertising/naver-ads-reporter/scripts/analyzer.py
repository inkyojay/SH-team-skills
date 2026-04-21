#!/usr/bin/env python3
"""
네이버 광고 성과 데이터 분석 유틸리티.

입력: stat_report.fetch_stat_report()로 받은 DataFrame
출력: 요약 딕셔너리 / 정렬된 DataFrame / 분석 결과

썬데이허그 판단 기준:
  - ROAS 500% 미만 = 개선 필요
  - CTR 2% 미만 + 노출 1,000+ = 소재/키워드 점검
  - 비용 10,000+ × 전환 0 = 낭비 키워드
  - 전일 대비 비용 ±50% = 이상치
"""

from __future__ import annotations

import sys
from typing import Optional

try:
    import numpy as np
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "numpy", "pandas",
         "--break-system-packages", "-q"]
    )
    import numpy as np
    import pandas as pd


# ───────── 공통 유틸 ─────────

def _safe_div(a, b):
    """0 나누기 안전 처리."""
    return a / b if b else 0


def _ensure_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """숫자 컬럼 보정."""
    for c in ["impressions", "clicks", "cost", "conversions", "conversion_value", "avg_rank"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df


def _add_derived(df: pd.DataFrame) -> pd.DataFrame:
    """CTR, CPC, ROAS 파생 컬럼 추가."""
    df = _ensure_numeric(df.copy())
    if "impressions" in df.columns and "clicks" in df.columns:
        df["ctr"] = df.apply(
            lambda r: _safe_div(r["clicks"], r["impressions"]) * 100, axis=1
        )
    if "clicks" in df.columns and "cost" in df.columns:
        df["cpc"] = df.apply(lambda r: _safe_div(r["cost"], r["clicks"]), axis=1)
    if "conversion_value" in df.columns and "cost" in df.columns:
        df["roas"] = df.apply(
            lambda r: _safe_div(r["conversion_value"], r["cost"]) * 100, axis=1
        )
    return df


# ───────── 1. 전체 요약 ─────────

def summarize_overall(df: pd.DataFrame) -> dict:
    """전체 기간 핵심 지표 요약."""
    if df.empty:
        return {"empty": True}

    df = _ensure_numeric(df)
    total_imp = int(df.get("impressions", pd.Series([0])).sum())
    total_clk = int(df.get("clicks", pd.Series([0])).sum())
    total_cost = int(df.get("cost", pd.Series([0])).sum())
    total_conv = int(df.get("conversions", pd.Series([0])).sum()) if "conversions" in df.columns else 0
    total_conv_value = int(df.get("conversion_value", pd.Series([0])).sum()) if "conversion_value" in df.columns else 0

    return {
        "impressions": total_imp,
        "clicks": total_clk,
        "cost": total_cost,
        "conversions": total_conv,
        "conversion_value": total_conv_value,
        "ctr": round(_safe_div(total_clk, total_imp) * 100, 2),
        "cpc": int(_safe_div(total_cost, total_clk)),
        "roas": round(_safe_div(total_conv_value, total_cost) * 100, 2),
        "cpa": int(_safe_div(total_cost, total_conv)) if total_conv else 0,
        "conv_rate": round(_safe_div(total_conv, total_clk) * 100, 2),
        "days": df["date"].nunique() if "date" in df.columns else 0,
    }


# ───────── 2. 캠페인별 집계 ─────────

def by_campaign(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "campaign_id" not in df.columns:
        return pd.DataFrame()

    df = _ensure_numeric(df)
    agg_cols = {
        "impressions": "sum",
        "clicks": "sum",
        "cost": "sum",
    }
    if "conversions" in df.columns:
        agg_cols["conversions"] = "sum"
    if "conversion_value" in df.columns:
        agg_cols["conversion_value"] = "sum"

    grouped = df.groupby("campaign_id", as_index=False).agg(agg_cols)
    return _add_derived(grouped).sort_values("cost", ascending=False)


# ───────── 3. 일별 추이 ─────────

def daily_trend(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "date" not in df.columns:
        return pd.DataFrame()

    df = _ensure_numeric(df)
    agg_cols = {"impressions": "sum", "clicks": "sum", "cost": "sum"}
    if "conversions" in df.columns:
        agg_cols["conversions"] = "sum"
    if "conversion_value" in df.columns:
        agg_cols["conversion_value"] = "sum"

    daily = df.groupby("date", as_index=False).agg(agg_cols)
    return _add_derived(daily).sort_values("date")


# ───────── 4. Top N 키워드 ─────────

def top_keywords(
    df: pd.DataFrame,
    metric: str = "cost",
    n: int = 20,
    keyword_map: Optional[dict] = None,
) -> pd.DataFrame:
    """
    키워드별 집계 → 지표 Top N.
    keyword_map: {keyword_id: keyword_text} (client.list_keywords로 별도 확보)
    """
    if df.empty or "keyword_id" not in df.columns:
        return pd.DataFrame()

    df = _ensure_numeric(df)
    agg_cols = {"impressions": "sum", "clicks": "sum", "cost": "sum"}
    if "conversions" in df.columns:
        agg_cols["conversions"] = "sum"
    if "conversion_value" in df.columns:
        agg_cols["conversion_value"] = "sum"

    grouped = df.groupby("keyword_id", as_index=False).agg(agg_cols)
    grouped = _add_derived(grouped)

    if keyword_map:
        grouped["keyword"] = grouped["keyword_id"].map(keyword_map).fillna(grouped["keyword_id"])

    if metric not in grouped.columns:
        metric = "cost"
    return grouped.sort_values(metric, ascending=False).head(n)


# ───────── 5. 낭비 키워드 ─────────

def wasted_keywords(
    df: pd.DataFrame,
    min_cost: int = 10_000,
    keyword_map: Optional[dict] = None,
) -> pd.DataFrame:
    """비용은 썼는데 전환 0인 키워드."""
    if df.empty or "keyword_id" not in df.columns:
        return pd.DataFrame()

    if "conversions" not in df.columns:
        print("  ⚠️  전환 컬럼 없음 — 낭비 키워드 분석 불가", file=sys.stderr)
        return pd.DataFrame()

    df = _ensure_numeric(df)
    grouped = df.groupby("keyword_id", as_index=False).agg({
        "impressions": "sum",
        "clicks": "sum",
        "cost": "sum",
        "conversions": "sum",
    })
    wasted = grouped[(grouped["cost"] >= min_cost) & (grouped["conversions"] == 0)]
    wasted = _add_derived(wasted)

    if keyword_map:
        wasted["keyword"] = wasted["keyword_id"].map(keyword_map).fillna(wasted["keyword_id"])

    return wasted.sort_values("cost", ascending=False)


# ───────── 6. 상품별 ROAS (쇼핑검색광고) ─────────

def product_roas_rank(df: pd.DataFrame, top: int = 20) -> pd.DataFrame:
    """NV_MID(상품) 단위 집계 → ROAS 순위."""
    if df.empty or "product_id_nv_mid" not in df.columns:
        return pd.DataFrame()

    df = _ensure_numeric(df)
    agg_cols = {
        "impressions": "sum",
        "clicks": "sum",
        "cost": "sum",
    }
    if "conversions" in df.columns:
        agg_cols["conversions"] = "sum"
    if "conversion_value" in df.columns:
        agg_cols["conversion_value"] = "sum"

    # 상품명은 최빈값 유지
    grouped = df.groupby("product_id_nv_mid", as_index=False).agg(agg_cols)
    if "product_name" in df.columns:
        name_map = df.groupby("product_id_nv_mid")["product_name"].agg(
            lambda s: s.mode().iat[0] if len(s.mode()) else ""
        )
        grouped["product_name"] = grouped["product_id_nv_mid"].map(name_map)

    grouped = _add_derived(grouped)
    if "roas" not in grouped.columns:
        # 전환 데이터가 없는 리포트일 경우 cost 기준
        return grouped.sort_values("cost", ascending=False).head(top)
    return grouped.sort_values("roas", ascending=False).head(top)


# ───────── 7. 기간 비교 ─────────

def compare_periods(df_a: pd.DataFrame, df_b: pd.DataFrame, label_a: str = "A", label_b: str = "B") -> dict:
    """두 기간의 요약을 비교하여 증감률 계산."""
    sum_a = summarize_overall(df_a)
    sum_b = summarize_overall(df_b)

    def pct_change(old, new):
        if old == 0:
            return None
        return round((new - old) / old * 100, 1)

    metrics = ["impressions", "clicks", "cost", "conversions", "conversion_value",
               "ctr", "cpc", "roas", "cpa", "conv_rate"]
    comparison = {}
    for m in metrics:
        a_val = sum_a.get(m, 0)
        b_val = sum_b.get(m, 0)
        comparison[m] = {
            label_a: a_val,
            label_b: b_val,
            "delta": b_val - a_val if isinstance(a_val, (int, float)) else None,
            "pct": pct_change(a_val, b_val) if isinstance(a_val, (int, float)) else None,
        }
    return {"label_a": label_a, "label_b": label_b, "metrics": comparison}


# ───────── 8. 이상치 탐지 ─────────

def detect_anomaly(
    df: pd.DataFrame,
    metric: str = "cost",
    z_threshold: float = 2.5,
) -> pd.DataFrame:
    """
    일별 추이 기준으로 metric의 z-score가 threshold 초과한 날 반환.
    """
    if df.empty or "date" not in df.columns:
        return pd.DataFrame()

    daily = daily_trend(df)
    if daily.empty or metric not in daily.columns:
        return pd.DataFrame()

    mean = daily[metric].mean()
    std = daily[metric].std(ddof=0)
    if std == 0:
        return pd.DataFrame()

    daily["z_score"] = (daily[metric] - mean) / std
    daily["pct_from_mean"] = ((daily[metric] - mean) / mean * 100).round(1)
    anomalies = daily[daily["z_score"].abs() >= z_threshold].copy()
    return anomalies.sort_values("date")


# ───────── 9. 인사이트 생성 ─────────

def generate_insights(
    overall: dict,
    campaigns: pd.DataFrame,
    daily: pd.DataFrame,
    wasted: pd.DataFrame,
    products: pd.DataFrame,
) -> list[str]:
    """분석 결과를 사람이 읽을 수 있는 인사이트 문장 리스트로."""
    insights = []

    # ROAS 판단
    roas = overall.get("roas", 0)
    if roas and roas < 200:
        insights.append(
            f"⚠️ 전체 ROAS가 {roas}%로 매우 낮습니다. 전환 추적 설정 점검 + 고ROAS 키워드 비중 확대 필요."
        )
    elif roas and roas < 500:
        insights.append(
            f"⚠️ 전체 ROAS {roas}%는 썬데이허그 기준(500%) 미달입니다. 비효율 키워드/상품 점검 필요."
        )
    elif roas and roas >= 500:
        insights.append(f"✅ 전체 ROAS {roas}%로 양호합니다.")

    # CTR
    ctr = overall.get("ctr", 0)
    if ctr and ctr < 2.0:
        insights.append(
            f"📉 전체 CTR {ctr}%가 2% 미만입니다. 광고 소재/키워드 관련성 재검토 권장."
        )

    # 낭비 키워드
    if not wasted.empty:
        total_waste = int(wasted["cost"].sum())
        insights.append(
            f"💸 전환 없는 낭비 키워드 {len(wasted)}개가 총 {total_waste:,}원 소진. "
            f"키워드 OFF 또는 입찰 조정 필요."
        )

    # 캠페인 집중도
    if not campaigns.empty and len(campaigns) >= 2:
        top_cost = campaigns.iloc[0]["cost"]
        total_cost = campaigns["cost"].sum()
        if total_cost > 0:
            concentration = top_cost / total_cost * 100
            if concentration > 60:
                insights.append(
                    f"📊 1위 캠페인이 전체 비용의 {concentration:.0f}%를 차지합니다. "
                    f"포트폴리오 다각화 검토 권장."
                )

    # 상품 성과
    if not products.empty and "roas" in products.columns:
        top_roas_product = products.iloc[0]
        if top_roas_product.get("roas", 0) >= 1000:
            name = top_roas_product.get("product_name", top_roas_product.get("product_id_nv_mid"))
            insights.append(
                f"🏆 최고 ROAS 상품: '{name}' ({top_roas_product['roas']:.0f}%). "
                f"예산 비중 확대 고려."
            )

    # 일별 이상치
    daily_anom = detect_anomaly(daily, metric="cost") if "cost" in daily.columns else pd.DataFrame()
    if not daily_anom.empty:
        for _, row in daily_anom.iterrows():
            direction = "급증" if row["z_score"] > 0 else "급감"
            insights.append(
                f"⚡ {row['date']} 비용 {direction} (평균 대비 {row['pct_from_mean']:+.0f}%). 원인 점검 필요."
            )

    if not insights:
        insights.append("✅ 특이사항 없음. 전반적으로 안정적 집행 중.")

    return insights


# ───────── CLI 테스트 ─────────

def _cli():
    """TSV 파일 입력 받아서 분석 결과 출력 (디버깅용)."""
    import argparse
    parser = argparse.ArgumentParser(description="수집된 TSV 파일을 분석")
    parser.add_argument("--input", required=True, help="TSV 파일 경로")
    parser.add_argument("--report-tp", default="AD")
    args = parser.parse_args()

    df = pd.read_csv(args.input, sep="\t", dtype=str)
    print(f"\n📂 로드: {len(df):,} rows, {len(df.columns)}컬럼")

    print("\n━━ 전체 요약 ━━")
    overall = summarize_overall(df)
    for k, v in overall.items():
        print(f"  {k}: {v:,}" if isinstance(v, (int, float)) else f"  {k}: {v}")

    print("\n━━ 캠페인별 ━━")
    camp = by_campaign(df)
    if not camp.empty:
        print(camp.head(10).to_string(index=False))

    print("\n━━ 인사이트 ━━")
    daily = daily_trend(df)
    wasted = wasted_keywords(df) if "keyword_id" in df.columns else pd.DataFrame()
    products = product_roas_rank(df) if "product_id_nv_mid" in df.columns else pd.DataFrame()
    for ins in generate_insights(overall, camp, daily, wasted, products):
        print(f"  {ins}")


if __name__ == "__main__":
    _cli()
