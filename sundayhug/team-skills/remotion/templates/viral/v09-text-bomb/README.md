# V09 - Text Bomb / 배민 Style

화면의 80%를 텍스트 한 줄로 채우는 안티디자인 감성 템플릿. 배달의민족 광고 스타일.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 5~8초 |

## 특징

- **안티디자인**: 의도적으로 파워포인트 슬라이드처럼 보이는 구성
- **텍스트 80%**: 메인 텍스트가 화면 폭의 80%를 차지
- **미니멀 모션**: spring scale(0.95->1) + fade만 사용
- **선택적 패턴**: dots, lines, grid 배경 패턴
- **4가지 폰트**: bold, retro, handwritten, impact

## 파일 구조

```
v09-text-bomb/
├── TextBomb.tsx               # 메인 컴포넌트
├── types.ts                   # TextBombConfig 타입
└── README.md
```

## 사용법

```tsx
import type { TextBombConfig } from "./types";

const config: TextBombConfig = {
  mainText: "잠 못 자는 아기는\n없습니다",
  subText: "잠 못 재우는 부모만 있을 뿐",
  brandName: "SUNDAYHUG",
  bgColor: "#FFE066",
  textColor: "#222",
  fontStyle: "impact",
  backgroundPattern: "dots",
};
```

## 배경 색상 추천

| 용도 | bgColor | textColor |
|------|---------|-----------|
| 밝은 노랑 | #FFE066 | #222 |
| 코랄 | #FF6B6B | #fff |
| 민트 | #4ECDC4 | #1a1a2e |
| 라벤더 | #A78BFA | #fff |
| 네온 그린 | #00FF88 | #000 |

## 모션 순서

1. 배경 즉시 채움
2. 메인 텍스트: spring scale(0.95->1) + fade
3. 서브 텍스트: 0.5초 후 같은 모션
4. 브랜드명: 1초 후 우하단에 은은하게 등장
