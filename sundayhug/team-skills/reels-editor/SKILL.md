---
name: reels-editor
description: 릴스 영상 편집 (9:16, 1080x1920)
triggers:
  - "릴스 편집"
  - "릴스 만들어줘"
  - "영상 세로로 변환"
  - "인스타 릴스"
---

# Instagram Reels 영상 편집 스킬

사용자가 업로드한 영상을 Instagram Reels 광고 형식(9:16, 1080x1920, 최대 90초)으로 자동 편집합니다.

## 기능

- **AI 영상 분석**: Gemini Vision API로 영상 내용 분석 및 편집 추천
- **9:16 변환**: 블러 배경으로 세로 영상 변환
- **클립 편집**: 트리밍, 여러 구간 병합
- **오버레이**: 헤드라인, CTA 버튼 추가

## 사용법

### 자동 모드 (AI 분석 기반)

```bash
python scripts/generate_reels.py \
  --video input.mp4 \
  --mode auto \
  --output output/
```

### 수동 모드

```bash
python scripts/generate_reels.py \
  --video input.mp4 \
  --mode manual \
  --clips "10-40,60-80" \
  --headline "매일 밤 꿀잠을 선물하세요" \
  --cta "지금 구매하기" \
  --output output/
```

## 개별 스크립트

### 1. 9:16 블러 배경 변환

```bash
python scripts/resize_video.py \
  --video input.mp4 \
  --output resized.mp4
```

### 2. 영상 트리밍

```bash
# 단일 구간
python scripts/trim_video.py \
  --video input.mp4 \
  --start 10 \
  --end 40 \
  --output trimmed.mp4

# 여러 구간 병합
python scripts/trim_video.py \
  --video input.mp4 \
  --clips "5-20,45-60,80-90" \
  --output merged.mp4
```

### 3. 텍스트 오버레이

```bash
python scripts/add_overlay.py \
  --video input.mp4 \
  --headline "매일 밤 꿀잠을 선물하세요" \
  --cta "지금 구매하기" \
  --output overlayed.mp4
```

### 4. AI 영상 분석

```bash
python scripts/analyze_video.py \
  --video input.mp4 \
  --output analysis.json \
  --context "수면 베개 제품 광고"
```

### 5. 프레임 추출

```bash
python scripts/extract_frames.py \
  --video input.mp4 \
  --output frames/ \
  --mode interval \
  --interval 5
```

## 출력 파일

자동 모드 실행 시 다음 파일이 생성됩니다:

```
output/
├── reels_YYYYMMDD_HHMMSS.mp4    # 최종 릴스 영상
├── thumbnail_YYYYMMDD_HHMMSS.jpg  # 썸네일
├── analysis.json                   # AI 분석 결과
└── metadata_YYYYMMDD_HHMMSS.json  # 메타데이터
```

## 릴스 규격

| 항목 | 규격 |
|------|------|
| 화면 비율 | 9:16 |
| 해상도 | 1080×1920 |
| 최대 길이 | 90초 |
| 안전 영역 | 상하단 14% (268px) |
| 파일 형식 | MP4 (H.264) |

## 의존성

```bash
# FFmpeg (필수)
brew install ffmpeg

# Python 패키지
pip install google-generativeai pillow

# Gemini API 키 설정
export GEMINI_API_KEY="your-api-key"
```

## 참고 문서

- [릴스 규격 가이드](references/reels-specs.md)
- [오버레이 템플릿 가이드](references/overlay-templates.md)

## 에이전트 사용

이 스킬은 `reels-editor-agent`와 함께 사용됩니다. 에이전트는 사용자와 대화하며 영상 편집을 자동으로 수행합니다.

### 예시 요청

- "test.mp4 영상으로 릴스 광고 만들어줘"
- "이 영상을 세로로 변환하고 자막 넣어줘"
- "영상에서 10초부터 40초까지만 잘라서 릴스로 만들어줘"
