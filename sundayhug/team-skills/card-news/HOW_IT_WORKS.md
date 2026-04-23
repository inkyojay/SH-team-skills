# Card News Creator 작동 방식

## 개요

유튜브, 웹페이지, PDF 등 다양한 소스에서 콘텐츠를 추출하여 Sunday Hug 스타일의 카드뉴스를 자동 생성하는 스킬입니다.

---

## 전체 워크플로우

```
┌─────────────────────────────────────────────────────────────────┐
│  1. 콘텐츠 소스                                                   │
│     YouTube URL / 웹페이지 / PDF / 텍스트                          │
└─────────────────┬───────────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. 콘텐츠 추출 (fetch_content.py)                                │
│     - 자막/본문 텍스트 추출                                        │
│     - 제목, 메타데이터 수집                                        │
└─────────────────┬───────────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  3. 카드 구조 설계 (Claude가 수행)                                 │
│     - 콘텐츠 분석 → 8-10장 카드 구조                               │
│     - 각 카드별 제목, 본문, 이미지 프롬프트 생성                     │
└─────────────────┬───────────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. 배경 이미지 생성 (gemini_image_api.py)                        │
│     - 각 카드 프롬프트 → Gemini API → PNG 이미지                   │
└─────────────────┬───────────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. HTML 카드 생성                                                │
│     - Sunday Hug 템플릿 + 내용 + 이미지 경로                       │
└─────────────────┬───────────────────────────────────────────────┘
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  6. 이미지 렌더링 (render_cards.py)                               │
│     - HTML → PNG (1080x1350px, 인스타그램 최적)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 스크립트별 역할

### 1. `fetch_content.py` - 콘텐츠 추출

다양한 소스에서 텍스트 콘텐츠를 추출합니다.

```bash
# YouTube
python3 scripts/fetch_content.py --source "https://youtube.com/watch?v=VIDEO_ID"

# 웹페이지
python3 scripts/fetch_content.py --source "https://example.com/article"

# PDF
python3 scripts/fetch_content.py --source "./document.pdf"

# 텍스트 파일
python3 scripts/fetch_content.py --source "./content.txt"
```

**출력 예시:**
```json
{
  "success": true,
  "source_type": "youtube",
  "title": "영상 제목",
  "channel": "채널명",
  "content": "자막 전체 텍스트...",
  "transcript_available": true
}
```

### 2. `gemini_image_api.py` - AI 이미지 생성

Google Gemini API를 사용하여 카드 배경 이미지를 생성합니다.

```bash
# API 키 설정 (최초 1회)
python3 scripts/gemini_image_api.py --setup

# 이미지 생성
python3 scripts/gemini_image_api.py \
  --prompt "cute robot character" \
  --style "soft watercolor, warm pastel colors, Korean aesthetic" \
  --output ./images/01_cover.png
```

**출력 예시:**
```json
{
  "success": true,
  "output": "./images/01_cover.png",
  "prompt": "soft watercolor, warm pastel colors, Korean aesthetic, cute robot character"
}
```

### 3. `render_cards.py` - HTML → PNG 변환

Playwright를 사용하여 HTML 카드를 PNG 이미지로 렌더링합니다.

```bash
# 디렉토리 내 모든 HTML 렌더링
python3 scripts/render_cards.py \
  --input-dir ./html \
  --output-dir ./final

# 단일 파일 렌더링
python3 scripts/render_cards.py \
  --html-file ./card.html \
  --output ./card.png
