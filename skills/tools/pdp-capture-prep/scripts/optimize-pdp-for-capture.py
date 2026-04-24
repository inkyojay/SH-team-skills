#!/usr/bin/env python3
"""
pdp-capture-prep: SundayHug PDP HTML·CSS를 이미지 캡처 최적화 상태로 변환.

수행 작업 (idempotent — 여러 번 실행 안전):
  1. HTML 인라인 IntersectionObserver <script> 제거
  2. HTML 원격 Cafe24 CSS 참조 → 로컬 상대경로 치환
  3. CSS `.v` 리빌 규칙 제거 (@keyframes rise + .v opacity:0 + .v.on animation)
  4. CSS 1차(+2px) 폰트 상향 (데스크톱 override 블록 + 모바일 @media 값 업데이트)

사용법:
    python3 optimize-pdp-for-capture.py <project-root> [--dry-run]
"""
from __future__ import annotations
import argparse
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path


# ============================================================================
# Config
# ============================================================================

# Disqualifier keywords — scripts containing these are NOT treated as IO-only.
IO_SCRIPT_DISQUALIFIERS = (
    "setCarouselTrack", "jQuery", "addEventListener", "Swiper",
    "setTimeout", "setInterval", "fetch(", "XMLHttpRequest",
    "showFabric",  # sleepsack_silky_bamboo.html inline helper
)

# Remote CSS URL → local path resolution
REMOTE_CAFE24_CSS = "https://sundayhugkr.cafe24.com/skin-skin69/product/details/styles.css"

# 1차(+2px) font values for the overlay block inserted before @media queries
OVERLAY_BLOCK = """/* === 전체 뷰 1차(+2px) 통합 적용 — 데스크톱/태블릿/모바일 공통 === */
.pdp-absolute .sec-label,
.pdp-absolute .sec-eyebrow,
.pdp-absolute .hero-tag,
.pdp-absolute .hero-eyebrow,
.pdp-absolute .feat-num,
.pdp-absolute .badge-bar-sub,
.pdp-absolute .trust-bar-item small,
.pdp-absolute .detail-item-label,
.pdp-absolute .step-num,
.pdp-absolute .callout-label,
.pdp-absolute .notice-label,
.pdp-absolute .cmp-card-tag,
.pdp-absolute .compare-card-tag,
.pdp-absolute .fabric-card-temp {
  font-size: 16px;
}

.pdp-absolute .sec-desc,
.pdp-absolute .sec-body,
.pdp-absolute .feat-desc,
.pdp-absolute .sub-pt-tx,
.pdp-absolute .notice-text,
.pdp-absolute .callout-text,
.pdp-absolute .alert-box p,
.pdp-absolute .step-desc,
.pdp-absolute .feat-overlay-sub,
.pdp-absolute .mid-cta-sub {
  font-size: 19px;
}

.pdp-absolute .cmp-list,
.pdp-absolute .cmp-hd,
.pdp-absolute .product-info-tbl,
.pdp-absolute .trust-bar-item {
  font-size: 16px;
}

.pdp-absolute .mid-cta a {
  font-size: 15px;
}

.pdp-absolute .color-card-name {
  font-size: 12px;
}

"""

OVERLAY_MARKER = "전체 뷰 1차(+2px) 통합 적용"


# ============================================================================
# Result tracking
# ============================================================================

@dataclass
class FileReport:
    path: Path
    changes: list

    def summary(self) -> str:
        if not self.changes:
            return ""
        return f"  {self.path}  — " + ", ".join(self.changes)


# ============================================================================
# Operation 1: HTML — Strip IntersectionObserver scripts
# ============================================================================

SCRIPT_BLOCK_RE = re.compile(r"\n*<script>(.*?)</script>\n?", re.DOTALL)


def is_io_only_script(body: str) -> bool:
    """True if script body is *just* the .v scroll-reveal observer."""
    if "new IntersectionObserver" not in body:
        return False
    if "querySelectorAll('.v')" not in body:
        return False
    for bad in IO_SCRIPT_DISQUALIFIERS:
        if bad in body:
            return False
    return len(body) < 500


def strip_io_from_html(text: str) -> tuple[str, bool]:
    """Returns (new_text, changed)."""
    changed = False

    def repl(m):
        nonlocal changed
        if is_io_only_script(m.group(1)):
            changed = True
            return "\n"
        return m.group(0)

    new = SCRIPT_BLOCK_RE.sub(repl, text)
    # Also surgically remove IO blocks inside a mixed <script> (e.g., script that
    # contains BOTH IO setup AND showFabric function — strip only the IO lines).
    IO_INLINE_RE = re.compile(
        r"\n\s*(?://[^\n]*\n\s*)?const io\s*=\s*new IntersectionObserver\(es\s*=>\s*\{"
        r".*?"
        r"document\.querySelectorAll\('\.v'\)\.forEach\(el\s*=>\s*io\.observe\(el\)\);",
        re.DOTALL,
    )
    new2, n = IO_INLINE_RE.subn("", new)
    if n > 0:
        changed = True
    new2 = re.sub(r"\n{3,}", "\n\n", new2)
    return new2, changed


