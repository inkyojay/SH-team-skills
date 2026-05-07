#!/usr/bin/env python3
"""
to_jpg.py — PDP 섹션 PNG 폴더 → 고해상도 JPG 일괄 변환

핵심 옵션 (글자 보존):
  - quality=95 (거의 무손실)
  - subsampling=0 (4:4:4 — 글자 색번짐 X)
  - optimize=True + progressive=True (점진 로딩)
  - 해상도 그대로 유지 (1800px 등)
  - 한도 초과 시 자동으로 quality 92로 fallback

Usage:
  # 단일 폴더
  python3 to_jpg.py "/path/to/{product}_sections"

  # 여러 폴더 (병렬)
  python3 to_jpg.py --bulk "/path/to/parent" --pattern "*_sections"

  # 한도 변경
  python3 to_jpg.py "/path/.../product_sections" --limit-mb 19

출력:
  /path/to/{product}_sections/jpg/*.jpg     ← 새 폴더에 모두
  PNG 원본은 그대로 보존 (사용자가 수동 정리)
"""

from __future__ import annotations

import argparse
import os
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("[!] Pillow 필요: pip install Pillow")


DEFAULT_LIMIT_MB = 19.0
DEFAULT_QUALITY = 95
SUBSAMPLING_444 = 0  # 4:4:4 — 글자 색 보간 안 함


def convert_one_png(
    src: Path,
    dst: Path,
    quality: int = DEFAULT_QUALITY,
    limit_mb: float = DEFAULT_LIMIT_MB,
) -> dict:
    """단일 PNG → JPG."""
    orig_size = src.stat().st_size

    img = Image.open(src)

    # 알파 채널 처리 (흰 배경 합성)
    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        if img.mode == "P":
            img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None)
        img_rgb = bg
    else:
        img_rgb = img.convert("RGB")

    dst.parent.mkdir(parents=True, exist_ok=True)

    # 시도 1: 지정 품질 + 4:4:4
    img_rgb.save(
        dst,
        "JPEG",
        quality=quality,
        subsampling=SUBSAMPLING_444,
        optimize=True,
        progressive=True,
    )
    new_size = dst.stat().st_size

    # 한도 초과 → q=92로 한 번 더
    if new_size / 1048576 > limit_mb:
        img_rgb.save(
            dst,
            "JPEG",
            quality=92,
            subsampling=SUBSAMPLING_444,
            optimize=True,
            progressive=True,
        )
        new_size = dst.stat().st_size
        # 그래도 한도 초과 → 1500px 리사이즈
        if new_size / 1048576 > limit_mb:
            w, h = img_rgb.size
            ratio = 1500 / w
            new_dim = (1500, int(h * ratio))
            img_resized = img_rgb.resize(new_dim, Image.LANCZOS)
            img_resized.save(
                dst,
                "JPEG",
                quality=92,
                subsampling=SUBSAMPLING_444,
                optimize=True,
                progressive=True,
            )
            new_size = dst.stat().st_size

    return {
        "src": str(src),
        "dst": str(dst),
        "orig_mb": orig_size / 1048576,
        "new_mb": new_size / 1048576,
        "ratio": orig_size / max(new_size, 1),
        "ok": new_size / 1048576 <= limit_mb,
    }


def convert_folder(
    folder: Path,
    quality: int = DEFAULT_QUALITY,
    limit_mb: float = DEFAULT_LIMIT_MB,
) -> dict:
    """단일 _sections 폴더 → jpg/ 서브폴더에 모든 PNG 변환."""
    if not folder.is_dir():
        return {"folder": str(folder), "error": "폴더 없음", "results": []}

    pngs = sorted(folder.glob("*.png"))
    if not pngs:
        return {"folder": str(folder), "skipped": "PNG 없음", "results": []}

    jpg_dir = folder / "jpg"
    jpg_dir.mkdir(exist_ok=True)

    results = []
    for p in pngs:
        out = jpg_dir / (p.stem + ".jpg")
        try:
            r = convert_one_png(p, out, quality=quality, limit_mb=limit_mb)
            results.append(r)
        except Exception as e:
            results.append({"src": str(p), "error": str(e)})

    total_orig = sum(r.get("orig_mb", 0) for r in results)
    total_new = sum(r.get("new_mb", 0) for r in results)
    over_limit = [r for r in results if not r.get("ok", True)]

    return {
        "folder": str(folder),
        "count": len(pngs),
        "total_orig_mb": total_orig,
        "total_new_mb": total_new,
        "ratio": total_orig / max(total_new, 0.001),
        "over_limit": len(over_limit),
        "results": results,
    }


