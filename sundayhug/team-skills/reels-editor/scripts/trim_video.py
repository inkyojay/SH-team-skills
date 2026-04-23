#!/usr/bin/env python3
"""
영상 트리밍/병합 스크립트

영상의 특정 구간을 추출하거나 여러 구간을 병합합니다.
Instagram Reels 최대 길이(90초)를 초과하지 않도록 검증합니다.
"""

import argparse
import subprocess
import sys
import tempfile
import os
from pathlib import Path
from typing import List, Tuple


REELS_MAX_DURATION = 90  # 릴스 최대 길이 (초)


def get_video_duration(video_path: str) -> float:
    """영상 길이 조회 (초)"""
    cmd = [
        'ffprobe', '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe 실행 실패: {result.stderr}")
    return float(result.stdout.strip())


def parse_clips(clips_str: str) -> List[Tuple[float, float]]:
    """
    클립 문자열 파싱

    예: "5-20,45-60" -> [(5.0, 20.0), (45.0, 60.0)]
    """
    clips = []
    for clip in clips_str.split(','):
        clip = clip.strip()
        if '-' not in clip:
            raise ValueError(f"잘못된 클립 형식: {clip} (예: '5-20')")
        parts = clip.split('-')
        if len(parts) != 2:
            raise ValueError(f"잘못된 클립 형식: {clip}")
        start = float(parts[0].strip())
        end = float(parts[1].strip())
        if start >= end:
            raise ValueError(f"시작 시간이 종료 시간보다 크거나 같습니다: {clip}")
        clips.append((start, end))
    return clips


def trim_single(
    input_path: str,
    output_path: str,
    start: float,
    end: float
) -> bool:
    """단일 구간 추출"""
    duration = end - start

    if duration > REELS_MAX_DURATION:
        print(f"경고: 구간 길이({duration:.1f}초)가 릴스 최대 길이({REELS_MAX_DURATION}초)를 초과합니다")

    cmd = [
        'ffmpeg', '-y',
        '-ss', str(start),
        '-i', input_path,
        '-t', str(duration),
        '-c:v', 'libx264',
        '-preset', 'medium',
        '-crf', '23',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-movflags', '+faststart',
        output_path
    ]

    print(f"트리밍 중: {start:.1f}s ~ {end:.1f}s (길이: {duration:.1f}s)")

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"FFmpeg 오류: {result.stderr}", file=sys.stderr)
        return False

    print(f"트리밍 완료: {output_path}")
    return True


def merge_clips(
    input_path: str,
    output_path: str,
    clips: List[Tuple[float, float]]
) -> bool:
    """여러 구간 추출 후 병합"""
    total_duration = sum(end - start for start, end in clips)

    if total_duration > REELS_MAX_DURATION:
        print(f"경고: 총 길이({total_duration:.1f}초)가 릴스 최대 길이({REELS_MAX_DURATION}초)를 초과합니다")

    # 임시 파일 생성
    temp_dir = tempfile.mkdtemp()
    temp_files = []
    concat_list_path = os.path.join(temp_dir, 'concat_list.txt')

    try:
        # 각 구간 추출
        for i, (start, end) in enumerate(clips):
            temp_path = os.path.join(temp_dir, f'clip_{i:03d}.mp4')
            temp_files.append(temp_path)

            duration = end - start
            cmd = [
                'ffmpeg', '-y',
                '-ss', str(start),
                '-i', input_path,
                '-t', str(duration),
                '-c:v', 'libx264',
                '-preset', 'medium',
                '-crf', '23',
                '-c:a', 'aac',
                '-b:a', '128k',
                temp_path
            ]

            print(f"클립 {i+1}/{len(clips)} 추출 중: {start:.1f}s ~ {end:.1f}s")
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                print(f"FFmpeg 오류: {result.stderr}", file=sys.stderr)
                return False

        # concat 리스트 파일 생성
        with open(concat_list_path, 'w') as f:
            for temp_path in temp_files:
                f.write(f"file '{temp_path}'\n")

        # 병합
        cmd = [
            'ffmpeg', '-y',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_list_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            '-crf', '23',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-movflags', '+faststart',
            output_path
        ]

        print(f"클립 병합 중...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FFmpeg 오류: {result.stderr}", file=sys.stderr)
            return False

        print(f"병합 완료: {output_path} (총 {total_duration:.1f}초)")
        return True

    finally:
        # 임시 파일 정리
        for temp_path in temp_files:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        if os.path.exists(concat_list_path):
            os.remove(concat_list_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


def main():
    parser = argparse.ArgumentParser(
        description='영상 트리밍 및 클립 병합'
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
        '--start', '-s',
        type=float,
        help='시작 시간 (초) - 단일 구간 추출 시'
    )
    parser.add_argument(
        '--end', '-e',
        type=float,
        help='종료 시간 (초) - 단일 구간 추출 시'
    )
    parser.add_argument(
        '--clips', '-c',
        help='여러 구간 (예: "5-20,45-60") - 병합 시'
    )

    args = parser.parse_args()

    if not Path(args.video).exists():
        print(f"오류: 입력 파일을 찾을 수 없습니다: {args.video}", file=sys.stderr)
        sys.exit(1)

    # 출력 디렉토리 생성
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    # 모드 결정
    if args.clips:
        # 여러 구간 병합 모드
        try:
            clips = parse_clips(args.clips)
        except ValueError as e:
            print(f"오류: {e}", file=sys.stderr)
            sys.exit(1)
        success = merge_clips(args.video, args.output, clips)
    elif args.start is not None and args.end is not None:
        # 단일 구간 추출 모드
        success = trim_single(args.video, args.output, args.start, args.end)
    else:
        print("오류: --start와 --end, 또는 --clips 옵션이 필요합니다", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
