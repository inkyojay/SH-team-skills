# V01 - iPhone Notes App (B급 바이럴)

Apple Notes 앱 UI를 재현한 타이핑 광고 템플릿.

## 컨셉
- 아이폰 메모 앱에 뭔가 적는 듯한 자연스러운 연출
- 타이핑 애니메이션 + 커서 깜빡임
- 제품명 노란 하이라이트
- 의도적 오타 가능 (typoAt 옵션)

## 사용법

```tsx
import { NotesApp } from "./NotesApp";
import type { NotesAppConfig } from "./types";

const config: NotesAppConfig = {
  lines: [
    { text: "아기가 밤에 안 자서", delay: 0 },
    { text: "이거 써봤는데", delay: 0.3 },
    { text: "진짜 효과 있음 ㄹㅇ", bold: true },
  ],
  brandName: "선데이허그",
  productName: "스와들스트랩",
  ctaText: "지금 바로 검색 🔍",
};
```

## Config

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| lines | NotesLine[] | O | 타이핑할 줄 목록 |
| brandName | string | X | 노트 헤더 표시명 |
| productName | string | X | 노란 하이라이트 처리할 텍스트 |
| ctaText | string | X | 하단 CTA 버튼 텍스트 |
| charSpeed | number | X | 글자당 타이핑 속도 (초, 기본 0.06) |
| ctaColor | string | X | CTA 버튼 색상 (기본 #007AFF) |

## 스타일
- 배경: #FFF (순백)
- 헤더: #F6F2E8 (Notes 노란 톤)
- 폰트: monospace 계열
- 그라디언트/그림자 없음, 울트라 플랫
- 기본 사이즈: 1080x1920 (9:16)
- 추천 길이: 5-10초
