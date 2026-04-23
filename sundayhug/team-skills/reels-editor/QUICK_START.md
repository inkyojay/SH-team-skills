# 릴스 편집 빠른 시작 가이드

## 설치 확인

```bash
# FFmpeg 설치 (Mac)
brew install ffmpeg

# FFmpeg 설치 (Ubuntu)
sudo apt install ffmpeg

# Python 패키지
pip install google-generativeai pillow

# Gemini API 키 설정
export GEMINI_API_KEY="your-api-key"
```

## 기본 사용법

### 1. 자동 모드

```
이 영상 릴스로 만들어줘
~/videos/product.mp4
```

AI가 영상을 분석하고 최적의 클립과 카피를 추천합니다.

### 2. 수동 모드

```
영상의 10-40초 구간만 릴스로 만들어줘
헤드라인: "아기의 꿀잠을 위한 선택"
CTA: "지금 구매하기"
```

### 3. 9:16 변환만

```
이 영상을 세로로 변환해줘
```

## 릴스 규격

| 항목 | 값 |
|------|-----|
| 비율 | 9:16 |
| 해상도 | 1080×1920 |
| 최대 길이 | 90초 |
| 안전 영역 | 상하단 14% |

## 출력 위치

```
reels-editor/output/
├── reels_YYYYMMDD_HHMMSS.mp4
├── thumbnail_YYYYMMDD_HHMMSS.jpg
└── metadata_YYYYMMDD_HHMMSS.json
```

## 문제 해결

### FFmpeg 없음
```bash
brew install ffmpeg  # Mac
sudo apt install ffmpeg  # Ubuntu
```

### API 키 없음
- 수동 모드로 전환하거나
- `export GEMINI_API_KEY="your-key"` 설정

### 영상 길이 초과
- 90초 이하로 트리밍 필요
- 구간을 지정해서 잘라주세요
