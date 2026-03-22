# V08 - Order vs Reality (주문 vs 현실)

"What I ordered" vs "What I got" 밈 스타일 비교 템플릿.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 10~20초 |

## 특징

- **밈 스타일**: Impact 폰트, 흰 글씨 + 검은 외곽선
- **드라마틱 트랜지션**: 줌 + 스핀 + 화면 플래시
- **isMatch 분기**: true=초록 체크+신뢰, false=빨간 X+코미디
- **간결한 구조**: 주문 → 트랜지션 → 현실 → 결과

## 파일 구조

```
v08-order-vs-reality/
├── OrderVsReality.tsx         # 메인 컴포넌트
├── types.ts                   # OrderVsRealityConfig 타입
└── README.md
```

## 사용법

```tsx
import type { OrderVsRealityConfig } from "./types";

// 긍정 (기대=현실, 신뢰 구축용)
const matchConfig: OrderVsRealityConfig = {
  orderImageSrc: "order-screenshot.png",
  realityImageSrc: "real-product.png",
  productName: "실키밤부 슬리핑백",
  isMatch: true,
  caption: "사진 그대로! 믿고 구매하세요",
};

// 부정 (코미디/밈용)
const mismatchConfig: OrderVsRealityConfig = {
  orderImageSrc: "competitor-ad.png",
  realityImageSrc: "competitor-real.png",
  productName: "짝퉁 제품",
  isMatch: false,
  caption: "이래서 정품을 사야합니다",
};
```

## 모션 순서

1. "주문한 것" 라벨 + 이미지 (3초 홀드)
2. 드라마틱 트랜지션: 줌(3x) + 360도 스핀 + 화면 플래시 (0.5초)
3. "받은 것" 라벨 + 이미지 리빌
4. isMatch에 따라 체크/X 아이콘 + 결과 텍스트 (1.5초 후)
