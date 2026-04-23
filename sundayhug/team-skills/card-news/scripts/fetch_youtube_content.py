#!/usr/bin/env python3
"""
YouTube 영상에서 카드뉴스 제작에 필요한 콘텐츠 추출

Usage:
    python fetch_youtube_content.py --url "https://youtube.com/watch?v=VIDEO_ID"
    python fetch_youtube_content.py --video-id VIDEO_ID

Output:
    JSON 형식으로 제목, 설명, 자막 출력

Requirements:
    pip install youtube-transcript-api
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error


def extract_video_id(url: str) -> str | None:
    """URL에서 비디오 ID 추출"""
    patterns = [
        r'(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'(?:embed/)([a-zA-Z0-9_-]{11})',
        r'(?:shorts/)([a-zA-Z0-9_-]{11})',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def fetch_video_metadata(video_id: str) -> dict:
    """YouTube 페이지에서 메타데이터 추출 (API 키 불필요)"""
    url = f"https://www.youtube.com/watch?v={video_id}"

    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')

        # 제목 추출
        title_match = re.search(r'<title>(.+?)</title>', html)
        title = title_match.group(1).replace(' - YouTube', '').strip() if title_match else None

        # 설명 추출 (og:description)
        desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
        description = desc_match.group(1) if desc_match else None

        # 채널명 추출
        channel_match = re.search(r'"ownerChannelName":"([^"]+)"', html)
        channel = channel_match.group(1) if channel_match else None

        return {
            'video_id': video_id,
            'title': title,
            'description': description,
            'channel': channel,
            'url': f'https://youtube.com/watch?v={video_id}'
        }
    except Exception as e:
        return {
            'video_id': video_id,
            'title': None,
            'description': None,
            'channel': None,
            'url': f'https://youtube.com/watch?v={video_id}',
            'error': str(e)
        }


def fetch_transcript(video_id: str, preferred_language: str = 'ko') -> dict:
    """영상 자막 가져오기"""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi, FetchedTranscript
    except ImportError:
        return {
            'available': False,
            'error': 'youtube-transcript-api가 설치되어 있지 않습니다. pip install youtube-transcript-api'
        }

    result = {
        'available': False,
        'language': None,
        'text': None,
        'error': None
    }

    try:
        # 새로운 API 형식 (v1.0.0+)
        ytt_api = YouTubeTranscriptApi()

        # 우선순위: 선호 언어 > 영어 > 아무거나
        languages_to_try = [preferred_language]
        if preferred_language != 'en':
            languages_to_try.append('en')

        transcript_data = None
        used_language = None

        for lang in languages_to_try:
            try:
                transcript_data = ytt_api.fetch(video_id, languages=[lang])
                used_language = lang
                break
            except Exception:
                continue

        # 언어 지정 없이 시도
        if not transcript_data:
            try:
                transcript_data = ytt_api.fetch(video_id)
                used_language = 'auto'
            except Exception:
                pass

        if transcript_data:
            if isinstance(transcript_data, FetchedTranscript):
                full_text = ' '.join([seg.text for seg in transcript_data])
            else:
                full_text = ' '.join([seg['text'] if isinstance(seg, dict) else seg.text for seg in transcript_data])
            result['available'] = True
            result['language'] = used_language
            result['text'] = full_text

    except Exception as e:
        result['error'] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(description='YouTube 영상 콘텐츠 추출')
    parser.add_argument('--url', help='YouTube URL')
    parser.add_argument('--video-id', help='영상 ID')
    parser.add_argument('--language', default='ko', help='자막 언어 (기본: ko)')

    args = parser.parse_args()

    # 비디오 ID 결정
    video_id = args.video_id
    if not video_id and args.url:
        video_id = extract_video_id(args.url)

    if not video_id:
        print(json.dumps({'error': 'URL 또는 video-id를 제공해주세요.'}, ensure_ascii=False))
        sys.exit(1)

    # 메타데이터 및 자막 수집
    metadata = fetch_video_metadata(video_id)
    transcript = fetch_transcript(video_id, args.language)

    result = {
        **metadata,
        'transcript': transcript
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
