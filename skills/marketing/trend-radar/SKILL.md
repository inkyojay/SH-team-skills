---
name: trend-radar
description: |
  썬데이허그(JAYCORP) 멀티소스 트렌드 데이터 수집·분석 엔진.
  
  네이버 데이터랩, 검색광고 API, TikTok Creative Center, YouTube, 맘카페, Reddit, Pinterest 등
  10개 이상의 데이터 소스에서 트렌드를 자동 수집하고, 급상승 키워드 감지, 트렌딩 사운드 큐레이션,
  영상 포맷 분석, 커뮤니티 버즈 모니터링, 해외 선행 트렌드 탐지까지 수행한다.
  
  수집된 데이터는 content-pipeline(마케팅)과 product-scout(상품기획) 양쪽에 피딩된다.

  다음 상황에서 반드시 이 스킬을 사용한다:
  - "트렌드 분석", "요즘 뭐가 뜨고 있어", "검색 트렌드", "키워드 트렌드"
  - "트렌딩 사운드", "인기 음악", "릴스 음악 추천", "TikTok 트렌드"
  - "맘카페 요즘 뭐 얘기해", "커뮤니티 버즈", "맘카페 트렌드"
  - "해외 트렌드", "글로벌 트렌드", "Reddit 트렌드", "Pinterest 트렌드"
  - "위클리 트렌드 리포트", "시장 트렌드", "트렌드 모니터링"
  - "영상 트렌드", "인기 영상 포맷", "숏폼 트렌드"
  - "급상승 키워드", "검색량 변화", "시즌 트렌드"
---

# Trend Radar — 멀티소스 트렌드 수집·분석 엔진

## 개요

10개 이상의 데이터 소스에서 트렌드를 수집하여 마케팅과 상품기획에 활용 가능한 인사이트를 생성한다.

```
수집 채널 (10+)
  ├─ 검색 키워드: 네이버 데이터랩, 검색광고 API, Google Trends
  ├─ 음악/릴스: TikTok Creative Center, TokChart
  ├─ 영상 트렌드: YouTube Data API, TikTok
  ├─ 소셜/커뮤니티: 맘카페, Instagram Graph API, Reddit
  └─ 비주얼: Pinterest API, Gemini Vision
         ↓
  분석 & 인사이트
         ↓
  ├→ content-pipeline (마케팅 콘텐츠 자동 생산)
  └→ product-scout (신상품 기회 탐색)
```

## 브랜드 컨텍스트

- **브랜드**: 썬데이허그 (SundayHug) / 주식회사 제이코프 (JAYCORP)
- **카테고리**: 아기 수면 용품 (슬리핑백, 속싸개, 접이식 침대, 백색소음기)
- **타겟**: 0~5세 자녀를 둔 30대 부모

---

## 데이터 수집 채널

### 1. 검색 키워드 트렌드

#### 네이버 데이터랩 (MCP: naver-search)
**키 보유 — 즉시 사용 가능**

MCP 도구 활용:
- `datalab_search`: 검색어 트렌드 (기간/성별/연령별)
- `datalab_shopping_category`: 쇼핑 인사이트 카테고리 클릭량
- `datalab_shopping_keywords`: 쇼핑 키워드 트렌드
- `datalab_shopping_by_age` / `by_gender` / `by_device`: 세그먼트별 분석

**모니터링 키워드 그룹:**
```
그룹 A (핵심): 아기 슬리핑백, 아기 수면조끼, 아기 속싸개, 유아 침낭
그룹 B (확장): 신생아 잠옷, 아기 이불, 아기 수면 환경, 아기 꿀잠
그룹 C (시즌): 여름 슬리핑백, 겨울 슬리핑백, 쿨매트 아기, 아기 난방
그룹 D (경쟁): 에르고파우치, 스와들업, 꿈비, 베베숲
```

#### 네이버 검색광고 API
**키 보유 — 즉시 사용 가능**

`web_fetch`로 검색광고 API 호출:
- 월간 검색량 (PC/모바일)
- 경쟁도 (높음/중간/낮음)
- 월평균 클릭수, 클릭율
- 연관 키워드 확장

**급상승 감지 기준:** 주간 검색량 20% 이상 증가

#### Google Trends
`web_search`로 pytrends 데이터 또는 직접 Google Trends 페이지 조회:
- 글로벌 검색 트렌드
- 관련 주제 / 관련 검색어
- 지역별 관심도

