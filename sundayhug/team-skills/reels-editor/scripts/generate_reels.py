#!/usr/bin/env python3
"""
Instagram Reels 통합 생성 스크립트

영상 분석부터 최종 릴스 생성까지 전체 파이프라인을 자동화합니다.
"""

import argparse
import subprocess
import sys
import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional, List


# 스크립트 경로
SCRIPT_DIR = Path(__file__).parent
ANALYZE_SCRIPT = SCRIPT_DIR / 'analyze_video.py'
RESIZE_SCRIPT = SCRIPT_DIR / 'resize_video.py'
TRIM_SCRIPT = SCRIPT_DIR / 'trim_video.py'
OVERLAY_SCRIPT = SCRIPT_DIR / 'add_overlay.py'

# 릴스 규격
REELS_WIDTH = 1080
REELS_HEIGHT = 1920
REELS_MAX_DURATION = 90


def run_script(script: Path, args: List[str]) -> tuple:
    """Python 스크립트 실행"""
    cmd = [sys.executable, str(script)] + args
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr


def get_video_duration(video_path: str) -> float:
    """영상 길이 조회"""
    cmd = [
        'ffprobe', '-v', 'quiet',
        '-show_entries', 'format=duration',
        '-of', 'csv=p=0',
        video_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return 0
    return float(result.stdout.strip())


def generate_thumbnail(video_path: str, output_path: str, timestamp: float = 1.0) -> bool:
    """썸네일 생성"""
    cmd = [
        'ffmpeg', '-y',
        '-ss', str(timestamp),
        '-i', video_path,
        '-vframes', '1',
        '-q:v', '2',
        output_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def generate_reels_auto(
    video_path: str,
    output_dir: str,
    api_key: Optional[str] = None,
    product_context: Optional[str] = None
) -> dict:
    """자동 모드: AI 분석 기반 릴스 생성"""

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    result = {
        'mode': 'auto',
        'input': video_path,
        'output_dir': output_dir,
        'success': False,
        'files': {}
    }

    # 1. 영상 분석
    print("\n[1/4] 영상 분석 중...")
    analysis_path = os.path.join(output_dir, 'analysis.json')

    analyze_args = [
        '--video', video_path,
        '--output', analysis_path
    ]
    if api_key:
        analyze_args.extend(['--api-key', api_key])
    if product_context:
        analyze_args.extend(['--context', product_context])

    code, stdout, stderr = run_script(ANALYZE_SCRIPT, analyze_args)
    print(stdout)

    if code != 0:
        print(f"분석 실패: {stderr}", file=sys.stderr)
        return result

    # 분석 결과 로드
    with open(analysis_path, 'r', encoding='utf-8') as f:
        analysis = json.load(f)

    result['files']['analysis'] = analysis_path
    result['analysis'] = analysis

    # 2. 클립 추출/병합
    print("\n[2/4] 클립 추출 중...")

    recommended_clips = analysis.get('recommended_clips', [])

    if not recommended_clips:
        # 추천 클립이 없으면 전체 영상 사용 (90초 제한)
        duration = analysis['video_info']['duration']
        if duration > REELS_MAX_DURATION:
            recommended_clips = [{
                'start': 0,
                'end': REELS_MAX_DURATION,
                'reason': '자동 트리밍 (90초 제한)'
            }]
        else:
            recommended_clips = [{
                'start': 0,
                'end': duration,
                'reason': '전체 영상 사용'
            }]

    # 클립 문자열 생성
    clips_str = ','.join([
        f"{clip['start']:.1f}-{clip['end']:.1f}"
        for clip in sorted(recommended_clips, key=lambda x: x.get('priority', x['start']))[:3]
    ])

    trimmed_path = os.path.join(output_dir, f'trimmed_{timestamp}.mp4')

    if len(recommended_clips) == 1:
        clip = recommended_clips[0]
        trim_args = [
            '--video', video_path,
            '--start', str(clip['start']),
            '--end', str(clip['end']),
            '--output', trimmed_path
        ]
    else:
        trim_args = [
            '--video', video_path,
            '--clips', clips_str,
            '--output', trimmed_path
        ]

    code, stdout, stderr = run_script(TRIM_SCRIPT, trim_args)
    print(stdout)

    if code != 0:
        print(f"트리밍 실패: {stderr}", file=sys.stderr)
        return result

    result['files']['trimmed'] = trimmed_path

    # 3. 9:16 변환
    print("\n[3/4] 9:16 변환 중...")
    resized_path = os.path.join(output_dir, f'resized_{timestamp}.mp4')

    resize_args = [
        '--video', trimmed_path,
        '--output', resized_path
    ]

    code, stdout, stderr = run_script(RESIZE_SCRIPT, resize_args)
    print(stdout)

    if code != 0:
        print(f"리사이즈 실패: {stderr}", file=sys.stderr)
        return result

    result['files']['resized'] = resized_path

    # 4. 오버레이 추가
    print("\n[4/4] 오버레이 추가 중...")
    final_path = os.path.join(output_dir, f'reels_{timestamp}.mp4')

    # 분석에서 추천 카피 가져오기
    suggested_copy = analysis.get('suggested_copy') or {}
    if analysis.get('analysis') and analysis['analysis'].get('suggested_copy'):
        suggested_copy = analysis['analysis']['suggested_copy']

    headline = None
    cta = None

    if suggested_copy:
        headlines = suggested_copy.get('headline_options', [])
        ctas = suggested_copy.get('cta_options', [])
        headline = headlines[0] if headlines else None
        cta = ctas[0] if ctas else None

    if headline or cta:
        overlay_args = [
            '--video', resized_path,
            '--output', final_path
        ]
        if headline:
            overlay_args.extend(['--headline', headline])
        if cta:
            overlay_args.extend(['--cta', cta])

        code, stdout, stderr = run_script(OVERLAY_SCRIPT, overlay_args)
        print(stdout)

        if code != 0:
            print(f"오버레이 추가 실패, 리사이즈된 영상 사용: {stderr}")
            shutil.copy(resized_path, final_path)
    else:
        print("추천 카피 없음, 오버레이 없이 진행")
        shutil.copy(resized_path, final_path)

    result['files']['final'] = final_path

    # 썸네일 생성
    thumbnail_path = os.path.join(output_dir, f'thumbnail_{timestamp}.jpg')
    if generate_thumbnail(final_path, thumbnail_path):
        result['files']['thumbnail'] = thumbnail_path

    # 메타데이터 저장
    metadata = {
        'created_at': datetime.now().isoformat(),
        'source': video_path,
        'mode': 'auto',
        'duration': get_video_duration(final_path),
        'resolution': f'{REELS_WIDTH}x{REELS_HEIGHT}',
        'clips_used': clips_str,
        'headline': headline,
        'cta': cta,
        'files': result['files']
    }

    metadata_path = os.path.join(output_dir, f'metadata_{timestamp}.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    result['files']['metadata'] = metadata_path
    result['success'] = True

    return result


def generate_reels_manual(
    video_path: str,
    output_dir: str,
    clips: Optional[str] = None,
    start: Optional[float] = None,
    end: Optional[float] = None,
    headline: Optional[str] = None,
    cta: Optional[str] = None
) -> dict:
    """수동 모드: 사용자 지정 설정으로 릴스 생성"""

    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    result = {
        'mode': 'manual',
        'input': video_path,
        'output_dir': output_dir,
        'success': False,
        'files': {}
    }

    current_video = video_path

    # 1. 트리밍 (필요한 경우)
    if clips or (start is not None and end is not None):
        print("\n[1/3] 클립 추출 중...")
        trimmed_path = os.path.join(output_dir, f'trimmed_{timestamp}.mp4')

        if clips:
            trim_args = [
                '--video', video_path,
                '--clips', clips,
                '--output', trimmed_path
            ]
        else:
            trim_args = [
                '--video', video_path,
                '--start', str(start),
                '--end', str(end),
                '--output', trimmed_path
            ]

        code, stdout, stderr = run_script(TRIM_SCRIPT, trim_args)
        print(stdout)

        if code != 0:
            print(f"트리밍 실패: {stderr}", file=sys.stderr)
            return result

        current_video = trimmed_path
        result['files']['trimmed'] = trimmed_path
    else:
        print("\n[1/3] 트리밍 건너뜀 (전체 영상 사용)")

    # 2. 9:16 변환
    print("\n[2/3] 9:16 변환 중...")
    resized_path = os.path.join(output_dir, f'resized_{timestamp}.mp4')

    resize_args = [
        '--video', current_video,
        '--output', resized_path
    ]

    code, stdout, stderr = run_script(RESIZE_SCRIPT, resize_args)
    print(stdout)

    if code != 0:
        print(f"리사이즈 실패: {stderr}", file=sys.stderr)
        return result

    result['files']['resized'] = resized_path

    # 3. 오버레이 추가
    print("\n[3/3] 오버레이 추가 중...")
    final_path = os.path.join(output_dir, f'reels_{timestamp}.mp4')

    if headline or cta:
        overlay_args = [
            '--video', resized_path,
            '--output', final_path
        ]
        if headline:
            overlay_args.extend(['--headline', headline])
        if cta:
            overlay_args.extend(['--cta', cta])

        code, stdout, stderr = run_script(OVERLAY_SCRIPT, overlay_args)
        print(stdout)

        if code != 0:
            print(f"오버레이 추가 실패: {stderr}")
            shutil.copy(resized_path, final_path)
    else:
        print("오버레이 없이 진행")
        shutil.copy(resized_path, final_path)

    result['files']['final'] = final_path

    # 썸네일 생성
    thumbnail_path = os.path.join(output_dir, f'thumbnail_{timestamp}.jpg')
    if generate_thumbnail(final_path, thumbnail_path):
        result['files']['thumbnail'] = thumbnail_path

    # 메타데이터 저장
    metadata = {
        'created_at': datetime.now().isoformat(),
        'source': video_path,
        'mode': 'manual',
        'duration': get_video_duration(final_path),
        'resolution': f'{REELS_WIDTH}x{REELS_HEIGHT}',
        'clips': clips,
        'start': start,
        'end': end,
        'headline': headline,
        'cta': cta,
        'files': result['files']
    }

    metadata_path = os.path.join(output_dir, f'metadata_{timestamp}.json')
    with open(metadata_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    result['files']['metadata'] = metadata_path
    result['success'] = True

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Instagram Reels 통합 생성 스크립트'
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
        choices=['auto', 'manual'],
        default='auto',
        help='생성 모드 (auto: AI 분석 기반, manual: 수동 설정)'
    )

    # 자동 모드 옵션
    parser.add_argument(
        '--api-key',
        help='Gemini API 키 (자동 모드)'
    )
    parser.add_argument(
        '--context', '-c',
        help='제품/서비스 컨텍스트 (자동 모드)'
    )

    # 수동 모드 옵션
    parser.add_argument(
        '--clips',
        help='클립 구간 (예: "5-20,45-60")'
    )
    parser.add_argument(
        '--start', '-s',
        type=float,
        help='시작 시간 (초)'
    )
    parser.add_argument(
        '--end', '-e',
        type=float,
        help='종료 시간 (초)'
    )
    parser.add_argument(
        '--headline',
        help='헤드라인 텍스트'
    )
    parser.add_argument(
        '--cta',
        help='CTA 텍스트'
    )

    args = parser.parse_args()

    if not Path(args.video).exists():
        print(f"오류: 입력 파일을 찾을 수 없습니다: {args.video}", file=sys.stderr)
        sys.exit(1)

    print("="*50)
    print("Instagram Reels 생성기")
    print("="*50)
    print(f"입력: {args.video}")
    print(f"출력: {args.output}")
    print(f"모드: {args.mode}")

    if args.mode == 'auto':
        api_key = args.api_key or os.environ.get('GEMINI_API_KEY')
        result = generate_reels_auto(
            args.video,
            args.output,
            api_key=api_key,
            product_context=args.context
        )
    else:
        result = generate_reels_manual(
            args.video,
            args.output,
            clips=args.clips,
            start=args.start,
            end=args.end,
            headline=args.headline,
            cta=args.cta
        )

    print("\n" + "="*50)
    if result['success']:
        print("릴스 생성 완료!")
        print("="*50)
        print("\n생성된 파일:")
        for name, path in result['files'].items():
            print(f"  {name}: {path}")

        final_duration = get_video_duration(result['files']['final'])
        print(f"\n최종 영상 길이: {final_duration:.1f}초")

        if final_duration > REELS_MAX_DURATION:
            print(f"경고: 영상이 릴스 최대 길이({REELS_MAX_DURATION}초)를 초과합니다!")
    else:
        print("릴스 생성 실패")
        print("="*50)
        sys.exit(1)


if __name__ == '__main__':
    main()
