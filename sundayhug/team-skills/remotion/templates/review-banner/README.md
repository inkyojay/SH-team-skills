# 리뷰 배너형 광고 템플릿

정적 컴포지트 레이아웃의 짧은 피드 광고 템플릿입니다. 리뷰 카드 + 제품 배너로 소셜 프루프를 강조합니다.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 5~10초 |

## 특징

- **정적 컴포지트**: 씬 전환 없이 단일 레이아웃
- **리뷰 카드**: 별점 + 리뷰 텍스트 말풍선 (소셜 프루프)
- **제품 배너**: 제품 이미지 + 이름 + 가격 + CTA 버튼
- **순차 등장 애니메이션**: 배경 → 리뷰 → 배너
- **Ken Burns 효과**: 배경에 살짝 줌인 효과

## 파일 구조

```
review-banner/
├── ReviewBanner.tsx        # 메인 컴포넌트
├── types.ts                # ReviewBannerConfig 타입
├── analysis.md             # 레퍼런스 영상 분석
├── components/
│   ├── ReviewCard.tsx      # 별점 + 리뷰 말풍선
│   ├── ProductBanner.tsx   # 하단 제품 정보 배너
│   └── BabyPhoto.tsx       # 배경 이미지/비디오 (Ken Burns)
├── references/             # 레퍼런스 영상
└── README.md
```

## 등장 타이밍

| 요소 | 기본 딜레이 | 애니메이션 |
|------|------------|-----------|
| 배경 | 0프레임 | 페이드인 + Ken Burns 줌 |
| 리뷰 카드 | 15프레임 (~0.5초) | 스케일인 |
| 제품 배너 | 30프레임 (~1초) | 슬라이드업 |

## 사용법

```tsx
import type { ReviewBannerConfig } from "./types";

const config: ReviewBannerConfig = {
  backgroundSrc: "baby-sleeping.jpg",
  isBackgroundVideo: false,
  durationSeconds: 6,
  brand: { name: "MY BRAND", color: "#5a7d65" },
  review: {
    rating: 5,
    reviewText: "아기가 정말 편하게 자요. 강추합니다!",
    reviewerName: "구매자 A",
  },
  product: {
    imageSrc: "product.png",
    productName: "실키밤부 슬리핑백",
    priceText: "39,000원",
    ctaText: "자세히 보기",
  },
  reviewDelay: 15,
  bannerDelay: 30,
};
```

## 비디오 배경 사용

```tsx
const videoConfig: ReviewBannerConfig = {
  backgroundSrc: "baby-video.mp4",
  isBackgroundVideo: true,
  backgroundStartFrom: 2,
  durationSeconds: 8,
  // ... 나머지 동일
};
```
