---
name: card-news-creator
description: 카드뉴스 제작 (인스타그램 스타일)
triggers:
  - "카드뉴스 만들어줘"
  - "인스타 카드뉴스"
  - "유튜브 카드뉴스로"
---

# Card News Creator

다양한 소스에서 콘텐츠를 추출하여 고품질 카드뉴스로 변환.

## 사전 요구사항

```bash
pip install youtube-transcript-api playwright requests pyyaml beautifulsoup4 PyPDF2
playwright install chromium
```

**나노바나 API 설정 (이미지 생성용):**
```bash
python3 scripts/nanobanana_api.py --setup
```

## 워크플로우

### 1. 콘텐츠 추출

다양한 소스에서 콘텐츠 추출:

```bash
# YouTube
python3 scripts/fetch_content.py --source "https://youtube.com/watch?v=..."

# 웹페이지
python3 scripts/fetch_content.py --source "https://example.com/article"

# PDF 파일
python3 scripts/fetch_content.py --source "./document.pdf"

# 텍스트 파일
python3 scripts/fetch_content.py --source "./content.txt"
```

### 2. 카드 구조 자동 생성

[references/auto-structure-guide.md](references/auto-structure-guide.md) 참조하여 콘텐츠 분석 후 8-10장 카드 구조 설계:

1. **cover** - 주제 소개, 호기심 유발
2. **content** x 5-7장 - 본문 내용 (카드당 3-4문장)
3. **info** - 핵심 포인트 리스트
4. **summary** - 핵심 요약
5. **cta** (선택) - 마무리

**출력 형식:** JSON으로 카드 구조 + 이미지 프롬프트 생성

### 3. 배경 이미지 생성 (나노바나 API)

```bash
# 단일 이미지
python3 scripts/nanobanana_api.py \
  --prompt "friendly robot character, soft watercolor illustration" \
  --style "warm pastel colors, Korean aesthetic" \
  --output ./images/01_background.png

# 스타일 접두사는 brand_config.yaml에서 설정
```

**권장 스타일 프롬프트:**
```
soft watercolor illustration style, warm pastel colors,
friendly and approachable, Korean aesthetic, minimal background
```

### 4. 브랜드 설정

`assets/brand_config.yaml` 수정하여 브랜드 커스터마이징:

```yaml
brand:
  name: "MY BRAND"

colors:
  preset: "warm"  # warm, cool, dark, minimal, vibrant

layout:
  preset: "sunday_hug"  # sunday_hug, modern, minimal

image_generation:
  style_prefix: "soft watercolor illustration style, warm colors"
```

### 5. HTML 카드 생성

**Sunday Hug 스타일 템플릿 사용:**

```
assets/templates/
├── sunday_hug_styles.css    # 메인 스타일
├── sunday_hug_cover.html    # 커버 카드
├── sunday_hug_content.html  # 콘텐츠 카드 (이미지+텍스트)
├── sunday_hug_full.html     # 전체 이미지 배경
├── sunday_hug_info.html     # 리스트형 카드
└── sunday_hug_summary.html  # 요약 카드
```

템플릿의 `{{변수}}`를 실제 내용으로 교체:
- `{{BRAND_NAME}}` - 브랜드명
- `{{BACKGROUND_IMAGE}}` - 배경 이미지 경로
- `{{TITLE}}`, `{{HEADING}}`, `{{BODY}}` 등

### 6. 이미지 렌더링

```bash
python3 scripts/render_cards.py \
  --input-dir ./card_output \
  --output-dir ./card_images
```

## 카드 유형별 가이드

| 유형 | 템플릿 | 용도 | 이미지 |
|------|--------|------|--------|
| cover | sunday_hug_cover | 주제 소개 | 주제 상징 일러스트 |
| content | sunday_hug_content | 본문 전달 | 개념 시각화 |
| full | sunday_hug_full | 강조 메시지 | 분위기 이미지 |
| info | sunday_hug_info | 리스트 정리 | 없음 (단색 배경) |
| summary | sunday_hug_summary | 핵심 요약 | 부드러운 배경 |

## 이미지 프롬프트 작성 팁

**좋은 프롬프트 예시:**
- `cute horse character wearing green saddle, soft watercolor, warm spring colors`
- `mother holding newborn baby, hospital scene, warm emotional atmosphere`
- `four seasons wheel diagram with sun in center, pastel illustration`

**피해야 할 것:**
- 텍스트 포함 요청 (이미지에 글자 생성 불가)
- 너무 복잡한 구도
- 사실적인 인물 사진 스타일

## 파일 구조

```
작업폴더/
├── brand_config.yaml      # 브랜드 설정 (복사해서 사용)
├── card_structure.json    # 자동 생성된 카드 구조
├── images/                # 나노바나 생성 이미지
│   ├── 01_background.png
│   └── ...
├── html/                  # 생성된 HTML 파일
│   ├── sunday_hug_styles.css
│   ├── 01_cover.html
│   └── ...
└── output/                # 최종 PNG 이미지
    ├── 01_cover.png
    └── ...
```

## 에러 처리

| 상황 | 해결 |
|------|------|
| 나노바나 API 키 없음 | `python3 scripts/nanobanana_api.py --setup` |
| YouTube 자막 없음 | 영상 설명 기반 또는 직접 내용 입력 |
| 이미지 생성 실패 | 프롬프트 단순화, API 한도 확인 |
| 렌더링 실패 | HTML 문법, CSS 경로 확인 |

## 참고 자료

- [자동 구조 생성 가이드](references/auto-structure-guide.md)
- [카드 구조 가이드](references/card-structure-guide.md)
- [나노바나 API 문서](https://nanobnana.com/docs)
