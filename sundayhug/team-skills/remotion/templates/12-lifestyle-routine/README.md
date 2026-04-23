# 12 라이프스타일/루틴 (Lifestyle Routine)

일상 루틴 속 제품 사용 과정을 스텝별로 보여주는 영상 템플릿.

## 핵심 모션

- **Step Number**: 원형 배지 scale(0→1) 팝인
- **Progress Dots**: 현재 스텝 하이라이트 + 길게 늘어남
- **Time Label**: 좌상단 시간대 슬라이드인
- **Title/Desc**: fade + translateY 순차 등장

## 권장 길이

20~30초 (스텝 3~5개)

## 씬 유형

| 유형 | 용도 |
|------|------|
| `intro` | 루틴 소개 ("우리 아기 취침 루틴") |
| `step` | 개별 루틴 스텝 (번호 + 제목 + 영상) |
| `summary` | 루틴 요약 |
| `cta` | CTA 엔드카드 |

## Config 예시

```typescript
const config: LifestyleRoutineConfig = {
  brand: { name: "SUNDAY HUG", color: "#8B7355" },
  palette: "default",
  scenes: [
    {
      type: "intro",
      mediaSrc: "routine-intro.mp4",
      durationSeconds: 4,
      title: "우리 아기 취침 루틴",
      subTitle: "with 썬데이허그",
    },
    {
      type: "step",
      durationSeconds: 5,
      totalSteps: 3,
      step: {
        stepNumber: 1,
        title: "목욕 후 보습",
        description: "촉촉한 피부로 준비해요",
        timeLabel: "PM 7:30",
        mediaSrc: "step1-bath.mp4",
      },
    },
    {
      type: "step",
      durationSeconds: 5,
      totalSteps: 3,
      step: {
        stepNumber: 2,
        title: "스와들 착용",
        description: "엄마 품처럼 포근하게",
        timeLabel: "PM 7:45",
        mediaSrc: "step2-swaddle.mp4",
      },
    },
    {
      type: "step",
      durationSeconds: 5,
      totalSteps: 3,
      step: {
        stepNumber: 3,
        title: "꿀잠 시작",
        description: "안정적인 수면으로",
        timeLabel: "PM 8:00",
        mediaSrc: "step3-sleep.mp4",
      },
    },
    {
      type: "cta",
      durationSeconds: 4,
      productName: "스와들 스트랩",
    },
  ],
  bgmSrc: "bgm-routine.mp3",
};
```
