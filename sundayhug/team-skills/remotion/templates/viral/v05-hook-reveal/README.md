# V05 - Scroll-Stop Hook + Reveal (B급 바이럴)

대형 텍스트 훅 → 하드 컷 → 제품 공개의 2단 구성 템플릿.

## 컨셉
- 훅 (0~1.5초): 화면 80%를 채우는 충격적 대형 텍스트, 스케일 펄스
- 전환: 2프레임 흰색 플래시 (하드 컷)
- 리빌 (1.5초~끝): 제품 공개 + 캡션 + CTA 버튼

## 사용법

```tsx
import { HookReveal } from "./HookReveal";
import type { HookRevealConfig } from "./types";

const config: HookRevealConfig = {
  hookText: "아기 재우는데\n10분이면 충분",
  hookEmoji: "😴",
  hookBgColor: "#000",
  revealProductName: "선데이허그 스와들스트랩",
  revealCaption: "특허받은 양팔 고정 설계로\n아기가 스스로 잠드는 기적",
  ctaText: "지금 바로 구매 →",
};
```

## Config

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| hookText | string | O | 훅 대형 텍스트 |
| hookEmoji | string | X | 훅 이모지 |
| hookBgColor | string | X | 훅 배경색 (기본 #000) |
| hookTextColor | string | X | 훅 텍스트색 (기본 #FFF) |
| revealProductName | string | O | 공개할 제품명 |
| revealMediaSrc | string | X | 제품 이미지 소스 |
| revealCaption | string | O | 제품 설명 캡션 |
| ctaText | string | O | CTA 버튼 텍스트 |
| ctaColor | string | X | CTA 색상 (기본 #FF0050) |
| revealBgColor | string | X | 리빌 배경색 (기본 #FFF) |
| hookDuration | number | X | 훅 시간 (초, 기본 1.5) |
| enableFlash | boolean | X | 플래시 효과 (기본 true) |

## 스타일
- 훅: 텍스트가 화면 80% 차지, 볼드, 글리치
- 플래시: 2프레임 흰색 전환
- 리빌: 캐주얼하지만 정돈된 레이아웃
- 기본 사이즈: 1080x1920 (9:16)
- 추천 길이: 10-15초
