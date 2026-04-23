#!/usr/bin/env python3
"""
텍스트/CTA 오버레이 스크립트 (Pillow 기반)

영상에 헤드라인 텍스트와 CTA 버튼을 추가합니다.
Instagram Reels 안전 영역(상하단 14%)을 고려하여 배치합니다.
"""

import argparse
import subprocess
import sys
import os
import tempfile
import shutil
from pathlib import Path
from typing import Optional, Tuple

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


# Reels 규격
REELS_WIDTH = 1080
REELS_HEIGHT = 1920
SAFE_ZONE_PERCENT = 14  # 상하단 안전 영역 비율
SAFE_ZONE_PX = int(REELS_HEIGHT * SAFE_ZONE_PERCENT / 100)  # 약 268px


def find_font(bold: bool = True) -> str:
    """사용 가능한 한글 폰트 찾기"""
    # 스크립트 위치 기준 상대 경로
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, '..', 'assets', 'fonts')

    if bold:
        font_paths = [
            os.path.join(assets_dir, 'Pretendard-Bold.otf'),
            os.path.join(assets_dir, 'Pretendard-SemiBold.otf'),
            '/System/Library/Fonts/AppleSDGothicNeo.ttc',
            '/Library/Fonts/AppleGothic.ttf',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc',
        ]
    else:
        font_paths = [
            os.path.join(assets_dir, 'Pretendard-Regular.otf'),
            os.path.join(assets_dir, 'Pretendard-SemiBold.otf'),
            '/System/Library/Fonts/AppleSDGothicNeo.ttc',
            '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
        ]

    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path

    return None