# ============================================================================
# Operation 2: HTML — Rewrite remote Cafe24 CSS reference
# ============================================================================

def rewrite_remote_css_ref(html_path: Path, text: str) -> tuple[str, bool]:
    """Replace remote Cafe24 CSS URL with a relative local path."""
    if REMOTE_CAFE24_CSS not in text:
        return text, False
    # Compute relative path from html file to the local CSS
    project_root = _find_project_root(html_path)
    if project_root is None:
        return text, False
    target_css = project_root / "product" / "details" / "styles.css"
    if not target_css.exists():
        return text, False
    rel = os.path.relpath(target_css, html_path.parent)
    return text.replace(REMOTE_CAFE24_CSS, rel), True


def _find_project_root(path: Path) -> Path | None:
    """Walk up until we find a directory that contains product/details/styles.css."""
    for p in [path] + list(path.parents):
        if (p / "product" / "details" / "styles.css").exists():
            return p
    return None


# ============================================================================
# Operation 3: CSS — Strip .v reveal rules
# ============================================================================

REVEAL_BLOCK_RE = re.compile(
    r"/\* ---------- Animations ---------- \*/\s*\n"
    r"@keyframes rise \{.*?\}\s*\n\s*"
    r"\.pdp-absolute \.v \{\s*opacity:\s*0\s*\}\s*\n\s*"
    r"\.pdp-absolute \.v\.on \{\s*animation:\s*rise[^}]*\}\s*",
    re.DOTALL,
)


def strip_reveal_from_css(text: str) -> tuple[str, bool]:
    """Remove the scroll-reveal block. Returns (new_text, changed)."""
    new, n = REVEAL_BLOCK_RE.subn("", text)
    return (new, n > 0)


# ============================================================================
# Operation 4a: CSS — Insert 1차 desktop override block
# ============================================================================

RESPONSIVE_HEADER_RE = re.compile(
    r"(/\* =+\s*\n\s*Responsive\s*\n\s*=+\s*\*/\s*\n@media\s*\(max-width:\s*767px\)\s*\{)",
    re.DOTALL,
)


def insert_desktop_overlay(text: str) -> tuple[str, bool]:
    """Insert the 1차 override block just before the Responsive @media section.
    Idempotent: skips if marker already present."""
    if OVERLAY_MARKER in text:
        return text, False
    m = RESPONSIVE_HEADER_RE.search(text)
    if not m:
        return text, False
    idx = m.start()
    return text[:idx] + OVERLAY_BLOCK + text[idx:], True


# ============================================================================
# Operation 4b: CSS — Update mobile @media values
# ============================================================================

# Match the entire mobile labels-block (15 selectors) and body-block (10 selectors)
# regardless of their current font-size value, then rewrite it to 1차.
MOBILE_LABEL_BLOCK_RE = re.compile(
    r"(  /\* ===[^\n]*===[^\n]*\*/\s*\n"           # === header comment (free-form)
    r"  /\*[^*]*라벨[^*]*\*/\s*\n"                 # "라벨류" comment
    r"  \.pdp-absolute \.sec-label,\s*\n"
    r"  \.pdp-absolute \.sec-eyebrow,\s*\n"
    r"  \.pdp-absolute \.hero-tag,\s*\n"
    r"  \.pdp-absolute \.hero-eyebrow,\s*\n"
    r"  \.pdp-absolute \.feat-num,\s*\n"
    r"  \.pdp-absolute \.badge-bar-sub,\s*\n"
    r"  \.pdp-absolute \.trust-bar-item small,\s*\n"
    r"  \.pdp-absolute \.detail-item-label,\s*\n"
    r"  \.pdp-absolute \.step-num,\s*\n"
    r"  \.pdp-absolute \.callout-label,\s*\n"
    r"  \.pdp-absolute \.notice-label,\s*\n"
    r"  \.pdp-absolute \.cmp-card-tag,\s*\n"
    r"  \.pdp-absolute \.compare-card-tag,\s*\n"
    r"  \.pdp-absolute \.fabric-card-temp \{\s*\n"
    r"    font-size:\s*)\d+(px;\s*\n  \})",
    re.DOTALL,
)

MOBILE_BODY_BLOCK_RE = re.compile(
    r"(  /\*[^*]*본문[^*]*\*/\s*\n"
    r"  \.pdp-absolute \.sec-desc,\s*\n"
    r"  \.pdp-absolute \.sec-body,\s*\n"
    r"  \.pdp-absolute \.feat-desc,\s*\n"
    r"  \.pdp-absolute \.sub-pt-tx,\s*\n"
    r"  \.pdp-absolute \.notice-text,\s*\n"
    r"  \.pdp-absolute \.callout-text,\s*\n"
    r"  \.pdp-absolute \.alert-box p,\s*\n"
    r"  \.pdp-absolute \.step-desc,\s*\n"
    r"  \.pdp-absolute \.feat-overlay-sub,\s*\n"
    r"  \.pdp-absolute \.mid-cta-sub \{\s*\n"
    r"    font-size:\s*)\d+(px;\s*\n  \})",
    re.DOTALL,
)

