#!/usr/bin/env python3
"""
9:16 블러 배경 영상 변환 스크립트

원본 영상을 Instagram Reels 규격(1080x1920, 9:16)으로 변환합니다.
원본 비율을 유지하면서 상하 여백은 블러 처리된 배경으로 채웁니다.
"""

import argparse
import subprocess
import sys
import json
from pathlib import Path


def get_video_info(video_path: str) -> dict:
    """영상 정보(해상도, 길이 등) 조회"""
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

    return {
        'width': int(video_stream['width']),
        'height': int(video_stream['height']),
        'duration': float(data['format'].get('duration', 0)),
        'codec': video_stream.get('codec_name', 'unknown')
    }


def resize_with_blur_background(
    input_path: str,
    output_path: str,
    target_width: int = 1080,
    target_height: int = 1920,
    blur_strength: int = 50
) -> bool:
    """
    블러 배경으로 9:16 영상 변환

    Args:
        input_path: 입력 영상 경로
        output_path: 출력 영상 경로
        target_width: 목표 너비 (기본 1080)
        target_height: 목표 높이 (기본 1920)
        blur_strength: 블러 강도 (기본 50)

    Returns:
        성공 여부
    """
    info = get_video_info(input_path)
    src_w, src_h = info['width'], info['height']

    # 원본 비율 계산
    src_ratio = src_w / src_h
    target_ratio = target_width / target_height

    # 원본을 타겟에 맞춰 스케일 계산 (비율 유지)
    if src_ratio > target_ratio:
        # 원본이 더 가로로 넓음 -> 너비 기준 맞춤
        scale_w = target_width
        scale_h = int(target_width / src_ratio)
    else:
        # 원본이 더 세로로 높음 -> 높이 기준 맞춤
        scale_h = target_height
        scale_w = int(target_height * src_ratio)

    # 짝수로 맞춤 (FFmpeg 요구사항)
    scale_w = scale_w - (scale_w % 2)
    scale_h = scale_h - (scale_h % 2)

    # FFmpeg 필터 체인 구성
    # 1. 블러 배경: 원본을 타겟 크기로 확대 + 블러
    # 2. 원본: 비율 유지하며 축소
    # 3. 오버레이: 블러 배경 위에 원본 중앙 배치
    filter_complex = (
        f"[0:v]scale={target_width}:{target_height}:force_original_aspect_ratio=increase,"
        f"crop={target_width}:{target_height},"
        f"boxblur={blur_strength}:5[bg];"
        f"[0:v]scale={scale_w}:{scale_h}[fg];"
        f"[bg][fg]overlay=(W-w)/2:(H-h)/2"
    )

    cmd = [
        'ffmpeg', '-y',
        '-i', input_path,
        '-filter_complex', filter_complex,
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        output_path
    ]

    print(f"변환 중: {input_path} -> {output_path}")
    print(f"  원본: {src_w}x{src_h}")
    print(f"  출력: {target_width}x{target_height}")
    print(f"  내부 영상: {scale_w}x{scale_h}")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"FFmpeg 오류: {result.stderr}", file=sys.stderr)
        return False

    print(f"변환 완료: {output_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Instagram Reels 규격(9:16, 1080x1920) 블러 배경 변환'
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
        '--width',
        type=int,
        default=1080,
        help='출력 너비 (기본: 1080)'
    )
    parser.add_argument(
        '--height',
        type=int,
        default=1920,
        help='출력 높이 (기본: 1920)'
    )
    parser.add_argument(
        '--blur',
        type=int,
        default=50,
        help='블러 강도 (기본: 50)'
    )

    args = parser.parse_args()

    if not Path(args.video).exists():
        print(f"오류: 입력 파일을 찾을 수 없습니다: {args.video}", file=sys.stderr)
        sys.exit(1)

    # 출력 디렉토리 생성
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    success = resize_with_blur_background(
        args.video,
        args.output,
        args.width,
        args.height,
        args.blur
    )

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
