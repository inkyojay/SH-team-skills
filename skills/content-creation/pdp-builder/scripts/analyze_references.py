#!/usr/bin/env python3
"""
analyze_references.py — 타사 레퍼런스 (URL/이미지/텍스트) 분석기

Usage:
    python3 analyze_references.py --input refs.json --output references.json

Input JSON 구조:
{
  "references": [
    {"type": "url",   "value": "https://smartstore.naver.com/..."},
    {"type": "url",   "value": "https://www.coupang.com/..."},
    {"type": "social","value": "https://www.instagram.com/p/..."},
    {"type": "image", "value": "/path/to/competitor-pdp-screenshot.png"},
    {"type": "text",  "value": "이 제품은 ... 라는 컨셉으로 ..."}
  ]
}

Output JSON: 통합된 references[].title/price/sections/copy_phrases/visual_notes
이미지 분석은 Claude Code(상위 호출자)가 Read 툴로 처리해야 한다.
이 스크립트는 URL/social/text만 직접 처리하고, image는 placeholder를 남긴다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print(
        "[!] requests + beautifulsoup4 필요: pip install requests beautifulsoup4",
        file=sys.stderr,
    )
    sys.exit(1)


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8",
}


def fetch(url: str, timeout: int = 15) -> str | None:
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"[!] fetch failed: {url} — {e}", file=sys.stderr)
        return None


def parse_meta(soup: BeautifulSoup) -> dict[str, str]:
    """OG / Twitter / 일반 meta 태그 통합 추출."""
    out: dict[str, str] = {}
    for tag in soup.find_all("meta"):
        prop = tag.get("property") or tag.get("name") or ""
        content = tag.get("content") or ""
        if not content:
            continue
        if prop in {"og:title", "twitter:title"}:
            out.setdefault("title", content)
        elif prop in {"og:description", "twitter:description", "description"}:
            out.setdefault("description", content)
        elif prop in {"og:image", "twitter:image"}:
            out.setdefault("image", content)
        elif prop == "og:price:amount":
            out.setdefault("price", content)
    if "title" not in out and soup.title:
        out["title"] = soup.title.get_text(strip=True)
    return out


PRICE_RE = re.compile(r"([0-9]{1,3}(?:,[0-9]{3})+|[0-9]{4,})\s*원")


def extract_price(text: str) -> str | None:
    m = PRICE_RE.search(text)
    return m.group(0) if m else None


def detect_platform(url: str) -> str:
    host = urlparse(url).hostname or ""
    if "smartstore.naver" in host or "shopping.naver" in host:
        return "naver_smartstore"
    if "coupang" in host:
        return "coupang"
    if "11st" in host:
        return "11st"
    if "gmarket" in host:
        return "gmarket"
    if "instagram" in host:
        return "instagram"
    if "facebook" in host or "fb.com" in host:
        return "facebook"
    if "youtube" in host or "youtu.be" in host:
        return "youtube"
    if "tiktok" in host:
        return "tiktok"
    if "cafe24" in host or "imweb" in host or "shopify" in host:
        return "self_store"
    return "generic"


def analyze_url(url: str) -> dict[str, Any]:
    html = fetch(url)
    if not html:
        return {
            "type": "url",
            "value": url,
            "platform": detect_platform(url),
            "error": "fetch_failed",
            "hint": "로그인 필요 가능. 캡처 이미지로 다시 제공하세요.",
        }
    soup = BeautifulSoup(html, "html.parser")
    meta = parse_meta(soup)
    body_text = soup.get_text(" ", strip=True)[:8000]

    # 카피 후보 — h1~h3 + strong 태그 텍스트
    copy_phrases = []
    for tag_name in ("h1", "h2", "h3", "strong"):
        for el in soup.find_all(tag_name):
            txt = el.get_text(" ", strip=True)
            if 4 <= len(txt) <= 60:
                copy_phrases.append(txt)
    copy_phrases = list(dict.fromkeys(copy_phrases))[:30]

    return {
        "type": "url",
        "value": url,
        "platform": detect_platform(url),
        "title": meta.get("title", ""),
        "description": meta.get("description", ""),
        "thumbnail": meta.get("image", ""),
        "price": meta.get("price") or extract_price(body_text) or "",
        "copy_phrases": copy_phrases,
        "raw_text_excerpt": body_text[:1500],
    }


def analyze_social(url: str) -> dict[str, Any]:
    """인스타/페북/유튜브 — og 메타만 (로그인 우회 X)."""
    html = fetch(url)
    out: dict[str, Any] = {
        "type": "social",
        "value": url,
        "platform": detect_platform(url),
    }
    if not html:
        out["error"] = "fetch_failed"
        out["hint"] = "공개 게시물만 og:meta 추출 가능. 비공개면 캡처로 제공."
        return out
    soup = BeautifulSoup(html, "html.parser")
    out.update(parse_meta(soup))
    return out


def analyze_image(path: str) -> dict[str, Any]:
    """이미지는 직접 파싱하지 않는다 — 상위 호출자(Claude)가 Vision으로 본다."""
    p = Path(path).expanduser()
    return {
        "type": "image",
        "value": str(p),
        "exists": p.exists(),
        "hint": "Claude Code가 Read 툴로 직접 분석할 것. 이 항목은 placeholder.",
    }


def analyze_text(text: str) -> dict[str, Any]:
    return {
        "type": "text",
        "value": text,
        "copy_phrases": [s.strip() for s in re.split(r"[\n。.!?]", text) if 4 <= len(s.strip()) <= 80][:20],
    }


def run(input_path: str, output_path: str) -> None:
    with open(input_path, encoding="utf-8") as f:
        data = json.load(f)

    out_refs = []
    for ref in data.get("references", []):
        kind = ref.get("type")
        value = ref.get("value", "")
        if kind == "url":
            out_refs.append(analyze_url(value))
        elif kind == "social":
            out_refs.append(analyze_social(value))
        elif kind == "image":
            out_refs.append(analyze_image(value))
        elif kind == "text":
            out_refs.append(analyze_text(value))
        else:
            out_refs.append({"type": "unknown", "value": value, "error": "unknown_type"})

    out_path = Path(output_path).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump({"references": out_refs}, f, ensure_ascii=False, indent=2)
    print(f"[OK] analyzed {len(out_refs)} reference(s) → {out_path}")


def main() -> None:
    ap = argparse.ArgumentParser(description="레퍼런스 분석기")
    ap.add_argument("--input", "-i", required=True, help="입력 JSON 경로")
    ap.add_argument("--output", "-o", required=True, help="출력 JSON 경로")
    args = ap.parse_args()
    run(args.input, args.output)


if __name__ == "__main__":
    main()
