# 비교 추천형 광고 템플릿

문제 제시 → 제품 비교 → 솔루션 시연 → 차별화 → CTA 흐름의 정보 전달형 비교 광고 템플릿입니다.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 45~60초 |

## 특징

- **제품 비교 그리드**: 2~4개 제품을 그리드로 비교, 추천 제품 하이라이트
- **필(pill) 스타일 자막**: 둥근 반투명 배경의 정보 전달형 자막
- **논리적 설득 흐름**: 문제 → 비교 → 솔루션 → 차별화
- **부드러운 전환**: 페이드 기반 (기본 10프레임)

## 파일 구조

```
comparison/
├── Comparison.tsx          # 메인 컴포넌트
├── types.ts                # ComparisonConfig 타입
├── analysis.md             # 레퍼런스 영상 분석
├── components/
│   ├── ProblemScene.tsx    # 문제 제시 씬
│   ├── ProductGrid.tsx     # 제품 비교 그리드
│   ├── SolutionDemo.tsx    # 솔루션 시연
│   └── PillCaption.tsx     # 둥근 필 스타일 자막
├── references/             # 레퍼런스 영상
└── README.md
```

## 씬 타입

| 타입 | 컴포넌트 | 용도 |
|------|----------|------|
| `problem` | ProblemScene | 문제/고민 제시 (어두운 오버레이) |
| `comparison` | ProductGrid | 제품 비교 그리드 (이미지 기반) |
| `solution` | SolutionDemo | 솔루션 시연 |
| `differentiator` | SolutionDemo | 차별화 포인트 |
| `cta` | SolutionDemo | 구매 유도 |

## 사용법

```tsx
import type { ComparisonConfig } from "./types";

const config: ComparisonConfig = {
  brand: { name: "MY BRAND", color: "#4A90D9" },
  scenes: [
    {
      type: "problem",
      videoSrc: "problem-bg.mp4",
      durationSeconds: 8,
      caption: { text: "아기 잠옷, 뭘 골라야 할지 모르겠다면?" },
      narrationSrc: "audio/scene1.mp3",
    },
    {
      type: "comparison",
      videoSrc: "comparison-bg.mp4",
      durationSeconds: 17,
      caption: { text: "4가지 인기 제품을 비교해봤어요" },
      questionText: "어떤 게 좋을까?",
      products: [
        { name: "A 브랜드", imageSrc: "product-a.png", description: "면 100%" },
        { name: "B 브랜드", imageSrc: "product-b.png", description: "폴리 혼방" },
        { name: "C 브랜드", imageSrc: "product-c.png", description: "오가닉" },
        {
          name: "MY BRAND",
          imageSrc: "product-d.png",
          description: "실키밤부",
          isRecommended: true,
        },
      ],
    },
    {
      type: "solution",
      videoSrc: "solution-demo.mp4",
      durationSeconds: 17,
      caption: { text: "실키밤부 원단으로 통기성이 달라요" },
      narrationSrc: "audio/scene3.mp3",
    },
    {
      type: "differentiator",
      videoSrc: "differentiator.mp4",
      durationSeconds: 8,
      caption: { text: "유일하게 OEKO-TEX 인증까지" },
    },
    {
      type: "cta",
      videoSrc: "cta.mp4",
      durationSeconds: 5,
      caption: { text: "지금 바로 확인하세요" },
    },
  ],
};
```

## 공유 컴포넌트

이 템플릿은 `meta-reels-ad`의 다음 컴포넌트를 재사용합니다:
- `Narration` - Audio 래퍼
- `calculateSceneStarts` - 씬 시작 프레임 계산 유틸
