# 브랜드 공식형 광고 템플릿

고정 헤더(로고+제품명+썸네일) + 하단 콘텐츠 순환 구조의 전문적 브랜드 공식 광고 템플릿입니다.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 30~45초 |

## 특징

- **고정 헤더**: 브랜드 로고 + 제품명 + 썸네일이 전체 영상 동안 상단 고정
- **컬러 하이라이트 자막**: 핵심 키워드에 브랜드 컬러 배경
- **전문적 톤**: 격식체 나레이션, 세련된 레이아웃
- **일관된 브랜딩**: 전체 영상에서 브랜드 아이덴티티 유지

## 파일 구조

```
branded-showcase/
├── BrandedShowcase.tsx     # 메인 컴포넌트
├── types.ts                # BrandedShowcaseConfig 타입
├── analysis.md             # 레퍼런스 영상 분석
├── components/
│   ├── BrandHeader.tsx     # 고정 상단 헤더 (로고+제품명+썸네일)
│   ├── FeatureSlide.tsx    # 특징 소개 슬라이드
│   └── HighlightCaption.tsx # 컬러 하이라이트 자막
├── references/             # 레퍼런스 영상
└── README.md
```

## 레이아웃

```
┌─────────────────┐
│ [로고]           │  ← 고정 헤더 (z-index: 10)
│ [제품명]         │
│ [제품 썸네일]    │
│─────────────────│
│                  │
│   비디오 콘텐츠   │  ← 씬마다 전환
│                  │
│ [하이라이트 자막] │
└─────────────────┘
```

## 사용법

```tsx
import type { BrandedShowcaseConfig } from "./types";

const config: BrandedShowcaseConfig = {
  brand: { name: "MY BRAND", color: "#5a7d65" },
  header: {
    logoSrc: "logo.png",
    productName: "실키밤부 슬리핑백",
    productImageSrc: "product-thumb.png",
  },
  scenes: [
    {
      type: "intro",
      videoSrc: "intro.mp4",
      durationSeconds: 5,
      caption: {
        text: "아기의 꿀잠을 위한 선택",
        highlightWords: ["꿀잠"],
      },
      narrationSrc: "audio/scene1.mp3",
    },
    {
      type: "feature",
      videoSrc: "feature1.mp4",
      durationSeconds: 10,
      caption: {
        text: "실키밤부 원단으로 부드러운 촉감",
        highlightWords: ["실키밤부"],
      },
      narrationSrc: "audio/scene2.mp3",
    },
    {
      type: "feature",
      videoSrc: "feature2.mp4",
      durationSeconds: 10,
      caption: {
        text: "OEKO-TEX 인증 안전한 소재",
        highlightWords: ["OEKO-TEX 인증"],
      },
      narrationSrc: "audio/scene3.mp3",
    },
    {
      type: "feature",
      videoSrc: "feature3.mp4",
      durationSeconds: 10,
      caption: {
        text: "양방향 지퍼로 기저귀 교체 편리",
        highlightWords: ["양방향 지퍼"],
      },
    },
    {
      type: "cta",
      videoSrc: "cta.mp4",
      durationSeconds: 5,
      caption: { text: "지금 만나보세요" },
    },
  ],
};
```

## 공유 컴포넌트

이 템플릿은 `meta-reels-ad`의 다음 컴포넌트를 재사용합니다:
- `Narration` - Audio 래퍼
- `calculateSceneStarts` - 씬 시작 프레임 계산 유틸
