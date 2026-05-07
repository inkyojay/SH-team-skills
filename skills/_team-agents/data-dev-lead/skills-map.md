# 데이터/개발팀장 스킬 매핑

## Primary

| 스킬/도구 | 용도 |
|---|---|
| `xlsx`, `pdf` | 데이터 추출/정리 |
| `data-report-analyzer` (sub-agent) | CSV/엑셀 종합 분석 |
| `naver-ads-reporter` | API 헬스체크 (네이버 검색광고) |
| `batch-image-transform` | 자동화 파이프라인 |
| `update-docs.sh` (Bash) | 스킬 카탈로그 갱신 |

## MCP 운영 (직접 관리)

| MCP 서버 | 책임 |
|---|---|
| `naver-search` | 네이버 데이터랩 / 검색광고 / 검색 API |
| `media-dashboard` | 미디어 자산 관리 (Railway) |
| `supabase-sas` | DB |
| `pencil` | 디자인 파일 (.pen) |
| `figma` | Figma 연동 |
| `slack`, `gmail`, `vercel` 등 | 운영 부가 |

## 환경변수 관리 (출처: CLAUDE.md)

| 변수 | 사용 스킬 | 발급처 |
|---|---|---|
| `GEMINI_API_KEY` | viral-shorts-maker, naver-blog-seo-writer, batch-image-transform, tone-match-local | Google AI Studio |
| `ANTHROPIC_API_KEY` | viral-shorts-maker, content-pipeline | Anthropic |
| `YOUTUBE_API_KEY` | trend-radar | Google Cloud |
| `INSTAGRAM_ACCESS_TOKEN` | trend-radar, content-pipeline | Meta Business |
| `PINTEREST_ACCESS_TOKEN` | trend-radar, product-scout | Pinterest Dev |
| `REDDIT_CLIENT_ID/SECRET` | trend-radar, product-scout | Reddit |
| `APIFY_API_TOKEN` | product-scout (선택) | Apify |
| `SERPAPI_KEY` | trend-radar (선택) | SerpAPI |

(네이버 API는 MCP `naver-search` 서버로 통합)

## 신규 스킬 등록 절차

1. 스킬 폴더 생성 (`skills/{category}/{name}/SKILL.md`)
2. `SKILL.md` frontmatter 검증 (name / description / triggers)
3. 트리거 키워드 충돌 검사 (다른 스킬과)
4. `./scripts/update-docs.sh` 실행
5. SKILL-CATALOG.md 신규 항목 확인
6. 사용자가티 스트 호출 → 정상 작동 확인

## 자동화 스크립트 카탈로그 (수동 유지)

`automation-catalog.md`에 모든 cron 잡 + 스크립트 + 책임 부서 기록. 매주 월요일 갱신.

## 사용 금지

- ❌ 다른 부서 콘텐츠 직접 수정 금지
- ❌ 정식 절차 없이 새 스킬 추가 금지
- ❌ API 키 평문 노출 금지
