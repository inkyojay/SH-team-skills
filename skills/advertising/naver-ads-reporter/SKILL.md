---
name: naver-ads-reporter
description: >
  썬데이허그(JAYCORP) 네이버 검색광고 계정의 집행 성과 데이터를 API로 직접 조회하여
  캠페인/광고그룹/키워드/상품(NV_MID)별 성과 리포트를 자동 생성하는 스킬.
  노출/클릭/비용/전환/ROAS/CTR/CPC를 일별/기간별로 집계하고, 낭비 키워드·고효율
  상품·기간 비교(WoW/MoM)·이상치 탐지까지 수행한 뒤 인터랙티브 HTML 리포트로 출력한다.

  다음 상황에서 반드시 이 스킬을 사용한다:
  - "네이버 광고 성과", "광고 리포트", "광고 보고서", "광고 집행 결과" 요청
  - "ROAS 조회", "캠페인 성과", "광고비 얼마 썼어", "이번달 광고비" 요청
  - "키워드 성과", "광고 키워드 분석", "낭비 키워드 찾아줘", "비효율 키워드" 요청
  - "쇼핑검색광고 성과", "상품별 광고 성과", "SKU별 ROAS" 요청
  - "광고 효율 분석", "CPC 얼마야", "전환율 얼마야", "CTR 얼마야" 요청
  - "지난주 대비", "전월 대비 광고" 등 기간 비교 요청
  - "광고 이상치", "광고비 갑자기 늘었어" 등 모니터링 요청
  - 썬데이허그 검색광고/쇼핑검색광고 집행 데이터 조회/분석 요청
---

# 네이버 광고 성과 리포터

네이버 검색광고 API로 썬데이허그 광고 계정의 실제 집행 성과를 가져와서
캠페인/키워드/상품별로 분석하고 인터랙티브 HTML 리포트를 생성하는 스킬.

관련 문서: `references/api-reference.md`, `references/report-types.md`

---

## 전체 플로우

```
STEP 0  API 크레덴셜 확인 (환경변수 or 사용자 입력)
   ↓
STEP 1  조회 범위 확정 (기간, 리포트 타입, 차원)
   ↓
STEP 2  Stat Report 비동기 발급 → 폴링 → TSV 다운로드
   ↓
STEP 3  데이터 가공 (집계, Top N, 낭비 키워드, 기간 비교)
   ↓
STEP 4  인터랙티브 HTML 리포트 생성 + /mnt/user-data/outputs 저장
```

---

## STEP 0 — API 크레덴셜 확인

### 필요한 값 3종
- `CUSTOMER_ID` (광고주 번호, 숫자)
- `API_KEY` (액세스라이선스)
- `SECRET_KEY` (비밀키)

### 확인 순서
1. **환경변수 우선 확인**:
   - `NAVER_AD_CUSTOMER_ID`
   - `NAVER_AD_API_KEY`
   - `NAVER_AD_SECRET_KEY`
2. 없으면 사용자에게 직접 요청:
   ```
   네이버 검색광고 API 크레덴셜이 필요합니다. searchad.naver.com
   > 도구 > API 사용 관리에서 확인 가능합니다.
   ```
3. 받은 값은 **현재 세션에서만** 사용, 저장하지 않음.

---

## STEP 1 — 조회 범위 확정

### 기본 기본값
- 사용자가 기간 명시 안 하면: **최근 7일**
- "이번달" → 이번달 1일~어제
- "지난달" → 지난달 전체
- "지난주" → 지난주 월~일
- 최대 조회 범위: **과거 365일**

### 리포트 타입 선정 (사용자 질문별)
| 사용자 질문 | 리포트 타입 | 차원 |
|---|---|---|
| "광고 성과", "전체 집행" | AD | 캠페인/광고그룹/광고 |
| "키워드 성과", "낭비 키워드" | KEYWORD | 키워드 |
| "상품별", "SKU별", "쇼핑검색광고" | SHOPPING_PRODUCT | NV_MID |
| "전환 분석" | AD_CONVERSION | 캠페인/전환유형 |
| "디바이스별" | AD_DETAIL | PC/Mobile |

여러 타입이 필요한 질문(예: "전체 광고 정리해줘")은 순차 발급.

---

## STEP 2 — Stat Report 발급 & 다운로드

`scripts/stat_report.py`를 활용. 비동기 플로우:

```
POST /stat-reports { reportTp, statDt }  →  reportJobId
   ↓ (폴링 3~10초 간격)
GET /stat-reports/{id}  →  status: REGIST → RUNNING → BUILT
   ↓ (BUILT 수령)
GET {downloadUrl}  →  TSV 파일
```

### 폴링 규칙
- 최대 대기: 180초
- 폴링 간격: 3초 → 실패하면 5초 → 10초 (지수 증가)
- 타임아웃 시 사용자에게 "리포트 생성이 지연됩니다. 잠시 후 재시도 하시겠어요?" 물어보기

