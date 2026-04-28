"""
kakao_factory.py — 카카오톡 메시지 빌드 엔진 (v2)

v2 신규:
- 변형(variant) 자동 생성: 팔레트×톤 조합으로 N개 버전 일괄 생성
- D-live-carousel (1080×1350, .card class) 지원
- data-editable / data-image-key 자동 주입 → server.py 편집 가능
- 멀티카드 캐러셀 split 자동화 (.km-card / .card 자동 감지)

핵심 동작:
1. CSS 클래스 기반 텍스트 치환 (BeautifulSoup)
2. CSS 인라인화 (self-contained HTML)
3. 이미지 경로 → 출력 폴더로 복사 후 상대경로로 참조
4. data-palette 자동 주입
5. 변형 N개 일괄 생성

사용:
    python3 kakao_factory.py build path/to/config.py
    python3 kakao_factory.py list-templates
    python3 kakao_factory.py inspect 04-carousel-feed:D-live-carousel--portable-bed
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import shutil
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup, NavigableString
except ImportError:
    print("❌ BeautifulSoup4 미설치. 설치: pip install beautifulsoup4", file=sys.stderr)
    sys.exit(1)

import kakao_validator as kv

# ─── 경로 ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_DIR = SCRIPT_DIR / ".template-cache"
TYPES_DIR = CACHE_DIR / "types"

DESKTOP = Path.home() / "Desktop"
OUTPUT_BASE = DESKTOP / "team-skills" / "카카오메시지"

# ─── 12 팔레트 ──────────────────────────────────────────────────────────────
PALETTES = [
    "golden-hour", "warm-spring", "cool-summer", "cozy-autumn", "gentle-winter",
    "rose-dawn", "fresh-garden", "moonlit-calm", "blush-touch",
    "slate-mood", "coral-sunset", "midnight-luxe",
]

# ─── 5 톤 (카피 스타일) ─────────────────────────────────────────────────────
TONES = ["emotional", "informational", "urgency", "premium", "soft"]


# ─── Dataclasses ────────────────────────────────────────────────────────────
@dataclass
class ToneCopy:
    """톤별 카피 변형 — 같은 클래스 키에 톤별로 다른 텍스트."""
    tone: str                                    # "emotional" 등
    palette: str                                 # 이 톤에 추천할 팔레트
    texts: dict[str, str | int] = field(default_factory=dict)


@dataclass
class MessageBuild:
    """단일 메시지 빌드 정의."""
    template_id: str                             # "02-wide-image:A-product"
    output_name: str                             # "abc-crib_promo" (확장자 X)
    images: dict[str, str] = field(default_factory=dict)  # 모든 변형이 공유
    base_texts: dict[str, str | int] = field(default_factory=dict)  # 변형 공통 텍스트
    variants: list[ToneCopy] = field(default_factory=list)  # 비어있으면 단일 빌드
    palette: str | None = None                   # variants 비어있을 때만 사용


@dataclass
class CarouselBuild:
    """캐러셀 빌드 (카드 N장 묶음 → 카드별 별도 HTML)."""
    template_id: str                             # "05-carousel-commerce:A-standard"
    output_name: str                             # "abc-crib_lineup"
    cards: list[dict[str, Any]] = field(default_factory=list)
    palette: str | None = None
    # D-live-carousel처럼 5개 카드가 한 템플릿 안에 모두 있는 경우
    # auto: .km-card 또는 .card 자동 감지
    card_strategy: str = "auto"


@dataclass
class KakaoCampaign:
    """캠페인 단위 빌드 정의."""
    brand: str = "sundayhug"
    campaign_slug: str = "campaign"
    palette: str = "warm-spring"
    messages: list[MessageBuild] = field(default_factory=list)
    carousels: list[CarouselBuild] = field(default_factory=list)


# ─── 템플릿 로딩/탐색 ───────────────────────────────────────────────────────
def parse_template_id(template_id: str) -> tuple[str, str]:
    """'02-wide-image:A-product' → ('02-wide-image', 'A-product')"""
    if ":" not in template_id:
        raise ValueError(f"Invalid template_id (need 'type:variation'): {template_id}")
    type_id, variation = template_id.split(":", 1)
    return type_id, variation


def load_template(template_id: str) -> str:
    """캐시에서 템플릿 HTML 로드."""
    type_id, variation = parse_template_id(template_id)
    path = TYPES_DIR / type_id / f"{variation}.html"
    if not path.exists():
        candidates = list((TYPES_DIR / type_id).glob(f"{variation}*.html"))
        if not candidates:
            raise FileNotFoundError(
                f"Template not found: {template_id} → {path}\n"
                f"sync_templates.py를 먼저 실행했는지 확인하세요."
            )
        path = candidates[0]
    return path.read_text(encoding="utf-8")


def list_templates() -> list[str]:
    if not TYPES_DIR.exists():
        return []
    result = []
    for type_dir in sorted(TYPES_DIR.iterdir()):
        if not type_dir.is_dir():
            continue
        for html in sorted(type_dir.glob("*.html")):
            result.append(f"{type_dir.name}:{html.stem}")
    return result


def detect_template_size(template_id: str) -> tuple[int, int]:
    """템플릿 HTML 주석에서 DIMENSIONS 파싱."""
    try:
        html = load_template(template_id)
    except FileNotFoundError:
        return _suffix_default_for_type(template_id.split(":")[0])
    # 주석 파싱: "DIMENSIONS: 1080 × 1350px" 또는 "1080×1350"
    m = re.search(r"DIMENSIONS:\s*(\d+)\s*[×x]\s*(\d+)", html)
    if m:
        return int(m.group(1)), int(m.group(2))
    return _suffix_default_for_type(template_id.split(":")[0])


def _suffix_default_for_type(type_id: str) -> tuple[int, int]:
    mapping = {
        "01-image": (800, 400),
        "02-wide-image": (800, 600),
        "03-wide-list": (800, 800),
        "04-carousel-feed": (800, 600),
        "05-carousel-commerce": (800, 800),
        "06-commerce": (800, 600),
        "07-alimtalk-image": (800, 400),
        "08-alimtalk-itemlist": (800, 800),
    }
    return mapping.get(type_id, (800, 600))


# ─── CSS 인라인화 ───────────────────────────────────────────────────────────
def inline_css(soup: BeautifulSoup) -> None:
    """캐시된 카카오 CSS 전체를 <style>로 인라인 (link 제거)."""
    css_files = ["_global-palettes.css", "_palettes.css", "_base-styles.css"]
    css_blocks = []
    for css_name in css_files:
        css_path = CACHE_DIR / css_name
        if css_path.exists():
            content = css_path.read_text(encoding="utf-8")
            content = re.sub(r"@import\s+url\([^)]*_global-palettes\.css\);?", "", content)
            css_blocks.append(f"/* === {css_name} === */\n{content}")

    for link in soup.find_all("link", rel="stylesheet"):
        href = link.get("href", "")
        if "_base-styles" in href or "_palettes" in href or "_global-palettes" in href:
            link.decompose()

    head = soup.find("head")
    if head is None:
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
    style = soup.new_tag("style")
    style.string = "\n\n".join(css_blocks)
    head.append(style)


# ─── 텍스트 포맷 ────────────────────────────────────────────────────────────
NUMERIC_PRICE_CLASSES = {
    "km-info-bar-price", "km-info-bar-orig",
    "km-commerce-price", "km-commerce-orig",
    "km-list-item-price", "km-list-item-orig",
    "km-dual-price", "km-dual-orig",
    "km-triple-price",
    "km-rec-card-price",
    "km-itemlist-item-price",
    "km-price", "km-price-orig", "km-price-value",
}

PERCENT_DISCOUNT_CLASSES = {
    "km-info-bar-discount", "km-commerce-discount",
    "km-list-item-discount", "km-dual-discount",
    "km-rec-card-discount",
}


def format_value(cls: str, value: str | int) -> str:
    """클래스명 기반 자동 포맷 (가격 → 29,900원, 할인율 → 52%)."""
    s = str(value).strip()
    if cls in NUMERIC_PRICE_CLASSES and s.replace(",", "").replace("원", "").isdigit():
        n = int(s.replace(",", "").replace("원", ""))
        return f"{n:,}원"
    if cls in PERCENT_DISCOUNT_CLASSES:
        if s.endswith("%"):
            return s
        if s.isdigit():
            return f"{s}%"
    return s


def replace_text_by_class(
    soup: BeautifulSoup,
    texts: dict[str, str | int],
    add_editable: bool = True,
) -> dict[str, int]:
    """
    클래스명별로 텍스트 치환 + data-editable 자동 부여.
    `cls@N` 형태로 N번째 매칭만 치환 가능.
    """
    counts = {}
    for cls, value in texts.items():
        if "@" in cls:
            base_cls, idx_str = cls.split("@", 1)
            idx = int(idx_str)
            elements = soup.select(f".{base_cls}")
            if 0 <= idx < len(elements):
                _set_element_text(soup, elements[idx], format_value(base_cls, value))
                if add_editable:
                    elements[idx]["data-editable"] = cls
                counts[cls] = 1
            else:
                counts[cls] = 0
        else:
            elements = soup.select(f".{cls}")
            for el in elements:
                _set_element_text(soup, el, format_value(cls, value))
                if add_editable:
                    el["data-editable"] = cls
            counts[cls] = len(elements)
    return counts


def _set_element_text(soup: BeautifulSoup, el, text: str) -> None:
    """요소 내용을 새 텍스트로 완전 교체. '\\n' → <br> 변환."""
    el.clear()
    parts = text.split("\n") if "\n" in text else [text]
    for i, part in enumerate(parts):
        if i > 0:
            el.append(soup.new_tag("br"))
        el.append(NavigableString(part))


# ─── 이미지 치환 ────────────────────────────────────────────────────────────
def replace_images_by_class(
    soup: BeautifulSoup,
    images: dict[str, str],
    output_dir: Path,
    images_subdir: str = "images",
    add_editable: bool = True,
) -> dict[str, str]:
    """
    이미지 경로 치환 + 출력 폴더로 복사 + data-image-key 부여.
    `<img class="...">` 또는 div의 background-image 모두 처리.
    """
    actually_used = {}
    img_dir = output_dir / images_subdir
    img_dir.mkdir(parents=True, exist_ok=True)

    for cls, src_path_str in images.items():
        src = Path(src_path_str).expanduser()
        if not src.exists():
            print(f"⚠️  이미지 누락: {src}", file=sys.stderr)
            continue
        dst = img_dir / src.name
        if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
            shutil.copy2(src, dst)
        rel_src = f"{images_subdir}/{src.name}"

        if "@" in cls:
            base_cls, idx_str = cls.split("@", 1)
            idx = int(idx_str)
            elements = soup.select(f"img.{base_cls}, .{base_cls}")
            if 0 <= idx < len(elements):
                el = elements[idx]
                _apply_image_src(el, rel_src, cls if add_editable else None)
                actually_used[cls] = rel_src
        else:
            for el in soup.select(f"img.{cls}, .{cls}"):
                _apply_image_src(el, rel_src, cls if add_editable else None)
            actually_used[cls] = rel_src

    return actually_used


def _apply_image_src(el, rel_src: str, editable_key: str | None) -> None:
    """img 태그면 src 변경, 그 외엔 background-image 변경."""
    if el.name == "img":
        el["src"] = rel_src
        if editable_key:
            el["data-image-key"] = editable_key
    else:
        style = el.get("style", "") or ""
        if "background-image" in style:
            el["style"] = re.sub(
                r"background-image:\s*url\([^)]+\)",
                f"background-image:url({rel_src})", style,
            )
        else:
            el["style"] = (style + f";background-image:url({rel_src})").lstrip(";")
        if editable_key:
            el["data-image-key"] = editable_key


# ─── 절대경로 src 자동 보정 (D-live 템플릿용) ──────────────────────────────
def fix_absolute_image_paths(
    soup: BeautifulSoup,
    image_overrides: dict[str, str],
    output_dir: Path,
) -> int:
    """
    템플릿이 절대경로(`/Users/.../이미지/메인.png`)를 사용하는 경우
    1) image_overrides의 alt-text 매칭 → 새 경로로 교체
    2) 매칭 안 된 경우 src를 비우고 placeholder 표시
    반환: 교체된 개수
    """
    img_dir = output_dir / "images"
    img_dir.mkdir(parents=True, exist_ok=True)
    replaced = 0

    for img in soup.find_all("img"):
        src = img.get("src", "") or ""
        # 절대경로 또는 깨진 상대경로
        if not (src.startswith("/Users/") or src.startswith("../") or "Desktop" in src):
            continue

        alt = img.get("alt", "").strip()
        # alt 텍스트 또는 파일명으로 override 매칭
        match_key = None
        for key in image_overrides:
            key_norm = key.lower().replace("-", "").replace("_", "").replace(" ", "")
            alt_norm = alt.lower().replace("-", "").replace("_", "").replace(" ", "")
            if key_norm == alt_norm or key_norm in alt_norm or alt_norm in key_norm:
                match_key = key
                break

        if match_key:
            new_src = Path(image_overrides[match_key]).expanduser()
            if new_src.exists():
                dst = img_dir / new_src.name
                if not dst.exists() or dst.stat().st_mtime < new_src.stat().st_mtime:
                    shutil.copy2(new_src, dst)
                img["src"] = f"images/{new_src.name}"
                img["data-image-key"] = match_key
                replaced += 1
                continue

        # 매칭 실패 → 공백 + 회색 placeholder
        img["src"] = ""
        img["alt"] = f"[누락: {alt}]"
        img["style"] = (img.get("style", "") + ";background:#ddd;color:#888;").lstrip(";")

    return replaced


# ─── 팔레트 주입 ────────────────────────────────────────────────────────────
def inject_palette(soup: BeautifulSoup, palette: str) -> None:
    body = soup.find("body")
    if body is not None:
        body["data-palette"] = palette


# ─── 카드 split (멀티카드 캐러셀 분리) ──────────────────────────────────────
def detect_cards(soup: BeautifulSoup) -> list[Any]:
    """템플릿 안의 카드 요소 리스트 자동 감지."""
    candidates = soup.select(".km-card") or soup.select(".kakao-frame") or soup.select(".card")
    return candidates


def isolate_card(soup: BeautifulSoup, card_index: int) -> bool:
    """
    템플릿 내 N번째 카드만 남기고 나머지 카드는 제거.
    카드 사이의 <h3> 라벨도 함께 제거.
    """
    cards = detect_cards(soup)
    if not cards or card_index >= len(cards):
        return False

    keep = cards[card_index]
    # 다른 카드 모두 제거
    for j, c in enumerate(cards):
        if j == card_index:
            continue
        c.decompose()

    # h3 라벨(라이브 캐러셀 템플릿의 "CARD 1 · MAIN" 등) 제거
    for h3 in soup.find_all("h3"):
        h3.decompose()

    # margin-top:20px 같은 카드 간 간격 스타일 제거
    if keep.get("style"):
        keep["style"] = re.sub(r"margin-top:\s*\d+px;?", "", keep["style"])
        keep["style"] = re.sub(r"margin-bottom:\s*\d+px;?", "", keep["style"])

    # body padding 제거 (단독 카드 캡처 시 여백 없애기)
    body = soup.find("body")
    if body is not None and body.get("style"):
        body["style"] = re.sub(r"padding:\s*\d+px;?", "padding:0;", body["style"])

    return True


# ─── 빌드: 단일 메시지 ──────────────────────────────────────────────────────
def build_single(
    template_id: str,
    output_dir: Path,
    output_filename: str,
    palette: str,
    images: dict[str, str],
    texts: dict[str, str | int],
) -> Path:
    """단일 HTML 빌드 → output_dir/output_filename"""
    html = load_template(template_id)
    soup = BeautifulSoup(html, "html.parser")

    inline_css(soup)
    inject_palette(soup, palette)
    replace_images_by_class(soup, images, output_dir)
    fix_absolute_image_paths(soup, images, output_dir)
    replace_text_by_class(soup, texts)

    out_path = output_dir / output_filename
    out_path.write_text(str(soup), encoding="utf-8")
    return out_path


def build_message(
    msg: MessageBuild,
    output_dir: Path,
    default_palette: str,
) -> list[Path]:
    """단일 메시지 빌드. 변형이 있으면 N개, 없으면 1개 HTML 생성."""
    type_id, _ = parse_template_id(msg.template_id)
    w, h = detect_template_size(msg.template_id)
    size_suffix = f"{w}x{h}"

    paths = []
    if msg.variants:
        for variant in msg.variants:
            merged_texts = {**msg.base_texts, **variant.texts}
            out_name = (
                f"{msg.output_name}_{variant.tone}_{variant.palette}_"
                f"{type_id}_{size_suffix}.html"
            )
            path = build_single(
                msg.template_id, output_dir, out_name,
                palette=variant.palette,
                images=msg.images,
                texts=merged_texts,
            )
            paths.append(path)
    else:
        palette = msg.palette or default_palette
        out_name = f"{msg.output_name}_{type_id}_{size_suffix}.html"
        path = build_single(
            msg.template_id, output_dir, out_name,
            palette=palette,
            images=msg.images,
            texts=msg.base_texts,
        )
        paths.append(path)

    return paths


# ─── 빌드: 캐러셀 ───────────────────────────────────────────────────────────
def build_carousel(
    car: CarouselBuild,
    output_dir: Path,
    default_palette: str,
) -> list[Path]:
    """
    캐러셀 빌드 — 각 카드를 별도 HTML 파일로 출력.
    템플릿이 N장의 카드 구조를 가진 경우(D-live-carousel),
    car.cards가 비어있으면 자동으로 모든 카드를 추출해서 N개 HTML 생성.
    """
    paths = []
    type_id, _ = parse_template_id(car.template_id)
    w, h = detect_template_size(car.template_id)
    size_suffix = f"{w}x{h}"
    palette = car.palette or default_palette

    if car.cards:
        # 사용자가 카드별 데이터 명시
        for i, card in enumerate(car.cards, start=1):
            card_index = card.get("card_index", i - 1)
            html = load_template(car.template_id)
            soup = BeautifulSoup(html, "html.parser")
            isolate_card(soup, card_index)
            inline_css(soup)
            inject_palette(soup, palette)
            replace_images_by_class(soup, card.get("images", {}), output_dir)
            fix_absolute_image_paths(soup, card.get("images", {}), output_dir)
            replace_text_by_class(soup, card.get("texts", {}))
            out_name = f"{car.output_name}_card{i:02d}_{type_id}_{size_suffix}.html"
            out_path = output_dir / out_name
            out_path.write_text(str(soup), encoding="utf-8")
            paths.append(out_path)
    else:
        # 카드 데이터 미지정 → 템플릿 그대로 N개 카드 분리
        html = load_template(car.template_id)
        soup_full = BeautifulSoup(html, "html.parser")
        n_cards = len(detect_cards(soup_full))
        if n_cards == 0:
            print(f"⚠️  {car.template_id}: 카드 감지 실패", file=sys.stderr)
            return paths
        for i in range(n_cards):
            html = load_template(car.template_id)
            soup = BeautifulSoup(html, "html.parser")
            isolate_card(soup, i)
            inline_css(soup)
            inject_palette(soup, palette)
            # 절대경로 이미지 placeholder 처리 (사용자 이미지 미제공)
            fix_absolute_image_paths(soup, {}, output_dir)
            out_name = f"{car.output_name}_card{i+1:02d}_{type_id}_{size_suffix}.html"
            out_path = output_dir / out_name
            out_path.write_text(str(soup), encoding="utf-8")
            paths.append(out_path)

    return paths


# ─── 캠페인 빌드 ────────────────────────────────────────────────────────────
def build_campaign(campaign: KakaoCampaign) -> dict[str, Any]:
    out_dir = OUTPUT_BASE / campaign.brand / campaign.campaign_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {"output_dir": str(out_dir), "messages": [], "carousels": [], "errors": []}

    print(f"\n📦 Building campaign: {campaign.campaign_slug}")
    print(f"📂 Output: {out_dir}")
    print(f"🎨 Default Palette: {campaign.palette}\n")

    for msg in campaign.messages:
        try:
            paths = build_message(msg, out_dir, campaign.palette)
            for p in paths:
                summary["messages"].append(str(p))
                print(f"  ✓ {p.name}")
        except Exception as e:
            summary["errors"].append({"type": "message", "id": msg.output_name, "error": str(e)})
            print(f"  ✗ {msg.output_name}: {e}", file=sys.stderr)

    for car in campaign.carousels:
        try:
            paths = build_carousel(car, out_dir, campaign.palette)
            summary["carousels"].append({"name": car.output_name, "cards": [str(p) for p in paths]})
            for p in paths:
                print(f"  ✓ {p.name}")
        except Exception as e:
            summary["errors"].append({"type": "carousel", "id": car.output_name, "error": str(e)})
            print(f"  ✗ {car.output_name}: {e}", file=sys.stderr)

    grid_path = generate_preview_grid(out_dir, campaign)
    summary["preview_grid"] = str(grid_path)

    n_msg = len(summary["messages"])
    n_card = sum(len(c["cards"]) for c in summary["carousels"])
    print(f"\n총: {n_msg}개 메시지 + {n_card}개 캐러셀 카드")
    print(f"🌐 Preview: {grid_path}")
    if summary["errors"]:
        print(f"⚠️  에러 {len(summary['errors'])}건", file=sys.stderr)
    return summary


# ─── Preview Grid ───────────────────────────────────────────────────────────
def generate_preview_grid(out_dir: Path, campaign: KakaoCampaign) -> Path:
    htmls = sorted(
        f for f in out_dir.glob("*.html")
        if f.name not in {"preview-grid.html", "template-guide.html"}
    )

    items = []
    for html in htmls:
        m = re.search(r"_(\d+)x(\d+)\.html$", html.name)
        w, h = (int(m.group(1)), int(m.group(2))) if m else (800, 600)
        type_m = re.search(r"_(\d{2}-[a-z-]+)_", html.name)
        type_label = type_m.group(1) if type_m else "?"
        card_m = re.search(r"_card(\d+)_", html.name)
        card_label = f" · 카드{int(card_m.group(1))}" if card_m else ""
        # variant 정보 추출
        variant_m = re.search(r"_(emotional|informational|urgency|premium|soft)_(" + "|".join(PALETTES) + ")_", html.name)
        variant_label = ""
        if variant_m:
            variant_label = f" · {variant_m.group(1)}/{variant_m.group(2)}"

        png_name = html.stem + ".png"
        scale = min(360 / w, 1)
        items.append(f"""
