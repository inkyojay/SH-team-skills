#!/usr/bin/env python3
"""
다양한 소스에서 콘텐츠 추출

지원 소스:
- YouTube URL
- 웹페이지 URL
- PDF 파일
- 텍스트 파일

Usage:
    python fetch_content.py --source "https://youtube.com/watch?v=..."
    python fetch_content.py --source "https://example.com/article"
    python fetch_content.py --source "./document.pdf"
    python fetch_content.py --source "./content.txt"

Requirements:
    pip install requests beautifulsoup4 youtube-transcript-api PyPDF2
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


def detect_source_type(source: str) -> str:
    """소스 타입 감지"""
    # 파일 경로인 경우
    if Path(source).exists():
        suffix = Path(source).suffix.lower()
        if suffix == ".pdf":
            return "pdf"
        elif suffix in [".txt", ".md"]:
            return "text"
        elif suffix in [".html", ".htm"]:
            return "html"
        else:
            return "text"

    # URL인 경우
    if source.startswith(("http://", "https://")):
        parsed = urlparse(source)
        domain = parsed.netloc.lower()

        if "youtube.com" in domain or "youtu.be" in domain:
            return "youtube"
        else:
            return "webpage"

    return "text"


def extract_youtube_video_id(url: str) -> str | None:
    """YouTube URL에서 비디오 ID 추출"""
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


def fetch_youtube(url: str, language: str = "ko") -> dict:
    """YouTube 콘텐츠 추출"""
    video_id = extract_youtube_video_id(url)
    if not video_id:
        return {"success": False, "error": "유효하지 않은 YouTube URL"}

    result = {
        "success": True,
        "source_type": "youtube",
        "video_id": video_id,
        "url": url,
        "title": None,
        "description": None,
        "channel": None,
        "content": None
    }

    # 메타데이터 추출
    try:
        req = urllib.request.Request(
            f"https://www.youtube.com/watch?v={video_id}",
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8')

        title_match = re.search(r'<title>(.+?)</title>', html)
        result["title"] = title_match.group(1).replace(' - YouTube', '').strip() if title_match else None

        desc_match = re.search(r'<meta name="description" content="([^"]*)"', html)
        result["description"] = desc_match.group(1) if desc_match else None

        channel_match = re.search(r'"ownerChannelName":"([^"]+)"', html)
        result["channel"] = channel_match.group(1) if channel_match else None
    except Exception as e:
        result["metadata_error"] = str(e)

    # 자막 추출
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        ytt_api = YouTubeTranscriptApi()
        transcript = None

        for lang in [language, 'en']:
            try:
                transcript = ytt_api.fetch(video_id, languages=[lang])
                break
            except:
                continue

        if not transcript:
            try:
                transcript = ytt_api.fetch(video_id)
            except:
                pass

        if transcript:
            result["content"] = ' '.join([seg.text for seg in transcript])
            result["transcript_available"] = True
        else:
            result["content"] = result.get("description", "")
            result["transcript_available"] = False

    except ImportError:
        result["content"] = result.get("description", "")
        result["transcript_error"] = "youtube-transcript-api 미설치"
    except Exception as e:
        result["content"] = result.get("description", "")
        result["transcript_error"] = str(e)

    return result


def fetch_webpage(url: str) -> dict:
    """웹페이지 콘텐츠 추출"""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return {
            "success": False,
            "error": "beautifulsoup4 미설치. pip install beautifulsoup4"
        }

    try:
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')

        soup = BeautifulSoup(html, 'html.parser')

        # 불필요한 태그 제거
        for tag in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe']):
            tag.decompose()

        # 제목 추출
        title = None
        if soup.title:
            title = soup.title.string
        if not title:
            h1 = soup.find('h1')
            title = h1.get_text(strip=True) if h1 else None

        # 본문 추출 (article 태그 우선)
        article = soup.find('article')
        if article:
            content = article.get_text(separator='\n', strip=True)
        else:
            # main 또는 body에서 추출
            main = soup.find('main') or soup.body
            if main:
                content = main.get_text(separator='\n', strip=True)
            else:
                content = soup.get_text(separator='\n', strip=True)

        # 빈 줄 정리
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        content = '\n'.join(lines)

        return {
            "success": True,
            "source_type": "webpage",
            "url": url,
            "title": title,
            "content": content[:30000]  # 최대 30000자
        }

    except Exception as e:
        return {
            "success": False,
            "source_type": "webpage",
            "url": url,
            "error": str(e)
        }


def fetch_pdf(file_path: str) -> dict:
    """PDF 파일에서 텍스트 추출"""
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        return {
            "success": False,
            "error": "PyPDF2 미설치. pip install PyPDF2"
        }

    path = Path(file_path)
    if not path.exists():
        return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}

    try:
        reader = PdfReader(str(path))
        content = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                content.append(text)

        return {
            "success": True,
            "source_type": "pdf",
            "file_path": str(path.absolute()),
            "title": path.stem,
            "page_count": len(reader.pages),
            "content": '\n\n'.join(content)
        }

    except Exception as e:
        return {
            "success": False,
            "source_type": "pdf",
            "file_path": file_path,
            "error": str(e)
        }


def fetch_text(file_path: str) -> dict:
    """텍스트 파일 읽기"""
    path = Path(file_path)
    if not path.exists():
        return {"success": False, "error": f"파일을 찾을 수 없습니다: {file_path}"}

    try:
        content = path.read_text(encoding='utf-8')
        return {
            "success": True,
            "source_type": "text",
            "file_path": str(path.absolute()),
            "title": path.stem,
            "content": content
        }
    except Exception as e:
        return {
            "success": False,
            "source_type": "text",
            "file_path": file_path,
            "error": str(e)
        }


def fetch_content(source: str, language: str = "ko") -> dict:
    """소스에서 콘텐츠 추출 (자동 타입 감지)"""
    source_type = detect_source_type(source)

    if source_type == "youtube":
        return fetch_youtube(source, language)
    elif source_type == "webpage":
        return fetch_webpage(source)
    elif source_type == "pdf":
        return fetch_pdf(source)
    else:
        return fetch_text(source)


def main():
    parser = argparse.ArgumentParser(description="다양한 소스에서 콘텐츠 추출")
    parser.add_argument("--source", required=True, help="콘텐츠 소스 (URL, 파일 경로)")
    parser.add_argument("--type", choices=["youtube", "webpage", "pdf", "text"],
                        help="소스 타입 (자동 감지됨)")
    parser.add_argument("--language", default="ko", help="선호 언어 (YouTube 자막용)")

    args = parser.parse_args()

    result = fetch_content(args.source, args.language)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