### 실행 예시
```bash
cd /mnt/skills/user/naver-ads-reporter
python scripts/stat_report.py \
  --customer-id $NAVER_AD_CUSTOMER_ID \
  --api-key $NAVER_AD_API_KEY \
  --secret-key $NAVER_AD_SECRET_KEY \
  --report-tp AD \
  --date-from 2026-04-14 \
  --date-to 2026-04-20 \
  --output /tmp/report_ad.tsv
```

---

## STEP 3 — 데이터 가공

`scripts/analyzer.py`의 함수들을 조합:

### 기본 집계
- `summarize_overall(df)` — 전체 노출/클릭/비용/전환/ROAS 한 줄 요약
- `by_campaign(df)` — 캠페인별 집계
- `daily_trend(df)` — 일별 추이 (차트용)

### 심층 분석
- `top_keywords(df, metric='cost', n=20)` — 지표 Top N
- `wasted_keywords(df, min_cost=10000)` — 비용만 쓰고 전환 0인 키워드
- `product_roas_rank(df, top=20)` — 쇼핑검색광고 상품 ROAS 순위
- `compare_periods(df_a, df_b)` — 기간 간 증감률
- `detect_anomaly(df, metric, z_threshold=2.5)` — z-score 기준 이상치

### 판단 기준 (리포트에 반영)
- ROAS 500% 미만 = 개선 필요 (썬데이허그 기준)
- CTR 2% 미만 + 노출 1000+ = 소재/키워드 점검 필요
- 비용 10,000원 이상 × 전환 0 = 낭비 키워드 분류
- 전일 대비 비용 ±50% = 이상치 알림

---

## STEP 4 — HTML 리포트 생성

`scripts/html_renderer.py`의 `render_report()` 호출.

### 리포트 구조
1. **헤더**: 기간, 조회 시각, 계정명
2. **핵심 지표 카드**: 총 비용, 노출, 클릭, 전환, ROAS, CPC
3. **일별 추이 차트**: Chart.js line chart (비용 + 클릭 + 전환)
4. **캠페인별 성과 테이블**: 정렬/필터 가능
5. **키워드 분석**: Top 비용 / Top ROAS / 낭비 키워드 3섹션
6. **상품(SKU) 성과**: 쇼핑검색광고 리포트 포함 시만
7. **인사이트 요약**: 분석 결과 기반 3~5개 액션 아이템
8. **푸터**: 데이터 출처 (네이버 측정 기준) + 면책 고지

### 디자인 톤
- 썬데이허그 브랜드 컬러 (코랄 #FF6B6B, 베이비 블루 #A8E6CF)
- 폰트: Pretendard
- 모바일 반응형
- 숫자는 한국식 포맷 (예: 1,234,567원, 12.3%)

### 출력 경로
`/mnt/user-data/outputs/naver_ads_report_YYYYMMDD_HHMM.html`

---

## 주의사항 & 주의할 점

### 전환 수치 고지
네이버 광고의 전환/전환매출은 네이버 자체 전환 추적 기준이며,
스마트스토어 실제 매출/Cafe24 실제 매출과 **숫자가 다를 수 있음**.
리포트 푸터에 반드시 명시:
> "※ 전환 지표는 네이버 광고 시스템의 측정 기준이며, 실제 판매 데이터와 다를 수 있습니다."

### 대용량 리포트 쿼터
- 1일 발급 개수 제한 있음 → 같은 세션에서 동일 리포트 재발급 자제
- 이미 받은 TSV는 `/tmp`에 캐시하고 세션 내 재사용

### API 에러 대응
- `400 invalid.signature` → 시그니처 생성 로직 재확인 (timestamp 단위: ms)
- `401 unauthorized` → 키 만료 or 잘못됨 → 사용자에게 재확인
- `429 rate limit` → 60초 대기 후 재시도, 3회 실패 시 포기

### 읽기 전용 원칙 (v1)
이 스킬은 **읽기 전용**. 캠페인/광고그룹/키워드 생성·수정·삭제·상태변경
API는 절대 호출하지 않음. 입찰가 조정도 안 함.

---

## 참고 리소스

상세 API 스펙은 `references/api-reference.md` 참조.
리포트 타입별 컬럼은 `references/report-types.md` 참조.
설치/환경설정은 `README.md` 참조.

---

## 다음 단계 (Phase 3+)

- 이 스킬로 수집한 데이터를 Supabase `naver_ads` 스키마에 적재 (Phase 3)
- MCP 서버화하여 Hermes Workers에서 자동 호출 (Phase 4)
- 경쟁사 분석(competitive-intelligence) + 자사 광고 성과 결합 리포트 (Phase 4)