MOBILE_CMPLIST_RE = re.compile(
    r"(  \.pdp-absolute \.cmp-list \{\s*\n"
    r"    padding:[^\n]+\n"
    r"    font-size:\s*)\d+(px;\s*\n"
    r"    line-height:\s*)[\d.]+(;\s*\n  \})",
    re.DOTALL,
)

MOBILE_SIMPLE_SIZE_RES = [
    (re.compile(r"(\.pdp-absolute \.cmp-hd \{\s*\n    padding:[^\n]+\n    font-size:\s*)\d+(px;\s*\n  \})"),
     r"\g<1>16\g<2>"),
    (re.compile(r"(\.pdp-absolute \.product-info-tbl \{\s*\n    font-size:\s*)\d+(px;\s*\n  \})"),
     r"\g<1>16\g<2>"),
    (re.compile(
        r"(/\* 트러스트 바 살짝 압축 \*/\s*\n  \.pdp-absolute \.trust-bar-item \{\s*\n    font-size:\s*)\d+(px;\s*\n  \})"),
     r"\g<1>16\g<2>"),
]


def update_mobile_fonts(text: str) -> tuple[str, bool]:
    """Update mobile @media block to 1차 values."""
    changed = False
    new, n = MOBILE_LABEL_BLOCK_RE.subn(r"\g<1>16\g<2>", text)
    if n > 0 and new != text:
        changed = True; text = new
    new, n = MOBILE_BODY_BLOCK_RE.subn(r"\g<1>19\g<2>", text)
    if n > 0 and new != text:
        changed = True; text = new
    new, n = MOBILE_CMPLIST_RE.subn(r"\g<1>16\g<2>1.75\g<3>", text)
    if n > 0 and new != text:
        changed = True; text = new
    for rx, rep in MOBILE_SIMPLE_SIZE_RES:
        new, n = rx.subn(rep, text)
        if n > 0 and new != text:
            changed = True; text = new
    return text, changed


# ============================================================================
# Driver
# ============================================================================

def process_html(path: Path, dry_run: bool) -> FileReport:
    report = FileReport(path=path, changes=[])
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        report.changes.append(f"read-error: {e}")
        return report
    original = text

    text, io_changed = strip_io_from_html(text)
    if io_changed:
        report.changes.append("stripped-io-script")

    text, css_changed = rewrite_remote_css_ref(path, text)
    if css_changed:
        report.changes.append("localized-css-ref")

    if text != original and not dry_run:
        path.write_text(text, encoding="utf-8")
    return report


def process_css(path: Path, dry_run: bool) -> FileReport:
    report = FileReport(path=path, changes=[])
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        report.changes.append(f"read-error: {e}")
        return report
    original = text

    text, reveal_changed = strip_reveal_from_css(text)
    if reveal_changed:
        report.changes.append("stripped-reveal-rules")

    text, overlay_changed = insert_desktop_overlay(text)
    if overlay_changed:
        report.changes.append("inserted-desktop-overlay")

    text, mobile_changed = update_mobile_fonts(text)
    if mobile_changed:
        report.changes.append("updated-mobile-fonts")

    if text != original and not dry_run:
        path.write_text(text, encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("root", type=Path, help="Project root (folder containing the PDP HTML files)")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files")
    args = parser.parse_args()

    root: Path = args.root.expanduser().resolve()
    if not root.is_dir():
        sys.exit(f"Not a directory: {root}")

    # Collect all HTML containing .pdp-absolute wrapper
    html_files = []
    for p in root.rglob("*.html"):
        try:
            if 'class="pdp-absolute"' in p.read_text(encoding="utf-8", errors="ignore"):
                html_files.append(p)
        except Exception:
            continue

    # Collect all styles.css files that might use the @keyframes rise / mobile block patterns
    css_files = [p for p in root.rglob("styles.css")
                 if "node_modules" not in str(p) and ".git" not in str(p)]

    print(f"Scanning {len(html_files)} HTML files and {len(css_files)} CSS files")
    print(f"Mode: {'DRY RUN (no writes)' if args.dry_run else 'WRITE'}")
    print()

    html_reports = [process_html(p, args.dry_run) for p in html_files]
    css_reports = [process_css(p, args.dry_run) for p in css_files]

    changed_html = [r for r in html_reports if r.changes]
    changed_css = [r for r in css_reports if r.changes]

    print(f"HTML: {len(changed_html)} / {len(html_files)} files changed")
    for r in changed_html:
        print(r.summary())
    print()
    print(f"CSS:  {len(changed_css)} / {len(css_files)} files changed")
    for r in changed_css:
        print(r.summary())


if __name__ == "__main__":
    main()
