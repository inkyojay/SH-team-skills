# Trend Radar API 소스 상세

## 1. 네이버 데이터랩 (MCP naver-search)

### 검색어 트렌드
```
MCP tool: datalab_search
params:
  startDate: "2026-01-01"
  endDate: "2026-04-08"
  timeUnit: "week"
  keywordGroups:
    - groupName: "슬리핑백"
      keywords: ["아기 슬리핑백", "베이비 슬리핑백", "아기 수면조끼"]
    - groupName: "속싸개"
      keywords: ["아기 속싸개", "신생아 속싸개"]
  device: ""  # PC+모바일
  gender: ""  # 전체
  ages: []    # 전체
```

### 쇼핑 인사이트 카테고리
```
MCP tool: datalab_shopping_category
params:
  startDate: "2026-01-01"
  endDate: "2026-04-08"
  timeUnit: "week"
  category: [
    {"name": "유아수면용품", "param": ["50005542"]},
    {"name": "유아의류", "param": ["50005541"]}
  ]
```

### 쇼핑 키워드 트렌드
```
MCP tool: datalab_shopping_keywords
params:
  startDate: "2026-01-01"
  endDate: "2026-04-08"
  timeUnit: "week"
  category: "50005542"  # 유아수면용품
  keyword: [
    {"name": "슬리핑백", "param": ["슬리핑백", "아기 슬리핑백"]},
    {"name": "속싸개", "param": ["속싸개", "아기 속싸개"]}
  ]
```

### 세그먼트별 분석
```
MCP tools:
  - datalab_shopping_by_age → 연령별 클릭 비율
  - datalab_shopping_by_gender → 성별 클릭 비율
  - datalab_shopping_by_device → PC/모바일 비율
  - datalab_shopping_keyword_by_age → 키워드별 연령 분석
```

## 2. 네이버 검색광고 API

### 연관 키워드 조회
```
GET https://api.searchad.naver.com/keywordstool
Headers:
  X-API-KEY: {API_KEY}
  X-Customer: {CUSTOMER_ID}
  X-Signature: {HMAC-SHA256}
  X-Timestamp: {timestamp}
Params:
  hintKeywords: "아기 슬리핑백"
  showDetail: 1
```

응답 데이터:
- `monthlyPcQcCnt`: PC 월간 검색량
- `monthlyMobileQcCnt`: 모바일 월간 검색량
- `monthlyAvePcClkCnt`: PC 월평균 클릭수
- `compIdx`: 경쟁도 (높음/중간/낮음)

## 3. YouTube Data API v3

### 인기 영상 조회
```
GET https://www.googleapis.com/youtube/v3/videos
?part=snippet,statistics,contentDetails
&chart=mostPopular
&regionCode=KR
&videoCategoryId=22
&maxResults=50
&key={API_KEY}
```

### 검색 (키워드별)
```
GET https://www.googleapis.com/youtube/v3/search
?part=snippet
&q=아기+슬리핑백
&type=video
&regionCode=KR
&order=viewCount
&publishedAfter=2026-03-01T00:00:00Z
&maxResults=25
&key={API_KEY}
```

## 4. TikTok Creative Center

### 트렌딩 음악
```
크롤링 대상: https://ads.tiktok.com/business/creativecenter/music/pc/en
필터: country_code=KR, period=7 (7일)
수집: 음악명, 아티스트, 사용 영상 수, 증가율, 상업용 여부
```

### 트렌딩 해시태그
```
크롤링 대상: https://ads.tiktok.com/business/creativecenter/hashtag/pc/en
필터: country_code=KR, period=7
수집: 해시태그, 조회수, 증가율, 관련 해시태그
```

## 5. TokChart

```
크롤링 대상: https://tokchart.com
수집: 24시간/주간 트렌딩 사운드, 지역 랭킹, 스코어
```

## 6. Reddit API

### 인기글 조회
```
GET https://oauth.reddit.com/r/{subreddit}/hot
Headers: Authorization: Bearer {ACCESS_TOKEN}
Params: limit=50, t=week

주요 서브레딧:
- r/beyondthebump (30만+)
- r/parenting (500만+)
- r/NewParents
- r/babyledweaning
- r/sleeptrain (수면 훈련 전문)
```

### 검색
```
GET https://oauth.reddit.com/r/{subreddit}/search
Params: q="sleep sack" OR "swaddle", sort=new, t=month
```

## 7. Pinterest API v5

### 트렌딩 검색어
```
GET https://api.pinterest.com/v5/trends/search
Headers: Authorization: Bearer {ACCESS_TOKEN}
Params: region=KR, trend_type=growing
```

### 핀 검색
```
GET https://api.pinterest.com/v5/search/pins
Params: query="baby sleep", sort_by=popularity
```

## 8. Instagram Graph API

### 자사 계정 인사이트
```
GET https://graph.facebook.com/v19.0/{ig-user-id}/media
?fields=id,caption,media_type,timestamp,like_count,comments_count,
        insights.metric(impressions,reach,saved,shares)
&access_token={TOKEN}
```

### 해시태그 검색
```
GET https://graph.facebook.com/v19.0/ig_hashtag_search
?q=아기슬리핑백
&user_id={IG_USER_ID}
&access_token={TOKEN}
```

## 9. Google Trends (pytrends)

```python
from pytrends.request import TrendReq

pytrends = TrendReq(hl='ko', tz=540)
pytrends.build_payload(
    kw_list=["아기 슬리핑백", "아기 속싸개"],
    timeframe="today 3-m",
    geo="KR"
)
interest = pytrends.interest_over_time()
related = pytrends.related_queries()
```

## 10. Gemini Vision (이미지 분석)

```python
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.0-flash")
response = model.generate_content([
    "이 인스타그램 피드 이미지의 톤, 무드, 컬러 팔레트, 촬영 스타일을 분석해줘.",
    image_data
])
```
