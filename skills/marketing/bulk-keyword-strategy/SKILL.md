---
name: bulk-keyword-strategy
description: |
  SundayHug 전제품 (PDP HTML 폴더 기반)을 일괄로 분석하여 네이버 SEO 키워드 전략을 1회 실행으로 생성하는 스킬.

  처리 흐름:
  ① PDP 폴더 스캔 → 모든 HTML 파싱 (제품명/USP/소재/사이즈/컬러)
  ② 슬러그 dedup (중복 카테고리 표시)
  ③ 카테고리별 시드 키워드 자동 도출
  ④ 네이버 검색광고 API → 연관 키워드 + 월간 검색수 + 경쟁도
  ⑤ 네이버 DataLab API → 12개월 트렌드 + 시즌성 판정
  ⑥ S/A/B/C/D 등급 자동 (검색량 + 경쟁도 + 시즌 보정)
  ⑦ 메인 키워드 1개 + 보조 4개 + 상품태그 10개 자동 선정
  ⑧ 50자 이내 네이버 상품명 1안 자동 생성 (브랜드실장 금기어 필터)
  ⑨ xlsx 1개 출력 (전제품 종합 + 카테고리별 시트)

  다음 상황에서 사용:
  - 시즌 진입 직전 전제품 키워드 일괄 갱신
  - 신제품 다수 추가 후 일괄 등록
  - 분기마다 정기적 키워드 재평가

  단일 제품만 보고 싶으면 --single 옵션.

  사용하지 말아야 할 때:
  - 1~2개 제품 분석 → keyword-optimizer 스킬이 더 빠름
  - 자사몰 자동 등록 → 별도 운영팀장 작업 (네이버 커머스 API)
triggers:
  - "전제품 키워드"
  - "전체 상품명"
  - "일괄 키워드"
  - "키워드 일괄"
  - "네이버 상품명 일괄"
  - "PDP 키워드 전략"
  - "bulk keyword"
  - "전제품 SEO"
---

# bulk-keyword-strategy — SundayHug 전제품 네이버 SEO 일괄 분석

## 무엇을 만드는가

PDP HTML 폴더 → 1회 실행 → xlsx 1개 (전제품 키워드 전략 종합)

## 결과물

```
~/Desktop/team-skills/리포트/keyword-strategy/
└── SundayHug-전제품-키워드-전략_{YYYY-MM-DD}.xlsx
   ├── 시트 "전제품 종합"  — 전 row 한눈에
   ├── 시트별 카테고리       — abc / daily-look / newborn / outlet / set-products / sleep-products / sleeping-bags
   └── 시트 "Meta"          — 생성 정보 + 등급 분포
```

xlsx 컬럼 (총 31개):
- 슬러그 / 카테고리 / 제품 정식명 / 1줄 USP / 소재 / 사이즈 / 컬러
- **네이버 상품명 (1안)** / 상품명 길이
- **메인 키워드** / 메인 검색량(월) / 메인 등급 / 경쟁도
- 보조1~4
- **태그1~10** (띄어쓰기 제거)
- 시즌 피크 / 현재 vs 피크 (%)
- 다중카테고리 / 경고

## 환경변수 (모두 필수)

| 변수 | 용도 | 발급처 |
|---|---|---|
| `NAVER_CUSTOMER_ID` | 검색광고 API | searchad.naver.com > 도구 > API |
| `NAVER_API_KEY` | 검색광고 API |  |
| `NAVER_SECRET_KEY` | 검색광고 API |  |
| `NAVER_CLIENT_ID` | DataLab + 쇼핑 API | developers.naver.com |
| `NAVER_CLIENT_SECRET` | DataLab + 쇼핑 API |  |

미설정 또는 `--skip-apis` 옵션 시 → 시드 키워드만으로 진행 (등급 매기기 X, 검증용).

## 의존성 설치

```bash
cd skills/marketing/bulk-keyword-strategy/scripts
pip install -r requirements.txt
```

## 사용법

### 전체 (기본)

```bash
# 환경변수 로드
set -a && . /path/to/.envrc && set +a

# 실행
python3 skills/marketing/bulk-keyword-strategy/scripts/bulk_keyword_research.py \
  --pdp-folder "~/Desktop/상세페이지 (절대경로)" \
  --output ~/Desktop/team-skills/리포트/keyword-strategy
```

### 단일 제품 시범