```

---

## 이미지 생성 프롬프트 구조

### 프롬프트 공식

```
[스타일 접두사] + [콘텐츠 설명]
```

### 권장 스타일 접두사

```
soft watercolor illustration style, warm pastel colors,
friendly and approachable, Korean aesthetic, minimal background
```

### 카드 유형별 프롬프트 예시

| 카드 유형 | 프롬프트 예시 |
|----------|-------------|
| cover | `friendly AI robot with multiple smaller robots around it` |
| content (기술) | `cute robot coding on laptop` |
| content (개념) | `brain with gears and light bulbs, knowledge concept` |
| content (연결) | `connected chain links forming a network` |
| content (속도) | `lightning bolt with speed lines, fast automation concept` |
| content (창작) | `art palette with colorful paint, creative design concept` |
| content (목표) | `rocket launching towards stars, ambitious goals concept` |
| summary | `soft gradient warm colors, abstract peaceful background` |

### 프롬프트 작성 팁

**좋은 예시:**
- `cute friendly robot character, soft watercolor illustration, warm pastel colors`
- `mother holding newborn baby, hospital scene, warm emotional atmosphere`
- `four seasons wheel diagram with sun in center, pastel illustration`

**피해야 할 것:**
- 텍스트 포함 요청 (이미지에 글자 생성 불가)
- 너무 복잡한 구도
- 사실적인 인물 사진 스타일

---

## 카드 구조 설계

### Claude가 생성하는 JSON 구조

```json
{
  "brand": {
    "name": "BUILDER JOSH",
    "theme": "warm"
  },
  "cards": [
    {
      "index": 1,
      "type": "cover",
      "template": "sunday_hug_cover.html",
      "content": {
        "episode": "커서마피아 최수민님 인터뷰",
        "title": "AI 에이전트 100개를\n한 번에 관리하는\n1인 유니콘 개발자",
        "subtitle": "클로드 코드가 압도적인 이유,\n그 비밀을 공개합니다"
      },
      "image_prompt": "friendly AI robot with multiple smaller robots around it"
    },
    {
      "index": 2,
      "type": "content",
      "template": "sunday_hug_content.html",
      "content": {
        "heading": "왜 클로드 코드가 압도적인가?",
        "body": "커서, 앤티 그래비티 같은 도구들도 좋지만\n에이전틱한 기능이 클로드 코드에 비해 너무 떨어져요.\n특히 '서브에이전트' 기능은 클로드 코드만 가능합니다."
      },
      "image_prompt": "cute robot coding on laptop"
    }
  ]
}
```

### 카드 유형

| 유형 | 템플릿 | 용도 | 이미지 |
|------|--------|------|--------|
| cover | sunday_hug_cover.html | 주제 소개, 호기심 유발 | 주제 상징 일러스트 |
| content | sunday_hug_content.html | 본문 내용 전달 | 개념 시각화 |
| full | sunday_hug_full.html | 강조 메시지 | 분위기 이미지 |
| info | sunday_hug_info.html | 리스트형 정리 | 없음 (단색 배경) |
| summary | sunday_hug_summary.html | 핵심 요약 | 부드러운 배경 |

### 8-10장 기본 구성

```
1. cover    - 주제 소개
2. content  - 배경/문제 제기
3. content  - 핵심 개념 1
4. content  - 핵심 개념 2
5. info     - 주요 포인트 정리
6. content  - 실제 사례/적용
7. content  - 추가 팁
8. summary  - 핵심 요약
9. cta      - 마무리 (선택)
```

---

## HTML 템플릿 변수

### sunday_hug_content.html 예시

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="sunday_hug_styles.css">
</head>
<body>
    <div class="card card-content-sh">
        <!-- 배경 이미지 -->
        <img class="background" src="{{BACKGROUND_IMAGE}}" alt="">

        <!-- 그라데이션 오버레이 -->
        <div class="overlay"></div>

        <!-- 콘텐츠 -->
        <div class="content">
            <div class="brand">{{BRAND_NAME}}</div>
            <div class="text-area">
                <div class="heading">{{HEADING}}</div>
                <div class="body">{{BODY}}</div>
            </div>
        </div>
    </div>
</body>
</html>
```

### 변수 목록

| 변수 | 설명 | 예시 |
|------|------|------|
| `{{BRAND_NAME}}` | 브랜드명 | BUILDER JOSH |
| `{{BACKGROUND_IMAGE}}` | 배경 이미지 경로 | ../images/01_cover.png |
| `{{EPISODE}}` | 에피소드/시리즈명 | 커서마피아 최수민님 인터뷰 |
| `{{TITLE}}` | 메인 타이틀 | AI 에이전트 100개를... |
| `{{SUBTITLE}}` | 부제목 | 클로드 코드가 압도적인 이유 |
| `{{HEADING}}` | 카드 소제목 | 왜 클로드 코드가 압도적인가? |
| `{{BODY}}` | 본문 내용 | 3-4문장 |

---

## 파일 구조

