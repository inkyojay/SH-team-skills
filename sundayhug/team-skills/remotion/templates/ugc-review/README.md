# UGC 리뷰형 광고 템플릿

셀카 훅 → 검색 화면 → 제품 시연 → 기능 소개 → CTA 흐름의 캐주얼 UGC 스타일 광고 템플릿입니다.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 30~45초 |

## 특징

- **셀카 훅**: 카메라를 직접 보며 시청자 관심 끌기
- **검색 화면**: 네이버/쇼핑 검색 UI로 신뢰감 형성
- **강조 키워드**: 핵심 단어 노랑(#FFE53B) 하이라이트
- **빠른 컷**: UGC 느낌의 짧은 트랜지션 (기본 4프레임)
- **나레이션 외부 배치**: meta-reels-ad와 동일 패턴 적용

## 파일 구조

```
ugc-review/
├── UgcReview.tsx          # 메인 컴포넌트
├── types.ts               # UgcReviewConfig 타입
├── analysis.md            # 레퍼런스 영상 분석
├── components/
│   ├── SelfieHook.tsx     # 셀카/미러 훅 씬
│   ├── SearchScreen.tsx   # 네이버 검색 화면
│   ├── DemoClip.tsx       # 제품 시연 클립
│   └── UgcCaption.tsx     # 캐주얼 스타일 자막 (키워드 하이라이트)
├── references/            # 레퍼런스 영상
└── README.md
```

## 씬 타입

| 타입 | 컴포넌트 | 용도 |
|------|----------|------|
| `selfie-hook` | SelfieHook | 첫 씬, 셀카 앵글로 훅 |
| `search-screen` | SearchScreen | 검색 화면 + 플랫폼 뱃지 |
| `demo-clip` | DemoClip | 제품 시연 (기본) |
| `feature` | DemoClip | 기능 소개 |
| `cta` | DemoClip | 구매 유도 |

## 사용법

```tsx
import type { UgcReviewConfig } from "./types";

const config: UgcReviewConfig = {
  brand: { name: "MY BRAND", color: "#5a7d65" },
  highlightColor: "#FFE53B",
  searchOverlay: {
    platform: "naver",
    searchQuery: "아기 슬리핑백",
  },
  scenes: [
    {
      type: "selfie-hook",
      videoSrc: "selfie-hook.mp4",
      durationSeconds: 5,
      caption: {
        text: "이거 진짜 대박이에요",
        highlightWords: ["대박"],
      },
      narrationSrc: "audio/scene1.mp3",
    },
    {
      type: "search-screen",
      videoSrc: "naver-search.mp4",
      durationSeconds: 5,
      caption: {
        text: "네이버에서 찾아봤는데",
      },
    },
    {
      type: "demo-clip",
      videoSrc: "product-demo.mp4",
      durationSeconds: 12,
      caption: {
        text: "실제로 써보니까 완전 다르더라구요",
        highlightWords: ["완전 다르더라구요"],
      },
      narrationSrc: "audio/scene3.mp3",
    },
    {
      type: "feature",
      videoSrc: "feature-closeup.mp4",
      durationSeconds: 11,
      caption: {
        text: "실키밤부 원단이라 진짜 부드러워요",
        highlightWords: ["실키밤부"],
      },
      narrationSrc: "audio/scene4.mp3",
    },
    {
      type: "cta",
      videoSrc: "cta.mp4",
      durationSeconds: 5,
      caption: {
        text: "링크 타고 확인해보세요!",
      },
      narrationSrc: "audio/scene5.mp3",
    },
  ],
};
```

## 공유 컴포넌트

이 템플릿은 `meta-reels-ad`의 다음 컴포넌트를 재사용합니다:
- `Narration` - Audio 래퍼
- `calculateSceneStarts` - 씬 시작 프레임 계산 유틸
