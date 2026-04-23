# 자동 카드 구조 생성 가이드

이 문서는 콘텐츠를 분석하여 카드뉴스 구조를 자동으로 생성하는 방법을 설명합니다.

## 콘텐츠 분석 프로세스

### 1단계: 핵심 주제 추출

콘텐츠에서 다음을 파악:
- **메인 주제**: 전체 콘텐츠가 다루는 핵심 주제 (커버 카드용)
- **서브 주제들**: 세부적으로 다루는 개별 주제들 (콘텐츠 카드용)
- **핵심 포인트**: 요약할 수 있는 주요 내용 (요약 카드용)

### 2단계: 카드 구조 설계

**8-10장 기본 구조:**

```yaml
cards:
  - type: cover
    purpose: 주제 소개, 관심 유도
    content:
      episode: "시리즈명 또는 에피소드"
      title: "메인 타이틀 (핵심 질문 또는 주제)"
      subtitle: "부제목 (기대효과 또는 요약)"
    image_prompt: "주제를 상징하는 일러스트"

  - type: content
    purpose: 배경/문제 제기
    content:
      heading: "왜 이게 중요한가?"
      body: "3-4문장으로 배경 설명"
    image_prompt: "문제 상황을 나타내는 이미지"

  - type: content
    purpose: 핵심 개념 1
    content:
      heading: "첫 번째 핵심 개념"
      body: "개념 설명 및 예시"
    image_prompt: "개념을 시각화한 이미지"

  - type: content
    purpose: 핵심 개념 2
    content:
      heading: "두 번째 핵심 개념"
      body: "개념 설명 및 예시"
    image_prompt: "개념을 시각화한 이미지"

  - type: info
    purpose: 핵심 포인트 정리
    content:
      title: "알아두면 좋은 포인트"
      items:
        - icon: "💡"
          text: "첫 번째 포인트"
        - icon: "📌"
          text: "두 번째 포인트"
        - icon: "✨"
          text: "세 번째 포인트"

  - type: content
    purpose: 실제 적용/사례
    content:
      heading: "실제로 어떻게 적용할까?"
      body: "구체적인 사례나 방법"
    image_prompt: "실제 적용 상황 이미지"

  - type: content
    purpose: 추가 팁 또는 주의사항
    content:
      heading: "주의할 점"
      body: "추가적인 팁이나 주의사항"
    image_prompt: "팁을 나타내는 이미지"

  - type: summary
    purpose: 핵심 요약
    content:
      title: "오늘의 핵심 정리"
      points:
        - "핵심 포인트 1"
        - "핵심 포인트 2"
        - "핵심 포인트 3"
    image_prompt: "정리를 나타내는 이미지"

  - type: cta (선택)
    purpose: 마무리, 행동 유도
    content:
      message: "마무리 메시지"
      action: "행동 유도 문구"
```

### 3단계: 이미지 프롬프트 생성

각 카드에 맞는 나노바나 이미지 프롬프트 생성 규칙:

**스타일 접두사 (brand_config.yaml에서 설정):**
```
soft watercolor illustration style, warm pastel colors,
friendly and approachable, Korean aesthetic, minimal background
```

**카드 유형별 프롬프트 패턴:**

| 카드 유형 | 프롬프트 패턴 |
|----------|-------------|
| cover | `[주제 상징물], centered composition, welcoming atmosphere` |
| content | `[개념 시각화], soft lighting, simple clean background` |
| info | 이미지 없음 (단색 배경) |
| summary | `abstract warm colors, soft gradient, peaceful` |
| cta | `[행동 관련 이미지], inviting, hopeful atmosphere` |

**예시 프롬프트:**
- 주제가 "AI 에이전트"일 때: `friendly robot character, soft watercolor style, warm colors, simple background`
- 주제가 "육아"일 때: `mother and baby illustration, soft pastel colors, warm cozy atmosphere`
- 주제가 "투자"일 때: `coins and growth plant, watercolor illustration, hopeful colors`

## 자동 구조 생성 JSON 형식

콘텐츠 분석 후 다음 JSON 형식으로 출력:

```json
{
  "source": {
    "type": "youtube",
    "title": "원본 제목",
    "url": "원본 URL"
  },
  "brand": {
    "name": "BRAND NAME",
    "theme": "warm"
  },
  "cards": [
    {
      "index": 1,
      "type": "cover",
      "template": "sunday_hug_cover.html",
      "content": {
        "episode": "EP 1. 시리즈명",
        "title": "메인 타이틀",
        "subtitle": "부제목"
      },
      "image_prompt": "이미지 생성 프롬프트"
    },
    {
      "index": 2,
      "type": "content",
      "template": "sunday_hug_content.html",
      "content": {
        "heading": "소제목",
        "body": "본문 내용 (3-4문장)"
      },
      "image_prompt": "이미지 생성 프롬프트"
    }
  ]
}
```

## 콘텐츠 분량 가이드

| 항목 | 권장 분량 |
|------|----------|
| 커버 타이틀 | 10-20자 |
| 커버 부제목 | 20-40자 |
| 카드 소제목 | 8-15자 |
| 카드 본문 | 60-120자 (3-4문장) |
| 요약 포인트 | 각 20-40자 |

## 톤앤매너

- 친근한 대화체 사용 ("~해요", "~거든요")
- 전문 용어는 쉽게 풀어서 설명
- 질문형 제목으로 호기심 유발
- 이모지 적절히 활용 (info 카드)
