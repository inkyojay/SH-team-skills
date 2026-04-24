"""preview-grid.html 만 재생성 (개별 광고 HTML 건드리지 않음).

다운로드 버튼, 원본 이미지 갤러리 등 UI 업데이트 시 사용.

Usage:
    python3 rebuild_grids.py          # 전체 재생성
    python3 rebuild_grids.py --slug swaddle-strap   # 특정 제품만
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from meta_ad_builder import (
    PREVIEW_GRID_TEMPLATE,
    SIZES,
    AdSpec,
    CopySet,
    ProductConfig,
    _build_images_section,
    build_card_html,
)

# ── 모든 제품 config import ──────────────────────────────────────────────────
from products.all_products import ALL_PRODUCTS  # type: ignore
from products.event_ads import ALL_EVENTS        # type: ignore


def rebuild_grid(cfg: ProductConfig, output_dir: Path) -> int:
    """기존 previews/ 폴더의 HTML 파일 목록을 읽어 preview-grid.html 재생성."""
    previews = output_dir / "previews"
    if not previews.exists():
        print(f"  ⚠️  {output_dir.name}: previews/ 없음, 건너뜀")
        return 0

    # 기존 HTML 파일에서 AdSpec 정보 복원 (파일명 파싱)
    htmls = sorted(f for f in previews.glob("*.html") if f.name != "preview-grid.html")
    if not htmls:
        print(f"  ⚠️  {output_dir.name}: HTML 없음, 건너뜀")
        return 0

    cards_html = []
    for html in htmls:
        parts = html.stem.split("_")  # e.g. 01_hero-image_1080x1080_emotional
        if len(parts) < 4:
            continue
        idx = int(parts[0])
        layout = parts[1]
        size_key = parts[2]
        tone = parts[3]
        # 더미 AdSpec (카드 렌더용)
        dummy_copy = CopySet(tone=tone, headline="", subtext="", cta="")
        spec = AdSpec(idx=idx, layout=layout, size_key=size_key, copy=dummy_copy, image_key="")
        cards_html.append(build_card_html(spec, html.stem))

    images_section = _build_images_section(cfg)

    grid_html = PREVIEW_GRID_TEMPLATE.format(
        product=f"{cfg.brand_name_ko} {cfg.product_name}",
        brand=cfg.brand,
        category=cfg.category,
        primary=cfg.colors["primary"],
        total=len(htmls),
        cards="\n".join(cards_html),
        images_section=images_section,
    )
    (previews / "preview-grid.html").write_text(grid_html, encoding="utf-8")
    return len(htmls)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--slug", "-s", action="append", help="특정 제품 슬러그만 재생성")
    args = ap.parse_args()

    OUTPUT_BASE = Path.home() / "Desktop" / "team-skills" / "광고카피" / "sundayhug-meta-bulk"

    all_cfgs: list[ProductConfig] = list(ALL_PRODUCTS) + list(ALL_EVENTS)

    if args.slug:
        all_cfgs = [c for c in all_cfgs if c.product_slug in args.slug]
        if not all_cfgs:
            print(f"❌ 슬러그를 찾을 수 없습니다: {args.slug}")
            sys.exit(1)

    total = 0
    for cfg in all_cfgs:
        # 카테고리 폴더 탐색: ROOT/{category}/{slug}
        matches = list(OUTPUT_BASE.glob(f"*/{cfg.product_slug}"))
        if not matches:
            print(f"  ⚠️  폴더 없음: {cfg.product_slug}")
            continue
        out_dir = matches[0]
        n = rebuild_grid(cfg, out_dir)
        print(f"  ✓ {cfg.product_slug}: preview-grid.html 재생성 ({n}개 크리에이티브)")
        total += 1

    print(f"\n🎉 완료: {total}개 preview-grid.html 재생성")


if __name__ == "__main__":
    main()
