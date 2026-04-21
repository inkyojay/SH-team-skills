"""Meta Ad Factory — reusable builder.

Generates Meta (Facebook/Instagram) ad creatives in multiple layouts, sizes,
and tones as standalone HTML files. Images are embedded as base64 so each
creative is self-contained and can be previewed or converted to PNG later.

Usage:
    from meta_ad_builder import build_ads

    build_ads(config, output_dir)

See products/swaddle_strap.py for a concrete example.
"""

from __future__ import annotations

import base64
import csv
import json
import mimetypes
from dataclasses import dataclass, field
from html import escape
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Size / font tables (from references/layout-templates.md)
# ---------------------------------------------------------------------------

SIZES = {
    "1080x1080": {"w": 1080, "h": 1080, "label": "1:1 피드"},
    "1080x1350": {"w": 1080, "h": 1350, "label": "4:5 IG 피드"},
    "1080x1920": {"w": 1080, "h": 1920, "label": "9:16 릴스/스토리"},
}

FONT_TABLES = {
    "hero-image": {
        "1080x1080": {"headline": 66, "subtext": 28, "cta": 26, "badge": 24},
        "1080x1350": {"headline": 76, "subtext": 32, "cta": 28, "badge": 26},
        "1080x1920": {"headline": 92, "subtext": 36, "cta": 32, "badge": 28},
    },
    "split-vertical": {
        "1080x1080": {"headline": 54, "subtext": 26, "cta": 24, "badge": 22},
        "1080x1350": {"headline": 62, "subtext": 28, "cta": 26, "badge": 24},
        "1080x1920": {"headline": 74, "subtext": 32, "cta": 28, "badge": 26},
    },
    "benefit-stack": {
        "1080x1080": {"headline": 46, "subtext": 22, "cta": 24},
        "1080x1350": {"headline": 54, "subtext": 24, "cta": 26},
        "1080x1920": {"headline": 62, "subtext": 26, "cta": 28},
    },
    "social-proof": {
        "1080x1080": {"headline": 44, "subtext": 26, "cta": 24},
        "1080x1350": {"headline": 52, "subtext": 28, "cta": 26},
        "1080x1920": {"headline": 58, "subtext": 30, "cta": 28},
    },
    "urgency": {
        "1080x1080": {"headline": 58, "subtext": 28, "cta": 28},
        "1080x1350": {"headline": 66, "subtext": 30, "cta": 30},
        "1080x1920": {"headline": 78, "subtext": 34, "cta": 32},
    },
    "split-horizontal": {
        "1080x1080": {"headline": 44, "subtext": 22, "cta": 22},
        "1080x1350": {"headline": 50, "subtext": 24, "cta": 24},
        "1080x1920": {"headline": 56, "subtext": 26, "cta": 26},
    },
}

# Reels/Stories safe zones (per meta-reels-ad-guide memory):
# top 108px, bottom 320px, left 60px, right 120px
REELS_SAFE_PAD = {"top": 108, "bottom": 320, "left": 60, "right": 120}


# ---------------------------------------------------------------------------
# Config dataclasses
# ---------------------------------------------------------------------------


@dataclass
class CopySet:
    tone: str  # emotional / informational / urgency
    headline: str
    subtext: str
    cta: str
    badge: str = ""  # optional discount badge
    urgency_label: str = ""  # for urgency layout


@dataclass
class Benefit:
    icon: str
    title: str
    desc: str


@dataclass
class AdSpec:
    idx: int
    layout: str
    size_key: str
    copy: CopySet
    image_key: str  # key in config["images"]


@dataclass
class ProductConfig:
    brand: str
    brand_name_ko: str
    product_name: str
    product_slug: str
    category: str
    colors: dict[str, str]
    images: dict[str, str]  # key -> file path
    copies: dict[str, list[CopySet]]  # tone -> list of CopySet
    benefits: list[Benefit] = field(default_factory=list)
    review: dict[str, str] = field(default_factory=dict)  # {"text": "", "name": ""}
    price_label: str = ""  # e.g. "19,900원"
    # Optional tone→image-pool mapping (image keys). Falls back to auto-pick if empty.
    tone_image_pools: dict[str, list[str]] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Image helpers
# ---------------------------------------------------------------------------


def encode_image(path: str | Path) -> str:
    """Return an <img src> compatible value.

    - If path starts with http(s), return it as-is (remote URL reference).
    - If it's a local path, base64-encode and return a data URI.
    """
    s = str(path)
    if s.startswith(("http://", "https://")):
        return s
    p = Path(s)
    mime, _ = mimetypes.guess_type(str(p))
    if mime is None:
        if p.suffix.lower() == ".webp":
            mime = "image/webp"
        else:
            mime = "application/octet-stream"
    data = p.read_bytes()
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"


# ---------------------------------------------------------------------------
# Layout renderers
# ---------------------------------------------------------------------------


