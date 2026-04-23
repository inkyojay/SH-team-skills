# V07 - Countdown Listicle

"Top 3 이유" 스타일 역순 카운트다운 드라마틱 리스티클 템플릿.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 15~25초 |

## 특징

- **드라마틱 카운트다운**: 숫자가 크게 줌인되며 등장
- **하드컷 전환**: 항목 간 부드러운 전환 없이 즉시 전환
- **#1 특별 효과**: 플래시, 더 큰 텍스트, 1.5배 긴 홀드
- **그라디언트 숫자**: 200px+ 크기의 그라디언트 숫자

## 파일 구조

```
v07-countdown/
├── Countdown.tsx              # 메인 컴포넌트
├── types.ts                   # CountdownConfig 타입
├── components/
│   └── CountdownCard.tsx      # 카운트다운 카드 (숫자 + 텍스트)
└── README.md
```

## 사용법

```tsx
import type { CountdownConfig } from "./types";

const config: CountdownConfig = {
  title: "이걸 안 쓰는 3가지 이유",
  items: [
    { number: 3, text: "매일 밤 아기가 깬다" },
    { number: 2, text: "기저귀 갈기가 불편하다" },
    { number: 1, text: "실크보다 부드러운 촉감을 모른다" },
  ],
  ctaText: "지금 바로 체험하세요",
};
```

## 모션 순서

1. 타이틀 카드: 제목 + 배경에 큰 숫자
2. 각 항목: 큰 숫자 줌인(3->1) -> 텍스트 슬라이드업
3. #1 항목: 화면 플래시 + 큰 텍스트 + 긴 홀드
4. CTA 텍스트 (선택)
