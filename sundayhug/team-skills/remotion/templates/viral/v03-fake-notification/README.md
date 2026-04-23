# V03 - Fake Notification Overlay (B급 바이럴)

iOS 알림 배너가 위에서 슬라이드 인되는 시선 강탈 템플릿.

## 컨셉
- 실제 핸드폰 알림처럼 보이는 가짜 알림 배너
- 배경 콘텐츠 위에 겹쳐서 호기심 자극
- 여러 알림 순차 등장 가능
- iOS 스타일 blur + rounded rect

## 사용법

```tsx
import { FakeNotification } from "./FakeNotification";
import type { FakeNotificationConfig } from "./types";

const config: FakeNotificationConfig = {
  notifications: [
    {
      appName: "쿠팡",
      title: "품절 임박!",
      body: "선데이허그 스와들스트랩 재입고 알림",
      delay: 1,
      appIcon: "🛒",
    },
    {
      appName: "인스타그램",
      title: "육아맘후기 님이 태그했습니다",
      body: "이거 진짜 신세계...",
      delay: 3,
      appIcon: "📸",
    },
  ],
  productContent: {
    text: "선데이허그",
    subText: "스와들스트랩",
    emoji: "👶",
  },
};
```

## Config

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| notifications | NotificationItem[] | O | 알림 목록 |
| backgroundSrc | string | X | 배경 이미지/영상 |
| backgroundColor | string | X | 배경색 (기본 #1C1C1E) |
| productContent | object | X | 배경 제품 콘텐츠 |

## 스타일
- 알림: 흰색 라운드, blur backdrop, iOS 정확 재현
- 앱 아이콘 + 볼드 제목 + 회색 본문
- 시간 "now" 표시
- 기본 사이즈: 1080x1920 (9:16)
- 추천 길이: 10-20초
