# V02 - KakaoTalk Chat (B급 바이럴)

카카오톡 채팅 UI를 재현한 대화형 광고 템플릿.

## 컨셉
- 카톡 대화 캡처 느낌의 자연스러운 광고
- 타이핑 인디케이터 → 메시지 등장 순서
- 마지막에 제품 공개 카드 삽입 가능
- 이모지/이미지 메시지 지원

## 사용법

```tsx
import { KakaoChat } from "./KakaoChat";
import type { KakaoChatConfig } from "./types";

const config: KakaoChatConfig = {
  chatTitle: "육아 고민 상담",
  messages: [
    { sender: "엄마A", text: "아기 잠투정 너무 심해ㅠ", isMe: false, delay: 0 },
    { sender: "나", text: "우리도 그랬는데", isMe: true, delay: 1 },
    { sender: "나", text: "스와들스트랩 쓰고 해결됨!", isMe: true, delay: 0.8 },
    { sender: "엄마A", text: "뭐야 그게??", isMe: false, delay: 0.5 },
  ],
  productReveal: {
    productName: "선데이허그 스와들스트랩",
    linkText: "sundayhug.kr에서 보기",
  },
};
```

## Config

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| messages | ChatMessage[] | O | 채팅 메시지 목록 |
| chatTitle | string | O | 채팅방 제목 |
| participantCount | number | X | 참여자 수 (기본 2) |
| productReveal | object | X | 제품 공개 카드 |
| typingDuration | number | X | 타이핑 표시 시간 (초, 기본 0.8) |

## 스타일
- 내 버블: #FEE500 (카톡 노란색)
- 상대 버블: #FFF
- 배경: #B2C7D9
- 헤더: #3C3C3C
- 기본 사이즈: 1080x1920 (9:16)
- 추천 길이: 15-25초
