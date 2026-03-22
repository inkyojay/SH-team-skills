# V04 - Ugly/Lo-Fi Review (B급 바이럴)

셀카캠 스타일의 볼드 캡션 리뷰 템플릿. 의도적으로 못생긴 디자인.

## 컨셉
- TikTok/릴스 캡션 스타일 (흰색 볼드 + 검정 아웃라인)
- 카메라 쉐이크 (미세한 흔들림)
- 제품명 노란/초록 하이라이트
- 하드 컷 등장 (페이드 없음)
- REC 표시, 셀카캠 느낌

## 사용법

```tsx
import { UglyReview } from "./UglyReview";
import type { UglyReviewConfig } from "./types";

const config: UglyReviewConfig = {
  reviewText: "진짜 써보고 깜놀함\n아기가 5분만에 잠듦\n이건 사기임 (좋은 의미로)",
  reviewerName: "육아맘 김**",
  productName: "스와들스트랩",
  bgColor: "#FF6B6B",
  rating: 5,
  ctaText: "지금 바로 검색",
};
```

## Config

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| reviewText | string | O | 리뷰 본문 (\n으로 줄바꿈) |
| reviewerName | string | O | 리뷰어 이름 |
| productName | string | O | 하이라이트할 제품명 |
| bgColor | string | X | 배경색 (기본 #FF6B6B) |
| bgGradientEnd | string | X | 그라디언트 끝 색상 |
| rating | number | X | 별점 (0~5) |
| highlightColor | string | X | 하이라이트 색상 (기본 #FFFF00) |
| shakeIntensity | number | X | 쉐이크 강도 (0~1, 기본 0.5) |
| ctaText | string | X | CTA 버튼 텍스트 |

## 스타일
- 배경: 단색 또는 그라디언트 (lo-fi)
- 캡션: 볼드 흰색 + 두꺼운 검정 아웃라인
- 폰트: system heavy/black
- 의도적 "언디자인드" 룩
- 기본 사이즈: 1080x1920 (9:16)
- 추천 길이: 15-25초
