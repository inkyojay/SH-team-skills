# 02 감성 (Emotional)

Ken Burns 풀블리드 + 슬로우 페이드 + 감성 인용구로 분위기를 전달하는 영상 템플릿.

## 핵심 모션

- **Ken Burns**: scale 1.0→1.08 미묘한 줌 + 비네트 오버레이
- **Quote**: Cormorant Garamond 이탤릭, 느린 spring 등장
- **전환**: 15프레임 느린 fade (다른 템플릿보다 길게)
- **텍스트**: fade + translateY만 (회전/바운스 금지)

## 권장 길이

15~25초 (느린 템포)

## Config 예시

```typescript
const config: EmotionalConfig = {
  brand: { name: "SUNDAY HUG", color: "#8B7355" },
  palette: "rose",
  scenes: [
    {
      type: "mood",
      mediaSrc: "baby-sleeping.jpg",
      durationSeconds: 6,
      kenBurnsDirection: "zoom-in",
      overlayText: "포근한 잠자리의 시작",
    },
    {
      type: "quote",
      durationSeconds: 7,
      quoteText: "아이가 편안하면\n엄마도 편안해요",
      attribution: "30대 워킹맘",
    },
    {
      type: "product",
      mediaSrc: "swaddle-product.mp4",
      durationSeconds: 5,
      caption: "스와들 스트랩",
      subCaption: "엄마 품처럼 포근하게",
    },
    {
      type: "cta",
      durationSeconds: 4,
      productName: "스와들 스트랩",
    },
  ],
  bgmSrc: "bgm-emotional.mp3",
};
```
