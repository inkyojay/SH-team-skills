# 04 사회적 증거 (Social Proof)

숫자 카운트업, 별점, 인증 뱃지로 제품 신뢰를 구축하는 영상 템플릿.

## 핵심 모션

- **Stats**: 숫자 0→목표값 spring 카운트업 + 라벨 순차 등장
- **Rating**: 큰 숫자 스케일업 + 별 하나씩 순차 등장
- **Badges**: 인증 뱃지 scale(0→1) 순차 팝인
- **Review**: 리뷰 카드 fade + translateY 등장

## 권장 길이

15~20초

## 씬 유형

| 유형 | 용도 |
|------|------|
| `stats` | 누적 판매 수, 만족도 등 숫자 통계 |
| `rating` | 별점 + 리뷰 수 + 대표 리뷰 |
| `badges` | KC인증, 네이버1위 등 인증 뱃지 |
| `reviews` | 리뷰 카루셀 |
| `cta` | CTA 엔드카드 |

## Config 예시

```typescript
const config: SocialProofConfig = {
  brand: { name: "SUNDAY HUG", color: "#8B7355" },
  palette: "trust",
  scenes: [
    {
      type: "stats",
      durationSeconds: 5,
      stats: [
        { value: 50000, suffix: "+", label: "누적 판매" },
        { value: 98, suffix: "%", label: "재구매율" },
      ],
    },
    {
      type: "rating",
      durationSeconds: 6,
      score: 4.9,
      reviewCountText: "3,842개 리뷰",
      featuredReview: {
        text: "아이가 정말 편하게 잠들어요",
        author: "30대 워킹맘",
        rating: 5,
      },
    },
    {
      type: "cta",
      durationSeconds: 4,
      productName: "스와들 스트랩",
    },
  ],
};
```
