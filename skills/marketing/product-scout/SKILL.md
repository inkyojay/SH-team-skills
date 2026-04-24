---
name: product-scout
description: |
  데이터 기반 신상품 기회 탐색 & 소싱 가능성 자동 매칭 스킬.
  
  네이버 쇼핑인사이트, 검색광고 API, 맘카페 VOC, 쿠팡 리뷰, Amazon BSR, Reddit, Pinterest 등에서
  수요 급등 신호 + 미충족 수요 + 해외 선행 트렌드 + 경쟁사 동향을 수집하고,
  기회 스코어링 → 1688/Alibaba 소싱 매칭까지 자동으로 수행한다.
  
  다음 상황에서 반드시 이 스킬을 사용한다:
  - "신상품 기회", "어떤 제품 만들까", "새 제품 아이디어"
  - "수요 분석", "시장 기회", "블루오션", "틈새 시장"
  - "요즘 뭐가 잘 팔려", "인기 상품", "베스트셀러 분석"
  - "맘카페 뭐 찾고 있어", "소비자 니즈", "VOC 분석"
  - "해외에서 뭐가 뜨고 있어", "아마존 트렌드"
  - "이거 소싱 가능해?", "원가 얼마나", "1688 검색"
  - "위클리 기회 리포트", "상품 기획 데이터"
  - "경쟁사 신상품", "신규 등록 제품 모니터링"
---

# Product Scout — 데이터 기반 신상품 기회 탐색

## 개요

```
데이터 수집 (5개 영역)
  ├─ 📈 수요 급등: 네이버 데이터랩/검색광고 → 검색량 급등 카테고리/키워드
  ├─ 💬 미충족 수요: 맘카페/쿠팡 리뷰 → "이런 제품 없나요" 패턴
  ├─ 🌏 해외 선행: Amazon/Reddit/Pinterest → 한국 미진출 트렌드
  ├─ 🏪 경쟁사 동향: 네이버 쇼핑 → 신규 등록 제품/가격 변동
  └─ 🏭 소싱 가능성: 1688/Alibaba → OEM 가능 여부/원가
         ↓
  기회 스코어링 (자동 순위)
         ↓
  위클리 기회 리포트 → Go 사인 → new-product-planner 연결
```

## 브랜드 컨텍스트

- **브랜드**: 썬데이허그 (SundayHug) / JAYCORP
- **카테고리**: 아기 수면 용품
- **가격대**: 30,000~150,000원 프리미엄
- **강점**: 디자인, 소재 품질, 기능성
- **확장 가능 카테고리**: 유아 의류, 수유 용품, 외출 용품

---

## 데이터 수집 채널

### 1. 수요 급등 감지

#### 네이버 데이터랩 쇼핑인사이트 (MCP: naver-search)
```
MCP tool: datalab_shopping_category
→ 카테고리 클릭량 급증 감지
→ 모니터링 카테고리: 유아수면용품, 유아의류, 수유용품, 유아외출

MCP tool: datalab_shopping_keywords
→ 인기검색어 TOP500 변화 추적
→ "아기 OO" 패턴 키워드 주간 20%↑ 자동 감지
```

#### 네이버 검색광고 API
```
→ 키워드 월간 검색량 + 경쟁도
→ 검색량은 높은데 경쟁도가 낮은 키워드 = 블루오션 시그널
```

### 2. 미충족 수요 (VOC 마이닝)

#### 맘카페 크롤링
```
감지 패턴:
- "이런 제품 없나요"
- "어디서 사요"  
- "추천해주세요 OO 되는"
- "왜 이런 건 안 나오지"
- "해외에서 직구하는데 국내는..."
```

`web_search` 쿼리:
```
1. site:cafe.naver.com "이런 제품 없나요" 아기
2. site:cafe.naver.com "추천해주세요" 수면 아기
3. site:cafe.naver.com "직구" 아기 수면
4. site:cafe.naver.com "불편해요" 슬리핑백
```

#### 쿠팡/네이버 쇼핑 리뷰 분석
```
감지 패턴:
- 별점 3점 이하 리뷰의 불만 키워드 클러스터링
- "이것만 있으면", "이것만 개선되면"
- "다른 브랜드는 되는데"
```

`web_search` + `web_fetch`:
```
1. web_search: "아기 슬리핑백 리뷰 불편" site:review.coupang.com
2. web_search: "아기 속싸개 단점" 리뷰
3. web_fetch: 네이버 쇼핑 리뷰 페이지 (가능한 경우)
```

### 3. 해외 선행 트렌드

#### Amazon Best Sellers
`web_search` 또는 Apify Actor:
```
1. web_search: "amazon best sellers baby sleep" site:amazon.com
2. web_search: "amazon new releases baby nursery"
3. Baby 카테고리 BSR 변동 추적
→ 한국 미진출 제품 필터링
```

#### Reddit
```
서브레딧: r/beyondthebump, r/NewParents, r/sleeptrain
감지 패턴:
- "game changer"
- "must have"
- "wish I knew about"  
- "just discovered"
→ 신제품 발견 + 사용 피드백 동시 수집
```

#### Pinterest Trends
```
Baby/Nursery 카테고리:
- 떠오르는 스타일 (색상, 소재, 디자인)
- 제품 트렌드 (예: "bamboo baby", "organic sleep")
- 예측 트렌드 (Pinterest Predicts)
```

### 4. 경쟁사 동향

#### 네이버 쇼핑 검색 API (MCP: naver-search)
```
MCP tool: search_shop
→ "아기 수면" 카테고리 신규 등록 제품 주간 모니터링
→ 경쟁사 가격 변동 감지
→ 신규 브랜드 진입 알림
```

### 5. 소싱 가능성 매칭

