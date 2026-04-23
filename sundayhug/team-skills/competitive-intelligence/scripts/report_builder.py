#!/usr/bin/env python3
"""
경쟁사 분석 인터랙티브 HTML 리포트 생성기
Usage:
  python3 report_builder.py --data analysis.json --brand "브랜드명" --output report.html
"""

import argparse
import json
import sys
from datetime import datetime


def generate_html(data, brand_name):
    """JSON 분석 데이터를 인터랙티브 HTML 리포트로 변환"""

    profile = data.get("profile", {})
    products = data.get("products", [])
    product_analysis = data.get("product_analysis", {})
    promotions = data.get("promotions", [])
    marketing = data.get("marketing", {})
    sentiment = data.get("sentiment", {})
    reviews = data.get("reviews", [])
    comparison = data.get("comparison", {})
    insights = data.get("insights", {})

    # 가격 분포 데이터
    price_dist = product_analysis.get("price_distribution", {})
    price_labels = json.dumps(list(price_dist.keys()), ensure_ascii=False)
    price_values = json.dumps(list(price_dist.values()))

    # 감성 분석 데이터
    pos_ratio = sentiment.get("positive", {}).get("ratio", 0)
    neg_ratio = sentiment.get("negative", {}).get("ratio", 0)
    neu_ratio = sentiment.get("neutral", {}).get("ratio", 0)

    # 긍정/부정 키워드
    pos_kw = sentiment.get("top_positive_keywords", [])
    neg_kw = sentiment.get("top_negative_keywords", [])
    pos_kw_labels = json.dumps([k[0] for k in pos_kw], ensure_ascii=False)
    pos_kw_values = json.dumps([k[1] for k in pos_kw])
    neg_kw_labels = json.dumps([k[0] for k in neg_kw], ensure_ascii=False)
    neg_kw_values = json.dumps([k[1] for k in neg_kw])

    today = datetime.now().strftime("%Y-%m-%d")

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{brand_name} 경쟁사 분석 리포트 — {today}</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
:root {{
  --bg: #FFFFFF;
  --text: #1A202C;
  --text-sec: #718096;
  --border: #E2E8F0;
  --card-bg: #F7FAFC;
  --sundayhug: #1D9E75;
  --sundayhug-lt: #E1F5EE;
  --competitor: #4299E1;
  --competitor-lt: #EBF8FF;
  --positive: #38A169;
  --negative: #E53E3E;
  --neutral: #A0AEC0;
  --warning: #EF9F27;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif; color:var(--text); background:var(--bg); }}
.header {{ background:linear-gradient(135deg,var(--competitor),#2B6CB0); color:#fff; padding:32px 24px; }}
.header h1 {{ font-size:24px; margin-bottom:4px; }}
.header p {{ opacity:0.85; font-size:14px; }}
.tabs {{ display:flex; overflow-x:auto; background:#f8f9fa; border-bottom:2px solid var(--border); padding:0 16px; gap:4px; }}
.tab {{ padding:12px 16px; cursor:pointer; border:none; background:none; font-size:13px; white-space:nowrap; border-bottom:3px solid transparent; color:var(--text-sec); transition:all 0.2s; }}
.tab:hover {{ color:var(--text); }}
.tab.active {{ color:var(--competitor); border-bottom-color:var(--competitor); font-weight:600; }}
.panel {{ display:none; padding:24px; max-width:1200px; margin:0 auto; }}
.panel.active {{ display:block; }}
.cards {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:16px; margin:20px 0; }}
.card {{ background:var(--card-bg); border:1px solid var(--border); border-radius:12px; padding:20px; }}
.card .label {{ font-size:12px; color:var(--text-sec); margin-bottom:4px; }}
.card .value {{ font-size:28px; font-weight:700; }}
.card .sub {{ font-size:12px; color:var(--text-sec); margin-top:4px; }}
h2 {{ font-size:20px; margin:24px 0 12px; }}
h3 {{ font-size:16px; margin:16px 0 8px; color:var(--text-sec); }}
table {{ width:100%; border-collapse:collapse; margin:12px 0; font-size:13px; }}
th {{ background:var(--card-bg); padding:10px 12px; text-align:left; border-bottom:2px solid var(--border); font-weight:600; }}
td {{ padding:10px 12px; border-bottom:1px solid var(--border); }}
tr:hover {{ background:#f8f9fa; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:20px; font-size:11px; font-weight:600; }}
.badge-pos {{ background:#C6F6D5; color:#22543D; }}
.badge-neg {{ background:#FED7D7; color:#742A2A; }}
.badge-neu {{ background:#E2E8F0; color:#4A5568; }}
.badge-urgent {{ background:#FED7D7; color:#742A2A; }}
.badge-recommend {{ background:#FEFCBF; color:#744210; }}
.badge-review {{ background:#C6F6D5; color:#22543D; }}
.chart-container {{ max-width:600px; margin:16px 0; }}
.insight-card {{ background:var(--card-bg); border-left:4px solid var(--competitor); border-radius:0 8px 8px 0; padding:16px; margin:8px 0; }}
.insight-card.opportunity {{ border-left-color:var(--sundayhug); }}
.insight-card.urgent {{ border-left-color:var(--negative); }}
.compare-row {{ display:grid; grid-template-columns:1fr auto 1fr; gap:12px; align-items:center; padding:12px 0; border-bottom:1px solid var(--border); }}
.compare-label {{ text-align:center; font-weight:600; font-size:13px; color:var(--text-sec); }}
.vs {{ font-size:12px; color:var(--text-sec); padding:4px 8px; background:var(--card-bg); border-radius:20px; }}
.channel-btn {{ display:inline-block; padding:6px 14px; background:var(--competitor-lt); color:var(--competitor); border-radius:6px; text-decoration:none; font-size:12px; margin:4px; }}
.channel-btn:hover {{ background:var(--competitor); color:#fff; }}
.review-card {{ background:var(--card-bg); border-radius:8px; padding:14px; margin:8px 0; }}
.review-card .stars {{ color:#ECC94B; }}
@media(max-width:768px) {{
  .cards {{ grid-template-columns:1fr 1fr; }}
  .compare-row {{ grid-template-columns:1fr; text-align:center; }}
}}
</style>
</head>
<body>
<div class="header">
  <h1>⚔️ {brand_name} 경쟁사 분석</h1>
  <p>분석일: {today} | 비교 기준: 썬데이허그</p>
</div>

<div class="tabs">
  <button class="tab active" onclick="showTab(0)">📊 프로필</button>
  <button class="tab" onclick="showTab(1)">🛒 제품&가격</button>
  <button class="tab" onclick="showTab(2)">🏷️ 프로모션</button>
  <button class="tab" onclick="showTab(3)">📱 마케팅</button>
  <button class="tab" onclick="showTab(4)">⭐ 리뷰&VOC</button>
  <button class="tab" onclick="showTab(5)">⚔️ vs 썬데이허그</button>
  <button class="tab" onclick="showTab(6)">💡 인사이트</button>
</div>

<!-- TAB 0: Profile -->
<div class="panel active" id="panel-0">
  <h2>브랜드 프로필</h2>
  <p id="profile-summary" style="color:var(--text-sec);margin-bottom:16px;">{profile.get('summary', '데이터 수집 후 자동 생성됩니다.')}</p>
  <div id="channel-links">
    <!-- 채널 링크 동적 생성 -->
  </div>
  <div class="cards" id="profile-cards">
    <div class="card">
      <div class="label">총 상품 수</div>
      <div class="value">{product_analysis.get('total_products', '-')}</div>
    </div>
    <div class="card">
      <div class="label">평균 가격</div>
      <div class="value">₩{product_analysis.get('price_stats', {}).get('avg', 0):,}</div>
    </div>
    <div class="card">
      <div class="label">총 리뷰 수</div>
      <div class="value">{product_analysis.get('review_stats', {}).get('total_reviews', '-'):,}</div>
    </div>
    <div class="card">
      <div class="label">무료배송 비율</div>
      <div class="value">{product_analysis.get('free_shipping_ratio', '-')}%</div>
    </div>
  </div>
</div>

<!-- TAB 1: Products -->
<div class="panel" id="panel-1">
  <h2>제품 라인업 & 가격</h2>
  <div class="cards">
    <div class="card">
      <div class="label">최저가</div>
      <div class="value">₩{product_analysis.get('price_stats', {}).get('min', 0):,}</div>
    </div>
    <div class="card">
      <div class="label">최고가</div>
      <div class="value">₩{product_analysis.get('price_stats', {}).get('max', 0):,}</div>
    </div>
    <div class="card">
      <div class="label">평균가</div>
      <div class="value">₩{product_analysis.get('price_stats', {}).get('avg', 0):,}</div>
    </div>
    <div class="card">
      <div class="label">중앙가</div>
      <div class="value">₩{product_analysis.get('price_stats', {}).get('median', 0):,}</div>
    </div>
  </div>
  <h3>가격 분포</h3>
  <div class="chart-container"><canvas id="priceChart"></canvas></div>
  <h3>베스트셀러 TOP 10</h3>
  <table>
    <tr><th>#</th><th>상품명</th><th>가격</th><th>리뷰수</th></tr>
    {"".join(f'<tr><td>{i+1}</td><td>{p.get("name","")[:40]}</td><td>₩{p.get("price",0):,}</td><td>{p.get("review_count",0):,}</td></tr>' for i, p in enumerate(product_analysis.get("best_sellers", [])[:10]))}
  </table>
</div>

<!-- TAB 2: Promotions -->
<div class="panel" id="panel-2">
  <h2>프로모션 & 행사</h2>
  {"".join(f'<div class="insight-card"><strong>{p.get("type","")}</strong> — {p.get("description","")}</div>' for p in promotions) if promotions else '<p style="color:var(--text-sec)">수집된 프로모션 데이터가 여기에 표시됩니다.</p>'}
</div>

<!-- TAB 3: Marketing -->
<div class="panel" id="panel-3">
  <h2>마케팅 채널 분석</h2>
  <div id="marketing-content">
    <p style="color:var(--text-sec)">인스타그램, 블로그, 검색 마케팅 분석 결과가 여기에 표시됩니다.</p>
  </div>
</div>

<!-- TAB 4: Reviews -->
<div class="panel" id="panel-4">
  <h2>리뷰 & VOC 분석</h2>
  <h3>감성 분포</h3>
  <div class="chart-container"><canvas id="sentimentChart"></canvas></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
    <div>
      <h3>👍 장점 키워드</h3>
      <div class="chart-container"><canvas id="posChart"></canvas></div>
    </div>
    <div>
      <h3>👎 불만 키워드</h3>
      <div class="chart-container"><canvas id="negChart"></canvas></div>
    </div>
  </div>
  <h3>대표 리뷰 발췌</h3>
  {"".join(f'<div class="review-card"><strong>{r.get("title","")}</strong><br><span style="color:var(--text-sec);font-size:13px;">{r.get("summary","")[:200]}</span></div>' for r in reviews[:6]) if reviews else '<p style="color:var(--text-sec)">리뷰 데이터가 여기에 표시됩니다.</p>'}
</div>

<!-- TAB 5: Comparison -->
<div class="panel" id="panel-5">
  <h2>⚔️ {brand_name} vs 썬데이허그</h2>
  <table>
    <tr><th>항목</th><th style="color:var(--competitor)">{brand_name}</th><th style="color:var(--sundayhug)">썬데이허그</th><th>판정</th></tr>
    {"".join(f'<tr><td>{c.get("item","")}</td><td>{c.get("competitor","")}</td><td>{c.get("sundayhug","")}</td><td>{c.get("verdict","")}</td></tr>' for c in comparison.get("items", [])) if comparison.get("items") else '<tr><td colspan="4" style="color:var(--text-sec);text-align:center">비교 데이터가 여기에 표시됩니다.</td></tr>'}
  </table>
</div>

<!-- TAB 6: Insights -->
<div class="panel" id="panel-6">
  <h2>💡 인사이트 & 액션</h2>
  <h3>📚 배울 점</h3>
  {"".join(f'<div class="insight-card">{item}</div>' for item in insights.get("learn", [])) if insights.get("learn") else '<div class="insight-card">분석 후 자동 생성됩니다.</div>'}
  <h3>🎯 우리의 기회</h3>
  {"".join(f'<div class="insight-card opportunity">{item}</div>' for item in insights.get("opportunity", [])) if insights.get("opportunity") else '<div class="insight-card opportunity">분석 후 자동 생성됩니다.</div>'}
  <h3>🚨 즉시 대응</h3>
  {"".join(f'<div class="insight-card urgent">{item}</div>' for item in insights.get("urgent", [])) if insights.get("urgent") else '<div class="insight-card urgent">해당 없음</div>'}
</div>

<script>
// Tab switching
function showTab(idx) {{
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', i===idx));
  document.querySelectorAll('.panel').forEach((p,i) => p.classList.toggle('active', i===idx));
}}

// Price distribution chart
new Chart(document.getElementById('priceChart'), {{
  type: 'bar',
  data: {{
    labels: {price_labels},
    datasets: [{{ label: '상품 수', data: {price_values}, backgroundColor: '#4299E1' }}]
  }},
  options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }} }}
}});

// Sentiment chart
new Chart(document.getElementById('sentimentChart'), {{
  type: 'doughnut',
  data: {{
    labels: ['긍정', '부정', '중립'],
    datasets: [{{ data: [{pos_ratio}, {neg_ratio}, {neu_ratio}], backgroundColor: ['#38A169', '#E53E3E', '#A0AEC0'] }}]
  }},
  options: {{ responsive: true }}
}});

// Positive keywords
if ({pos_kw_labels}.length > 0) {{
  new Chart(document.getElementById('posChart'), {{
    type: 'bar',
    data: {{
      labels: {pos_kw_labels},
      datasets: [{{ data: {pos_kw_values}, backgroundColor: '#38A169' }}]
    }},
    options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }} }} }}
  }});
}}

// Negative keywords
if ({neg_kw_labels}.length > 0) {{
  new Chart(document.getElementById('negChart'), {{
    type: 'bar',
    data: {{
      labels: {neg_kw_labels},
      datasets: [{{ data: {neg_kw_values}, backgroundColor: '#E53E3E' }}]
    }},
    options: {{ indexAxis: 'y', responsive: true, plugins: {{ legend: {{ display: false }} }} }}
  }});
}}
</script>
</body>
</html>"""
    return html


def main():
    parser = argparse.ArgumentParser(description="경쟁사 분석 HTML 리포트 생성")
    parser.add_argument("--data", required=True, help="분석 데이터 JSON 파일 경로")
    parser.add_argument("--brand", required=True, help="경쟁사 브랜드명")
    parser.add_argument("--output", required=True, help="HTML 출력 경로")
    args = parser.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = generate_html(data, args.brand)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[INFO] 리포트 생성 완료: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
