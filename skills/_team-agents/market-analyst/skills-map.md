# 시장분석관 스킬 매핑

## Primary (직접 호출)

| 스킬 | 용도 |
|---|---|
| `trend-radar` | 멀티소스 트렌드 (네이버/유튜브/인스타/레딧) |
| `competitive-intelligence` | 경쟁사 모니터링 (단일 심층 + 시장 모니터링 두 모드) |
| `keyword-trend` | 네이버 시즌 트렌드 (DataLab) |
| `product-scout` | 신상품 기회 발굴 |
| `keyword-optimizer` | 키워드 시드/검색량 (시장분석 관점) |

## MCP 직접 사용

| MCP 도구 | 용도 |
|---|---|
| `naver-search.datalab_*` | 검색량 / 카테고리별 / 성연령별 트렌드 |
| `naver-search.search_news` | 베이비 카테고리 뉴스 모니터링 |
| `naver-search.search_blog` | 맘카페/블로그 멘션 트렌드 |
| `naver-search.search_shop` | 쇼핑 카테고리 신상품 추적 |

## Secondary (위임)

| 에이전트/스킬 | 호출 시점 |
|---|---|
| `market-researcher` (sub-agent) | 깊은 웹 리서치 필요할 때 |
| `xlsx` | 트렌드 데이터 정리 / 차트 |
| `pptx` | 분기 시장 리포트 발표용 |

## Reference Knowledge

- `~/Desktop/team-skills/리포트/market-analyst/` 본인 과거 리포트 (자기 예측 추적용)
- 경쟁사 5개 핵심 정보:
  - **Kyte Baby** (미국, 대나무 슬립백, 시즌 컬러)
  - **ergoPouch** (호주, TOG 시스템)
  - **MORI** (영국, 프리미엄 패키징)
  - **제니티브** (한국, 미니멀 디자인)
  - **쉐베베** (한국, 유아 패브릭)
- 브랜드 가이드 10번 포지셔닝 맵 (`skills/brand/sundayhug-brand-director/guidance/sundayhug-brand-project.md`)

## 사용 금지

- ❌ 카피/디자인 직접 제작 금지 (마케팅팀장/디자이너 영역)
- ❌ 의사결정 단정 금지 — "추천한다"가 아니라 "신호가 강하다"

## 신호 강도 판정 기준

| 강도 | 조건 | 추천 액션 |
|---|---|---|
| 🔴 **강** | 검색량 +30% 이상 / 경쟁사 동시 진입 / SNS 멘션 급증 | 즉시 상품기획팀장 + CEO 보고 |
| 🟡 **중** | 검색량 +10~30% / 한 채널 신호 | 2주 모니터링 후 재평가 |
| 🟢 **약** | ±10% / 노이즈 가능성 | 참고 기록 |

## 데이터 출처 표기 형식

매 데이터 인용 시:
```
[출처: 네이버 데이터랩 쇼핑 / 2025-04-20~2025-04-26 / 베이비 카테고리]
```