<div class="grid-item">
  <div class="grid-meta">
    <span class="grid-type">{type_label}{card_label}</span>
    <span class="grid-size">{w}×{h}</span>
  </div>
  <div class="grid-variant">{variant_label}</div>
  <div class="grid-frame" style="width:{int(w*scale)}px;height:{int(h*scale)}px;">
    <iframe src="{html.name}" width="{w}" height="{h}"
            style="transform:scale({scale:.4f});transform-origin:top left;border:0;"></iframe>
  </div>
  <div class="grid-actions">
    <a href="{html.name}" target="_blank">🔍 HTML</a>
    <a href="png/{png_name}" download>📥 PNG</a>
    <button class="copy-name" data-name="{html.stem}">📋 파일명</button>
  </div>
</div>""")

    grid_html = f"""<!DOCTYPE html>
<html lang="ko"><head>
<meta charset="UTF-8">
<title>{campaign.campaign_slug} — 카카오 메시지</title>
<style>
  body{{font-family:'Noto Sans KR',-apple-system,sans-serif;background:#f5f5f5;margin:0;padding:24px;}}
  h1{{font-size:24px;margin:0 0 4px;}}
  .meta{{color:#666;margin-bottom:20px;}}
  .summary{{background:#fff;padding:14px 18px;border-radius:8px;margin-bottom:24px;font-size:13px;color:#555;line-height:1.6;font-family:monospace;}}
  .summary code{{background:#eef;padding:2px 6px;border-radius:3px;}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:24px;}}
  .grid-item{{background:#fff;border-radius:12px;padding:16px;box-shadow:0 2px 8px rgba(0,0,0,.06);}}
  .grid-meta{{display:flex;justify-content:space-between;font-size:12px;margin-bottom:6px;}}
  .grid-type{{background:#1D9E75;color:#fff;padding:3px 8px;border-radius:4px;font-weight:600;}}
  .grid-size{{color:#888;font-family:monospace;}}
  .grid-variant{{font-size:11px;color:#9C5BD5;font-weight:600;margin-bottom:8px;height:14px;}}
  .grid-frame{{overflow:hidden;border:1px solid #eee;background:#eee;border-radius:8px;margin-bottom:8px;}}
  .grid-actions{{display:flex;gap:6px;}}
  .grid-actions a, .grid-actions button{{font-size:12px;padding:6px 12px;border-radius:6px;background:#f0f0f0;color:#333;text-decoration:none;border:0;cursor:pointer;font-family:inherit;}}
  .grid-actions a:hover, .grid-actions button:hover{{background:#1D9E75;color:#fff;}}
</style>
</head><body>
<h1>📨 {campaign.campaign_slug}</h1>
<div class="meta">brand: <b>{campaign.brand}</b> · default palette: <b>{campaign.palette}</b> · {len(htmls)}개 출력물</div>
<div class="summary">
💡 PNG 변환 (자동 압축): <code>python3 export_png.py "{out_dir}"</code><br>
✏️  텍스트/이미지 편집 서버: <code>python3 server.py --slug {campaign.campaign_slug}</code>
</div>
<div class="grid">{"".join(items)}</div>
<script>
  document.querySelectorAll('.copy-name').forEach(b=>{{
    b.addEventListener('click',()=>{{navigator.clipboard.writeText(b.dataset.name);b.textContent='✓ 복사됨';setTimeout(()=>b.textContent='📋 파일명',1500);}});
  }});
</script>
</body></html>"""
    grid_path = out_dir / "preview-grid.html"
    grid_path.write_text(grid_html, encoding="utf-8")
    return grid_path


# ─── 변형 생성 헬퍼 ────────────────────────────────────────────────────────
def make_variants(
    base_texts: dict[str, str | int],
    tone_overrides: dict[str, dict[str, str | int]] | None = None,
    palettes: list[str] | None = None,
    n: int = 5,
) -> list[ToneCopy]:
    """
    팔레트 × 톤 조합으로 N개 ToneCopy 변형 자동 생성.

    tone_overrides: {"emotional": {"km-info-bar-name": "엄마의 첫 한 마디", ...}}
    palettes: 사용할 팔레트 리스트 (None이면 기본 5개)
    n: 생성할 변형 개수 (default 5)
    """
    palettes = palettes or ["warm-spring", "cool-summer", "cozy-autumn", "midnight-luxe", "rose-dawn"]
    tones = TONES[:n]
    variants = []
    for i in range(min(n, len(tones), len(palettes))):
        tone = tones[i]
        palette = palettes[i % len(palettes)]
        overrides = (tone_overrides or {}).get(tone, {})
        variants.append(ToneCopy(
            tone=tone,
            palette=palette,
            texts=overrides,
        ))
    return variants


# ═══════════════════════════════════════════════════════════════════════════
# v3 — 시맨틱 슬롯 + 다양성 레시피 (시각적으로 다른 N변형 자동 생성)
# ═══════════════════════════════════════════════════════════════════════════

@dataclass
class SemanticData:
    """시맨틱 슬롯 기반 입력 — 한 번 채우면 모든 템플릿에 자동 매핑."""
    # 텍스트 슬롯
    title: str = ""
    desc: str = ""
    badge: str = ""
    category: str = ""
    discount: int = 0
    price: int = 0
    orig: int = 0
    label: str = ""
    tag: str = ""
    info: str = ""
    brand: str = ""
    sub: str = ""
    date: str = ""

    # 이미지 슬롯 (key = 시맨틱, value = 파일 경로)
    images: dict = field(default_factory=dict)

    # 톤별 텍스트 오버라이드 (Claude가 인터뷰 후 채움)
    # {"emotional": {"title": "엄마의...", "desc": "..."}, "urgency": {...}, ...}
    tone_overrides: dict = field(default_factory=dict)

    # 캐러셀 카드별 시맨틱 데이터 (카루셀 레시피 사용 시)
    # 예: items=[{"title":"크림","price":119000,"image":"/path"}, ...]
    items: list = field(default_factory=list)


@dataclass
class CampaignV3:
    """v3 레시피 기반 캠페인."""
    brand: str = "sundayhug"
    campaign_slug: str = ""
    recipes: list = field(default_factory=list)  # ["wide-mix-5", "carousel-mix-5"]
    data: Any = None  # SemanticData

    # 라이브 캐러셀용 (live-carousel 레시피 사용 시)
    live_template_hint: str = ""  # "abc-bed" | "portable-bed" | "" (auto)
    live_data: dict = field(default_factory=dict)


def to_semantic_dict(sd) -> dict:
    """SemanticData → dict (None/0/'' 제외)."""
    d = {}
    for f in ("title", "desc", "badge", "category", "discount", "price", "orig",
              "label", "tag", "info", "brand", "sub", "date"):
        v = getattr(sd, f, None)
        if v not in (None, "", 0):
            d[f] = v
        elif f in ("discount", "price", "orig") and v == 0:
            # 가격 0은 제외, 사용자 명시 안 함
            pass
    return d


def build_v3_message(
    template_id: str,
    palette: str,
    tone: str,
    semantic: Any,
    output_dir: Path,
    output_name: str,
) -> Path:
    """v3: 시맨틱 데이터를 받아 템플릿에 자동 매핑."""
    from semantic_slots import map_semantic_to_classes, map_semantic_images
    from recipes import apply_tone_transform

    type_id, _ = parse_template_id(template_id)
    w, h = detect_template_size(template_id)
    size_suffix = f"{w}x{h}"

    # 톤별 오버라이드 적용
    base_dict = to_semantic_dict(semantic)
    tone_override = (semantic.tone_overrides or {}).get(tone, {})
    merged = {**base_dict, **tone_override}

    # 톤 fallback 변형 (오버라이드 없을 때만)
    if "title" in merged and "title" not in tone_override:
        merged["title"] = apply_tone_transform(tone, str(merged["title"]), "title")
    if "desc" in merged and "desc" not in tone_override:
        merged["desc"] = apply_tone_transform(tone, str(merged["desc"]), "desc")

    # 시맨틱 → 클래스 매핑
    text_dict = map_semantic_to_classes(template_id, merged)
    image_dict = map_semantic_images(template_id, semantic.images)

    # 빌드
    html = load_template(template_id)
    soup = BeautifulSoup(html, "html.parser")
    inline_css(soup)
    inject_palette(soup, palette)
    replace_images_by_class(soup, image_dict, output_dir)
    fix_absolute_image_paths(soup, semantic.images, output_dir)
    replace_text_by_class(soup, text_dict)

    out_name = f"{output_name}_{tone}_{palette}_{type_id}_{size_suffix}.html"
    out_path = output_dir / out_name
    out_path.write_text(str(soup), encoding="utf-8")
    return out_path


def build_v3_carousel(
    template_id: str,
    palette: str,
    tone: str,
    semantic: Any,
    output_dir: Path,
    output_name: str,
) -> list[Path]:
    """v3 캐러셀: 카드별로 분리해서 생성. items[] 데이터 활용."""
    from semantic_slots import map_semantic_to_classes, map_semantic_images, SEMANTIC_TEXT_SLOTS, SEMANTIC_IMAGE_SLOTS

    type_id, _ = parse_template_id(template_id)
    w, h = detect_template_size(template_id)
    size_suffix = f"{w}x{h}"

    # 카드별로 슬롯 매핑 (시맨틱 데이터를 카드 내용에 분배)
    paths = []
    html_full = load_template(template_id)
    soup_full = BeautifulSoup(html_full, "html.parser")
    n_cards = len(detect_cards(soup_full))

    if n_cards == 0:
        # 카드 없는 단일 템플릿 → 메시지처럼 처리
        return [build_v3_message(template_id, palette, tone, semantic, output_dir, output_name)]

    base_dict = to_semantic_dict(semantic)
    tone_override = (semantic.tone_overrides or {}).get(tone, {})
    merged_base = {**base_dict, **tone_override}
    items = semantic.items or []

    for i in range(n_cards):
        html = load_template(template_id)
        soup = BeautifulSoup(html, "html.parser")
        isolate_card(soup, i)
        inline_css(soup)
        inject_palette(soup, palette)

        # 카드 0 = cover/intro, 카드 1+ = product
        if i == 0:
            # 인트로 카드: title/sub/tag/date 같은 cover 슬롯 사용
            card_dict = {k: v for k, v in merged_base.items()
                        if k in ("title", "sub", "tag", "date", "label", "info")}
            card_images = {k: v for k, v in semantic.images.items()
                          if k in ("hero",)}
        else:
            # 제품 카드: items[] 에서 (i-1)번째 사용, 없으면 base 사용
            item_idx = i - 1
            if item_idx < len(items):
                item = items[item_idx]
                card_dict = {
                    "title": item.get("title", merged_base.get("title", "")),
                    "desc": item.get("desc", ""),
                    "category": item.get("category", merged_base.get("category", "")),
                    "badge": item.get("badge", ""),
                    "discount": item.get("discount", merged_base.get("discount", 0)),
                    "price": item.get("price", merged_base.get("price", 0)),
                    "orig": item.get("orig", merged_base.get("orig", 0)),
                    "product_title": item.get("title", ""),
                    "product_desc": item.get("desc", ""),
                    "product_discount": item.get("discount", 0),
                    "product_price": item.get("price", 0),
                    "product_orig": item.get("orig", 0),
                    "product_category": item.get("category", ""),
                    "product_badge": item.get("badge", ""),
                }
                card_images = {
                    "product": item.get("image", semantic.images.get("hero", "")),
                    "hero": item.get("image", semantic.images.get("hero", "")),
                }
            else:
                card_dict = merged_base
                card_images = semantic.images

        # 슬롯 매핑
        text_dict = map_semantic_to_classes(template_id, {**merged_base, **card_dict})
        image_dict = map_semantic_images(template_id, {**semantic.images, **card_images})

        # 다중 슬롯 (item1_, item2_, item3_, option_a, option_b 등)
        # 캐러셀 안에 여러 아이템이 들어가는 템플릿 (B-dual, C-triple, D-option)
        if items and i > 0:
            # 카드 내부에 N개 아이템 슬롯이 있는 경우 (B-dual은 2개, C-triple은 3개)
            for idx, item in enumerate(items[:3]):
                slot_prefix = f"item{idx+1}_"
                for k, v in item.items():
                    sem_key = f"{slot_prefix}{k}"
                    text_slots = SEMANTIC_TEXT_SLOTS.get(template_id, {})
                    if sem_key in text_slots:
                        text_dict[text_slots[sem_key]] = v
                # item image
                if "image" in item:
                    img_slots = SEMANTIC_IMAGE_SLOTS.get(template_id, {})
                    img_sem_key = f"item{idx+1}"
                    if img_sem_key in img_slots:
                        image_dict[img_slots[img_sem_key]] = item["image"]

        replace_images_by_class(soup, image_dict, output_dir)
        fix_absolute_image_paths(soup, semantic.images, output_dir)
        replace_text_by_class(soup, text_dict)

        out_name = f"{output_name}_{tone}_card{i+1:02d}_{type_id}_{size_suffix}.html"
        out_path = output_dir / out_name
        out_path.write_text(str(soup), encoding="utf-8")
        paths.append(out_path)

    return paths


def build_v3_live(
    template_id: str,
    palette: str,
    semantic: Any,
    output_dir: Path,
    output_name: str,
) -> list[Path]:
    """라이브 캐러셀 — 5카드 자동 분리 + 절대경로 alt 매칭."""
    type_id, _ = parse_template_id(template_id)
    w, h = detect_template_size(template_id)
    size_suffix = f"{w}x{h}"

    paths = []
    html_full = load_template(template_id)
    soup_full = BeautifulSoup(html_full, "html.parser")
    n_cards = len(detect_cards(soup_full))

    for i in range(n_cards):
        html = load_template(template_id)
        soup = BeautifulSoup(html, "html.parser")
        isolate_card(soup, i)
        inline_css(soup)
        inject_palette(soup, palette)
        # alt 텍스트 매칭으로 이미지 교체
        fix_absolute_image_paths(soup, semantic.images, output_dir)
        out_name = f"{output_name}_card{i+1:02d}_{type_id}_{size_suffix}.html"
        out_path = output_dir / out_name
        out_path.write_text(str(soup), encoding="utf-8")
        paths.append(out_path)

    return paths


def build_campaign_v3(campaign) -> dict:
    """v3 캠페인 빌드 — 레시피 기반."""
    from recipes import expand_recipe, get_recipe

    out_dir = OUTPUT_BASE / campaign.brand / campaign.campaign_slug
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {
        "output_dir": str(out_dir),
        "messages": [],
        "carousels": [],
        "errors": [],
        "recipes_applied": campaign.recipes,
    }

    print(f"\n📦 [v3] Building campaign: {campaign.campaign_slug}")
    print(f"📂 Output: {out_dir}")
    print(f"🍳 Recipes: {campaign.recipes}\n")

    for recipe_name in campaign.recipes:
        try:
            recipe = get_recipe(recipe_name)
        except KeyError as e:
            summary["errors"].append({"recipe": recipe_name, "error": str(e)})
            print(f"  ✗ {recipe_name}: {e}", file=sys.stderr)
            continue

        print(f"  🍳 {recipe_name}: {recipe['label']}")
        rtype = recipe["type"]

        if rtype == "messages":
            for tpl, palette, tone in recipe["variants"]:
                try:
                    path = build_v3_message(
                        tpl, palette, tone, campaign.data,
                        out_dir, output_name=campaign.campaign_slug + "_wide",
                    )
                    summary["messages"].append(str(path))
                    print(f"    ✓ {path.name}")
                except Exception as e:
                    summary["errors"].append({"variant": (tpl, palette, tone), "error": str(e)})
                    print(f"    ✗ {tpl} ({palette}/{tone}): {e}", file=sys.stderr)

        elif rtype == "carousels":
            for tpl, palette, label in recipe["variants"]:
                try:
                    paths = build_v3_carousel(
                        tpl, palette, "informational", campaign.data,
                        out_dir, output_name=f"{campaign.campaign_slug}_{tpl.split(':')[1]}",
                    )
                    summary["carousels"].append({"name": label, "cards": [str(p) for p in paths]})
                    for p in paths:
                        print(f"    ✓ {p.name}")
                except Exception as e:
                    summary["errors"].append({"variant": (tpl, palette, label), "error": str(e)})
                    print(f"    ✗ {tpl} ({palette}): {e}", file=sys.stderr)

        elif rtype == "live_carousel":
            # 힌트 기반으로 1개 D-live 템플릿 선택
            hint = (campaign.live_template_hint or "").lower()
            chosen = None
            for t in recipe["templates"]:
                if hint and hint in t.lower():
                    chosen = t
                    break
            if not chosen:
                chosen = recipe["templates"][0]
            print(f"    📺 Selected live template: {chosen}")

            # live_data를 SemanticData에 병합 (alt 매칭용 이미지)
            live_semantic = SemanticData(images=dict(campaign.live_data.get("images", {})))
            try:
                paths = build_v3_live(
                    chosen, "cool-summer", live_semantic,
                    out_dir, output_name=f"{campaign.campaign_slug}_live",
                )
                summary["carousels"].append({"name": "live", "cards": [str(p) for p in paths]})
                for p in paths:
                    print(f"    ✓ {p.name}")
            except Exception as e:
                summary["errors"].append({"recipe": recipe_name, "error": str(e)})
                print(f"    ✗ live: {e}", file=sys.stderr)

    # preview-grid (KakaoCampaign 호환 객체로 변환해 재사용)
    fake_campaign = KakaoCampaign(
        brand=campaign.brand,
        campaign_slug=campaign.campaign_slug,
        palette="warm-spring",
    )
    grid_path = generate_preview_grid(out_dir, fake_campaign)
    summary["preview_grid"] = str(grid_path)

    n_msg = len(summary["messages"])
    n_card = sum(len(c["cards"]) for c in summary["carousels"])
    print(f"\n총: {n_msg}개 메시지 + {n_card}개 캐러셀 카드")
    print(f"🌐 Preview: {grid_path}")
    if summary["errors"]:
        print(f"⚠️  에러 {len(summary['errors'])}건", file=sys.stderr)
    return summary


# ─── Config 로딩 ────────────────────────────────────────────────────────────
def load_config_from_path(config_path: Path):
    spec = importlib.util.spec_from_file_location("kakao_config", config_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load config: {config_path}")
    module = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(config_path.parent))
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.pop(0)
        sys.path.pop(0)
    if not hasattr(module, "CAMPAIGN"):
        raise AttributeError(f"Config 파일에 'CAMPAIGN' 변수가 없습니다: {config_path}")
    campaign = module.CAMPAIGN
    if not isinstance(campaign, (KakaoCampaign, CampaignV3)):
        raise TypeError(f"CAMPAIGN must be KakaoCampaign or CampaignV3, got {type(campaign)}")
    return campaign


# ─── CLI ────────────────────────────────────────────────────────────────────
def _cli():
    parser = argparse.ArgumentParser(description="카카오 메시지 빌드 (v2)")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_build = sub.add_parser("build", help="config 파일로 빌드")
    p_build.add_argument("config", help="config.py 파일 경로")

    sub.add_parser("list-templates", help="사용 가능한 템플릿 리스트")
    sub.add_parser("list-recipes", help="사용 가능한 레시피 리스트")

    p_inspect = sub.add_parser("inspect", help="템플릿 내 클래스/이미지 스캔")
    p_inspect.add_argument("template_id")

    args = parser.parse_args()

    if args.cmd == "build":
        config = load_config_from_path(Path(args.config).expanduser().resolve())
        if isinstance(config, CampaignV3):
            result = build_campaign_v3(config)
        else:
            result = build_campaign(config)
        return 1 if result["errors"] else 0

    if args.cmd == "list-recipes":
        from recipes import list_recipes
        for name, label in list_recipes():
            print(f"  {name}\n    {label}")
        return 0

    if args.cmd == "list-templates":
        for tid in list_templates():
            w, h = detect_template_size(tid)
            print(f"{tid}  ({w}×{h})")
        return 0

    if args.cmd == "inspect":
        html = load_template(args.template_id)
        soup = BeautifulSoup(html, "html.parser")
        w, h = detect_template_size(args.template_id)
        cards = detect_cards(soup)
        print(f"\n📋 {args.template_id}")
        print(f"   사이즈: {w}×{h}px")
        print(f"   카드 수: {len(cards)}장 (.{cards[0].get('class', ['?'])[0] if cards else '?'})")
        # km- 또는 kakao- 클래스
        classes = set()
        for el in soup.select("[class*='km-'], [class*='kakao-']"):
            for cls in el.get("class", []):
                if cls.startswith(("km-", "kakao-")):
                    classes.add(cls)
        if classes:
            print(f"\n   📝 텍스트 클래스 ({len(classes)}개):")
            for cls in sorted(classes):
                count = len(soup.select(f".{cls}"))
                print(f"     .{cls}  (×{count})")
        # 이미지 alt
        imgs = soup.find_all("img")
        if imgs:
            print(f"\n   🖼  이미지 ({len(imgs)}개):")
            for img in imgs:
                alt = img.get("alt", "(no alt)")
                cls = " ".join(img.get("class", []))
                src = img.get("src", "")[:60]
                print(f"     alt='{alt}' class='{cls}' src='{src}...'")
        return 0

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
