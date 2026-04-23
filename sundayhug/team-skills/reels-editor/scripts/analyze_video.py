#!/usr/bin/env python3
"""
AI 영상 분석 스크립트 (Gemini Vision API)

영상에서 프레임을 추출하고 Gemini Vision API로 분석하여
릴스 편집을 위한 추천 정보를 생성합니다.
"""

import argparse
import subprocess
import sys
import os
import json
import base64
import tempfile
from fractions import Fraction
from pathlib import Path
from typing import List, Optional

try:
    import google.generativeai as genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


REELS_MAX_DURATION = 90  # 릴스 최대 길이 (초)


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
        'fps': float(Fraction(video_stream.get('r_frame_rate', '30/1'))),
        'codec': video_stream.get('codec_name', 'unknown'),
        'file_size': int(data['format'].get('size', 0))
    }


def extract_analysis_frames(
    video_path: str,
    output_dir: str,
    num_frames: int = 10
) -> List[dict]:
    """분석용 프레임 추출"""
    info = get_video_info(video_path)
    duration = info['duration']

    # 균등 간격으로 프레임 추출
    interval = duration / (num_frames + 1)
    timestamps = [interval * (i + 1) for i in range(num_frames)]

    os.makedirs(output_dir, exist_ok=True)

    frames = []
    for i, ts in enumerate(timestamps):
        output_path = os.path.join(output_dir, f'analysis_frame_{i:02d}.jpg')

        cmd = [
            'ffmpeg', '-y',
            '-ss', str(ts),
            '-i', video_path,
            '-vframes', '1',
            '-q:v', '2',
            output_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0 and os.path.exists(output_path):
            frames.append({
                'path': output_path,
                'timestamp': ts
            })

    return frames


def encode_image_base64(image_path: str) -> str:
    """이미지를 base64로 인코딩"""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')


def analyze_with_gemini(
    frames: List[dict],
    video_info: dict,
    api_key: str,
    product_context: Optional[str] = None
) -> dict:
    """Gemini Vision API로 영상 분석"""
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash')

    # 이미지 준비
    image_parts = []
    for frame in frames:
        with open(frame['path'], 'rb') as f:
            image_data = f.read()
        image_parts.append({
            'mime_type': 'image/jpeg',
            'data': image_data
        })

    # 프롬프트 구성
    context = f"제품/서비스 정보: {product_context}" if product_context else ""

    prompt = f"""다음은 영상에서 추출한 프레임들입니다.
이 영상을 Instagram Reels 광고(9:16, 최대 90초)로 편집하기 위한 분석을 해주세요.

영상 정보:
- 전체 길이: {video_info['duration']:.1f}초
- 해상도: {video_info['width']}x{video_info['height']}
{context}

각 프레임의 타임스탬프:
{chr(10).join([f"- 프레임 {i+1}: {f['timestamp']:.1f}초" for i, f in enumerate(frames)])}

다음 JSON 형식으로 분석 결과를 제공해주세요:

```json
{{
    "content_type": "제품 소개 / 튜토리얼 / 언박싱 / 리뷰 / 브이로그 / 기타",
    "main_subject": "영상의 주요 대상 (제품명, 인물, 장소 등)",
    "key_moments": [
        {{
            "timestamp_range": "시작초-종료초",
            "description": "해당 구간 설명",
            "importance": "high/medium/low",
            "reason": "중요한 이유"
        }}
    ],
    "recommended_clips": [
        {{
            "start": 시작초(숫자),
            "end": 종료초(숫자),
            "reason": "이 구간을 추천하는 이유",
            "priority": 1
        }}
    ],
    "suggested_copy": {{
        "headline_options": ["헤드라인 옵션 1", "헤드라인 옵션 2", "헤드라인 옵션 3"],
        "cta_options": ["CTA 옵션 1", "CTA 옵션 2"],
        "hashtags": ["해시태그1", "해시태그2", "해시태그3"]
    }},
    "editing_suggestions": {{
        "pacing": "빠름/보통/느림 - 권장 편집 속도",
        "transitions": "권장 전환 효과",
        "music_mood": "권장 음악 분위기",
        "color_tone": "권장 색감"
    }},
    "warnings": ["주의사항이 있다면 여기에"]
}}
```

분석 시 고려사항:
1. 릴스 최대 길이는 90초입니다
2. 시청자 주목을 끌 수 있는 하이라이트 구간을 우선 추천해주세요
3. 헤드라인과 CTA는 한국어로 작성해주세요
4. 추천 클립의 총 길이가 60-90초가 되도록 해주세요
"""

    try:
        response = model.generate_content([prompt] + image_parts)
        response_text = response.text

        # JSON 추출
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1

        if json_start >= 0 and json_end > json_start:
            json_str = response_text[json_start:json_end]
            analysis = json.loads(json_str)
            return analysis
        else:
            return {
                'error': 'JSON 파싱 실패',
                'raw_response': response_text
            }

    except Exception as e:
        return {
            'error': str(e)
        }


def analyze_video(
    video_path: str,
    output_path: str,
    api_key: Optional[str] = None,
    product_context: Optional[str] = None,
    num_frames: int = 10
) -> dict:
    """영상 분석 메인 함수"""

    # 1. 영상 정보 수집
    print("영상 정보 분석 중...")
    video_info = get_video_info(video_path)
    print(f"  해상도: {video_info['width']}x{video_info['height']}")
    print(f"  길이: {video_info['duration']:.1f}초")

    # 2. 프레임 추출
    print(f"\n프레임 추출 중 ({num_frames}개)...")
    temp_dir = tempfile.mkdtemp()
    frames = extract_analysis_frames(video_path, temp_dir, num_frames)
    print(f"  {len(frames)}개 프레임 추출 완료")

    result = {
        'video_path': video_path,
        'video_info': video_info,
        'frames_extracted': len(frames),
        'analysis': None,
        'recommended_clips': [],
        'suggested_copy': None
    }

    # 3. AI 분석 (API 키가 있는 경우)
    if api_key and GENAI_AVAILABLE:
        print("\nGemini Vision API 분석 중...")
        analysis = analyze_with_gemini(frames, video_info, api_key, product_context)

        if 'error' not in analysis:
            result['analysis'] = analysis
            result['recommended_clips'] = analysis.get('recommended_clips', [])
            result['suggested_copy'] = analysis.get('suggested_copy')
            print("  AI 분석 완료")
        else:
            print(f"  AI 분석 실패: {analysis.get('error')}")
            result['analysis_error'] = analysis.get('error')
    elif not api_key:
        print("\n주의: GEMINI_API_KEY가 설정되지 않아 AI 분석을 건너뜁니다")
        # 기본 추천 생성
        duration = video_info['duration']
        if duration <= REELS_MAX_DURATION:
            result['recommended_clips'] = [{
                'start': 0,
                'end': duration,
                'reason': '전체 영상 사용 (90초 이하)',
                'priority': 1
            }]
        else:
            # 긴 영상은 균등 분할 제안
            clip_length = 30
            clips = []
            for i in range(min(3, int(duration / clip_length))):
                clips.append({
                    'start': i * clip_length,
                    'end': (i + 1) * clip_length,
                    'reason': f'구간 {i+1} (수동 검토 필요)',
                    'priority': i + 1
                })
            result['recommended_clips'] = clips
    else:
        print("\n주의: google-generativeai 패키지가 설치되지 않았습니다")
        print("  pip install google-generativeai")

    # 4. 임시 파일 정리
    for frame in frames:
        if os.path.exists(frame['path']):
            os.remove(frame['path'])
    if os.path.exists(temp_dir):
        os.rmdir(temp_dir)

    # 5. 결과 저장
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"\n분석 결과 저장: {output_path}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Gemini Vision API를 사용한 영상 분석'
    )
    parser.add_argument(
        '--video', '-v',
        required=True,
        help='입력 영상 파일 경로'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='분석 결과 JSON 파일 경로'
    )
    parser.add_argument(
        '--api-key',
        help='Gemini API 키 (또는 GEMINI_API_KEY 환경변수)'
    )
    parser.add_argument(
        '--context', '-c',
        help='제품/서비스 컨텍스트 정보'
    )
    parser.add_argument(
        '--frames', '-f',
        type=int,
        default=10,
        help='분석할 프레임 수 (기본: 10)'
    )

    args = parser.parse_args()

    if not Path(args.video).exists():
        print(f"오류: 입력 파일을 찾을 수 없습니다: {args.video}", file=sys.stderr)
        sys.exit(1)

    # API 키 결정
    api_key = args.api_key or os.environ.get('GEMINI_API_KEY')

    if not api_key:
        print("경고: Gemini API 키가 없습니다. 기본 분석만 수행합니다.")
        print("  --api-key 옵션 또는 GEMINI_API_KEY 환경변수를 설정하세요.")

    result = analyze_video(
        args.video,
        args.output,
        api_key=api_key,
        product_context=args.context,
        num_frames=args.frames
    )

    # 요약 출력
    print("\n" + "="*50)
    print("분석 요약")
    print("="*50)

    if result.get('analysis'):
        analysis = result['analysis']
        print(f"콘텐츠 유형: {analysis.get('content_type', 'N/A')}")
        print(f"주요 대상: {analysis.get('main_subject', 'N/A')}")

        if analysis.get('suggested_copy'):
            copy = analysis['suggested_copy']
            print(f"\n추천 헤드라인:")
            for h in copy.get('headline_options', [])[:3]:
                print(f"  - {h}")
            print(f"\n추천 CTA:")
            for c in copy.get('cta_options', [])[:2]:
                print(f"  - {c}")

    if result.get('recommended_clips'):
        print(f"\n추천 클립:")
        for clip in result['recommended_clips'][:3]:
            print(f"  - {clip['start']:.1f}s ~ {clip['end']:.1f}s: {clip.get('reason', '')}")

    sys.exit(0)


if __name__ == '__main__':
    main()
