# 07 비포/애프터 (Before-After)

clipPath wipe로 전/후 상태를 극적으로 비교하는 영상 템플릿.

## 핵심 모션

- **Before**: 채도 0.3 + 어두운 톤으로 "이전" 상태 표현
- **Wipe Reveal**: clipPath 슬라이드로 After 상태 드러남
- **After**: 풀 채도 + 밝은 톤으로 "이후" 상태 강조
- **Wipe Line**: 전환 경계에 흰색 라인 + 글로우

## 권장 길이

15~20초

## Config 예시

```typescript
const config: BeforeAfterConfig = {
  brand: { name: "SUNDAY HUG", color: "#8B7355" },
  scenes: [
    {
      type: "compare",
      durationSeconds: 8,
      pair: {
        beforeSrc: "sleep-before.jpg",
        afterSrc: "sleep-after.jpg",
        caption: "스와들 하나로 달라지는 수면",
      },
    },
    {
      type: "cta",
      durationSeconds: 4,
      productName: "스와들 스트랩",
    },
  ],
};
```
