---
name: html2img
description: HTML을 이미지로 변환
triggers:
  - "HTML 이미지로 변환해줘"
  - "고해상도 스크린샷"
  - "페이지 캡처"
---

# HTML to Image

HTML 파일 전체를 고해상도 이미지로 변환합니다.

## 트리거
- "HTML 이미지로 변환해줘"
- "고해상도 스크린샷"
- "페이지 캡처"

## 기능
- HTML 파일을 PNG 이미지로 변환
- 2x~4x 고해상도 스케일 지원
- 섹션별 분할 캡처 가능

## 옵션
| 옵션 | 설명 | 기본값 |
|------|------|--------|
| scale | 이미지 배율 | 2.0 |
| width | 뷰포트 너비 | 1440px |
| format | png 또는 jpeg | png |
| full-page | 전체 페이지 | false |

## 해상도 가이드
- 2x: 웹용 (기본)
- 3x: 인쇄용
- 4x: 초고해상도

## 사용법
```bash
python3 skills/tools/html-section-capture/scripts/capture_sections.py --html-file input.html --output-dir ./output --full-page
```

> **참고**: 실제 스크립트는 `html-section-capture` 스킬에 포함되어 있습니다.

## 사전 요구사항
```bash
pip install playwright
playwright install chromium
```