### 2. 트렌딩 사운드/음악

#### TikTok Creative Center
`web_fetch`로 TikTok Creative Center 크롤링:
```
URL: https://ads.tiktok.com/business/creativecenter/music/pc/en
필터: Region=KR, Period=7days
```
수집 항목:
- 트렌딩 음악 TOP 50
- 사용량 증가율
- 상업용 가능 여부 (Commercial Use 필터)
- 장르, BPM 정보

#### TokChart
`web_fetch`로 크롤링:
```
URL: https://tokchart.com
```
- 24시간 / 주간 트렌딩 사운드
- 지역별 랭킹 (KR)
- 트렌드 스코어

### 3. 영상 트렌드

#### YouTube Data API v3
`web_fetch`로 YouTube API 호출:
```
GET https://www.googleapis.com/youtube/v3/videos
?part=snippet,statistics
&chart=mostPopular
&regionCode=KR
&videoCategoryId=22 (People & Blogs)
&maxResults=50
&key={API_KEY}
```
분석 항목:
- 카테고리별 인기 영상 메타데이터
- 태그, 제목 패턴
- 조회수 대비 좋아요 비율
- 영상 길이 분포

#### TikTok Creative Center (영상)
- 트렌딩 해시태그
- 인기 영상 포맷 (before/after, tutorial, unboxing 등)
- 크리에이터 랭킹

### 4. 소셜/커뮤니티

#### 맘카페 버즈 모니터 (네이버 카페)
`web_search` + `web_fetch`로 수집:
```
검색 패턴:
1. web_search: "site:cafe.naver.com 아기 수면 추천" (최근 1주)
2. web_search: "site:cafe.naver.com 슬리핑백 추천해주세요"
3. web_search: "site:cafe.naver.com 아기 잠옷 요즘"
```

감지 패턴:
```
추천 요청: "추천해주세요", "어떤게 좋을까요", "써보신 분"
불만/니즈: "이런 제품 없나요", "왜 이런 건 안 나오지", "불편해요"
트렌드: "요즘", "핫한", "인기", "대박"
```

#### Instagram Graph API
자사 계정 성과 분석:
- 게시물 도달/저장/공유 성과
- 해시태그 트렌드
- 인게이지먼트 높은 콘텐츠 유형 분석

#### Reddit
`web_fetch`로 Reddit API 호출:
```
GET https://oauth.reddit.com/r/beyondthebump/hot
GET https://oauth.reddit.com/r/parenting/hot
GET https://oauth.reddit.com/r/NewParents/hot
```
- 해외 육아 선행 트렌드 (한국보다 2-3개월 앞선)
- "game changer", "must have" 패턴 감지

### 5. 비주얼 트렌드

#### Pinterest API v5
- 트렌딩 키워드/토픽 (Baby, Nursery 카테고리)
- 카테고리별 인기 핀
- 예측 트렌드 (Pinterest Predicts)

#### Gemini Vision
- 경쟁사/인플루언서 피드 이미지 톤&무드 자동 분류
- 비주얼 트렌드 패턴 감지

---

## 핵심 기능

### 1. 급상승 키워드 감지
네이버 데이터랩 + 검색광고 API로 주간 검색량 20%↑ 키워드 자동 필터링.
시즌 수요 조기 포착 (예: "아기 쿨매트", "신생아 에어컨").

### 2. 트렌딩 사운드 큐레이션
TikTok Creative Center + TokChart 크롤링으로 한국 지역 필터 트렌딩 음악 TOP 20.
상업용 가능 여부 자동 태깅.

### 3. 영상 포맷 분석
YouTube/TikTok 인기 영상의 구조 패턴 자동 분류:
- hook 방식 (질문, 충격, 비포/애프터)
- 영상 길이 분포
- 텍스트 오버레이 스타일
- 전환 타이밍

### 4. 맘카페 버즈 모니터
네이버 맘카페 인기글 크롤링 → 키워드 클러스터링 → "요즘 맘들이 뭘 고민하는지" 위클리 인사이트.

### 5. 해외 선행 트렌드
Reddit 육아 서브레딧 + Pinterest 트렌드 → 한국보다 2-3개월 앞선 트렌드 감지.

### 6. 위클리 트렌드 리포트
모든 데이터 종합 → 인터랙티브 HTML 위클리 리포트 자동 생성.

---

## 실행 모드