def _worker(args):
    folder, quality, limit_mb = args
    return convert_folder(Path(folder), quality=quality, limit_mb=limit_mb)


def convert_bulk(
    parent: Path,
    pattern: str = "*_sections",
    workers: int = 4,
    quality: int = DEFAULT_QUALITY,
    limit_mb: float = DEFAULT_LIMIT_MB,
) -> list[dict]:
    """여러 _sections 폴더를 병렬 처리."""
    folders = [p for p in parent.rglob(pattern) if p.is_dir()]
    if not folders:
        print(f"[!] '{parent}' 안에서 '{pattern}' 폴더를 찾지 못했습니다.")
        return []

    print(f"📁 발견된 폴더: {len(folders)}개")
    print(f"⚙️  설정: quality={quality}, limit={limit_mb}MB, workers={workers}")
    print("=" * 80)

    args = [(str(f), quality, limit_mb) for f in folders]
    results: list[dict] = []
    with ProcessPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(_worker, a): a[0] for a in args}
        for i, fut in enumerate(as_completed(futures), 1):
            r = fut.result()
            results.append(r)
            folder_name = Path(r["folder"]).name
            cnt = r.get("count", 0)
            orig = r.get("total_orig_mb", 0)
            new = r.get("total_new_mb", 0)
            over = r.get("over_limit", 0)
            flag = "⚠️ " if over else "✅"
            print(
                f"  [{i:>3}/{len(folders)}] {flag} {folder_name:<40} "
                f"{cnt:>2}개  {orig:>6.1f}MB → {new:>5.1f}MB  ({orig/max(new,0.001):>4.1f}x)"
            )

    print("=" * 80)
    total_orig = sum(r.get("total_orig_mb", 0) for r in results)
    total_new = sum(r.get("total_new_mb", 0) for r in results)
    total_files = sum(r.get("count", 0) for r in results)
    total_over = sum(r.get("over_limit", 0) for r in results)
    print(f"전체: {len(folders)}개 폴더 / {total_files}개 PNG")
    print(f"  원본 합계:  {total_orig:>7.1f} MB")
    print(f"  변환본 합계: {total_new:>7.1f} MB")
    print(f"  전체 압축율: {total_orig/max(total_new,0.001):.1f}x")
    if total_over:
        print(f"  ⚠️  한도 초과 (1500px 리사이즈로 처리): {total_over}개")
    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="PDP 섹션 PNG → 고해상도 JPG 변환")
    ap.add_argument("path", nargs="?", help="단일 폴더 또는 부모 폴더 (--bulk와 함께)")
    ap.add_argument("--bulk", action="store_true", help="하위의 *_sections 폴더 모두 일괄 처리")
    ap.add_argument("--pattern", default="*_sections", help="bulk 모드 폴더 패턴 (default: *_sections)")
    ap.add_argument("--workers", type=int, default=4, help="bulk 병렬 워커 수 (default: 4)")
    ap.add_argument("--quality", type=int, default=DEFAULT_QUALITY, help="JPEG 품질 (default: 95)")
    ap.add_argument("--limit-mb", type=float, default=DEFAULT_LIMIT_MB, help="파일당 최대 MB (default: 19)")
    args = ap.parse_args()

    if not args.path:
        ap.print_help()
        sys.exit(1)

    target = Path(args.path).expanduser()

    if args.bulk:
        if not target.is_dir():
            print(f"[!] 부모 폴더가 아닙니다: {target}")
            sys.exit(1)
        convert_bulk(
            target,
            pattern=args.pattern,
            workers=args.workers,
            quality=args.quality,
            limit_mb=args.limit_mb,
        )
    else:
        result = convert_folder(target, quality=args.quality, limit_mb=args.limit_mb)
        if result.get("error"):
            print(f"[!] {result['error']}: {result['folder']}")
            sys.exit(1)
        if result.get("skipped"):
            print(f"[skip] {result['skipped']}: {result['folder']}")
            return
        cnt = result["count"]
        orig = result["total_orig_mb"]
        new = result["total_new_mb"]
        print(f"📁 {result['folder']}")
        print(f"   {cnt}개 PNG → JPG ({orig:.1f}MB → {new:.1f}MB, {orig/max(new,0.001):.1f}x)")
        print(f"   📂 출력: {Path(result['folder']) / 'jpg'}")


if __name__ == "__main__":
    main()
