"""
sync_templates.py — Synology 카카오 템플릿을 로컬 캐시로 동기화

Synology Drive 동기화가 끊긴 PC에서도 빌드 가능하도록
스킬 폴더에 .template-cache/ 를 유지한다.

사용:
    python3 sync_templates.py            # 변경된 파일만 갱신 (mtime 비교)
    python3 sync_templates.py --force    # 전체 강제 복사
    python3 sync_templates.py --status   # 동기화 상태만 출력

환경변수:
    KAKAO_TEMPLATE_DIR  — Synology 경로 오버라이드 (기본값: 아래 DEFAULT_SYNO_DIR)
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# ─── 경로 설정 ──────────────────────────────────────────────────────────────
DEFAULT_SYNO_DIR = Path(
    "/Users/inkyo/Library/CloudStorage/SynologyDrive-contents"
    "/스킬/sundayhug-brand/templates/promotion/kakao-messages"
)
SCRIPT_DIR = Path(__file__).resolve().parent
CACHE_DIR = SCRIPT_DIR / ".template-cache"

# 부모 디렉토리의 _global-palettes.css도 함께 복사 (12 팔레트 정의)
GLOBAL_PALETTES_REL = Path("../_global-palettes.css")  # promotion/_global-palettes.css

# 복사 대상 파일 패턴
INCLUDE_FILES = [
    "GUIDE.md",
    "_base-styles.css",
    "_palettes.css",
    "_guide-chrome.css",
    "template-guide.html",
]
INCLUDE_DIRS = ["types"]


def get_source_dir() -> Path:
    """환경변수 우선, 없으면 기본 Synology 경로."""
    override = os.environ.get("KAKAO_TEMPLATE_DIR")
    if override:
        return Path(override)
    return DEFAULT_SYNO_DIR


def needs_update(src: Path, dst: Path) -> bool:
    """mtime 비교로 갱신 필요 여부 판단."""
    if not dst.exists():
        return True
    return src.stat().st_mtime > dst.stat().st_mtime


def copy_file(src: Path, dst: Path, force: bool = False) -> str:
    """단일 파일 복사. 반환값: 'copied' | 'skipped' | 'missing'."""
    if not src.exists():
        return "missing"
    if not force and not needs_update(src, dst):
        return "skipped"
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return "copied"


def copy_dir(src_dir: Path, dst_dir: Path, force: bool = False) -> dict[str, int]:
    """디렉토리 재귀 복사. 카운트 dict 반환."""
    counts = {"copied": 0, "skipped": 0, "missing": 0}
    if not src_dir.exists():
        counts["missing"] += 1
        return counts
    for src in src_dir.rglob("*"):
        if src.is_dir():
            continue
        rel = src.relative_to(src_dir)
        dst = dst_dir / rel
        result = copy_file(src, dst, force=force)
        counts[result] += 1
    return counts


def sync(force: bool = False, status_only: bool = False) -> int:
    """전체 동기화 실행. 반환값: exit code."""
    src_dir = get_source_dir()

    print(f"📂 Source: {src_dir}")
    print(f"📦 Cache:  {CACHE_DIR}")

    if not src_dir.exists():
        print(f"❌ Source directory not found: {src_dir}", file=sys.stderr)
        print("   Synology Drive가 연결되어 있는지, 경로가 맞는지 확인하세요.", file=sys.stderr)
        print("   환경변수 KAKAO_TEMPLATE_DIR로 경로를 오버라이드할 수 있습니다.", file=sys.stderr)
        return 1

    if status_only:
        cache_exists = CACHE_DIR.exists()
        types_count = len(list((CACHE_DIR / "types").glob("*"))) if cache_exists else 0
        print(f"\n캐시 존재: {'YES' if cache_exists else 'NO'}")
        print(f"types 하위 폴더 수: {types_count}")
        return 0

    total = {"copied": 0, "skipped": 0, "missing": 0}

    # 1. 단일 파일들
    for fname in INCLUDE_FILES:
        src = src_dir / fname
        dst = CACHE_DIR / fname
        result = copy_file(src, dst, force=force)
        total[result] += 1
        symbol = {"copied": "✓", "skipped": "·", "missing": "✗"}[result]
        print(f"  {symbol} {fname}")

    # 2. 부모의 _global-palettes.css
    global_src = (src_dir / GLOBAL_PALETTES_REL).resolve()
    global_dst = CACHE_DIR / "_global-palettes.css"
    result = copy_file(global_src, global_dst, force=force)
    total[result] += 1
    symbol = {"copied": "✓", "skipped": "·", "missing": "✗"}[result]
    print(f"  {symbol} _global-palettes.css (from parent)")

    # 3. types/ 디렉토리
    for dname in INCLUDE_DIRS:
        src_sub = src_dir / dname
        dst_sub = CACHE_DIR / dname
        counts = copy_dir(src_sub, dst_sub, force=force)
        for k in total:
            total[k] += counts[k]
        print(
            f"  📁 {dname}/  copied={counts['copied']} "
            f"skipped={counts['skipped']} missing={counts['missing']}"
        )

    print(
        f"\n총: copied={total['copied']}  skipped={total['skipped']}  missing={total['missing']}"
    )

    if total["missing"] > 0:
        print("⚠️  일부 파일을 찾지 못했습니다. Synology 동기화 상태를 확인하세요.", file=sys.stderr)
        return 2

    print("✅ 동기화 완료")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Synology 카카오 템플릿 → 로컬 캐시 동기화"
    )
    parser.add_argument("--force", action="store_true", help="전체 강제 복사")
    parser.add_argument(
        "--status", action="store_true", help="동기화 상태만 출력 (복사 X)"
    )
    args = parser.parse_args()
    return sync(force=args.force, status_only=args.status)


if __name__ == "__main__":
    sys.exit(main())