### 모드 A: 키워드 중심 분석 (빠른 실행)
특정 키워드나 카테고리에 대한 즉석 트렌드 분석.
```
입력: "아기 슬리핑백 트렌드 분석해줘"
출력: 검색량 추이 + 연관 키워드 + 경쟁도 + 시즌 패턴
```

**실행 순서:**
1. 네이버 데이터랩 MCP로 검색어 트렌드 조회
2. 검색광고 API로 월간 검색량/경쟁도 확인
3. 네이버 쇼핑 검색으로 관련 상품 현황 확인
4. 분석 결과 종합 리포트 출력

### 모드 B: 위클리 풀 스캔
전체 모니터링 키워드 + 소셜 + 영상 + 해외까지 종합 스캔.
```
입력: "위클리 트렌드 리포트 만들어줘"
출력: 전체 채널 종합 인터랙티브 HTML 리포트
```

**실행 순서:**
1. 검색 키워드: 데이터랩 + 검색광고 API (전체 키워드 그룹)
2. 트렌딩 사운드: TikTok + TokChart
3. 영상 트렌드: YouTube + TikTok 해시태그
4. 커뮤니티: 맘카페 + Reddit
5. 비주얼: Pinterest
6. 종합 분석 + HTML 리포트 생성

### 모드 C: 특정 채널 딥다이브
특정 채널만 집중 분석.
```
입력: "TikTok 트렌딩 사운드 분석해줘"
입력: "맘카페 요즘 뭐 얘기해?"
입력: "Reddit 해외 육아 트렌드"
```

---

## 출력 포맷

### JSON 데이터 구조
```json
{
  "report_date": "2026-04-08",
  "trending_keywords": [
    {
      "keyword": "아기 쿨매트",
      "volume_change": "+34%",
      "volume": 12400,
      "competition": "중",
      "season_signal": true
    }
  ],
  "trending_sounds": [
    {
      "title": "Heaven Can Wait - MJ",
      "platform": "tiktok",
      "region": "KR",
      "growth": "+180%",
      "commercial_ok": true
    }
  ],
  "video_formats": [
    {
      "pattern": "before_after_hook",
      "avg_views": 45000,
      "platform": "reels",
      "duration": "15s"
    }
  ],
  "community_buzz": [
    {
      "topic": "여름 슬리핑백 언제 바꿀까",
      "source": "맘카페",
      "mentions": 23,
      "sentiment": "neutral"
    }
  ],
  "global_early_signals": [
    {
      "topic": "bamboo sleep sack",
      "source": "reddit",
      "trend_stage": "emerging"
    }
  ]
}
```

### HTML 리포트 (모드 B)
인터랙티브 HTML 위클리 리포트:
- 단일 HTML 파일 (외부 의존성 없음, CDN 허용)
- Chart.js로 트렌드 차트
- 탭 구조: 키워드 | 사운드 | 영상 | 커뮤니티 | 해외 | 종합
- 각 항목에 content-pipeline / product-scout 연결 액션 버튼

파일 저장: `output/리포트/trend-radar_{YYYYMMDD}.html`

---

## 연동 스킬

| 연동 스킬 | 연동 방식 |
|----------|----------|
| **content-pipeline** | 급상승 키워드 + 트렌딩 사운드 + 인기 포맷 데이터를 콘텐츠 기획에 피딩 |
| **product-scout** | 검색 트렌드 + 해외 신호 + 커뮤니티 버즈를 신상품 기회 탐색에 피딩 |
| **competitive-intelligence** | 경쟁사 동향과 트렌드 데이터 교차 분석 |

---

## API 키 현황

| API | 상태 | 비용 |
|-----|------|------|
| 네이버 데이터랩 | **보유** (MCP naver-search) | 무료 |
| 네이버 검색광고 | **보유** | 무료 |
| YouTube Data API v3 | 발급 필요 (Google Cloud Console) | 무료 (10,000 units/일) |
| Instagram Graph API | 발급 필요 (Meta Business) | 무료 (비즈니스 계정) |
| Pinterest API v5 | 발급 필요 (Pinterest Business) | 무료 (비즈니스 계정) |
| Reddit API | 발급 필요 (reddit.com/prefs/apps) | 무료 (100 req/min) |
| Gemini Vision | **보유** | 무료 티어 |
| Claude API | **보유** | 사용량 기반 |

**네이버 API는 즉시 사용 가능. 나머지는 모두 무료 발급.**

## 참조 파일

- `references/api-sources.md` → 각 API 상세 엔드포인트 및 파라미터
