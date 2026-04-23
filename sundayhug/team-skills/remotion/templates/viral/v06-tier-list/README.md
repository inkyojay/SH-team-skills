# V06 - Tier List / Ranking

S/A/B/C/F 티어 그리드에 제품/항목을 배치하는 B급 감성 랭킹 템플릿.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080x1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 20~30초 |

## 특징

- **티어 그리드**: S(금)/A(녹)/B(파)/C(주)/F(적) 컬러 행
- **슬라이드 인**: 아이템이 오른쪽에서 하나씩 등장
- **브랜드 하이라이트**: 지정 아이템 S티어 글로우/펄스 효과
- **하드컷**: 타이틀은 즉시 등장, B급 감성

## 파일 구조

```
v06-tier-list/
├── TierList.tsx              # 메인 컴포넌트
├── types.ts                  # TierListConfig 타입
├── components/
│   ├── TierGrid.tsx          # 티어 그리드 배경
│   └── TierItem.tsx          # 개별 아이템 (슬라이드 인 + 글로우)
└── README.md
```

## 사용법

```tsx
import type { TierListConfig } from "./types";

const config: TierListConfig = {
  title: "육아용품 티어표",
  items: [
    { name: "우리 슬리핑백", tier: "S", delay: 2 },
    { name: "A사 제품", tier: "A", delay: 4 },
    { name: "B사 제품", tier: "B", delay: 6 },
    { name: "C사 제품", tier: "C", delay: 8 },
    { name: "짝퉁 제품", tier: "F", delay: 10 },
  ],
  brandHighlight: "우리 슬리핑백",
  ctaText: "S급 제품 지금 만나보세요",
};
```

## 모션 순서

1. 타이틀 하드컷 등장
2. 빈 티어 그리드 행이 왼쪽에서 순차 등장
3. 아이템이 delay 순서대로 오른쪽에서 슬라이드 인
4. brandHighlight 아이템은 S티어에 글로우 펄스
5. CTA 텍스트 (선택)
