# Supabase 스키마 — 경쟁사 인텔리전스

프로젝트: `kppukyscaghqsccqvrsm` (기존 JAYCORP 프로젝트)
테이블 prefix: `ci_`

---

## 테이블 정의

### ci_competitors (경쟁사 마스터)
```sql
CREATE TABLE ci_competitors (
  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  brand_name      text NOT NULL,           -- 브랜드명
  brand_name_en   text,                    -- 영문명
  type            text NOT NULL,           -- 'primary' | 'secondary'
  naver_store_url text,                    -- 네이버 스마트스토어 URL
  instagram_handle text,                  -- 인스타 계정 (@제외)
  website_url     text,                   -- 공식 홈페이지
  price_range_min integer,                -- 최저가 (원)
  price_range_max integer,                -- 최고가 (원)
  main_categories text[],                 -- 주력 카테고리 배열
  is_active       boolean DEFAULT true,   -- 모니터링 활성화 여부
  notes           text,                   -- 메모
  created_at      timestamptz DEFAULT now(),
  updated_at      timestamptz DEFAULT now()
);
```

### ci_price_snapshots (일별 가격 스냅샷)
```sql
CREATE TABLE ci_price_snapshots (
  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  competitor_id   uuid REFERENCES ci_competitors(id),
  product_name    text NOT NULL,           -- 제품명
  product_url     text,                    -- 상품 URL
  price           integer NOT NULL,        -- 현재 판매가 (원)
  original_price  integer,                 -- 정가 (할인 전)
  discount_rate   numeric(5,2),            -- 할인율 (%)
  has_coupon      boolean DEFAULT false,   -- 쿠폰 여부
  coupon_amount   integer,                 -- 쿠폰 할인액
  review_count    integer,                 -- 리뷰 수
  rating          numeric(3,2),            -- 평점
  snapshot_date   date NOT NULL,           -- 수집 날짜
  created_at      timestamptz DEFAULT now(),
  UNIQUE(competitor_id, product_url, snapshot_date)
);
```

### ci_promo_events (프로모션 이벤트)
```sql
CREATE TABLE ci_promo_events (
  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  competitor_id   uuid REFERENCES ci_competitors(id),
  promo_type      text NOT NULL,           -- 'sale' | 'coupon' | 'bundle' | 'event' | 'timedeal'
  title           text NOT NULL,           -- 프로모션명
  description     text,                   -- 상세 내용
  discount_rate   numeric(5,2),           -- 할인율
  start_date      date,                   -- 시작일
  end_date        date,                   -- 종료일
  source_url      text,                   -- 발견 URL
  source_channel  text,                   -- 'naver' | 'instagram' | 'website'
  detected_at     timestamptz DEFAULT now(),
  is_active       boolean DEFAULT true
);
```

### ci_social_snapshots (소셜 지표 스냅샷)
```sql
CREATE TABLE ci_social_snapshots (
  id                  uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  competitor_id       uuid REFERENCES ci_competitors(id),
  platform            text NOT NULL,        -- 'instagram' | 'naver_blog' | 'mamcafe'
  followers_count     integer,              -- 팔로워 수
  posts_count         integer,              -- 총 게시물 수
  posts_7d            integer,              -- 최근 7일 게시물
  avg_likes_7d        numeric(10,2),        -- 평균 좋아요 (7일)
  avg_comments_7d     numeric(10,2),        -- 평균 댓글 (7일)
  has_sponsored       boolean,              -- 광고 게시물 여부
  top_hashtags        text[],               -- 주요 해시태그 배열
  content_types       jsonb,                -- {"product": 40, "ugc": 30, "event": 20, "ad": 10}
  snapshot_date       date NOT NULL,
  created_at          timestamptz DEFAULT now(),
  UNIQUE(competitor_id, platform, snapshot_date)
);
```

### ci_buzz_mentions (버즈/언급 데이터)
```sql
CREATE TABLE ci_buzz_mentions (
  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  competitor_id   uuid REFERENCES ci_competitors(id),
  source          text NOT NULL,            -- 'naver_blog' | 'naver_cafe' | 'instagram' | 'naver_review'
  source_url      text,
  title           text,
  content_summary text,                     -- 내용 요약 (원문 저장 금지)
  sentiment       text,                     -- 'positive' | 'negative' | 'neutral'
  sentiment_score numeric(3,2),             -- -1.0 ~ 1.0
  keywords        text[],                   -- 추출 키워드
  mention_date    date,
  collected_at    timestamptz DEFAULT now()
);
```

### ci_run_logs (실행 이력)
```sql
CREATE TABLE ci_run_logs (
  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  run_type        text NOT NULL,            -- 'daily' | 'weekly' | 'manual'
  status          text NOT NULL,            -- 'success' | 'partial' | 'failed'
  competitors_checked integer,             -- 조사한 경쟁사 수
  changes_detected integer,               -- 감지된 변경사항 수
  alerts_sent     integer,                -- 발송된 알림 수
  report_path     text,                   -- 생성된 리포트 경로
  error_details   jsonb,                  -- 오류 내용 (있을 경우)
  duration_secs   integer,                -- 실행 소요 시간
  started_at      timestamptz DEFAULT now(),
  completed_at    timestamptz
);
```

---

## 인덱스 (성능 최적화)
```sql
CREATE INDEX idx_ci_price_snapshots_date ON ci_price_snapshots(snapshot_date DESC);
CREATE INDEX idx_ci_price_snapshots_competitor ON ci_price_snapshots(competitor_id);
CREATE INDEX idx_ci_social_snapshots_date ON ci_social_snapshots(snapshot_date DESC);
CREATE INDEX idx_ci_buzz_mentions_date ON ci_buzz_mentions(mention_date DESC);
CREATE INDEX idx_ci_buzz_mentions_sentiment ON ci_buzz_mentions(sentiment);
CREATE INDEX idx_ci_promo_events_active ON ci_promo_events(is_active, end_date);
```

---

## 유용한 쿼리

### 최근 가격 변동 감지
```sql
SELECT 
  c.brand_name,
  p_today.product_name,
  p_yesterday.price AS price_yesterday,
  p_today.price AS price_today,
  ROUND(((p_today.price - p_yesterday.price)::numeric / p_yesterday.price) * 100, 1) AS change_pct
FROM ci_price_snapshots p_today
JOIN ci_price_snapshots p_yesterday 
  ON p_today.competitor_id = p_yesterday.competitor_id
  AND p_today.product_url = p_yesterday.product_url
  AND p_yesterday.snapshot_date = CURRENT_DATE - 1
JOIN ci_competitors c ON p_today.competitor_id = c.id
WHERE p_today.snapshot_date = CURRENT_DATE
  AND ABS(p_today.price - p_yesterday.price)::numeric / p_yesterday.price > 0.1
ORDER BY ABS(change_pct) DESC;
```

### 브랜드별 버즈 점유율
```sql
SELECT 
  c.brand_name,
  COUNT(*) AS mention_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS buzz_share_pct,
  AVG(bm.sentiment_score) AS avg_sentiment
FROM ci_buzz_mentions bm
JOIN ci_competitors c ON bm.competitor_id = c.id
WHERE bm.mention_date >= CURRENT_DATE - 7
GROUP BY c.brand_name
ORDER BY mention_count DESC;
```
