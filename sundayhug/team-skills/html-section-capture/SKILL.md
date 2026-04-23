---
name: html-section-capture
description: HTML 상세페이지 파일을 섹션별로 구분하여 고해상도 이미지로 변환하는 skill. 사용자가 (1) HTML 파일을 이미지로 변환 요청하거나, (2) 상세페이지를 섹션별 이미지로 나눠달라고 하거나, (3) HTML을 고해상도 스크린샷으로 캡처해달라고 할 때 사용.
---

# HTML Section Capture

HTML 상세페이지를 섹션별로 자동 감지하여 고해상도 이미지로 캡처.

## 사전 요구사항

**필수 패키지:**
```bash
pip install playwright
playwright install chromium
```

## 워크플로우

### 1. 기본 사용

HTML 파일을 섹션별 이미지로 변환:

```bash
python3 scripts/capture_sections.py --html-file input.html --output-dir ./output
```

**결과:** `./output/` 폴더에 섹션별 PNG 이미지 생성.

### 2. 고해상도 옵션

더 높은 해상도가 필요한 경우:

```bash
# 3배 해상도 (인쇄용)
python3 scripts/capture_sections.py --html-file input.html --output-dir ./output --scale 3

# 4배 해상도 (초고해상도)
python3 scripts/capture_sections.py --html-file input.html --output-dir ./output --scale 4
```

### 3. 커스텀 섹션 선택자

특정 CSS 선택자로 섹션 지정:

```bash
python3 scripts/capture_sections.py \
    --html-file input.html \
    --output-dir ./output \
    --selectors "section,.product-section,div.content-block"
```

### 4. 전체 페이지 포함

섹션 이미지와 함께 전체 페이지도 캡처:

```bash
python3 scripts/capture_sections.py --html-file input.html --output-dir ./output --full-page
```

## 스크립트 옵션

### capture_sections.py

| 옵션 | 설명 |
|------|------|
| `--html-file`, `-f` | 변환할 HTML 파일 경로 (필수) |
| `--output-dir`, `-o` | 이미지 저장 디렉토리 (기본: ./output) |
| `--scale`, `-s` | 이미지 스케일 (기본: 2.0 = 2배 해상도) |
| `--width`, `-w` | 뷰포트 너비 (기본: 1440px) |
| `--selectors` | 섹션 CSS 선택자 (쉼표 구분) |
| `--full-page` | 전체 페이지 스크린샷 포함 |
| `--format` | 이미지 포맷: png 또는 jpeg (기본: png) |

## 섹션 자동 감지

스크립트는 다음 선택자로 섹션을 자동 감지:
- `section` 태그
- `[class*='section']`, `[class*='Section']`
- `[class*='block']`, `[class*='Block']`
- `[class*='container']`, `[class*='Container']`
- `article`, `main > div`

섹션을 찾지 못하면 페이지를 일정 높이(1200px)로 자동 분할.

## 출력 파일명

이미지 파일명 형식: `{순번}_{클래스명}.png`

예시:
```
01_hero-section.png
02_product-info.png
03_detail-content.png
04_review-section.png
```

## 에러 처리

| 상황 | 안내 메시지 |
|------|------------|
| playwright 미설치 | "pip install playwright && playwright install chromium" |
| HTML 파일 없음 | "HTML 파일을 찾을 수 없습니다" |
| 섹션 없음 | 전체 페이지를 자동 분할하여 캡처 |