#### 1688.com
`web_search` 또는 Apify Actor:
```
1. web_search: "site:1688.com 婴儿睡袋" (아기 슬리핑백)
2. web_search: "site:1688.com 竹纤维婴儿" (대나무 소재 아기)
수집: OEM 가능 여부, 예상 원가, 공급자 평점, MOQ
```

#### Alibaba.com
```
1. web_search: "site:alibaba.com baby sleep sack bamboo"
수집: 글로벌 소싱 대안, MOQ, 가격 비교
```

---

## 기회 스코어링

### 스코어 공식

```
기회 점수 = 검색량 증가율 × (1 / 경쟁 강도) × 마진 가능성 × 기존 라인업 시너지
```

### 세부 요소

| 요소 | 가중치 | 측정 방법 |
|------|--------|----------|
| 검색량 증가율 | 30% | 네이버 데이터랩 주간 변화율 |
| 경쟁 강도 (역수) | 25% | 검색광고 경쟁도 + 네이버 쇼핑 등록 상품 수 |
| 마진 가능성 | 25% | (예상 소비자가 - 예상 원가) / 예상 소비자가 |
| 라인업 시너지 | 20% | 기존 제품과의 카테고리 연관성 + 교차판매 가능성 |

### 등급

| 점수 | 등급 | 의미 |
|------|------|------|
| 80+ | A | 즉시 검토 권장 |
| 60~79 | B | 추가 조사 후 판단 |
| 40~59 | C | 모니터링 유지 |
| 40 미만 | D | 현재 시기 부적합 |

---

## 실행 모드

### 모드 A: 키워드 기반 기회 탐색
```
입력: "아기 쿨매트 시장 기회 분석해줘"
실행:
  1. 검색량/경쟁도 분석 (네이버)
  2. 맘카페 VOC 수집
  3. 해외 트렌드 확인
  4. 소싱 가능성 체크
  5. 기회 스코어 산출
출력: 단일 기회 분석 리포트
```

### 모드 B: 위클리 전체 스캔
```
입력: "위클리 기회 리포트 만들어줘"
실행:
  1. 전체 모니터링 카테고리 수요 스캔
  2. 맘카페 미충족 수요 마이닝
  3. Amazon/Reddit/Pinterest 해외 트렌드
  4. 경쟁사 신규 동향
  5. TOP 10 기회 스코어링
  6. 소싱 매칭 (상위 5건)
출력: 종합 기회 리포트 HTML
```

### 모드 C: 소싱 검색
```
입력: "대나무 슬리핑백 소싱 가능한지 알아봐줘"
실행:
  1. 1688 제품 검색
  2. Alibaba 대안 검색
  3. 원가/MOQ/품질 비교
  4. 마진 시뮬레이션
출력: 소싱 가능성 리포트
```

---

## 출력 포맷

### 기회 리포트 JSON
```json
{
  "report_date": "2026-04-08",
  "opportunities": [
    {
      "rank": 1,
      "product_concept": "대나무 섬유 여름 슬리핑백",
      "opportunity_score": 87,
      "grade": "A",
      "signals": {
        "search_surge": "아기 대나무 잠옷 +45% (네이버)",
        "global_trend": "bamboo sleep sack trending on Reddit/Pinterest",
        "unmet_demand": "맘카페 12건: '대나무 소재 슬리핑백 없나요'",
        "competitor_gap": "국내 브랜드 0개 (현재 직구만 존재)"
      },
      "sourcing": {
        "1688_matches": 23,
        "est_cost_range": "8,000~15,000원",
        "est_retail": "39,000~49,000원",
        "est_margin": "55~65%",
        "moq": "500~1,000개"
      },
      "synergy": "기존 슬리핑백 라인업 확장, 여름 시즌 보완",
      "next_action": "→ new-product-planner 연결 가능"
    }
  ]
}
```

### HTML 리포트 (모드 B)
인터랙티브 HTML 위클리 기회 리포트:
- 단일 HTML 파일 (Chart.js CDN 허용)
- 기회 카드 TOP 10 (스코어 + 시그널 요약)
- 소싱 가능성 매트릭스
- 경쟁사 신규 동향 테이블
- 각 기회에 "Go/Hold" 액션 버튼

파일 저장: `~/Desktop/team-skills/리포트/product-scout_{YYYYMMDD}.html`

---

## 기존 스킬 연동

| 기존 스킬 | 연동 방식 |
|----------|----------|
| **trend-radar** | 검색 트렌드 + 해외 신호 + 커뮤니티 버즈 데이터 입력 |
| **new-product-planner** | Go 사인 후 → 전체 신상품 기획 프로세스 연결 |
| **competitive-intelligence** | 특정 기회에 대한 경쟁사 심층 분석 연동 |
| **product-analyzer** | 기존 제품 대비 시너지 분석 |
| **brand-dna-extractor** | 브랜드 정체성과 신제품 적합성 검증 |

---

## API 키 현황

| API | 상태 | 비용 |
|-----|------|------|
| 네이버 데이터랩 | **보유** (MCP) | 무료 |
| 네이버 검색광고 | **보유** | 무료 |
| 네이버 쇼핑 검색 | **보유** (MCP) | 무료 (25,000/일) |
| Reddit API | 발급 필요 | 무료 |
| Pinterest API v5 | 발급 필요 | 무료 |
| 1688 (Apify) | 선택 | 무료~$49/mo |
| Alibaba (Apify) | 선택 | 무료~$49/mo |
| Amazon BSR (Apify) | 선택 | 무료~$49/mo |

**핵심 API(네이버)는 즉시 사용 가능. 소싱 API는 필요 시 추가.**

## 참조 파일

- `references/scoring-framework.md` → 기회 스코어링 상세 로직
- `references/sourcing-guide.md` → 1688/Alibaba 소싱 가이드
