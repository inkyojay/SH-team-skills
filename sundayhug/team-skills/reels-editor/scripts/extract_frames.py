#!/usr/bin/env python3
"""
프레임 추출 스크립트

AI 영상 분석을 위해 영상에서 주요 프레임을 추출합니다.
"""

import argparse
import subprocess
import sys
import os
import json
from fractions import Fraction
from pathlib import Path
from typing import List


def get_video_info(video_path: str) -> dict:
    """영상 정보 조회"""
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
        'fps': float(Fraction(video_stream.get('r_frame_rate', '30/1')))
    }


def extract_frames(
    video_path: str,
    output_dir: str,
    interval: float = 5.0,
    max_frames: int = 20,
    format: str = 'jpg',
    quality: int = 2
) -> List[dict]:
    """
    영상에서 프레임 추출

    Args:
        video_path: 입력 영상 경로
        output_dir: 출력 디렉토리
        interval: 프레임 추출 간격 (초)
        max_frames: 최대 추출 프레임 수
        format: 출력 이미지 형식 (jpg, png)
        quality: JPEG 품질 (1-31, 낮을수록 좋음)

    Returns:
        추출된 프레임 정보 리스트
    """
    info = get_video_info(video_path)
    duration = info['duration']

    # 추출할 타임스탬프 계산
    timestamps = []
    t = 0
    while t < duration and len(timestamps) < max_frames:
        timestamps.append(t)
        t += interval

    # 마지막 프레임도 포함 (영상 끝 직전)
    if duration > 0 and (not timestamps or timestamps[-1] < duration - 1):
        if len(timestamps) < max_frames:
            timestamps.append(max(0, duration - 0.5))

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    extracted = []

    for i, timestamp in enumerate(timestamps):
        output_path = os.path.join(output_dir, f'frame_{i:03d}_{timestamp:.1f}s.{format}')

        cmd = [
            'ffmpeg', '-y',
            '-ss', str(timestamp),
            '-i', video_path,
            '-vframes', '1',
            '-q:v', str(quality),
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and os.path.exists(output_path):
            extracted.append({
                'path': output_path,
                'timestamp': timestamp,
                'index': i
            })
            print(f"프레임 추출: {timestamp:.1f}s -> {output_path}")
        else:
            print(f"프레임 추출 실패: {timestamp:.1f}s", file=sys.stderr)

    return extracted


def extract_keyframes(
    video_path: str,
    output_dir: str,
    max_frames: int = 20,
    format: str = 'jpg'
) -> List[dict]:
    """
    영상에서 키프레임(I-frame) 추출

    장면 전환 감지에 유용합니다.
    """
    os.makedirs(output_dir, exist_ok=True)

    # 키프레임 추출
    output_pattern = os.path.join(output_dir, f'keyframe_%03d.{format}')

    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vf', 'select=eq(pict_type\\,I)',
        '-vsync', 'vfr',
        '-frames:v', str(max_frames),
        '-q:v', '2',
        output_pattern
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"키프레임 추출 실패: {result.stderr}", file=sys.stderr)
        return []

    # 추출된 파일 목록
    extracted = []
    for i in range(max_frames):
        path = os.path.join(output_dir, f'keyframe_{i+1:03d}.{format}')
        if os.path.exists(path):
            extracted.append({
                'path': path,
                'index': i
            })

    print(f"키프레임 {len(extracted)}개 추출 완료")
    return extracted


def extract_scene_changes(
    video_path: str,
    output_dir: str,
    threshold: float = 0.3,
    max_frames: int = 20,
    format: str = 'jpg'
) -> List[dict]:
    """
    장면 전환 감지하여 프레임 추출

    Args:
        threshold: 장면 전환 감지 임계값 (0-1, 낮을수록 민감)
    """
    os.makedirs(output_dir, exist_ok=True)

    output_pattern = os.path.join(output_dir, f'scene_%03d.{format}')

    cmd = [
        'ffmpeg', '-y',
        '-i', video_path,
        '-vf', f"select='gt(scene,{threshold})',showinfo",
        '-vsync', 'vfr',
        '-frames:v', str(max_frames),
        '-q:v', '2',
        output_pattern
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # 추출된 파일 목록
    extracted = []
    for i in range(max_frames):
        path = os.path.join(output_dir, f'scene_{i+1:03d}.{format}')
        if os.path.exists(path):
            extracted.append({
                'path': path,
                'index': i
            })

    print(f"장면 전환 프레임 {len(extracted)}개 추출 완료")
    return extracted


def main():
    parser = argparse.ArgumentParser(
        description='AI 분석을 위한 영상 프레임 추출'
    )
    parser.add_argument(
        '--video', '-v',
        required=True,
        help='입력 영상 파일 경로'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='출력 디렉토리 경로'
    )
    parser.add_argument(
        '--mode', '-m',
        choices=['interval', 'keyframe', 'scene'],
        default='interval',
        help='추출 모드 (interval: 일정 간격, keyframe: 키프레임, scene: 장면 전환)'
    )
    parser.add_argument(
        '--interval', '-i',
        type=float,
        default=5.0,
        help='프레임 추출 간격 (초, interval 모드에서만 사용)'
    )
    parser.add_argument(
        '--max-frames',
        type=int,
        default=20,
        help='최대 추출 프레임 수 (기본: 20)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.3,
        help='장면 전환 감지 임계값 (scene 모드, 기본: 0.3)'
    )
    parser.add_argument(
        '--format',
        choices=['jpg', 'png'],
        default='jpg',
        help='출력 이미지 형식 (기본: jpg)'
    )
    parser.add_argument(
        '--json',
        help='추출 결과를 JSON 파일로 저장'
    )

    args = parser.parse_args()

    if not Path(args.video).exists():
        print(f"오류: 입력 파일을 찾을 수 없습니다: {args.video}", file=sys.stderr)
        sys.exit(1)

    # 모드별 추출
    if args.mode == 'interval':
        extracted = extract_frames(
            args.video,
            args.output,
            interval=args.interval,
            max_frames=args.max_frames,
            format=args.format
        )
    elif args.mode == 'keyframe':
        extracted = extract_keyframes(
            args.video,
            args.output,
            max_frames=args.max_frames,
            format=args.format
        )
    else:  # scene
        extracted = extract_scene_changes(
            args.video,
            args.output,
            threshold=args.threshold,
            max_frames=args.max_frames,
            format=args.format
        )

    # JSON 출력
    if args.json:
        info = get_video_info(args.video)
        result = {
            'video': args.video,
            'video_info': info,
            'mode': args.mode,
            'frames': extracted
        }
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"결과 저장: {args.json}")

    print(f"\n총 {len(extracted)}개 프레임 추출 완료")
    sys.exit(0 if extracted else 1)


if __name__ == '__main__':
    main()
