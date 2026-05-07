#!/usr/bin/env python3
"""
render_pdp.py — 수집한 데이터로 SundayHug PDP HTML 생성

Usage:
    python3 render_pdp.py --input pdp_data.json --output ~/Desktop/team-skills/상세페이지/sundayhug/{slug}/

Input JSON 예시 (pdp_data.json):
{
  "slug": "abc-blanket",
  "product": {
    "name": "썬데이허그 ABC 아기 블랭킷",
    "category": "newborn",
    "color": "아이보리",
    "size": "ONE",
    "dimensions": "80 x 80 cm",
    "image_base": "https://sundayhugkr.cafe24.com/skin-skin69/pdp/newborn/abc-blanket/images"
  },
  "hero": {
    "headline_lines": ["부드러운 감촉이", "아기를 감싸는 시간"],
    "sub_lines": ["프리미엄 무염색 코튼 블랭킷", "썬데이허그 ABC 아기 블랭킷"],
    "img": "hero-01.webp"
  },
  "trust_bar": [
    {"label": "OEKO-TEX 인증", "sub": "안심 원단"},
    {"label": "사계절 사용", "sub": "통기성 우수"},
    {"label": "기계세탁 가능", "sub": "관리 편리"}
  ],
  "intro": {
    "label": "Designed For Comfort",
    "title": "\"아기 피부에 닿는 모든 것을, 더 신중하게 고르고 싶지 않으세요?\"",
    "body_html": "신생아의 피부는 어른보다 ...",
    "img": "intro-01.webp"
  },
  "why_blocks": [
    {"label_en": "Soft Touch", "title": "부드러운 감촉의 이유",
     "body_html": "<span class='hl'>4중 거즈 ...</span>", "bg": "cool"}
  ],
  "features": [
    {"num": "01", "title": "OEKO-TEX 인증", "img": "feature-01.webp",
     "body_html": "유해물질이 검출되지 않은 ..."}
  ],
  "faq": [
    {"q": "세탁기에 돌려도 되나요?", "a": "네, ..."}
  ],
  "specs": [
    {"label": "사이즈", "value": "80 x 80 cm"},
    {"label": "소재", "value": "코튼 100%"}
  ],
  "final_cta": {
    "headline_lines": ["우리 아기의 첫 블랭킷", "썬데이허그가 함께합니다"],
    "benefits": "OEKO-TEX 인증 / 4중 거즈 / 기계세탁 가능"
  }
}
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"


# ────────────────────────────────────────────────────────────────────────────
# 인라인 스타일 (제품별 스타일 마스터 위에 얹는 부분 — feat-hz, info-tbl 등)
# ────────────────────────────────────────────────────────────────────────────

INLINE_STYLE = """
<style>
  /* 제품별 인라인 스타일 — 마스터 styles.css에 없는 클래스만 정의 */
  .pdp-absolute .feat-hz { display: flex; gap: 20px; align-items: center; margin-top: 24px; }
  .pdp-absolute .feat-hz.rev { flex-direction: row-reverse; }
  .pdp-absolute .feat-hz-img { flex: 0 0 48%; border-radius: 6px; overflow: hidden; }
  .pdp-absolute .feat-hz-img img { width: 100%; display: block; }
  .pdp-absolute .feat-hz-body { flex: 1; }
  .pdp-absolute .feat-hz-body .feat-num { margin-bottom: 6px; }
  .pdp-absolute .feat-hz-body .feat-title { font-size: 22px; margin-bottom: 8px; }
  .pdp-absolute .feat-hz-body .feat-desc { font-size: 15px; line-height: 1.85; }
  .pdp-absolute .info-tbl { width: 100%; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
  .pdp-absolute .info-tbl th { width: 90px; font-weight: 600; color: var(--dark); padding: 11px 0; text-align: left; vertical-align: top; border-bottom: 1px solid var(--line); }
  .pdp-absolute .info-tbl td { color: var(--body); padding: 11px 0; border-bottom: 1px solid var(--line); line-height: 1.65; }
</style>
"""


# ────────────────────────────────────────────────────────────────────────────
# 섹션별 렌더러
# ────────────────────────────────────────────────────────────────────────────

def img_url(base: str, name: str) -> str:
    """이미지 베이스 URL + 파일명 → full URL. name이 이미 절대경로면 그대로."""
    if not name:
        return ""
    if name.startswith("http"):
        return name
    return f"{base.rstrip('/')}/{name.lstrip('/')}"


def render_hero(p: dict, hero: dict) -> str:
    base = p["product"].get("image_base", "")
    img = img_url(base, hero.get("img", ""))
    h1 = "<br>".join(hero.get("headline_lines", []))
    sub = "<br>".join(hero.get("sub_lines", []))
    return f"""
  <!-- HERO -->
  <div class="hero">
    <img class="hero-img" src="{img}" alt="{p['product'].get('name','')}">
    <div class="hero-text">
      <div class="hero-tag">SUNDAY HUG</div>
      <h1>{h1}</h1>
      <p class="hero-sub">{sub}</p>
    </div>
  </div>
"""


def render_trust_bar(items: list[dict]) -> str:
    if not items:
        return ""
    its = "\n    ".join(
        f'<div class="trust-bar-item">{it["label"]}<small>{it.get("sub","")}</small></div>'
        for it in items
    )
    return f"""
  <!-- TRUST BAR -->
  <div class="trust-bar">
    {its}
  </div>
"""


def render_intro(p: dict, intro: dict) -> str:
    if not intro:
        return ""
    base = p["product"].get("image_base", "")
    img = img_url(base, intro.get("img", ""))
    img_block = (
        f'<div class="fb-img"><img src="{img}" alt="{intro.get("title","")[:30]}"></div>'
        if img
        else ""
    )
    return f"""
  <!-- INTRO -->
  <div class="sec v">
    <div class="sec-label">{intro.get("label","")}</div>
    <div class="sec-title">{intro.get("title","")}</div>
    <div class="sec-desc">
      {intro.get("body_html","")}
    </div>
    {img_block}
  </div>

  <div class="thin-line"></div>
"""


def render_overview(p: dict, ov: dict) -> str:
    if not ov:
        return ""
    base = p["product"].get("image_base", "")
    img = img_url(base, ov.get("img", ""))
    img_block = f'<div class="fb-img"><img src="{img}" alt="overview"></div>' if img else ""
    return f"""
  <!-- OVERVIEW -->
  <div class="sec warm v">
    <div class="sec-label tx-center">Overview</div>
    <div class="sec-title tx-center">{ov.get("title","")}</div>
    <div class="sec-desc tx-center">
      {ov.get("body_html","")}
    </div>
    {img_block}
  </div>
"""


def render_brand_quote(quote: dict) -> str:
    if not quote:
        return ""
    text = "<br>".join(quote.get("lines", []))
    return f"""
  <!-- BRAND QUOTE -->
  <div class="bq">
    <p>"{text}"</p>
    <small>SUNDAY HUG</small>
  </div>
"""


def render_why(why: dict, idx: int) -> str:
    bg = why.get("bg", "cool")
    label_en = why.get("label_en", "")
    title = why.get("title", "")
    body = why.get("body_html", "")
    return f"""
  <!-- WHY {label_en.upper() or f"BLOCK_{idx}"} -->
  <div class="sec {bg} v">
    <div class="sec-label">Why {label_en}?</div>
    <div class="sec-title">{title}</div>
    <div class="sec-desc">
      {body}
    </div>
  </div>
"""


def render_feature(p: dict, feat: dict, idx: int) -> str:
    base = p["product"].get("image_base", "")
    img = img_url(base, feat.get("img", ""))
    rev = " rev" if idx % 2 == 0 else ""
    bg = " warm" if idx % 2 == 0 else ""
    num = feat.get("num", f"{idx:02d}")
    title = feat.get("title", "")
    return f"""
  <!-- FEAT {num} -- {title} -->
  <div class="feat{bg} v">
    <div class="feat-hz{rev}">
      <div class="feat-hz-img"><img src="{img}" alt="{title}"></div>
      <div class="feat-hz-body">
        <div class="feat-num">KEY FEATURE {num}</div>
        <div class="feat-title">{title}</div>
        <div class="feat-desc">
          {feat.get("body_html","")}
        </div>
      </div>
    </div>
  </div>
"""


def render_use_cases(uc: dict) -> str:
    if not uc:
        return ""
    cases = uc.get("cases", [])
    if not cases:
        return ""
    items = "\n      ".join(
        f"""<div class="step-item v">
        <div class="step-num">CASE {i+1:02d}</div>
        <div class="step-title">{c.get("title","")}</div>
        <div class="step-desc">{c.get("body_html","")}</div>
      </div>"""
        for i, c in enumerate(cases)
    )
    return f"""
  <!-- USE CASE -->
  <div class="sec v">
    <div class="sec-label">Use Case</div>
    <div class="sec-title">{uc.get("headline","")}</div>
    <div class="sec-desc">{uc.get("intro","")}</div>

    <div class="step-list">
      {items}
    </div>
  </div>
"""


def render_faq(faq: list[dict]) -> str:
    if not faq:
        return ""
    items = "\n      ".join(
        f"""<div class="faq-item">
        <div class="faq-q">Q{i+1}. {q.get("q","")}</div>
        <div class="faq-a">{q.get("a","")}</div>
      </div>"""
        for i, q in enumerate(faq)
    )
    return f"""
  <!-- FAQ -->
  <div class="sec warm v">
    <div class="sec-label">FAQ</div>
    <div class="sec-title">자주 묻는 질문</div>

    <div style="margin-top:24px;">
      {items}
    </div>
  </div>
"""


BRAND_STORY_BLOCK = """
  <!-- BRAND STORY -->
  <div class="sec warm v">
    <div class="sec-label tx-center">Our Story</div>
    <div class="sec-title tx-center">가족의 행복한 일상,<br>썬데이허그</div>
    <div class="sec-desc tx-center">
      우리는 가족 구성원 각자가<br>
      다양한 역할과 책임으로<br>
      분주한 일상을 보내고 있음을<br>
      잘 알고 있습니다.<br><br>
      이러한 일상 속에서도,<br>
      우리 브랜드를 통해<br>
      가족 모두가 함께<br>
      소중한 순간을 만들고<br>
      일상의 행복을<br>
      누릴 수 있기를 바랍니다.
    </div>
  </div>
"""


def render_final_cta(p: dict, cta: dict) -> str:
    if not cta:
        return ""
    h2 = "<br>".join(cta.get("headline_lines", []))
    benefits = cta.get("benefits", "")
    pr = p["product"]
    note_parts = [pr.get("color"), pr.get("size"), pr.get("dimensions")]
    note = " / ".join([x for x in note_parts if x])
    return f"""
  <!-- FINAL CTA -->
  <div class="final-cta v">
    <div class="final-cta-label">SUNDAY HUG</div>
    <h2>{h2}</h2>
    <p>{benefits}</p>
    <div class="final-cta-note">{note}</div>
  </div>
"""


def render_specs(specs: list[dict]) -> str:
    if not specs:
        return ""
    rows = "\n      ".join(
        f'<tr><th>{s["label"]}</th><td>{s["value"]}</td></tr>' for s in specs
    )
    return f"""
  <!-- SPECS -->
  <div class="sec v">
    <div class="sec-label">Specifications</div>
    <div class="sec-title">제품 사양</div>
    <table class="info-tbl">
      {rows}
    </table>
  </div>
"""


# ────────────────────────────────────────────────────────────────────────────
# 메인
# ────────────────────────────────────────────────────────────────────────────

def render(data: dict[str, Any], css_href: str = "./styles.css") -> str:
    parts: list[str] = [
        '<meta charset="UTF-8">',
        f'<link rel="stylesheet" href="{css_href}">',
        INLINE_STYLE,
        '<div class="pdp-absolute">',
        render_hero(data, data.get("hero", {})),
        render_trust_bar(data.get("trust_bar", [])),
        render_intro(data, data.get("intro", {})),
        render_overview(data, data.get("overview", {})),
    ]

    # 첫 BQ
    if data.get("brand_quote_top"):
        parts.append(render_brand_quote(data["brand_quote_top"]))

    # WHY 블록들
    for i, why in enumerate(data.get("why_blocks", []), 1):
        parts.append(render_why(why, i))

    # FEATURE 블록들
    for i, feat in enumerate(data.get("features", []), 1):
        parts.append(render_feature(data, feat, i))

    parts.append(render_use_cases(data.get("use_cases", {})))
    parts.append(render_faq(data.get("faq", [])))

    # 두 번째 BQ
    if data.get("brand_quote_bottom"):
        parts.append(render_brand_quote(data["brand_quote_bottom"]))

    parts.append(BRAND_STORY_BLOCK)
    parts.append(render_final_cta(data, data.get("final_cta", {})))
    parts.append(render_specs(data.get("specs", [])))

    parts.append("</div>")
    return "\n".join(p for p in parts if p)


def run(input_path: str, output_dir: str) -> None:
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    out = Path(output_dir).expanduser()
    out.mkdir(parents=True, exist_ok=True)

    # styles.css 동봉
    src_css = ASSETS_DIR / "styles.css"
    dst_css = out / "styles.css"
    if src_css.exists():
        shutil.copy2(src_css, dst_css)

    html = render(data, css_href="./styles.css")
    (out / "index.html").write_text(html, encoding="utf-8")

    # references.json도 같이 두면 트레이스에 도움
    if "references" in data:
        (out / "references.json").write_text(
            json.dumps({"references": data["references"]}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    print(f"[OK] PDP rendered → {out / 'index.html'}")


def main() -> None:
    ap = argparse.ArgumentParser(description="SundayHug PDP HTML 렌더러")
    ap.add_argument("--input", "-i", required=True, help="입력 JSON 경로")
    ap.add_argument("--output", "-o", required=True, help="출력 폴더")
    args = ap.parse_args()
    run(args.input, args.output)


if __name__ == "__main__":
    main()