COMMON_HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
html,body{{background:#333;font-family:'Noto Sans KR',sans-serif;}}
body{{display:flex;align-items:center;justify-content:center;min-height:100vh;}}
.ad-container{{width:{w}px;height:{h}px;position:relative;overflow:hidden;background:{secondary};}}
.ad-container img.product{{width:100%;height:100%;object-fit:cover;display:block;}}
</style>
</head>
<body>
"""


def _hero_image_html(spec: AdSpec, img_data: str, cfg: ProductConfig) -> str:
    size = SIZES[spec.size_key]
    fonts = FONT_TABLES["hero-image"][spec.size_key]
    c = cfg.colors
    copy = spec.copy
    badge = copy.badge.strip()
    is_reels = spec.size_key == "1080x1920"
    # Safe zone padding for 9:16
    pad_bottom = REELS_SAFE_PAD["bottom"] if is_reels else int(size["h"] * 0.08)
    pad_top = REELS_SAFE_PAD["top"] if is_reels else int(size["h"] * 0.05)
    pad_x = REELS_SAFE_PAD["left"] if is_reels else int(size["w"] * 0.08)

    badge_html = ""
    if badge:
        badge_html = f"""
        <div style="position:absolute;top:{pad_top}px;right:{pad_x}px;background:{c['accent']};
          color:#fff;padding:12px 24px;border-radius:50px;font-weight:900;
          font-size:{fonts['badge']}px;z-index:3;letter-spacing:1px;">
          {escape(badge)}
        </div>"""

    brand_html = f"""
        <div style="position:absolute;top:{pad_top}px;left:{pad_x}px;z-index:3;
          font-size:{int(fonts['badge']*0.85)}px;color:#fff;font-weight:700;
          letter-spacing:3px;text-transform:uppercase;
          text-shadow:0 2px 8px rgba(0,0,0,0.5);">
          {escape(cfg.brand)}
        </div>"""

    return f"""
    <div class="ad-container">
      <img class="product" src="{img_data}" alt="{escape(cfg.product_name)}">
      <div style="position:absolute;bottom:0;left:0;right:0;height:60%;
        background:linear-gradient(transparent,rgba(0,0,0,0.78));z-index:1;"></div>
      {brand_html}
      {badge_html}
      <div style="position:absolute;bottom:{pad_bottom}px;left:{pad_x}px;right:{pad_x}px;
        z-index:2;color:#fff;">
        <p style="font-size:{fonts['subtext']}px;opacity:0.92;margin-bottom:12px;line-height:1.4;
          font-weight:500;">
          {escape(copy.subtext)}
        </p>
        <h2 style="font-size:{fonts['headline']}px;font-weight:900;line-height:1.18;
          margin-bottom:24px;letter-spacing:-0.5px;white-space:pre-line;">{escape(copy.headline)}</h2>
        <div style="display:inline-block;background:{c['primary']};color:#fff;
          padding:16px 40px;border-radius:10px;font-weight:700;
          font-size:{fonts['cta']}px;">
          {escape(copy.cta)}
        </div>
      </div>
    </div>
    """


def _split_vertical_html(spec: AdSpec, img_data: str, cfg: ProductConfig) -> str:
    size = SIZES[spec.size_key]
    fonts = FONT_TABLES["split-vertical"][spec.size_key]
    c = cfg.colors
    copy = spec.copy
    badge = copy.badge.strip()
    badge_html = ""
    if badge:
        badge_html = f"""
          <div style="position:absolute;top:6%;right:6%;background:{c['accent']};
            color:#fff;padding:12px 26px;border-radius:50px;font-weight:900;
            font-size:{fonts['badge']}px;">{escape(badge)}</div>"""

    return f"""
    <div class="ad-container" style="display:flex;flex-direction:column;">
      <div style="flex:6;position:relative;overflow:hidden;">
        <img class="product" src="{img_data}" alt="{escape(cfg.product_name)}">
        {badge_html}
      </div>
      <div style="flex:4;display:flex;flex-direction:column;justify-content:center;
        align-items:center;padding:6% 8%;background:{c['secondary']};text-align:center;">
        <div style="font-size:{int(fonts['subtext']*0.7)}px;color:{c['primary']};
          font-weight:700;text-transform:uppercase;letter-spacing:3px;margin-bottom:16px;">
          {escape(cfg.brand)}
        </div>
        <h2 style="font-size:{fonts['headline']}px;font-weight:900;color:#1a1a1a;
          line-height:1.2;margin-bottom:16px;white-space:pre-line;">{escape(copy.headline)}</h2>
        <p style="font-size:{fonts['subtext']}px;color:#555;line-height:1.5;margin-bottom:24px;">
          {escape(copy.subtext)}
        </p>
        <div style="background:{c['primary']};color:#fff;padding:16px 44px;
          border-radius:10px;font-weight:700;font-size:{fonts['cta']}px;">
          {escape(copy.cta)}
        </div>
      </div>
    </div>
    """


def _benefit_stack_html(spec: AdSpec, img_data: str, cfg: ProductConfig) -> str:
    size = SIZES[spec.size_key]
    fonts = FONT_TABLES["benefit-stack"][spec.size_key]
    c = cfg.colors
    copy = spec.copy
    benefits = cfg.benefits[:4] if cfg.benefits else []

    items_html = ""
    for b in benefits:
        items_html += f"""
          <div style="display:flex;align-items:center;gap:20px;">
            <div style="width:64px;height:64px;background:{c['primary']};border-radius:50%;
              display:flex;align-items:center;justify-content:center;flex-shrink:0;">
              <span style="color:#fff;font-size:30px;">{escape(b.icon)}</span>
            </div>
            <div style="text-align:left;">
              <div style="font-weight:800;font-size:{fonts['subtext']+4}px;color:#1a1a1a;
                margin-bottom:4px;">{escape(b.title)}</div>
              <div style="font-size:{fonts['subtext']}px;color:#666;line-height:1.4;">
                {escape(b.desc)}
              </div>
            </div>
          </div>"""

    return f"""
    <div class="ad-container" style="display:flex;flex-direction:column;background:{c['secondary']};">
      <div style="flex:4;position:relative;overflow:hidden;">
        <img class="product" src="{img_data}" alt="{escape(cfg.product_name)}">
      </div>
      <div style="flex:6;padding:6% 8%;display:flex;flex-direction:column;justify-content:center;">
        <div style="font-size:{int(fonts['subtext']*0.85)}px;color:{c['primary']};
          font-weight:700;letter-spacing:3px;text-transform:uppercase;text-align:center;margin-bottom:12px;">
          {escape(cfg.brand)}
        </div>
        <h2 style="font-size:{fonts['headline']}px;font-weight:900;color:#1a1a1a;
          text-align:center;margin-bottom:28px;line-height:1.2;white-space:pre-line;">{escape(copy.headline)}</h2>
        <div style="display:flex;flex-direction:column;gap:20px;margin-bottom:28px;">
          {items_html}
        </div>
        <div style="background:{c['primary']};color:#fff;padding:16px 40px;
          border-radius:10px;font-weight:700;font-size:{fonts['cta']}px;text-align:center;">
          {escape(copy.cta)}
        </div>
      </div>
    </div>
    """


def _social_proof_html(spec: AdSpec, img_data: str, cfg: ProductConfig) -> str:
    size = SIZES[spec.size_key]
    fonts = FONT_TABLES["social-proof"][spec.size_key]
    c = cfg.colors
    copy = spec.copy
    review = cfg.review or {"text": "추천해요!", "name": "익명"}

    return f"""
    <div class="ad-container" style="display:flex;flex-direction:column;
      background:{c['secondary']};padding:7% 8%;">
      <div style="text-align:center;margin-bottom:24px;">
        <div style="font-size:{int(fonts['headline']*0.8)}px;margin-bottom:10px;color:#FFB800;">
          ⭐⭐⭐⭐⭐
        </div>
        <p style="font-size:{fonts['subtext']+4}px;color:#222;font-style:italic;
          line-height:1.55;font-weight:500;">
          "{escape(review.get('text',''))}"
        </p>
        <p style="font-size:{int(fonts['subtext']*0.8)}px;color:#888;margin-top:10px;">
          — {escape(review.get('name','리뷰어'))}
        </p>
      </div>
      <div style="flex:1;position:relative;overflow:hidden;border-radius:18px;
        margin-bottom:28px;box-shadow:0 8px 24px rgba(0,0,0,0.12);">
        <img class="product" src="{img_data}" alt="{escape(cfg.product_name)}">
      </div>
      <div style="text-align:center;">
        <h2 style="font-size:{fonts['headline']}px;font-weight:900;color:#1a1a1a;
          margin-bottom:18px;line-height:1.22;white-space:pre-line;">{escape(copy.headline)}</h2>
        <div style="display:inline-block;background:{c['primary']};color:#fff;
          padding:16px 44px;border-radius:10px;font-weight:700;
          font-size:{fonts['cta']}px;">{escape(copy.cta)}</div>
      </div>
    </div>
    """


LAYOUT_RENDERERS = {
    "hero-image": _hero_image_html,
    "split-vertical": _split_vertical_html,
    "benefit-stack": _benefit_stack_html,
    "social-proof": _social_proof_html,
}


def render_ad(spec: AdSpec, cfg: ProductConfig) -> str:
    size = SIZES[spec.size_key]
    img_data = encode_image(cfg.images[spec.image_key])
    body = LAYOUT_RENDERERS[spec.layout](spec, img_data, cfg)
    filename = f"{spec.idx:02d}_{spec.layout}_{spec.size_key}_{spec.copy.tone}"
    head = COMMON_HEAD.format(
        title=f"{cfg.product_name} — {filename}",
        w=size["w"],
        h=size["h"],
        secondary=cfg.colors["secondary"],
    )
    return head + body + "\n</body></html>"


# ---------------------------------------------------------------------------
# Smart combination planner
# ---------------------------------------------------------------------------


def plan_ads(cfg: ProductConfig) -> list[AdSpec]:
    """Generate a diverse pool of creatives.

    Strategy: every (layout, size, tone) slot picks a DIFFERENT image and copy
    via independent counters per tone, so images/copies rotate through the full
    pool instead of repeating the same one.

    - hero-image: 3 sizes × 3 tones = 9
    - split-vertical: 2 sizes × 3 tones = 6
    - benefit-stack: 2 sizes × 2 tones (info, urgency) = 4
    - social-proof: 2 sizes × 1 tone (informational, rotates copy) = 2
    Total: ~21
    """
    specs: list[AdSpec] = []
    idx = 1

    image_keys = list(cfg.images.keys())
    hero_imgs = [k for k in image_keys if "hero" in k or "main" in k] or image_keys[:1]
    lifestyle_imgs = [k for k in image_keys if "lifestyle" in k or "life" in k] or hero_imgs
    detail_imgs = [
        k for k in image_keys
        if k not in hero_imgs + lifestyle_imgs
    ] or hero_imgs

    # Per-tone pools (user override wins, else auto-infer)
    def _pool(tone: str) -> list[str]:
        if cfg.tone_image_pools.get(tone):
            return [k for k in cfg.tone_image_pools[tone] if k in cfg.images] or image_keys
        if tone == "emotional":
            return lifestyle_imgs + hero_imgs
        if tone == "informational":
            return detail_imgs + hero_imgs
        if tone == "urgency":
            return hero_imgs + detail_imgs[:2] + lifestyle_imgs[-1:]
        return image_keys

    pools = {t: _pool(t) for t in ("emotional", "informational", "urgency")}

    # Independent rotation counters so each tone cycles through its full pool
    img_counters: dict[str, int] = {"emotional": 0, "informational": 0, "urgency": 0}
    copy_counters: dict[str, int] = {"emotional": 0, "informational": 0, "urgency": 0}

    def next_image(tone: str) -> str:
        pool = pools[tone]
        k = pool[img_counters[tone] % len(pool)]
        img_counters[tone] += 1
        return k

    def next_copy(tone: str) -> CopySet | None:
        if tone not in cfg.copies or not cfg.copies[tone]:
            return None
        arr = cfg.copies[tone]
        c = arr[copy_counters[tone] % len(arr)]
        copy_counters[tone] += 1
        return c

    def add(layout: str, size_key: str, tone: str) -> None:
        nonlocal idx
        copy = next_copy(tone)
        if not copy:
            return
        img_key = next_image(tone)
        specs.append(
            AdSpec(
                idx=idx,
                layout=layout,
                size_key=size_key,
                copy=copy,
                image_key=img_key,
            )
        )
        idx += 1

    # hero-image : 3 sizes × 3 tones
    for size_key in ["1080x1080", "1080x1350", "1080x1920"]:
        for tone in ("emotional", "informational", "urgency"):
            add("hero-image", size_key, tone)

    # split-vertical : 2 sizes × 3 tones
    for size_key in ["1080x1350", "1080x1920"]:
        for tone in ("emotional", "informational", "urgency"):
            add("split-vertical", size_key, tone)

    # benefit-stack : 2 sizes × 2 tones (needs USP list)
    if cfg.benefits:
        for size_key in ["1080x1350", "1080x1920"]:
            for tone in ("informational", "urgency"):
                add("benefit-stack", size_key, tone)

    # social-proof : 2 sizes × 1 tone (rotates review/copy)
    if cfg.review:
        for size_key in ["1080x1350", "1080x1920"]:
            add("social-proof", size_key, "informational")

    return specs


# ---------------------------------------------------------------------------
# Preview grid
# ---------------------------------------------------------------------------


PREVIEW_GRID_TEMPLATE = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<title>{product} — Meta Ad Preview Grid</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box;}}
body{{font-family:'Noto Sans KR',sans-serif;background:#f3f4f6;color:#1a1a1a;min-height:100vh;}}
header{{background:#fff;padding:24px 32px;box-shadow:0 1px 3px rgba(0,0,0,0.08);position:sticky;top:0;z-index:100;}}
h1{{font-size:22px;font-weight:900;margin-bottom:4px;}}
.meta{{font-size:13px;color:#666;}}
.meta b{{color:{primary};}}
.filters{{display:flex;gap:12px;margin-top:16px;flex-wrap:wrap;align-items:center;}}
.filter-label{{font-size:12px;font-weight:700;color:#555;margin-right:4px;}}
.filter-group{{display:flex;gap:6px;background:#f3f4f6;padding:4px;border-radius:8px;}}
.filter-btn{{padding:6px 14px;border:none;background:transparent;border-radius:6px;cursor:pointer;font-size:12px;font-weight:600;color:#555;}}
.filter-btn.active{{background:{primary};color:#fff;}}
.action-row{{margin-left:auto;display:flex;gap:8px;align-items:center;}}
.action-btn{{padding:8px 16px;background:{primary};color:#fff;border:none;border-radius:6px;font-weight:700;cursor:pointer;font-size:13px;}}
.action-btn.ghost{{background:transparent;color:{primary};border:1px solid {primary};}}
.count{{font-size:12px;color:#666;margin-right:8px;}}

.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;padding:24px 32px;}}
.card{{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.08);transition:transform 0.15s,box-shadow 0.15s;cursor:pointer;position:relative;}}
.card:hover{{transform:translateY(-2px);box-shadow:0 4px 12px rgba(0,0,0,0.12);}}
.card.selected{{outline:3px solid {primary};}}
.card-preview{{background:#000;position:relative;overflow:hidden;}}
.card-preview iframe{{border:none;pointer-events:none;transform-origin:top left;position:absolute;top:0;left:0;}}
.card-body{{padding:12px 14px;}}
.card-name{{font-size:12px;font-family:monospace;color:#555;margin-bottom:4px;word-break:break-all;}}
.card-meta{{display:flex;gap:6px;flex-wrap:wrap;}}
.tag{{font-size:10px;padding:3px 8px;border-radius:4px;font-weight:700;letter-spacing:0.5px;}}
.tag.size{{background:#e0e7ff;color:#3730a3;}}
.tag.layout{{background:#d1fae5;color:#065f46;}}
.tag.tone-emotional{{background:#fce7f3;color:#9f1239;}}
.tag.tone-informational{{background:#dbeafe;color:#1e40af;}}
.tag.tone-urgency{{background:#fed7aa;color:#9a3412;}}
.checkbox{{position:absolute;top:10px;right:10px;width:28px;height:28px;background:rgba(255,255,255,0.95);border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:900;color:transparent;border:2px solid #ccc;z-index:10;pointer-events:none;}}
.card.selected .checkbox{{background:{primary};border-color:{primary};color:#fff;}}
.card.selected .checkbox::after{{content:"✓";}}

/* 원본 이미지 갤러리 */
.img-section{{padding:24px 32px 48px;}}
.img-section-title{{font-size:16px;font-weight:900;color:#1a1a1a;margin-bottom:4px;}}
.img-section-sub{{font-size:12px;color:#888;margin-bottom:16px;}}
.img-toggle{{background:none;border:1px solid #ddd;border-radius:6px;padding:6px 14px;font-size:12px;font-weight:600;cursor:pointer;color:#555;margin-bottom:16px;}}
.img-gallery{{display:none;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px;}}
.img-gallery.open{{display:grid;}}
.img-card{{background:#fff;border-radius:10px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,0.08);}}
.img-card img{{width:100%;aspect-ratio:1/1;object-fit:cover;display:block;background:#f3f4f6;}}
.img-card-body{{padding:8px 10px;}}
.img-card-key{{font-size:11px;font-family:monospace;color:#555;margin-bottom:4px;word-break:break-all;}}
.img-card-dl{{display:block;text-align:center;background:{primary};color:#fff;font-size:11px;font-weight:700;padding:6px;border-radius:4px;text-decoration:none;margin-top:6px;}}
.img-card-dl:hover{{opacity:0.85;}}
.img-card-video{{display:block;text-align:center;background:#1a1a1a;color:#fff;font-size:11px;font-weight:700;padding:6px;border-radius:4px;cursor:pointer;border:none;width:100%;margin-top:4px;position:relative;}}
.img-card-video:hover{{background:#333;}}
.img-cmd-panel{{display:none;margin-top:8px;background:#0f1117;border-radius:6px;padding:8px;}}
.img-cmd-panel.open{{display:block;}}
.img-cmd-code{{font-family:monospace;font-size:10px;color:#7ee787;white-space:pre-wrap;word-break:break-all;line-height:1.6;}}
.img-cmd-copy{{display:block;margin-top:6px;background:#238636;color:#fff;border:none;border-radius:4px;padding:5px 10px;font-size:10px;font-weight:700;cursor:pointer;width:100%;}}
.img-cmd-copy:hover{{background:#2ea043;}}
.img-toast-video{{position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:#1a1a1a;color:#7ee787;padding:10px 20px;border-radius:8px;font-size:13px;font-weight:700;display:none;z-index:9999;border:1px solid #238636;}}
.img-vid-status{{margin-top:6px;}}
.img-vid-bar{{height:4px;background:#e5e7eb;border-radius:4px;overflow:hidden;margin-bottom:4px;}}
.img-vid-fill{{height:100%;background:{primary};border-radius:4px;transition:width 0.4s ease,background 0.3s;width:0%;}}
.img-vid-msg{{font-size:10px;color:#555;line-height:1.4;word-break:break-all;}}

/* Modal */
.modal{{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.85);z-index:1000;padding:20px;overflow:auto;}}
.modal.active{{display:flex;align-items:center;justify-content:center;}}
.modal-inner{{background:#fff;border-radius:12px;padding:20px;max-width:95vw;max-height:95vh;overflow:auto;position:relative;}}
.modal-close{{position:absolute;top:10px;right:14px;font-size:28px;cursor:pointer;color:#999;}}
.modal iframe{{border:1px solid #ddd;display:block;}}
</style>
</head>
<body>
<header>
  <h1>{product} — Meta Ad Preview Grid</h1>
  <div class="meta">총 <b>{total}</b>개 크리에이티브 · {brand} · {category}</div>
  <div class="filters">
    <span class="filter-label">사이즈</span>
    <div class="filter-group" data-filter="size">
      <button class="filter-btn active" data-value="all">전체</button>
      <button class="filter-btn" data-value="1080x1080">1:1</button>
      <button class="filter-btn" data-value="1080x1350">4:5</button>
      <button class="filter-btn" data-value="1080x1920">9:16</button>
    </div>
    <span class="filter-label">레이아웃</span>
    <div class="filter-group" data-filter="layout">
      <button class="filter-btn active" data-value="all">전체</button>
      <button class="filter-btn" data-value="hero-image">Hero</button>
      <button class="filter-btn" data-value="split-vertical">Split</button>
      <button class="filter-btn" data-value="benefit-stack">Benefit</button>
      <button class="filter-btn" data-value="social-proof">Social</button>
    </div>
    <span class="filter-label">톤</span>
    <div class="filter-group" data-filter="tone">
      <button class="filter-btn active" data-value="all">전체</button>
      <button class="filter-btn" data-value="emotional">감성</button>
      <button class="filter-btn" data-value="informational">정보형</button>
      <button class="filter-btn" data-value="urgency">긴급성</button>
    </div>
    <div class="action-row">
      <span class="count" id="count">선택 0개</span>
      <button class="action-btn ghost" onclick="selectAll()">전체 선택</button>
      <button class="action-btn ghost" onclick="copySelection()">파일명 복사</button>
      <button class="action-btn" onclick="downloadPNGs(false)" title="선택된 PNG 다운로드 (선택 없으면 전체)">📥 PNG 다운로드</button>
    </div>
  </div>
</header>

<div class="grid" id="grid">
  {cards}
</div>

<!-- 원본 소스 이미지 갤러리 -->
{images_section}

<div class="modal" id="modal" onclick="closeModal(event)">
  <div class="modal-inner" onclick="event.stopPropagation()">
    <span class="modal-close" onclick="closeModal()">&times;</span>
    <iframe id="modal-iframe"></iframe>
  </div>
</div>

<script>
const cards = document.querySelectorAll('.card');
const filters = {{size:'all',layout:'all',tone:'all'}};
const selected = new Set();

document.querySelectorAll('.filter-group').forEach(group=>{{
  const key = group.dataset.filter;
  group.querySelectorAll('.filter-btn').forEach(btn=>{{
    btn.addEventListener('click',()=>{{
      group.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      filters[key] = btn.dataset.value;
      applyFilters();
    }});
  }});
}});

function applyFilters(){{
  cards.forEach(c=>{{
    const s = filters.size==='all' || c.dataset.size===filters.size;
    const l = filters.layout==='all' || c.dataset.layout===filters.layout;
    const t = filters.tone==='all' || c.dataset.tone===filters.tone;
    c.style.display = (s&&l&&t) ? '' : 'none';
  }});
}}

cards.forEach(card=>{{
  card.addEventListener('click',(e)=>{{
    if(e.shiftKey){{
      openModal(card.dataset.src);
      return;
    }}
    const name = card.dataset.name;
    if(selected.has(name)){{
      selected.delete(name);
      card.classList.remove('selected');
    }} else {{
      selected.add(name);
      card.classList.add('selected');
    }}
    updateCount();
  }});
  card.addEventListener('dblclick',()=>openModal(card.dataset.src));
}});

function openModal(src){{
  const m = document.getElementById('modal');
  const f = document.getElementById('modal-iframe');
  f.src = src;
  const c = [...cards].find(x=>x.dataset.src===src);
  if(c){{
    const [w,h] = c.dataset.size.split('x').map(Number);
    const maxW = window.innerWidth*0.9, maxH = window.innerHeight*0.85;
    const scale = Math.min(maxW/w, maxH/h, 1);
    f.style.width = (w*scale)+'px';
    f.style.height = (h*scale)+'px';
  }}
  m.classList.add('active');
}}
function closeModal(e){{ if(!e || e.target.id==='modal' || e.target.className==='modal-close'){{ document.getElementById('modal').classList.remove('active'); document.getElementById('modal-iframe').src=''; }} }}

function updateCount(){{ document.getElementById('count').textContent = '선택 '+selected.size+'개'; }}
function selectAll(){{ cards.forEach(c=>{{ if(c.style.display!=='none'){{ selected.add(c.dataset.name); c.classList.add('selected'); }} }}); updateCount(); }}
function copySelection(){{
  if(selected.size===0){{ alert('선택된 소재가 없습니다.'); return; }}
  navigator.clipboard.writeText([...selected].join('\\n')).then(()=>{{
    alert('선택된 '+selected.size+'개 파일명이 클립보드에 복사되었습니다.');
  }});
}}

function downloadPNGs(allVisible){{
  let targets;
  if(allVisible || selected.size===0){{
    targets = [...document.querySelectorAll('.card')]
      .filter(c=>c.style.display!=='none')
      .map(c=>c.dataset.name);
  }} else {{
    targets = [...selected];
  }}
  if(targets.length===0){{ alert('다운로드할 소재가 없습니다.'); return; }}
  const btn = document.querySelector('[onclick*="downloadPNGs"]');
  if(btn) btn.textContent = '⏳ 다운로드 중...';
  targets.forEach((name,i)=>{{
    setTimeout(()=>{{
      const stem = name.replace('.html','');
      const a = document.createElement('a');
      a.href = '../final/'+stem+'.png';
      a.download = stem+'.png';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      if(i===targets.length-1 && btn) btn.textContent = '📥 PNG 다운로드';
    }}, i*150);
  }});
}}

// ── 영상 광고 명령어 패널 ─────────────────────────────────────────────────────
function toggleCmd(id){{
  const panel = document.getElementById(id);
  if(!panel) return;
  panel.classList.toggle('open');
}}

function copyCmd(id){{
  const el = document.getElementById(id);
  if(!el) return;
  const text = el.textContent;
  navigator.clipboard.writeText(text).then(()=>{{
    const toast = document.getElementById('toastVideo');
    if(toast){{
      toast.style.display = 'block';
      setTimeout(()=>{{ toast.style.display='none'; }}, 2500);
    }}
  }}).catch(()=>{{
    // clipboard 실패 시 선택 fallback
    const range = document.createRange();
    range.selectNode(el);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
    alert('명령어가 복사되었습니다!');
  }});
}}
</script>
</body>
</html>
"""


def build_card_html(spec: AdSpec, filename: str) -> str:
    size = SIZES[spec.size_key]
    # Thumbnail max width 280px
    max_thumb_w = 280
    scale = max_thumb_w / size["w"]
    thumb_w = max_thumb_w
    thumb_h = int(size["h"] * scale)
    iframe_w = size["w"]
    iframe_h = size["h"]
    src = f"./{filename}.html"
    return f"""
  <div class="card" data-name="{filename}.html" data-src="{src}" data-size="{spec.size_key}" data-layout="{spec.layout}" data-tone="{spec.copy.tone}">
    <div class="checkbox"></div>
    <div class="card-preview" style="width:{thumb_w}px;height:{thumb_h}px;">
      <iframe src="{src}" width="{iframe_w}" height="{iframe_h}" style="transform:scale({scale:.4f});"></iframe>
    </div>
    <div class="card-body">
      <div class="card-name">{filename}.html</div>
      <div class="card-meta">
        <span class="tag size">{SIZES[spec.size_key]['label']}</span>
        <span class="tag layout">{spec.layout}</span>
        <span class="tag tone-{spec.copy.tone}">{_tone_ko(spec.copy.tone)}</span>
      </div>
    </div>
  </div>"""


def _tone_ko(tone: str) -> str:
    return {"emotional": "감성", "informational": "정보형", "urgency": "긴급성"}.get(tone, tone)


# ---------------------------------------------------------------------------
# Main entry
# ---------------------------------------------------------------------------


def _build_images_section(cfg: ProductConfig) -> str:
    """원본 소스 이미지 갤러리 HTML 섹션 생성 (🎬 원클릭 영상 생성 버튼 포함)."""
    slug = cfg.product_slug
    VIDEO_SERVER = "http://localhost:5173"

    cards = []
    for key, src in cfg.images.items():
        s = str(src)
        if s.startswith(("http://", "https://")):
            img_src = s
            dl_href = s
            dl_target = ' target="_blank"'
            img_arg = s
        else:
            abs_path = Path(s).resolve()
            img_src = abs_path.as_uri()
            dl_href = img_src
            dl_target = ''
            img_arg = str(abs_path)
        filename = Path(s).name
        card_id = f"vc_{slug}_{key}".replace("-", "_").replace(".", "_")
        # JSON 이스케이프된 값 (JS 인라인 삽입용)
        img_arg_js = img_arg.replace("\\", "\\\\").replace('"', '\\"')
        slug_js = slug.replace('"', '\\"')

        cards.append(f"""
  <div class="img-card" id="card_{card_id}">
    <img src="{img_src}" alt="{escape(key)}" loading="lazy" onerror="this.style.background='#e5e7eb';this.alt='이미지 없음'">
    <div class="img-card-body">
      <div class="img-card-key">{escape(key)}</div>
      <div class="img-card-key" style="color:#aaa;font-size:10px;">{escape(filename)}</div>
      <a class="img-card-dl" href="{dl_href}" download="{escape(filename)}"{dl_target}>⬇ 원본 다운로드</a>
      <div style="display:flex;gap:4px;margin-top:4px;">
        <button class="img-card-video" style="flex:1;" onclick="makeVideo('{card_id}','{img_arg_js}','{slug_js}','9:16')">🎬 9:16</button>
        <button class="img-card-video" style="flex:1;" onclick="makeVideo('{card_id}','{img_arg_js}','{slug_js}','1:1')">🎬 1:1</button>
      </div>
      <div class="img-vid-status" id="status_{card_id}" style="display:none;">
        <div class="img-vid-bar"><div class="img-vid-fill" id="fill_{card_id}"></div></div>
        <div class="img-vid-msg" id="msg_{card_id}">대기 중...</div>
      </div>
    </div>
  </div>""")

    toggle_js = "this.nextElementSibling.classList.toggle('open');this.textContent=this.nextElementSibling.classList.contains('open')?'▲ 원본 사진 닫기':'▼ 원본 사진 보기 ({n}장)'.replace('{n}','{count}')".replace("{count}", str(len(cards)))
    return f"""
<div class="img-section">
  <div class="img-section-title">📷 원본 소스 이미지</div>
  <div class="img-section-sub">원본 사진 {len(cards)}장 · ⬇ 다운로드 · 🎬 원클릭 영상 광고 생성
    <span id="srv-badge" style="margin-left:8px;font-size:10px;padding:2px 8px;border-radius:10px;background:#fee2e2;color:#991b1b;">서버 꺼짐</span>
  </div>
  <button class="img-toggle" onclick="{toggle_js}">▼ 원본 사진 보기 ({len(cards)}장)</button>
  <div class="img-gallery">
    {"".join(cards)}
  </div>
</div>
<div class="img-toast-video" id="toastVideo"></div>
<script>
const VIDEO_SERVER = '{VIDEO_SERVER}';

// ── 서버 연결 상태 체크 ────────────────────────────────────────────────────────
(function checkServer(){{
  const badge = document.getElementById('srv-badge');
  fetch(VIDEO_SERVER, {{mode:'cors'}})
    .then(r=>r.json())
    .then(d=>{{
      badge.style.background = '#dcfce7';
      badge.style.color = '#166534';
      badge.textContent = d.mode === 'mock' ? '🧪 Mock 서버 켜짐' : '🎬 Kling 서버 켜짐';
    }})
    .catch(()=>{{
      badge.style.background = '#fee2e2';
      badge.style.color = '#991b1b';
      badge.textContent = '⚠️ 서버 꺼짐 — python3 video_server.py --mock';
    }});
  setTimeout(checkServer, 5000);
}})();

// ── 영상 생성 요청 ─────────────────────────────────────────────────────────────
function makeVideo(cardId, image, slug, ratio){{
  const statusEl = document.getElementById('status_'+cardId);
  const fillEl   = document.getElementById('fill_'+cardId);
  const msgEl    = document.getElementById('msg_'+cardId);
  if(!statusEl) return;

  statusEl.style.display = 'block';
  fillEl.style.width = '5%';
  msgEl.textContent = '서버에 요청 중...';

  fetch(VIDEO_SERVER+'/make-video', {{
    method:'POST',
    headers:{{'Content-Type':'application/json'}},
    body: JSON.stringify({{image, slug, ratio, duration:5}})
  }})
  .then(r=>r.json())
  .then(d=>{{
    if(d.error){{ msgEl.textContent='❌ '+d.error; return; }}
    msgEl.textContent = '생성 중... (job: '+d.job_id+')';
    fillEl.style.width = '15%';
    pollJob(d.job_id, cardId, fillEl, msgEl);
  }})
  .catch(e=>{{
    msgEl.textContent = '❌ 서버 연결 실패. python3 video_server.py --mock 실행 후 재시도';
  }});
}}

function pollJob(jobId, cardId, fillEl, msgEl){{
  let pct = 20;
  const iv = setInterval(()=>{{
    fetch(VIDEO_SERVER+'/status/'+jobId)
      .then(r=>r.json())
      .then(d=>{{
        if(d.status==='running'){{
          pct = Math.min(pct+8, 85);
          fillEl.style.width = pct+'%';
          const last = d.log && d.log.length ? d.log[d.log.length-1] : '처리 중...';
          msgEl.textContent = last.replace(/^\\s+/,'');
        }} else if(d.status==='done'){{
          clearInterval(iv);
          fillEl.style.width = '100%';
          fillEl.style.background = '#22c55e';
          const dest = d.dest || 'video/ 폴더';
          msgEl.innerHTML = '✅ 완료! <a href="#" onclick="alert(\\''+dest+'\\')">저장 위치 확인</a>';
          showToast('✅ 영상 완료! video/ 폴더에 저장됨');
        }} else if(d.status==='error'){{
          clearInterval(iv);
          fillEl.style.background = '#ef4444';
          fillEl.style.width = '100%';
          msgEl.textContent = '❌ '+(d.error||'오류 발생');
        }}
      }})
      .catch(()=>clearInterval(iv));
  }}, 2000);
}}

function showToast(msg){{
  const t = document.getElementById('toastVideo');
  if(!t) return;
  t.textContent = msg;
  t.style.display = 'block';
  setTimeout(()=>{{ t.style.display='none'; }}, 3000);
}}
</script>"""


def build_ads(cfg: ProductConfig, output_dir: Path) -> list[AdSpec]:
    previews = output_dir / "previews"
    previews.mkdir(parents=True, exist_ok=True)

    specs = plan_ads(cfg)
    cards_html = []
    csv_rows = []

    for spec in specs:
        filename = f"{spec.idx:02d}_{spec.layout}_{spec.size_key}_{spec.copy.tone}"
        html = render_ad(spec, cfg)
        (previews / f"{filename}.html").write_text(html, encoding="utf-8")
        cards_html.append(build_card_html(spec, filename))
        csv_rows.append({
            "ad_name": filename,
            "primary_text": spec.copy.subtext,
            "headline": spec.copy.headline,
            "description": spec.copy.badge or "",
            "cta": spec.copy.cta,
            "image_file": Path(cfg.images[spec.image_key]).name,
            "size": spec.size_key,
            "layout": spec.layout,
            "tone": spec.copy.tone,
        })

    # 원본 이미지 갤러리 섹션
    images_section = _build_images_section(cfg)

    # Preview grid
    grid_html = PREVIEW_GRID_TEMPLATE.format(
        product=f"{cfg.brand_name_ko} {cfg.product_name}",
        brand=cfg.brand,
        category=cfg.category,
        primary=cfg.colors["primary"],
        total=len(specs),
        cards="\n".join(cards_html),
        images_section=images_section,
    )
    (previews / "preview-grid.html").write_text(grid_html, encoding="utf-8")

    # Copy CSV
    csv_path = output_dir / "copy.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "ad_name", "primary_text", "headline", "description",
                "cta", "image_file", "size", "layout", "tone",
            ],
        )
        writer.writeheader()
        writer.writerows(csv_rows)

    # Meta JSON (for later PNG conversion)
    meta = {
        "product": cfg.product_name,
        "brand": cfg.brand,
        "category": cfg.category,
        "total": len(specs),
        "specs": [
            {
                "idx": s.idx,
                "layout": s.layout,
                "size": s.size_key,
                "tone": s.copy.tone,
                "image": cfg.images[s.image_key],
                "filename": f"{s.idx:02d}_{s.layout}_{s.size_key}_{s.copy.tone}.html",
            }
            for s in specs
        ],
    }
    (output_dir / "build-meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    return specs
