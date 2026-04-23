# 01 문제-해결 (Problem-Solution)

다크 톤의 문제 제시 → 밝은 솔루션 전환으로 제품의 문제 해결력을 강조하는 영상 템플릿.

## 핵심 모션

- **Problem**: 다크 오버레이 + 미세 흔들림(shake)으로 불안감 표현
- **Transition**: Circle wipe + 화살표로 전환점 강조
- **Solution**: 밝은 톤 + spring 스케일업으로 긍정적 전환
- **CTA**: 순차적 spring 등장

## 권장 길이

15~20초 (씬 3~4개)

## Config 예시

```typescript
const config: ProblemSolutionConfig = {
  brand: { name: "SUNDAY HUG", color: "#8B7355" },
  palette: "default",
  scenes: [
    {
      type: "problem",
      mediaSrc: "problem-clip.mp4",
      durationSeconds: 5,
      problemText: "아기 등센서에 잠을 못 자나요?",
      subText: "매일 반복되는 수면 고민",
    },
    {
      type: "solution",
      mediaSrc: "solution-clip.mp4",
      durationSeconds: 7,
      solutionText: "포근한 감싸기로 깊은 잠을",
      productName: "스와들 스트랩",
    },
    {
      type: "cta",
      durationSeconds: 4,
      productName: "스와들 스트랩",
      ctaText: "지금 바로 구매하기",
    },
  ],
  bgmSrc: "bgm-calm.mp3",
  bgmVolume: 0.25,
};
```

## 포맷

| 포맷 | Composition ID 접미사 |
|------|---------------------|
| Reels 9:16 | `-reels` |
| Feed Square 1:1 | `-square` |
| Feed Vertical 4:5 | `-vertical` |
