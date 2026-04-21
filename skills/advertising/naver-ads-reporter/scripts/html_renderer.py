#!/usr/bin/env python3
"""
네이버 광고 성과 데이터를 인터랙티브 HTML 리포트로 렌더링.

썬데이허그 브랜드 톤:
  - 프라이머리: 코랄 #FF6B6B
  - 서브: 베이비 블루 #A8E6CF
  - 폰트: Pretendard
  - 모바일 반응형
  - Chart.js 일별 추이 차트

출력: /mnt/user-data/outputs/naver_ads_report_YYYYMMDD_HHMM.html
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from html import escape
from pathlib import Path
from typing import Optional

try:
    import pandas as pd
except ImportError:
    import subprocess
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "pandas", "--break-system-packages", "-q"]
    )
    import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from analyzer import (  # noqa: E402
    summarize_overall, by_campaign, daily_trend, top_keywords,
    wasted_keywords, product_roas_rank, generate_insights
)


def _fmt_money(v) -> str:
    return f"{int(v):,}원" if v else "0원"


def _fmt_int(v) -> str:
    return f"{int(v):,}" if v else "0"


def _fmt_pct(v, digits: int = 2) -> str:
    return f"{float(v):.{digits}f}%" if v else "0%"


def _metric_card(label: str, value: str, sub: str = "", color: str = "default") -> str:
    color_class = {
        "good": "card-good",
        "warn": "card-warn",
        "bad": "card-bad",
        "default": "",
    }.get(color, "")
    sub_html = f'<div class="metric-sub">{escape(sub)}</div>' if sub else ""
    return f"""
    <div class="metric-card {color_class}">
      <div class="metric-label">{escape(label)}</div>
      <div class="metric-value">{escape(value)}</div>
      {sub_html}
    </div>
    """


def _roas_color(roas: float) -> str:
    if roas >= 500: return "good"
    if roas >= 200: return "warn"
    if roas > 0: return "bad"
    return "default"


def _table_from_df(df: pd.DataFrame, columns: list[tuple[str, str, str]]) -> str:
    """
    columns: [(df_col, display_name, formatter), ...]
    formatter ∈ {"int", "money", "pct", "text", "pct2"}
    """
    if df.empty:
        return '<p class="empty">데이터 없음</p>'

    thead = "".join(f"<th>{escape(name)}</th>" for _, name, _ in columns)
    rows_html = []
    for _, row in df.iterrows():
        tds = []
        for col, _, fmt in columns:
            val = row.get(col, "")
            if fmt == "int":
                tds.append(f"<td class='num'>{_fmt_int(val)}</td>")
            elif fmt == "money":
                tds.append(f"<td class='num'>{_fmt_money(val)}</td>")
            elif fmt == "pct":
                tds.append(f"<td class='num'>{_fmt_pct(val, 1)}</td>")
            elif fmt == "pct2":
                tds.append(f"<td class='num'>{_fmt_pct(val, 2)}</td>")
            else:
                tds.append(f"<td>{escape(str(val))}</td>")
        rows_html.append("<tr>" + "".join(tds) + "</tr>")

    return f"""
    <table class="data-table">
      <thead><tr>{thead}</tr></thead>
      <tbody>{"".join(rows_html)}</tbody>
    </table>
    """


def render_report(
    df_ad: pd.DataFrame,
    date_from: str,
    date_to: str,
    df_shopping: Optional[pd.DataFrame] = None,
    keyword_map: Optional[dict] = None,
    campaign_map: Optional[dict] = None,
    output_path: Optional[str] = None,
) -> str:
    """
    메인 렌더 함수.
    df_ad: AD 리포트 DataFrame
    df_shopping: SHOPPING_PRODUCT 리포트 DataFrame (선택)
    keyword_map/campaign_map: ID → 이름 매핑 딕셔너리
    반환: 저장된 파일 경로
    """
    # 집계
    overall = summarize_overall(df_ad)
    camp_df = by_campaign(df_ad)
    if campaign_map is not None and not camp_df.empty:
        camp_df["campaign_name"] = camp_df["campaign_id"].map(campaign_map).fillna(camp_df["campaign_id"])
    else:
        camp_df["campaign_name"] = camp_df.get("campaign_id", "")

    daily_df = daily_trend(df_ad)
    top_kw = top_keywords(df_ad, metric="cost", n=20, keyword_map=keyword_map)
    wasted_kw = wasted_keywords(df_ad, keyword_map=keyword_map)

    if df_shopping is not None and not df_shopping.empty:
        product_df = product_roas_rank(df_shopping, top=20)
    else:
        product_df = pd.DataFrame()

    insights = generate_insights(overall, camp_df, daily_df, wasted_kw, product_df)

    # 일별 추이 차트 데이터 (Chart.js용)
    chart_data = {
        "labels": daily_df["date"].tolist() if not daily_df.empty else [],
        "cost": daily_df["cost"].tolist() if not daily_df.empty else [],
        "clicks": daily_df["clicks"].tolist() if not daily_df.empty else [],
        "conversions": daily_df["conversions"].tolist()
                       if not daily_df.empty and "conversions" in daily_df.columns else [],
    }

    # ───────── HTML 빌드 ─────────
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    days_count = overall.get("days", 0)

    # 핵심 지표 카드
    roas_val = overall.get("roas", 0)
    cards_html = (
        _metric_card("총 광고비", _fmt_money(overall.get("cost", 0)),
                     f"{days_count}일 집행") +
        _metric_card("노출 수", _fmt_int(overall.get("impressions", 0))) +
        _metric_card("클릭 수", _fmt_int(overall.get("clicks", 0)),
                     f"CTR {overall.get('ctr', 0)}%") +
        _metric_card("CPC", _fmt_money(overall.get("cpc", 0))) +
        _metric_card("전환 수", _fmt_int(overall.get("conversions", 0)),
                     f"전환율 {overall.get('conv_rate', 0)}%") +
        _metric_card("전환 매출", _fmt_money(overall.get("conversion_value", 0))) +
        _metric_card("ROAS", _fmt_pct(roas_val, 0),
                     "썬데이허그 기준 500%", _roas_color(roas_val)) +
        _metric_card("CPA", _fmt_money(overall.get("cpa", 0)))
    )

    # 캠페인 테이블
    camp_cols = [
        ("campaign_name", "캠페인", "text"),
        ("impressions", "노출", "int"),
        ("clicks", "클릭", "int"),
        ("ctr", "CTR", "pct2"),
        ("cost", "비용", "money"),
        ("cpc", "CPC", "money"),
    ]
    if "conversions" in camp_df.columns:
        camp_cols += [
            ("conversions", "전환", "int"),
            ("roas", "ROAS", "pct"),
        ]
    camp_table_html = _table_from_df(camp_df, camp_cols)

    # Top 비용 키워드
    top_cost_cols = [
        ("keyword", "키워드", "text") if "keyword" in top_kw.columns else ("keyword_id", "키워드 ID", "text"),
        ("impressions", "노출", "int"),
        ("clicks", "클릭", "int"),
        ("ctr", "CTR", "pct2"),
        ("cost", "비용", "money"),
    ]
    if "roas" in top_kw.columns:
        top_cost_cols.append(("roas", "ROAS", "pct"))
    top_cost_html = _table_from_df(top_kw.head(20), top_cost_cols)

    # Top ROAS 키워드
    if "roas" in top_kw.columns:
        top_roas_kw = top_kw.sort_values("roas", ascending=False).head(20)
        top_roas_html = _table_from_df(top_roas_kw, top_cost_cols)
    else:
        top_roas_html = '<p class="empty">전환 데이터가 없어 ROAS 순위를 계산할 수 없습니다.</p>'

    # 낭비 키워드
    wasted_cols = [
        ("keyword", "키워드", "text") if "keyword" in wasted_kw.columns else ("keyword_id", "키워드 ID", "text"),
        ("clicks", "클릭", "int"),
        ("cost", "낭비 비용", "money"),
        ("conversions", "전환", "int"),
    ]
    wasted_html = _table_from_df(wasted_kw.head(30), wasted_cols)

    # 상품별 성과
    if not product_df.empty:
        prod_cols = [
            ("product_name", "상품명", "text") if "product_name" in product_df.columns
            else ("product_id_nv_mid", "NV_MID", "text"),
            ("impressions", "노출", "int"),
            ("clicks", "클릭", "int"),
            ("cost", "비용", "money"),
        ]
        if "conversions" in product_df.columns:
            prod_cols += [
                ("conversions", "전환", "int"),
                ("roas", "ROAS", "pct"),
            ]
        product_html = _table_from_df(product_df, prod_cols)
        product_section = f"""
        <section class="section">
          <h2>🛒 쇼핑검색광고 상품별 성과 (Top 20)</h2>
          {product_html}
        </section>
        """
    else:
        product_section = ""

    # 인사이트 리스트
    insights_html = "\n".join(
        f'<li class="insight-item">{escape(ins)}</li>' for ins in insights
    )

    # ───────── 최종 HTML ─────────
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>썬데이허그 네이버 광고 성과 리포트 · {date_from} ~ {date_to}</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<style>
  :root {{
    --primary: #FF6B6B;
    --primary-dark: #E55555;
    --accent: #A8E6CF;
    --accent-dark: #6FD5AA;
    --bg: #FAFAFA;
    --card-bg: #FFFFFF;
    --text: #2D3436;
    --text-sub: #6E7277;
    --border: #EAEAEA;
    --good: #27AE60;
    --warn: #F39C12;
    --bad: #E74C3C;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 0;
    font-family: 'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
  }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px 20px; }}
  header {{
    background: linear-gradient(135deg, var(--primary) 0%, #FF8E8E 100%);
    color: white;
    padding: 32px 20px;
    text-align: center;
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(255, 107, 107, 0.2);
  }}
  header h1 {{ margin: 0 0 8px 0; font-size: 24px; font-weight: 700; }}
  header .period {{ font-size: 15px; opacity: 0.95; }}
  header .sub {{ font-size: 13px; opacity: 0.85; margin-top: 8px; }}

  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 12px;
    margin-bottom: 28px;
  }}
  .metric-card {{
    background: var(--card-bg);
    border-radius: 12px;
    padding: 16px;
    border: 1px solid var(--border);
    transition: transform 0.15s, box-shadow 0.15s;
  }}
  .metric-card:hover {{ transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.06); }}
  .metric-card.card-good {{ border-left: 4px solid var(--good); }}
  .metric-card.card-warn {{ border-left: 4px solid var(--warn); }}
  .metric-card.card-bad {{ border-left: 4px solid var(--bad); }}
  .metric-label {{ font-size: 12px; color: var(--text-sub); margin-bottom: 6px; font-weight: 500; }}
  .metric-value {{ font-size: 22px; font-weight: 700; color: var(--text); }}
  .metric-sub {{ font-size: 12px; color: var(--text-sub); margin-top: 4px; }}

  .section {{
    background: var(--card-bg);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid var(--border);
  }}
  .section h2 {{
    margin: 0 0 16px 0;
    font-size: 18px;
    font-weight: 700;
    color: var(--text);
    padding-bottom: 10px;
    border-bottom: 2px solid var(--accent);
  }}

  .insights {{ list-style: none; padding: 0; margin: 0; }}
  .insight-item {{
    padding: 12px 16px;
    margin-bottom: 8px;
    background: #FFF9F9;
    border-left: 3px solid var(--primary);
    border-radius: 6px;
    font-size: 14px;
  }}

  .chart-container {{ position: relative; height: 320px; margin: 16px 0; }}

  .data-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }}
  .data-table thead {{ background: #F5F5F7; }}
  .data-table th {{
    padding: 10px 8px;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid var(--border);
  }}
  .data-table td {{
    padding: 10px 8px;
    border-bottom: 1px solid var(--border);
  }}
  .data-table td.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .data-table tbody tr:hover {{ background: #FAFAFA; }}

  .tabs {{ display: flex; gap: 8px; margin-bottom: 16px; border-bottom: 1px solid var(--border); }}
  .tab {{
    padding: 10px 16px;
    cursor: pointer;
    border: none;
    background: transparent;
    font-size: 14px;
    color: var(--text-sub);
    font-weight: 500;
    border-bottom: 2px solid transparent;
    transition: color 0.15s, border-color 0.15s;
    font-family: inherit;
  }}
  .tab.active {{ color: var(--primary); border-bottom-color: var(--primary); }}
  .tab-content {{ display: none; }}
  .tab-content.active {{ display: block; }}

  .empty {{ text-align: center; color: var(--text-sub); padding: 24px; }}

  footer {{
    text-align: center;
    font-size: 12px;
    color: var(--text-sub);
    padding: 20px;
    line-height: 1.8;
  }}
  footer .disclaimer {{ background: #FFF3CD; padding: 10px; border-radius: 6px; margin-bottom: 10px; color: #856404; }}

  @media (max-width: 640px) {{
    .metric-value {{ font-size: 18px; }}
    header h1 {{ font-size: 18px; }}
    .data-table {{ font-size: 12px; }}
    .data-table th, .data-table td {{ padding: 6px 4px; }}
  }}
</style>
</head>
<body>

<div class="container">

<header>
  <h1>📊 네이버 광고 성과 리포트</h1>
  <div class="period">{date_from} ~ {date_to} ({days_count}일간)</div>
  <div class="sub">생성: {now_str} · 썬데이허그 (JAYCORP)</div>
</header>

<section class="section">
  <h2>💡 핵심 인사이트</h2>
  <ul class="insights">
    {insights_html}
  </ul>
</section>

<div class="metrics-grid">
  {cards_html}
</div>

<section class="section">
  <h2>📈 일별 추이</h2>
  <div class="chart-container">
    <canvas id="trendChart"></canvas>
  </div>
</section>

<section class="section">
  <h2>🎯 캠페인별 성과</h2>
  {camp_table_html}
</section>

<section class="section">
  <h2>🔍 키워드 분석</h2>
  <div class="tabs">
    <button class="tab active" data-tab="top-cost">비용 Top 20</button>
    <button class="tab" data-tab="top-roas">ROAS Top 20</button>
    <button class="tab" data-tab="wasted">낭비 키워드</button>
  </div>
  <div class="tab-content active" id="tab-top-cost">{top_cost_html}</div>
  <div class="tab-content" id="tab-top-roas">{top_roas_html}</div>
  <div class="tab-content" id="tab-wasted">{wasted_html}</div>
</section>

{product_section}

<footer>
  <div class="disclaimer">
    ※ 전환 지표는 네이버 광고 시스템의 측정 기준이며, 스마트스토어/Cafe24 실제 매출과 다를 수 있습니다.
  </div>
  <div>naver-ads-reporter skill · JAYCORP 내부 운영용</div>
</footer>

</div>

<script>
  // 탭 전환
  document.querySelectorAll('.tab').forEach(btn => {{
    btn.addEventListener('click', () => {{
      const target = btn.dataset.tab;
      document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      document.getElementById('tab-' + target).classList.add('active');
    }});
  }});

  // 일별 추이 차트
  const chartData = {json.dumps(chart_data, ensure_ascii=False)};
  const ctx = document.getElementById('trendChart');
  if (ctx && chartData.labels.length) {{
    new Chart(ctx, {{
      type: 'line',
      data: {{
        labels: chartData.labels,
        datasets: [
          {{
            label: '비용(원)',
            data: chartData.cost,
            borderColor: '#FF6B6B',
            backgroundColor: 'rgba(255, 107, 107, 0.1)',
            yAxisID: 'y',
            tension: 0.3,
          }},
          {{
            label: '클릭',
            data: chartData.clicks,
            borderColor: '#6FD5AA',
            backgroundColor: 'rgba(168, 230, 207, 0.1)',
            yAxisID: 'y1',
            tension: 0.3,
          }},
          {{
            label: '전환',
            data: chartData.conversions,
            borderColor: '#4A90E2',
            backgroundColor: 'rgba(74, 144, 226, 0.1)',
            yAxisID: 'y1',
            tension: 0.3,
          }}
        ]
      }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        interaction: {{ mode: 'index', intersect: false }},
        scales: {{
          y: {{
            type: 'linear', position: 'left',
            title: {{ display: true, text: '비용(원)' }},
            ticks: {{ callback: v => v.toLocaleString() + '원' }}
          }},
          y1: {{
            type: 'linear', position: 'right',
            title: {{ display: true, text: '클릭/전환' }},
            grid: {{ drawOnChartArea: false }}
          }}
        }}
      }}
    }});
  }}
</script>

</body>
</html>
"""

    # 저장
    if output_path is None:
        out_dir = Path("/mnt/user-data/outputs")
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M")
        output_path = str(out_dir / f"naver_ads_report_{stamp}.html")

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"\n💾 리포트 저장: {output_path}")
    return output_path


# ───────── CLI 테스트 ─────────

def _cli():
    import argparse
    parser = argparse.ArgumentParser(description="TSV → HTML 리포트 렌더링 (디버깅용)")
    parser.add_argument("--ad-tsv", required=True)
    parser.add_argument("--shopping-tsv", default=None)
    parser.add_argument("--date-from", required=True)
    parser.add_argument("--date-to", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    df_ad = pd.read_csv(args.ad_tsv, sep="\t", dtype=str)
    df_shop = pd.read_csv(args.shopping_tsv, sep="\t", dtype=str) if args.shopping_tsv else None

    path = render_report(
        df_ad=df_ad,
        df_shopping=df_shop,
        date_from=args.date_from,
        date_to=args.date_to,
        output_path=args.output,
    )
    print(f"✅ {path}")


if __name__ == "__main__":
    _cli()
