# naver-ads-reporter

썬데이허그(JAYCORP) 네이버 검색광고 계정의 집행 성과를
API로 직접 조회하여 인터랙티브 HTML 리포트로 만드는 Claude Skill.

---

## 설치

이 스킬 디렉터리 전체를 `/mnt/skills/user/naver-ads-reporter/`로 업로드하면 됩니다.
Claude가 스킬 설명의 트리거 문구를 감지하면 자동 로딩됩니다.

## 크레덴셜 준비

1. https://searchad.naver.com 로그인
2. 우측 상단 **광고시스템** → **도구** → **API 사용 관리**
3. 다음 3개 값 확인:
   - `CUSTOMER_ID` (광고주 번호, 숫자)
   - `API_KEY` (액세스라이선스)
   - `SECRET_KEY` (비밀키)

## 사용 방법

### A. 환경변수로 제공 (권장)

스킬 실행 전에 다음을 설정:
```bash
export NAVER_AD_CUSTOMER_ID="3216549"
export NAVER_AD_API_KEY="0100000..."
export NAVER_AD_SECRET_KEY="AQAAAAA..."
```

### B. 대화 중 Claude에게 직접 전달

```
Claude: 네이버 검색광고 API 크레덴셜이 필요합니다.
You:    customer_id=3216549, api_key=..., secret_key=...
```

이 경우 값은 **현재 세션에서만** 사용되고 어디에도 저장되지 않습니다.

## 트리거 예시

스킬이 자동으로 실행되는 사용자 발화 예:
- "네이버 광고 성과 보여줘"
- "이번달 ROAS 어때?"
- "지난주 대비 광고비 비교해줘"
- "낭비 키워드 찾아줘"
- "쇼핑검색광고 상품별 성과"
- "광고 이상치 있어?"

## 직접 CLI 실행

```bash
cd /mnt/skills/user/naver-ads-reporter

# 지난 7일 + 쇼핑검색광고 포함
python scripts/run_report.py --preset last7 --include-shopping

# 특정 기간
python scripts/run_report.py --date-from 2026-04-01 --date-to 2026-04-20

# 인증 테스트만
python scripts/naver_ads_client.py --test
```

## 파일 구조

```
naver-ads-reporter/
├── SKILL.md                    ← Claude가 읽는 스킬 진입점
├── README.md                   ← 이 파일
├── scripts/
│   ├── naver_ads_client.py     ← API 클라이언트 (HMAC + 요청)
│   ├── stat_report.py          ← 대용량 보고서 발급/폴링/다운로드
│   ├── analyzer.py             ← 분석 함수 (Top N, 낭비, 비교, 이상치)
│   ├── html_renderer.py        ← HTML 리포트 렌더러
│   └── run_report.py           ← E2E 오케스트레이션 (메인)
└── references/
    ├── api-reference.md        ← 엔드포인트 상세 스펙
    └── report-types.md         ← 리포트 타입별 가이드
```

## 출력

- 기본 경로: `/mnt/user-data/outputs/naver_ads_report_YYYYMMDD_HHMM.html`
- 단일 HTML 파일 (브라우저에서 바로 열기 가능)
- Chart.js로 일별 추이 차트 렌더링
- 캠페인/키워드/상품 테이블 탭 전환

## 판단 기준 (썬데이허그 기본값)

| 지표 | 양호 | 경고 | 위험 |
|---|---|---|---|
| ROAS | 500%+ | 200~500% | 0~200% |
| CTR | 3%+ | 2~3% | <2% (+ 노출 1,000+) |
| 낭비 키워드 | - | - | 비용 10,000원+ × 전환 0 |
| 비용 이상치 | - | - | 평균 대비 ±50% (z-score 2.5+) |

이 기준은 `scripts/analyzer.py`의 `generate_insights()`에서 조정 가능.

## 제약 사항 (v1)

1. **읽기 전용**: 캠페인/입찰가 수정 API는 절대 호출 안 함
2. **과거 365일**까지만 조회 가능 (네이버 API 제약)
3. **전환 지표**는 네이버 측정 기준 — 실매출과 다를 수 있음
4. **성과형 디스플레이(GFA)** 미지원 — 공식 파트너사만 API 접근 가능
5. **일자별 발급 필요**: 7일이면 7번 API 호출 (약 7×15초 = 1.5분 소요)

## 알려진 이슈 / TODO

- [ ] AD_CONVERSION 리포트 자동 merge (현재는 AD 리포트의 전환 컬럼만 사용)
- [ ] 광고 소재(ad_id) 단위 분석 섹션
- [ ] 검색어(searchQuery) 리포트 — 별도 엔드포인트 필요
- [ ] Supabase 자동 적재 (Phase 3에서 추가)
- [ ] MCP 서버화 (Phase 4에서 추가)

## 관련 스킬

- `sundayhug-marketing-planner` — 롱테일 키워드 발굴 시 이미 집행 중인 키워드 필터링 연동 가능
- `promotion-planner` — 프로모션 기간 성과 자동 회고에 활용
- `competitive-intelligence` — 경쟁사 분석 + 자사 광고 효율 결합 리포트 가능 (Phase 4)
- `new-product-planner` — 시장 기회 분석에 자사 실집행 데이터 반영 가능

## 문의 / 수정

수정이 필요하면 Claude에게:
```
naver-ads-reporter 스킬에서 [원하는 변경사항]을 수정해줘
```
