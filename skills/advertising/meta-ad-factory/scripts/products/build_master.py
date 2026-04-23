"""Build a master dashboard across all products.

Outputs:
- output/광고카피/sundayhug-meta-bulk/index.html        — product landing
- output/광고카피/sundayhug-meta-bulk/all_copies.csv     — merged CSV for Meta bulk upload
- output/광고카피/sundayhug-meta-bulk/build-summary.json — counts + stats
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path("/Users/inkyo/Projects/team-skills/output/광고카피/sundayhug-meta-bulk")


def find_products() -> list[tuple[str, str, Path]]:
    """Return list of (category, slug, product_dir)."""
    products = []
    for cat_dir in sorted(ROOT.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("."):
            continue
        if cat_dir.name in ("_master",):
            continue
        for pdir in sorted(cat_dir.iterdir()):
            if pdir.is_dir() and (pdir / "copy.csv").exists():
                products.append((cat_dir.name, pdir.name, pdir))
    return products


def merge_csvs(products: list[tuple[str, str, Path]]) -> Path:
    out_csv = ROOT / "all_copies.csv"
    with out_csv.open("w", encoding="utf-8", newline="") as fo:
        writer = None
        for cat, slug, pdir in products:
            with (pdir / "copy.csv").open("r", encoding="utf-8") as fi:
                reader = csv.DictReader(fi)
                if writer is None:
                    writer = csv.DictWriter(
                        fo,
                        fieldnames=["category", "product", *reader.fieldnames],
                    )
                    writer.writeheader()
                for row in reader:
                    writer.writerow({"category": cat, "product": slug, **row})
    return out_csv


def build_summary(products: list[tuple[str, str, Path]]) -> dict:
    summary = {
        "total_products": len(products),
        "total_creatives": 0,
        "by_category": {},
        "products": [],
    }
    for cat, slug, pdir in products:
        meta_file = pdir / "build-meta.json"
        if not meta_file.exists():
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        count = meta.get("total", 0)
        summary["total_creatives"] += count
        summary["by_category"].setdefault(cat, {"products": 0, "creatives": 0})
        summary["by_category"][cat]["products"] += 1
        summary["by_category"][cat]["creatives"] += count
        summary["products"].append({
            "category": cat,
            "slug": slug,
            "product": meta.get("product", slug),
            "creatives": count,
            "preview": f"./{cat}/{slug}/previews/preview-grid.html",
        })
    return summary


def build_index_html(summary: dict) -> Path:
    products_html = ""
    by_cat: dict[str, list[dict]] = {}
    for p in summary["products"]:
        by_cat.setdefault(p["category"], []).append(p)

    cat_labels = {
        "newborn": "👶 Newborn — 신생아용품",
        "sleeping-bags": "🌙 Sleeping Bags — 슬립색",
        "sleep-products": "💤 Sleep Products — 수면용품",
        "daily-look": "👚 Daily Look — 데일리 의류",
    }

    for cat_key in ["newborn", "sleeping-bags", "sleep-products", "daily-look"]:
        if cat_key not in by_cat:
            continue
        items = by_cat[cat_key]
        cards_html = "\n".join(
            f"""
        <a class="card" href="{p['preview']}">
          <div class="card-name">{p['product']}</div>
          <div class="card-meta">{p['slug']} · <b>{p['creatives']}</b>개 크리에이티브</div>
        </a>"""
            for p in items
        )
        products_html += f"""
    <section class="cat-section">
      <h2 class="cat-title">{cat_labels.get(cat_key, cat_key)}</h2>
      <div class="cat-meta">{len(items)}개 제품 · {sum(p['creatives'] for p in items)}개 크리에이티브</div>
      <div class="cards">
        {cards_html}
      </div>
    </section>
    """

    cat_stats = "".join(
        f"<div class='stat'><div class='stat-num'>{v['products']}</div><div class='stat-lbl'>{cat_labels.get(k, k).split('—')[0].strip()}</div><div class='stat-sub'>{v['creatives']}개 소재</div></div>"
        for k, v in summary["by_category"].items()
    )

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>SUNDAY HUG — Meta Ad Factory Dashboard</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Noto Sans KR',sans-serif;background:#f5f0eb;color:#1a1a1a;min-height:100vh;padding:40px 32px;}}
.container{{max-width:1200px;margin:0 auto;}}
.hero{{background:#1D9E75;color:#fff;padding:40px 48px;border-radius:20px;margin-bottom:32px;box-shadow:0 10px 40px rgba(29,158,117,0.2);}}
.hero h1{{font-size:32px;font-weight:900;margin-bottom:8px;}}
.hero .subtitle{{font-size:15px;opacity:0.92;}}
.top-stats{{display:flex;gap:16px;margin-top:24px;flex-wrap:wrap;}}
.top-stats .stat{{background:rgba(255,255,255,0.15);padding:16px 20px;border-radius:12px;flex:1;min-width:140px;}}
.top-stats .stat-num{{font-size:28px;font-weight:900;}}
.top-stats .stat-lbl{{font-size:12px;opacity:0.85;margin-top:2px;letter-spacing:1px;}}
.top-stats .stat-sub{{font-size:11px;opacity:0.65;margin-top:4px;}}
.cat-section{{background:#fff;border-radius:16px;padding:32px;margin-bottom:20px;box-shadow:0 1px 3px rgba(0,0,0,0.04);}}
.cat-title{{font-size:22px;font-weight:900;margin-bottom:4px;}}
.cat-meta{{font-size:13px;color:#888;margin-bottom:20px;}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;}}
.card{{display:block;background:#f5f0eb;padding:20px;border-radius:12px;text-decoration:none;color:inherit;transition:all 0.15s;border:2px solid transparent;}}
.card:hover{{background:#fff;border-color:#1D9E75;transform:translateY(-2px);box-shadow:0 4px 16px rgba(29,158,117,0.15);}}
.card-name{{font-size:16px;font-weight:700;margin-bottom:6px;}}
.card-meta{{font-size:12px;color:#666;}}
.card-meta b{{color:#1D9E75;font-weight:700;}}
footer{{text-align:center;font-size:12px;color:#999;margin-top:32px;}}
.csv-link{{display:inline-block;margin-top:16px;background:#FF6B35;color:#fff;padding:12px 24px;border-radius:8px;font-weight:700;text-decoration:none;font-size:13px;}}
.csv-link:hover{{background:#e55a2b;}}
</style>
</head>
<body>
<div class="container">
  <div class="hero">
    <h1>SUNDAY HUG — Meta Ad Factory</h1>
    <div class="subtitle">{summary['total_products']}개 제품 · {summary['total_creatives']}개 크리에이티브 · 사이즈 3종(1:1/4:5/9:16) × 톤 3종(감성/정보형/긴급성) × 레이아웃 4종</div>
    <div class="top-stats">
      {cat_stats}
    </div>
    <a class="csv-link" href="./all_copies.csv" download>📊 통합 카피 CSV 다운로드 (Meta 벌크 업로드용)</a>
  </div>
  {products_html}
  <footer>© SUNDAY HUG · meta-ad-factory · Generated locally</footer>
</div>
</body>
</html>"""

    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    return out


def main() -> None:
    products = find_products()
    print(f"Found {len(products)} products:")
    for cat, slug, _ in products:
        print(f"  · {cat}/{slug}")

    csv_path = merge_csvs(products)
    print(f"\n✓ Merged CSV: {csv_path}")

    summary = build_summary(products)
    summary_path = ROOT / "build-summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ Summary: {summary_path}")

    index_path = build_index_html(summary)
    print(f"✓ Master index: {index_path}")

    print(f"\n🎉 Total: {summary['total_products']} products, {summary['total_creatives']} creatives")


if __name__ == "__main__":
    main()