```
card-news-creator/
├── SKILL.md                     # 스킬 설명서
├── HOW_IT_WORKS.md              # 작동 방식 설명 (이 파일)
│
├── scripts/
│   ├── fetch_content.py         # 소스 → 텍스트 추출
│   ├── fetch_youtube_content.py # YouTube 전용 (레거시)
│   ├── gemini_image_api.py      # Gemini 이미지 생성
│   ├── nanobanana_api.py        # 나노바나 이미지 생성 (대안)
│   └── render_cards.py          # HTML → PNG 변환
│
├── assets/
│   ├── brand_config.yaml        # 브랜드 설정
│   └── templates/
│       ├── sunday_hug_styles.css    # Sunday Hug 스타일
│       ├── sunday_hug_cover.html    # 커버 카드
│       ├── sunday_hug_content.html  # 콘텐츠 카드
│       ├── sunday_hug_full.html     # 전체 이미지 카드
│       ├── sunday_hug_info.html     # 리스트형 카드
│       ├── sunday_hug_summary.html  # 요약 카드
│       ├── styles.css               # 기본 스타일 (레거시)
│       ├── cover.html               # 기본 커버 (레거시)
│       ├── content.html             # 기본 콘텐츠 (레거시)
│       ├── info.html                # 기본 리스트 (레거시)
│       └── summary.html             # 기본 요약 (레거시)
│
└── references/
    ├── auto-structure-guide.md  # 자동 구조 생성 가이드
    └── card-structure-guide.md  # 카드 유형별 가이드
```

---

## 실행 순서

### 전체 프로세스

```bash
# 0. 사전 설정 (최초 1회)
pip install youtube-transcript-api playwright requests pyyaml beautifulsoup4 PyPDF2 google-genai pillow
playwright install chromium
python3 scripts/gemini_image_api.py --setup

# 1. 콘텐츠 추출
python3 scripts/fetch_content.py --source "https://youtube.com/watch?v=VIDEO_ID"

# 2. (Claude가) 카드 구조 설계 + 이미지 프롬프트 생성

# 3. 작업 폴더 생성
mkdir -p ./output/{images,html,final}

# 4. 배경 이미지 생성 (카드 수만큼 반복)
python3 scripts/gemini_image_api.py \
  --prompt "프롬프트" \
  --style "soft watercolor, warm pastel colors, Korean aesthetic" \
  --output ./output/images/01_cover.png

# 5. CSS 복사
cp assets/templates/sunday_hug_styles.css ./output/html/

# 6. HTML 파일 생성 (템플릿 변수 치환)

# 7. PNG 렌더링
python3 scripts/render_cards.py \
  --input-dir ./output/html \
  --output-dir ./output/final
```

---

## 브랜드 설정

`assets/brand_config.yaml` 파일로 브랜드 커스터마이징:

```yaml
brand:
  name: "MY BRAND"

colors:
  preset: "warm"  # warm, cool, dark, minimal, vibrant

layout:
  preset: "sunday_hug"
  width: 1080
  height: 1350

image_generation:
  style_prefix: "soft watercolor illustration style, warm pastel colors, Korean aesthetic"
```

### 색상 프리셋

| 프리셋 | 적합한 주제 |
|--------|------------|
| warm | 육아, 라이프스타일, 따뜻한 주제 |
| cool | 기술, 비즈니스, 신뢰 |
| dark | 테크, 게임, 모던 |
| minimal | 심플, 고급스러운 주제 |
| vibrant | 에너지, 활력, 젊은 타겟 |

---

## 에러 처리

| 상황 | 해결 |
|------|------|
| API 키 없음 | `python3 scripts/gemini_image_api.py --setup` |
| YouTube 자막 없음 | 영상 설명 기반 또는 직접 내용 입력 |
| 이미지 생성 실패 | 프롬프트 단순화, API 한도 확인 |
| 렌더링 실패 | HTML 문법, CSS 경로 확인 |
| 패키지 미설치 | 상단 pip install 명령어 실행 |

---

## 참고 자료

- [SKILL.md](./SKILL.md) - 스킬 기본 설명
- [auto-structure-guide.md](./references/auto-structure-guide.md) - 자동 구조 생성 가이드
- [card-structure-guide.md](./references/card-structure-guide.md) - 카드 유형별 가이드
- [Google AI Studio](https://aistudio.google.com/apikey) - API 키 발급
