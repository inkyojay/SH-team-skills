#!/usr/bin/env python3
"""
pdp_parser.py — SundayHug PDP HTML 파싱

각 PDP HTML에서 제품 정보를 추출:
- 제품 정식명 (h1)
- 1줄 USP (.hero-sub or trust-bar)
- 소재 / 사이즈 / 컬러 (info-tbl / product-info-tbl)
- 카테고리 폴더
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit("[!] beautifulsoup4 필요: pip install beautifulsoup4")


@dataclass
class ProductInfo:
    slug: str
    category: str
    file_path: str
    title: str = ""
    sub_title: str = ""  # h1 두 번째 줄 (제품 정식명)
    usp_short: str = ""  # .hero-sub 또는 trust-bar 첫 줄
    material: str = ""
    color: str = ""
    size: str = ""
    kc_cert: str = ""
    manufacturer: str = ""
    extra_specs: dict[str, str] = field(default_factory=dict)
    parsing_warnings: list[str] = field(default_factory=list)
    # 본문 키워드 자료 (시드 도출용)
    sec_titles: list[str] = field(default_factory=list)        # <h2 class="sec-title|feat-title">
    highlights: list[str] = field(default_factory=list)        # <span class="hl"> ★ 가장 중요
    faq_questions: list[str] = field(default_factory=list)     # .faq-q
    section_comments: list[str] = field(default_factory=list)  # <!-- HERO --> <!-- FEAT 01 -->
    trust_items: list[str] = field(default_factory=list)       # .trust-bar-item 전체


def _clean(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def _extract_h1(soup: BeautifulSoup) -> tuple[str, str]:
    """h1 → (첫 줄, 두 번째 줄). 첫 줄이 슬로건, 두 번째가 제품명."""
    h1 = soup.find("h1")
    if not h1:
        return "", ""
    raw = h1.get_text(separator="|", strip=True)
    parts = [_clean(p) for p in raw.split("|") if _clean(p)]
    if len(parts) >= 2:
        return parts[0], parts[1]
    if len(parts) == 1:
        return "", parts[0]
    return "", ""


def _extract_usp(soup: BeautifulSoup) -> str:
    """1줄 USP — .hero-sub 우선, 없으면 trust-bar 첫 항목."""
    sub = soup.select_one(".hero-sub")
    if sub:
        return _clean(sub.get_text(separator=" "))
    trust = soup.select_one(".trust-bar .trust-bar-item")
    if trust:
        return _clean(trust.get_text(separator=" "))
    return ""


def _extract_specs(soup: BeautifulSoup) -> dict[str, str]:
    """info-tbl / product-info-tbl에서 모든 th-td 쌍 추출."""
    specs: dict[str, str] = {}
    for selector in ["table.product-info-tbl", "table.info-tbl"]:
        for tbl in soup.select(selector):
            for tr in tbl.select("tr"):
                th = tr.select_one("th")
                td = tr.select_one("td")
                if th and td:
                    k = _clean(th.get_text())
                    v = _clean(td.get_text())
                    if k and v:
                        specs[k] = v
    return specs


def _map_specs(specs: dict[str, str]) -> dict[str, str]:
    """한국어 라벨 → 표준 키 매핑."""
    mapping = {
        "material": ["소재", "재질", "원단", "구성"],
        "color": ["색상", "컬러", "color"],
        "size": ["사이즈", "크기", "치수", "규격"],
        "kc_cert": ["KC 인증", "인증", "안전인증"],
        "manufacturer": ["제조자", "제조사", "수입원"],
    }
    result: dict[str, str] = {}
    for std_key, labels in mapping.items():
        for label in labels:
            for k, v in specs.items():
                if label in k:
                    result[std_key] = v
                    break
            if std_key in result:
                break
    return result


def _extract_sec_titles(soup: BeautifulSoup) -> list[str]:
    """모든 <h2 class="sec-title"> + <h2 class="feat-title"> 추출 (제품 핵심 기능)."""
    out: list[str] = []
    for sel in ["h2.sec-title", "h2.feat-title", "h3.sec-title", "h3.feat-title"]:
        for el in soup.select(sel):
            txt = _clean(el.get_text(separator=" "))
            if txt and txt not in out:
                out.append(txt)
    return out


def _extract_highlights(soup: BeautifulSoup) -> list[str]:
    """<span class="hl"> 텍스트 — 팀이 직접 강조한 핵심 키워드 (★ 시드로 가장 가치)."""
    out: list[str] = []
    for el in soup.select(".hl, span.hl, em.hl"):
        txt = _clean(el.get_text(separator=" "))
        if txt and 2 <= len(txt) <= 30 and txt not in out:
            out.append(txt)
    return out


def _extract_faq_questions(soup: BeautifulSoup) -> list[str]:
    """FAQ 질문 — 실제 소비자 언어 (롱테일 키워드 후보)."""
    out: list[str] = []
    for el in soup.select(".faq-q, .faq-question, dt.faq"):
        txt = _clean(el.get_text(separator=" "))
        # "Q1." 같은 prefix 제거
        txt = re.sub(r"^Q\d+[\.\)]\s*", "", txt)
        if txt and txt not in out:
            out.append(txt)
    return out


def _extract_section_comments(html: str) -> list[str]:
    """<!-- HERO --> / <!-- FEAT 01 -- 차광률 --> 같은 주석 라벨."""
    pattern = re.compile(r"<!--\s*([^->]+?)\s*-->", re.DOTALL)
    raw = pattern.findall(html)
    out: list[str] = []
    for r in raw:
        # "FEAT 01 -- 차광률" → "차광률" 부분만
        if "--" in r:
            r = r.split("--", 1)[1].strip()
        r = r.strip()
        # 너무 긴 / 너무 짧은 주석 제외, 영문 only는 제외 (HERO, FAQ 등은 의미는 있지만 키워드는 아님)
        if r and 2 <= len(r) <= 40 and r not in out:
            # 영문만이면 스킵 (HERO, FAQ, INTRO 등)
            if not any("가" <= ch <= "힣" for ch in r):
                continue
            out.append(r)
    return out


def _extract_trust_items(soup: BeautifulSoup) -> list[str]:
    """모든 .trust-bar-item (3개 핵심 특징 전체)."""
    out: list[str] = []
    for el in soup.select(".trust-bar .trust-bar-item, .trust-bar-item"):
        # <small> 태그를 분리
        small = el.find("small")
        small_txt = _clean(small.get_text()) if small else ""
        # main text = 전체 - small
        full = _clean(el.get_text(separator=" "))
        if small_txt and full.endswith(small_txt):
            main = _clean(full[: -len(small_txt)])
        else:
            main = full
        if main:
            out.append(main)
        if small_txt:
            out.append(small_txt)
    return [t for t in out if t and 2 <= len(t) <= 30]


def parse_pdp(file_path: Path, root_dir: Path) -> ProductInfo:
    """단일 PDP HTML 파싱."""
    rel = file_path.relative_to(root_dir)
    parts = rel.parts
    category = parts[0] if len(parts) > 0 else "unknown"
    slug = file_path.stem

    info = ProductInfo(slug=slug, category=category, file_path=str(file_path))

    try:
        html = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        info.parsing_warnings.append(f"파일 읽기 실패: {e}")
        return info

    soup = BeautifulSoup(html, "html.parser")

    # H1 (제품명 + 슬로건)
    info.title, info.sub_title = _extract_h1(soup)
    if not info.sub_title and not info.title:
        info.parsing_warnings.append("h1 추출 실패")

    # USP
    info.usp_short = _extract_usp(soup)
    if not info.usp_short:
        info.parsing_warnings.append("USP 추출 실패")

    # Specs
    specs_raw = _extract_specs(soup)
    info.extra_specs = specs_raw
    mapped = _map_specs(specs_raw)
    info.material = mapped.get("material", "")
    info.color = mapped.get("color", "")
    info.size = mapped.get("size", "")
    info.kc_cert = mapped.get("kc_cert", "")
    info.manufacturer = mapped.get("manufacturer", "")

    if not info.material and not info.size:
        info.parsing_warnings.append("스펙 추출 실패 (info-tbl 없음 가능성)")

    # 본문 키워드 자료 (NEW)
    info.sec_titles = _extract_sec_titles(soup)
    info.highlights = _extract_highlights(soup)
    info.faq_questions = _extract_faq_questions(soup)
    info.section_comments = _extract_section_comments(html)
    info.trust_items = _extract_trust_items(soup)

    return info


def discover_pdps(root: Path) -> list[Path]:
    """PDP 폴더 안의 .html 파일 모두 (master/template 폴더 제외)."""
    skip_dirs = {"product", "details", "reference", ".git"}
    files = []
    for p in root.rglob("*.html"):
        if any(part in skip_dirs for part in p.parts):
            continue
        files.append(p)
    return sorted(files)


def parse_folder(root: Path) -> list[ProductInfo]:
    """폴더 전체 파싱 (dedup 전)."""
    files = discover_pdps(root)
    return [parse_pdp(f, root) for f in files]


def dedup_by_slug(products: list[ProductInfo]) -> list[ProductInfo]:
    """같은 슬러그가 여러 카테고리에 있으면 통합 (extra_specs에 다중 카테고리 표시)."""
    seen: dict[str, ProductInfo] = {}
    for p in products:
        if p.slug in seen:
            existing = seen[p.slug]
            cats = existing.extra_specs.get("__multi_categories__", existing.category)
            cats_set = set(cats.split(","))
            cats_set.add(p.category)
            existing.extra_specs["__multi_categories__"] = ",".join(sorted(cats_set))
            # 더 풍부한 정보를 가진 쪽 유지 (스펙 row 수 비교)
            if len(p.extra_specs) > len(existing.extra_specs):
                p.extra_specs["__multi_categories__"] = ",".join(sorted(cats_set))
                seen[p.slug] = p
        else:
            seen[p.slug] = p
    return list(seen.values())


if __name__ == "__main__":
    import sys, json
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Desktop/상세페이지 (절대경로)"
    products = parse_folder(root)
    print(f"Total HTML files: {len(products)}")
    deduped = dedup_by_slug(products)
    print(f"Unique slugs:     {len(deduped)}")
    print()
    for p in deduped[:5]:
        print(json.dumps(asdict(p), ensure_ascii=False, indent=2))
