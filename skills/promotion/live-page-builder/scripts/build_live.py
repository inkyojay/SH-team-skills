"""Live page builder — spec dict → 섹션별 HTML + preview-grid.

Usage (CLI):
    # JSON spec 파일로 빌드
    python3 build_live.py --spec /tmp/silky-bamboo.json

    # 빠르게 dry-run (활성 섹션 + 슬롯 충족 여부만 점검)
    python3 build_live.py --spec /tmp/silky-bamboo.json --dry-run

Programmatic:
    from build_live import build, LiveSpec
    out = build(LiveSpec.from_dict(spec_dict))
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import chevron

# 같은 폴더의 section_catalog import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from section_catalog import (  # noqa: E402
    SECTIONS_DIR, TEMPLATES_DIR, PALETTE_LIST, MONTH_TO_PALETTE,
    PREMIUM_PRESET, SECTION_DEFAULTS,
    load_catalog, get_defaults, get_preset,
)


# 출력 베이스 경로
OUTPUT_BASE = Path.home() / "Desktop" / "output" / "상세페이지" / "라이브"


# ── Spec 모델 ────────────────────────────────────────────────────────────────
@dataclass
class LiveSpec:
    """라이브 페이지 빌드 명세 — 인터뷰 답변을 구조화한 형태."""
    campaign_slug: str
    product_name: str
    palette: str = "golden-hour"
    active_sections: list[str] = field(default_factory=lambda: list(PREMIUM_PRESET))
    copy: dict[str, Any] = field(default_factory=dict)
    pdp_path: str = ""
    image_dir: str = ""

    @classmethod
    def from_dict(cls, d: dict) -> "LiveSpec":
        return cls(
            campaign_slug=d["campaign_slug"],
            product_name=d.get("product_name", ""),
            palette=d.get("palette", "golden-hour"),
            active_sections=list(d.get("active_sections") or PREMIUM_PRESET),
            copy=dict(d.get("copy") or {}),
            pdp_path=d.get("pdp_path", ""),
            image_dir=d.get("image_dir", ""),
        )

    def to_dict(self) -> dict:
        return {
            "campaign_slug": self.campaign_slug,
            "product_name": self.product_name,
            "palette": self.palette,
            "active_sections": list(self.active_sections),
            "copy": dict(self.copy),
            "pdp_path": self.pdp_path,
            "image_dir": self.image_dir,
        }


# ── 템플릿 전처리 ──────────────────────────────────────────────────────────
_COND_RE = re.compile(r"\{\{\?([a-zA-Z_][a-zA-Z0-9_]*)\}\}")
_HEADER_COMMENT_RE = re.compile(r"<!--=+\n.*?\n=+-->\n?", re.DOTALL)
# `_html` 또는 `_html_*`로 끝나는 변수는 HTML escape 안 함 → triple-brace로 변환
# (예: live_title_html, answer_html, host_quote_html, brand_story_desc_html, ...)
_HTML_VAR_RE = re.compile(r"\{\{(\s*([a-zA-Z_][a-zA-Z0-9_]*_html)\s*)\}\}")


def _preprocess_template(tpl: str) -> str:
    """렌더 전 템플릿 정리:
      1. 헤더 문서 코멘트(`<!--==...==-->`)는 chevron이 안에 있는 `{{#...}}`도 토큰으로
         인식해서 매칭 실패 → 통째로 제거.
      2. `{{?cond}}` 비표준 문법을 chevron 표준 `{{#cond}}`로 변환
         (07-bundle-deals, 12-quick-showcase에서 사용).
      3. `{{var_html}}` 형식 슬롯은 HTML escape 안 하도록 `{{{var_html}}}` 로 변환
         (live_title_html, answer_html 등 — 사용자가 <br> 등 raw HTML 넣을 수 있게).
    """
    tpl = _HEADER_COMMENT_RE.sub("", tpl)
    tpl = _COND_RE.sub(r"{{#\1}}", tpl)
    tpl = _HTML_VAR_RE.sub(r"{{{\2}}}", tpl)
    return tpl


# ── 섹션 1개 렌더 ────────────────────────────────────────────────────────────
def _render_section(section_id: str, copy: dict[str, Any], catalog) -> tuple[str, list[str]]:
    """특정 섹션을 렌더링해서 (HTML, 경고 리스트) 반환."""
    if section_id not in catalog:
        return "", [f"❌ 카탈로그에 없는 섹션: {section_id}"]

    meta = catalog[section_id]
    template_text = meta.template_path.read_text(encoding="utf-8")
    template_text = _preprocess_template(template_text)

    # 컨텍스트 = 브랜드 default → 사용자 copy 순으로 머지
    ctx = {**get_defaults(section_id), **copy}

    warnings: list[str] = []

    # 배열 슬롯 비어있으면 섹션 제외 신호
    for arr_key in meta.array_slots:
        val = ctx.get(arr_key)
        if not val:
            warnings.append(f"⚠️  {section_id}: 배열 슬롯 '{arr_key}' 비어있음 — 섹션 자동 제외")
            return "", warnings

    # 단일 슬롯 빈 곳 검사 (필수 섹션의 핵심 슬롯이 비면 경고만, 빌드는 진행)
    important_singles = {
        "01-live-hero":   ["live_title_html", "host_image"],
        "03-schedule":    ["schedule_date", "schedule_time"],
        "06-coupon":      ["coupon_amount"],
        "10-mid-cta":     ["mid_cta_title"],
        "25-final-cta":   ["final_cta_title_html"],
    }
    for k in important_singles.get(section_id, []):
        if not ctx.get(k):
            warnings.append(f"⚠️  {section_id}: 핵심 슬롯 '{k}' 비어있음 (default도 없음)")

    rendered = chevron.render(template_text, ctx)
    return rendered, warnings


# ── 섹션 HTML을 standalone 페이지로 래핑 ─────────────────────────────────────
_PAGE_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Noto+Sans+KR:wght@300;400;500;700&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css_base}">
<link rel="stylesheet" href="{css_palettes}">
<style>
  body {{ margin:0; padding:0; background:#fff; }}
  .lp-page {{ width:600px; margin:0 auto; }}
</style>
</head>
<body data-palette="{palette}">
<div class="lp-page">
{body}
</div>
</body>
</html>
"""