```bash
python3 skills/marketing/bulk-keyword-strategy/scripts/bulk_keyword_research.py \
  --single "sleep-products/cooling-pad/cooling-mesh-dual-pad.html" \
  --output /tmp/test
```

### API 스킵 (파싱+시드만)

```bash
python3 skills/marketing/bulk-keyword-strategy/scripts/bulk_keyword_research.py \
  --skip-apis \
  --output /tmp/test
```

## 폴더 구조

```
skills/marketing/bulk-keyword-strategy/
├── SKILL.md
├── scripts/
│   ├── bulk_keyword_research.py    # 메인 진입점
│   ├── parsers/
│   │   └── pdp_parser.py            # HTML 파싱 + dedup
│   ├── apis/
│   │   ├── naver_searchad.py       # 검색광고 keywordstool
│   │   ├── naver_datalab.py        # DataLab 트렌드
│   │   └── naver_shop.py           # 쇼핑 검색 (보조)
│   ├── analyzers/
│   │   ├── seed_keywords.py        # 카테고리별 시드 룰
│   │   ├── grader.py               # S/A/B/C/D 등급
│   │   └── name_generator.py       # 50자 상품명 생성
│   └── exporters/
│       └── xlsx_writer.py          # 7시트 출력
├── templates/
│   ├── product-name-formula.md     # 상품명 공식
│   └── tag-grading-rules.md        # 등급 룰
└── requirements.txt
```

## 처리 시간

- 파싱: ~2초/제품
- 검색광고 API: ~1초/제품 (rate limit 0.5초 대기)
- DataLab API: ~3초/제품 (5개 키워드까지)
- xlsx 출력: 5초
- **총 ~6~10분** (50개 제품 기준)

## 등급 룰 (요약)

| 등급 | 검색량 | 경쟁도 | 시즌 일치 |
|---|---|---|---|
| **S** | ≥ 10,000 | 또는 시즌+경쟁도 중하 보정 | × 1.3 |
| **A** | ≥ 5,000 | | |
| **B** | ≥ 1,000 | | |
| **C** | ≥ 100 | | |
| **D** | < 100 | | |

상세: `templates/tag-grading-rules.md`

## 상품명 생성 룰 (요약)

```
[브랜드] [시리즈] [메인키워드] [보조1] [소재] [보조2~3] [타겟] [시즌]
50자 이내 / 금기어 자동 필터
```

상세: `templates/product-name-formula.md`

## 절대 원칙

1. ✅ **모든 출력물 → 운영팀장 등록 전 시각 검토** (자동화는 1차 안만)
2. ✅ **상품명 → 브랜드실장 검수** (금기어는 자동 필터하지만 톤 검수는 수동)
3. ✅ **블록리스트 (호환 침대명)** 자동 제외 — 우리 SKU 아닌 키워드 X
4. ❌ **자동 등록 금지** — 네이버 커머스 API 연동은 별도 작업
5. ❌ **API 키 평문 노출 금지**

## 연계 스킬

| 단계 | 스킬 |
|---|---|
| 출력 검토 | [sundayhug-brand-director](../../brand/sundayhug-brand-director/SKILL.md) (상품명 톤 검수) |
| 단일 제품 분석 | [keyword-optimizer](../keyword-optimizer/SKILL.md) |
| 자사몰 등록 | [pdp-builder](../../content-creation/pdp-builder/SKILL.md) (PDP 생성) → 운영팀장 |
| 광고 빌드 | [meta-ad-factory](../../advertising/meta-ad-factory/SKILL.md) (메타 광고) |

## 후속 (이 스킬 범위 외)

- 네이버 커머스 API로 자동 등록 → 운영팀장 작업
- 등록 후 1~2주 태그사전 채택 모니터링 → 별도 cron
- 분기마다 재실행 → 트렌드 변화 반영

## 트러블슈팅

### 검색광고 API 403 "Invalid API-KEY"
- API 키가 만료되거나 폐기됨. searchad.naver.com > 도구 > API 사용 관리에서 갱신.

### DataLab API "Invalid Client"
- developers.naver.com 애플리케이션 등록 필요. 데이터랩 > 검색트렌드 사용 권한 활성.

### "스펙 추출 실패" 경고
- HTML에 `info-tbl` / `product-info-tbl` 태그가 없는 페이지. 수동 입력 필요 또는 무시.

### 빈 메인 키워드
- 검색광고 API에서 응답이 없거나 모든 키워드가 블록리스트에 걸림. 시드 룰 확장 또는 수동 보완.
