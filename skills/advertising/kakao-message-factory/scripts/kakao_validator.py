"""
kakao_validator.py — 카카오 메시지 빌드/PNG 검증 모듈

검증 항목:
1. 알림톡 카피 광고 키워드 검열
2. 캐러셀 카드 사이즈 일관성
3. PNG 용량 한도 (알림톡 500KB / 친구톡 2MB)
4. 한도 초과 시 Pillow quality 단계적 압축

CLI 사용:
    python3 kakao_validator.py check-copy "지금 50% 할인"
    python3 kakao_validator.py check-size path/to/png 800 400
    python3 kakao_validator.py compress path/to/png 500
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Iterable

# ─── 알림톡 광고성 카피 차단 키워드 ─────────────────────────────────────────
BANNED_WORDS_NOTIFICATION = [
    # 할인/세일
    "할인", "%", "퍼센트", "특가", "세일", "SALE", "최저가", "반값",
    "공짜", "무료증정", "사은품",
    # 프로모션
    "프로모션", "이벤트", "EVENT", "쿠폰", "적립금", "포인트 적립",
    "선착순", "한정", "한정수량", "한정판매", "마감임박",
    # 광고 유도
    "지금 구매", "지금 주문", "오늘만", "오늘까지", "단 하루",
    "놓치지마", "절호의 기회", "역대급", "역대 최저",
    # 이모지 (광고성 분류 위험)
    "★", "♥", "❤", "💝", "🎁", "🔥", "⭐",
]

# ─── 카카오 캔버스 사이즈 정의 ──────────────────────────────────────────────
EXPECTED_SIZES = {
    "01-image": [(800, 400), (800, 800), (800, 1200)],  # 비율 가변
    "02-wide-image": [(800, 600)],
    "03-wide-list-header": [(800, 400)],
    "03-wide-list-item": [(800, 800)],
    "04-carousel-feed": [(800, 600), (800, 400)],  # 카드 간 통일 필요
    "05-carousel-commerce": [(800, 800)],
    "06-commerce": [(800, 600)],
    "07-alimtalk-image": [(800, 400)],
    "bizboard": [(1029, 258)],
}

# ─── 용량 한도 (KB) ─────────────────────────────────────────────────────────
SIZE_LIMITS_KB = {
    "alimtalk": 500,        # 07, 08
    "friendtalk": 2048,     # 01~06
    "bizboard": 300,
}

# ============================================================================
# 1. 알림톡 카피 검열
# ============================================================================


def validate_copy_for_notification(text: str) -> list[str]:
    """알림톡 카피에서 금지 키워드 검출. 검출된 키워드 리스트 반환 (빈 리스트 = OK)."""
    found = []
    for word in BANNED_WORDS_NOTIFICATION:
        if word in text:
            found.append(word)
    return found


def check_alimtalk_safe(texts: dict[str, str], strict: bool = True) -> tuple[bool, dict[str, list[str]]]:
    """알림톡 전체 텍스트 dict 검사. (안전 여부, 위반 dict) 반환."""
    violations = {}
    for key, val in texts.items():
        if not val:
            continue
        found = validate_copy_for_notification(str(val))
        if found:
            violations[key] = found
    safe = len(violations) == 0
    if not safe and strict:
        return False, violations
    return safe, violations


# ============================================================================
# 2. 캐러셀 카드 일관성 검증
# ============================================================================


def get_image_size(png_path: Path) -> tuple[int, int] | None:
    """PNG 사이즈 읽기 (Pillow)."""
    try:
        from PIL import Image
    except ImportError:
        print("⚠️  Pillow 미설치 — pip install Pillow", file=sys.stderr)
        return None
    if not png_path.exists():
        return None
    with Image.open(png_path) as im:
        return im.size


def validate_carousel_uniformity(card_paths: Iterable[Path]) -> tuple[bool, str]:
    """캐러셀 카드들이 모두 같은 사이즈인지 검증."""
    paths = list(card_paths)
    if len(paths) < 2:
        return False, f"카드 수가 부족합니다 ({len(paths)}장, 최소 2장 필요)"
    if len(paths) > 7:
        return False, f"카드 수 초과 ({len(paths)}장, 최대 7장)"

    sizes = []
    for p in paths:
        size = get_image_size(p)
        if size is None:
            return False, f"파일 읽기 실패: {p}"
        sizes.append(size)

    first = sizes[0]
    for i, sz in enumerate(sizes):
        if sz != first:
            return False, f"카드 {i+1} 사이즈 불일치: {sz} vs 카드1 {first}"
    return True, f"OK — 모두 {first[0]}×{first[1]}, {len(paths)}장"


# ============================================================================
# 3. PNG 용량 검증 + 자동 압축
# ============================================================================


def get_filesize_kb(path: Path) -> float:
    """파일 크기 KB."""
    return path.stat().st_size / 1024


def validate_filesize(png_path: Path, max_kb: int) -> tuple[bool, float]:
    """용량 검증. (통과 여부, 실제 KB) 반환."""
    if not png_path.exists():
        return False, 0.0
    actual = get_filesize_kb(png_path)
    return actual <= max_kb, actual


def compress_to_target(
    png_path: Path,
    target_kb: int,
    qualities: tuple[int, ...] = (95, 85, 75, 65),
) -> tuple[bool, float, int | None]:
    """
    PNG를 target_kb 이하로 압축.
    PIL Image quality 단계적 하향 (PNG는 quality 무의미하므로 JPEG 변환 후 다시 PNG로 재저장 X
    → 대신 PNG optimize=True + 256색 quantize로 최적화).

    반환: (성공 여부, 최종 KB, 사용된 quality 또는 None)
    """
    try:
        from PIL import Image
    except ImportError:
        return False, get_filesize_kb(png_path), None

    if not png_path.exists():
        return False, 0.0, None

    # 1차: 그대로 검사
    actual = get_filesize_kb(png_path)
    if actual <= target_kb:
        return True, actual, None

    # 2차: PNG optimize 재저장
    with Image.open(png_path) as im:
        im.save(png_path, format="PNG", optimize=True)
    actual = get_filesize_kb(png_path)
    if actual <= target_kb:
        return True, actual, 100

    # 3차: 256색 quantize (PNG-8)
    with Image.open(png_path) as im:
        if im.mode != "RGBA":
            im = im.convert("RGBA")
        # alpha 보존하며 quantize
        quantized = im.quantize(colors=256, method=Image.Quantize.LIBIMAGEQUANT if hasattr(Image.Quantize, "LIBIMAGEQUANT") else Image.Quantize.MEDIANCUT)
        quantized.save(png_path, format="PNG", optimize=True)
    actual = get_filesize_kb(png_path)
    if actual <= target_kb:
        return True, actual, 256

    # 4차: JPEG로 변환 후 PNG 재저장 (quality 단계 하향, 알파 손실)
    for q in qualities:
        with Image.open(png_path) as im:
            if im.mode == "RGBA":
                # 알파 → 흰색 배경 합성
                bg = Image.new("RGB", im.size, (255, 255, 255))
                bg.paste(im, mask=im.split()[3] if len(im.split()) == 4 else None)
                rgb = bg
            else:
                rgb = im.convert("RGB")
        # 임시 jpg 만든 뒤 다시 PNG로 저장 (확장자는 png 유지)
        tmp_jpg = png_path.with_suffix(".tmp.jpg")
        rgb.save(tmp_jpg, format="JPEG", quality=q, optimize=True)
        with Image.open(tmp_jpg) as im2:
            im2.save(png_path, format="PNG", optimize=True)
        tmp_jpg.unlink(missing_ok=True)
        actual = get_filesize_kb(png_path)
        if actual <= target_kb:
            return True, actual, q

    return False, actual, qualities[-1]


# ============================================================================
# 4. 사이즈 정확성 검증
# ============================================================================


def validate_size(png_path: Path, expected_w: int, expected_h: int) -> tuple[bool, str]:
    """PNG가 정확한 사이즈인지 검증."""
    actual = get_image_size(png_path)
    if actual is None:
        return False, "파일 읽기 실패"
    if actual == (expected_w, expected_h):
        return True, f"OK — {expected_w}×{expected_h}"
    return False, f"불일치 — 실제 {actual[0]}×{actual[1]}, 기대 {expected_w}×{expected_h}"


# ============================================================================
# 5. 원본 이미지 해상도 검증
# ============================================================================


def validate_source_resolution(image_path: Path, min_width: int = 1600) -> tuple[bool, int]:
    """원본 이미지가 supersampling 가능한 해상도인지 검증."""
    size = get_image_size(image_path)
    if size is None:
        return False, 0
    return size[0] >= min_width, size[0]


# ============================================================================
# CLI
# ============================================================================


def _cli():
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd = sys.argv[1]

    if cmd == "check-copy" and len(sys.argv) >= 3:
        text = " ".join(sys.argv[2:])
        found = validate_copy_for_notification(text)
        if found:
            print(f"❌ 광고성 키워드 검출: {found}")
            return 1
        print("✅ 알림톡 카피 OK")
        return 0

    if cmd == "check-size" and len(sys.argv) == 5:
        path = Path(sys.argv[2])
        w = int(sys.argv[3])
        h = int(sys.argv[4])
        ok, msg = validate_size(path, w, h)
        print(("✅ " if ok else "❌ ") + msg)
        return 0 if ok else 1

    if cmd == "compress" and len(sys.argv) == 4:
        path = Path(sys.argv[2])
        target = int(sys.argv[3])
        ok, kb, q = compress_to_target(path, target)
        symbol = "✅" if ok else "❌"
        q_msg = f" (quality={q})" if q else ""
        print(f"{symbol} {path.name} → {kb:.1f}KB{q_msg} (target={target}KB)")
        return 0 if ok else 1

    print(f"알 수 없는 명령: {cmd}")
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(_cli())