def _wrap_section_page(section_html: str, *, title: str, palette: str) -> str:
    """렌더된 섹션 HTML을 600px 폭 standalone 페이지로 감싼다."""
    base_uri = TEMPLATES_DIR.resolve().as_uri()
    return _PAGE_TEMPLATE.format(
        title=title,
        css_base=f"{base_uri}/_base-styles.css",
        css_palettes=f"{base_uri}/_palettes.css",
        palette=palette,
        body=section_html,
    )


# ── preview-grid.html 빌드 ─────────────────────────────────────────────────
_GRID_TEMPLATE = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><title>{campaign} — Live Page Preview</title>
<style>
  * {{ box-sizing:border-box; }}
  body {{ font-family:-apple-system, "Apple SD Gothic Neo", system-ui; margin:0; padding:24px; background:#f5f5f7; }}
  h1 {{ font-size:22px; margin:0 0 4px; }}
  .sub {{ color:#86868b; font-size:13px; margin-bottom:8px; }}
  .helpbar {{ background:#fff; padding:12px 16px; border-radius:8px; margin-bottom:24px; font-size:12px; color:#424245; line-height:1.6; }}
  .helpbar code {{ background:#f0f0f2; padding:1px 6px; border-radius:3px; font-size:11px; }}
  .grid {{ display:grid; gap:24px; grid-template-columns:repeat(auto-fill, minmax(640px, 1fr)); }}
  .card {{ background:#fff; border-radius:12px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,.06); }}
  .card-head {{ padding:12px 16px; border-bottom:1px solid #e5e5e7; display:flex; justify-content:space-between; align-items:center; }}
  .card-head .name {{ font-size:14px; font-weight:600; }}
  .card-head .id {{ font-size:11px; color:#86868b; }}
  .card iframe {{ width:100%; height:600px; border:0; display:block; background:#fff; }}
  .actions {{ padding:8px 12px; display:flex; gap:6px; justify-content:flex-end; border-top:1px solid #e5e5e7; flex-wrap:wrap; }}
  .actions a {{ padding:6px 12px; border:0; border-radius:6px; font-size:12px; cursor:pointer; text-decoration:none; }}
  .btn-primary {{ background:#1d9e75; color:#fff; }}
  .btn-secondary {{ background:#f0f0f2; color:#424245; }}
  .btn-warning {{ background:#fff3cd; color:#856404; }}
  .palette-tag {{ display:inline-block; padding:2px 8px; border-radius:4px; background:#1d9e75; color:#fff; font-size:11px; margin-left:8px; }}
  .warn {{ color:#dc3545; font-size:11px; margin-top:4px; }}
</style></head><body>
<h1>{campaign} <span class="palette-tag">{palette}</span></h1>
<div class="sub">{n} 섹션 · 제품: {product}</div>
<div class="helpbar">
  <strong>사용법:</strong>
  ① 미리보기 확인 → ② 텍스트 수정 필요 시 <code>previews/*.html</code> 직접 편집 →
  ③ <code>export_png.py --campaign {campaign}</code> 실행해서 PNG 갱신 → ④ "PNG 다운로드" 클릭.
</div>
<div class="grid">{cards}</div>
</body></html>
"""

_CARD_TEMPLATE = """<div class="card" id="{section_id}">
  <div class="card-head"><span class="name">{name}</span><span class="id">{section_id}</span></div>
  <iframe src="./{filename}" loading="lazy"></iframe>
  <div class="actions">
    <a href="../final/{png_filename}" download class="btn-primary">PNG 다운로드</a>
    <a href="./{filename}" target="_blank" class="btn-secondary">HTML 새 창</a>
  </div>
</div>"""


# ── 메인 빌드 함수 ───────────────────────────────────────────────────────────
def build(spec: LiveSpec, *, log: bool = True, dry_run: bool = False) -> dict:
    """spec → 섹션별 HTML + preview-grid → manifest dict 반환."""
    catalog = load_catalog()

    if spec.palette not in PALETTE_LIST:
        raise ValueError(f"Unknown palette '{spec.palette}'. Valid: {PALETTE_LIST}")

    out_root = OUTPUT_BASE / spec.campaign_slug
    previews_dir = out_root / "previews"
    if not dry_run:
        previews_dir.mkdir(parents=True, exist_ok=True)
        # spec 저장 (재실행/재편집용)
        (out_root / "spec.json").write_text(
            json.dumps(spec.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")

    manifest = {
        "campaign_slug": spec.campaign_slug,
        "product_name": spec.product_name,
        "palette": spec.palette,
        "sections": [],
    }

    cards_html: list[str] = []
    all_warnings: list[str] = []

    if log:
        print(f"▶ Live page build: {spec.campaign_slug}")
        print(f"  Palette: {spec.palette} | Active sections: {len(spec.active_sections)}")

    for sec_id in spec.active_sections:
        if sec_id not in catalog:
            all_warnings.append(f"❌ 카탈로그에 없음: {sec_id}")
            if log:
                print(f"  ✗ {sec_id} — 카탈로그에 없음")
            continue

        meta = catalog[sec_id]
        body, warns = _render_section(sec_id, spec.copy, catalog)
        all_warnings.extend(warns)

        if not body:
            # 배열 비어있어서 자동 제외된 케이스
            if log:
                print(f"  ⊘ {sec_id} — {warns[0] if warns else '제외'}")
            continue

        page = _wrap_section_page(body, title=f"{spec.campaign_slug} - {meta.name}", palette=spec.palette)
        filename = f"{sec_id}_600w_{spec.palette}.html"
        out_path = previews_dir / filename

        if not dry_run:
            out_path.write_text(page, encoding="utf-8")

        png_filename = filename.replace(".html", ".png")
        cards_html.append(_CARD_TEMPLATE.format(
            section_id=sec_id, name=meta.name, filename=filename, png_filename=png_filename))
        manifest["sections"].append({
            "id": sec_id, "name": meta.name, "file": filename,
            "warnings": warns,
        })
        if log:
            warn_tag = f"  ({len(warns)} warnings)" if warns else ""
            print(f"  ✓ {sec_id} → {filename}{warn_tag}")

    # preview-grid 작성
    if not dry_run and cards_html:
        grid_html = _GRID_TEMPLATE.format(
            campaign=spec.campaign_slug,
            palette=spec.palette,
            n=len(manifest["sections"]),
            product=spec.product_name or "—",
            cards="\n".join(cards_html),
        )
        (previews_dir / "preview-grid.html").write_text(grid_html, encoding="utf-8")

    if log:
        ok = len(manifest["sections"])
        skipped = len(spec.active_sections) - ok
        print(f"\n🎉 Done: {ok}/{len(spec.active_sections)} 섹션 빌드 완료 ({skipped} skipped)")
        if not dry_run:
            print(f"   Output: {out_root}")
        if all_warnings:
            print(f"\n⚠️  경고 {len(all_warnings)}개:")
            for w in all_warnings[:10]:
                print(f"   {w}")
            if len(all_warnings) > 10:
                print(f"   ... and {len(all_warnings) - 10} more")

    manifest["warnings"] = all_warnings
    return manifest


# ── CLI ─────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--spec", "-s", required=True, help="JSON spec 파일 경로")
    ap.add_argument("--dry-run", action="store_true", help="파일 생성 안 함, 검증만")
    ap.add_argument("--quiet", action="store_true", help="로그 출력 끄기")
    args = ap.parse_args()

    spec_data = json.loads(Path(args.spec).read_text(encoding="utf-8"))
    spec = LiveSpec.from_dict(spec_data)
    build(spec, log=not args.quiet, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
