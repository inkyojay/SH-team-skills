# V10 - ASMR Unboxing

클로즈업 제품 샷 + 느린 줌인으로 만족감을 주는 ASMR 스타일 언박싱 템플릿.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 15~25초 |

## 특징

- **프리미엄 감성**: B급 시리즈의 예외, ASMR은 고급스러워야 함
- **느린 줌인**: 각 레이어 scale 1->1.05 (만족스러운 시각 경험)
- **소프트 페이드**: 레이어 간 부드러운 전환 (0.8초)
- **미니멀 텍스트**: 제품명만 마지막에 작고 우아하게
- **워밍 오버레이**: 따뜻한 색감 필터

## 파일 구조

```
v10-asmr-unboxing/
├── AsmrUnboxing.tsx           # 메인 컴포넌트
├── types.ts                   # AsmrUnboxingConfig 타입
├── components/
│   └── UnboxLayer.tsx         # 개별 레이어 (줌인 + 페이드)
└── README.md
```

## 사용법

```tsx
import type { AsmrUnboxingConfig } from "./types";

const config: AsmrUnboxingConfig = {
  layers: [
    { mediaSrc: "box-closeup.jpg", label: "unboxing", durationSeconds: 5 },
    { mediaSrc: "tissue-paper.jpg", durationSeconds: 4 },
    { mediaSrc: "fabric-detail.jpg", label: "texture", durationSeconds: 4 },
    { mediaSrc: "product-reveal.jpg", durationSeconds: 5 },
  ],
  productName: "Silky Bamboo Sleeping Bag",
  finalRevealSrc: "beauty-shot.jpg",
  brandName: "SUNDAYHUG",
  warmOverlayIntensity: 0.15,
};
```

## 모션 순서

1. 레이어 순차 표시: 각 레이어 느린 줌인(1->1.05)
2. 레이어 간 전환: 소프트 페이드 (0.8초)
3. 최종 리빌: 뷰티샷 + 은은한 글로우
4. 제품명: 마지막 1.5초 후 작고 우아하게 등장
5. 브랜드명: 좌하단, 매우 절제된 크기