def get_video_info(video_path: str) -> dict:
    """영상 정보 조회"""
    import json
    cmd = [
        'ffprobe', '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams', '-show_format',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe 실행 실패: {result.stderr}")

    data = json.loads(result.stdout)
    video_stream = next(
        (s for s in data['streams'] if s['codec_type'] == 'video'),
        None
    )
    if not video_stream:
        raise RuntimeError("영상 스트림을 찾을 수 없습니다")

    # FPS 계산
    fps_str = video_stream.get('r_frame_rate', '30/1')
    if '/' in fps_str:
        num, den = fps_str.split('/')
        fps = float(num) / float(den)
    else:
        fps = float(fps_str)

    return {
        'width': int(video_stream['width']),
        'height': int(video_stream['height']),
        'duration': float(data['format'].get('duration', 0)),
        'fps': fps
    }


def create_overlay_image(
    width: int,
    height: int,
    headline: Optional[str] = None,
    cta: Optional[str] = None,
    headline_size: int = 48,
    cta_size: int = 36,
    headline_color: str = 'white',
    cta_color: str = 'white',
    cta_bg_color: Tuple[int, int, int] = (0, 149, 246),  # Instagram 블루
    show_safe_zone: bool = False
) -> Image.Image:
    """오버레이 이미지 생성 (투명 배경)"""

    # RGBA 이미지 생성 (투명 배경)
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 폰트 로드
    font_path = find_font(bold=True)
    try:
        headline_font = ImageFont.truetype(font_path, headline_size) if font_path else ImageFont.load_default()
        cta_font = ImageFont.truetype(font_path, cta_size) if font_path else ImageFont.load_default()
    except Exception as e:
        print(f"폰트 로드 실패, 기본 폰트 사용: {e}")
        headline_font = ImageFont.load_default()
        cta_font = ImageFont.load_default()

    # 안전 영역 계산 (비율 기반)
    safe_zone_top = int(height * SAFE_ZONE_PERCENT / 100)
    safe_zone_bottom = height - int(height * SAFE_ZONE_PERCENT / 100)

    # 안전 영역 표시 (디버그용)
    if show_safe_zone:
        draw.rectangle([0, 0, width, safe_zone_top], fill=(255, 0, 0, 76))
        draw.rectangle([0, safe_zone_bottom, width, height], fill=(255, 0, 0, 76))

    # 헤드라인 텍스트 (상단 안전 영역 바로 아래)
    if headline:
        # 텍스트 크기 계산
        bbox = draw.textbbox((0, 0), headline, font=headline_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 위치 계산 (안전 영역 바로 아래, 중앙 정렬)
        y_pos = safe_zone_top + 50
        x_pos = (width - text_width) // 2

        # 배경 박스 (반투명 검정)
        padding = 20
        draw.rectangle(
            [0, y_pos - padding, width, y_pos + text_height + padding],
            fill=(0, 0, 0, 128)
        )

        # 텍스트 그림자
        shadow_offset = 2
        draw.text(
            (x_pos + shadow_offset, y_pos + shadow_offset),
            headline,
            font=headline_font,
            fill=(0, 0, 0, 200)
        )

        # 헤드라인 텍스트
        draw.text((x_pos, y_pos), headline, font=headline_font, fill=headline_color)

    # CTA 버튼 (하단 안전 영역 바로 위)
    if cta:
        # 텍스트 크기 계산
        bbox = draw.textbbox((0, 0), cta, font=cta_font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # 버튼 크기 및 위치
        btn_width = max(text_width + 80, 400)
        btn_height = text_height + 40
        btn_x = (width - btn_width) // 2
        btn_y = safe_zone_bottom - btn_height - 50

        # 버튼 배경 (Instagram 블루)
        btn_color_with_alpha = (*cta_bg_color, 230)
        draw.rounded_rectangle(
            [btn_x, btn_y, btn_x + btn_width, btn_y + btn_height],
            radius=10,
            fill=btn_color_with_alpha
        )

        # CTA 텍스트 (버튼 중앙)
        text_x = btn_x + (btn_width - text_width) // 2
        text_y = btn_y + (btn_height - text_height) // 2
        draw.text((text_x, text_y), cta, font=cta_font, fill=cta_color)

    return overlay


def add_text_overlay(
    input_path: str,
    output_path: str,
    headline: Optional[str] = None,
    cta: Optional[str] = None,
    headline_size: int = 48,
    cta_size: int = 36,
    headline_color: str = 'white',
    cta_color: str = 'white',
    cta_bg_color: str = '0x0095F6',
    show_safe_zone: bool = False
) -> bool:
    """
    텍스트 오버레이 추가 (Pillow + FFmpeg)

    1. Pillow로 오버레이 PNG 생성
    2. FFmpeg으로 영상에 오버레이 합성
    """

    if not PIL_AVAILABLE:
        print("오류: Pillow가 설치되지 않았습니다. pip install pillow", file=sys.stderr)
        return False

    if not headline and not cta:
        print("오류: 헤드라인 또는 CTA가 필요합니다", file=sys.stderr)
        return False

    # 영상 정보 조회
    info = get_video_info(input_path)
    width, height = info['width'], info['height']

    print(f"영상 크기: {width}x{height}")
    print(f"폰트 사용: {find_font()}")

    # CTA 배경색 파싱
    if cta_bg_color.startswith('0x'):
        hex_color = cta_bg_color[2:]
        cta_bg_rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    elif cta_bg_color.startswith('#'):
        hex_color = cta_bg_color[1:]
        cta_bg_rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    else:
        cta_bg_rgb = (0, 149, 246)  # 기본 Instagram 블루

    # 오버레이 이미지 생성
    overlay_img = create_overlay_image(
        width, height,
        headline=headline,
        cta=cta,
        headline_size=headline_size,
        cta_size=cta_size,
        headline_color=headline_color,
        cta_color=cta_color,
        cta_bg_color=cta_bg_rgb,
        show_safe_zone=show_safe_zone
    )

    # 임시 디렉토리에 오버레이 저장
    temp_dir = tempfile.mkdtemp()
    overlay_path = os.path.join(temp_dir, 'overlay.png')

    try:
        overlay_img.save(overlay_path, 'PNG')
        print(f"오버레이 이미지 생성: {overlay_path}")

        # FFmpeg으로 오버레이 합성
        cmd = [
            'ffmpeg', '-y',
            '-i', input_path,
            '-i', overlay_path,
            '-filter_complex', '[0:v][1:v]overlay=0:0',
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'copy',
            '-movflags', '+faststart',
            output_path
        ]

        print(f"오버레이 추가 중...")
        if headline:
            print(f"  헤드라인: {headline}")
        if cta:
            print(f"  CTA: {cta}")

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FFmpeg 오류: {result.stderr}", file=sys.stderr)
            return False

        print(f"오버레이 완료: {output_path}")
        return True

    finally:
        # 임시 파일 정리
        if os.path.exists(overlay_path):
            os.remove(overlay_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


def main():
    parser = argparse.ArgumentParser(
        description='영상에 텍스트/CTA 오버레이 추가'
    )
    parser.add_argument(
        '--video', '-v',
        required=True,
        help='입력 영상 파일 경로'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='출력 영상 파일 경로'
    )
    parser.add_argument(
        '--headline',
        help='상단 헤드라인 텍스트'
    )
    parser.add_argument(
        '--cta',
        help='하단 CTA 버튼 텍스트'
    )
    parser.add_argument(
        '--headline-size',
        type=int,
        default=48,
        help='헤드라인 폰트 크기 (기본: 48)'
    )
    parser.add_argument(
        '--cta-size',
        type=int,
        default=36,
        help='CTA 폰트 크기 (기본: 36)'
    )
    parser.add_argument(
        '--headline-color',
        default='white',
        help='헤드라인 색상 (기본: white)'
    )
    parser.add_argument(
        '--cta-color',
        default='white',
        help='CTA 텍스트 색상 (기본: white)'
    )
    parser.add_argument(
        '--cta-bg',
        default='0x0095F6',
        help='CTA 배경 색상 (기본: Instagram 블루)'
    )
    parser.add_argument(
        '--show-safe-zone',
        action='store_true',
        help='안전 영역 표시 (디버그용)'
    )

    args = parser.parse_args()

    if not Path(args.video).exists():
        print(f"오류: 입력 파일을 찾을 수 없습니다: {args.video}", file=sys.stderr)
        sys.exit(1)

    if not args.headline and not args.cta:
        print("오류: --headline 또는 --cta 중 하나 이상 지정해야 합니다", file=sys.stderr)
        sys.exit(1)

    # 출력 디렉토리 생성
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    success = add_text_overlay(
        args.video,
        args.output,
        headline=args.headline,
        cta=args.cta,
        headline_size=args.headline_size,
        cta_size=args.cta_size,
        headline_color=args.headline_color,
        cta_color=args.cta_color,
        cta_bg_color=args.cta_bg,
        show_safe_zone=args.show_safe_zone
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
