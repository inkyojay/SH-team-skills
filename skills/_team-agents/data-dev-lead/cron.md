# 데이터/개발팀장 주기적 작업

## 매일

### 1. MCP 서버 헬스체크 — 매일 6:17

**Cron**: `17 6 * * *`

**프롬프트**:
```
모든 MCP 서버 헬스체크:

- naver-search (네이버 검색광고 / DataLab API)
- media-dashboard (Railway URL 응답)
- supabase-sas (DB 연결)
- pencil (.pen 파일 접근)
- figma (Figma API)

각 서버:
- ✅ 정상 (응답 < 2s)
- 🟡 느림 (응답 2~10s)
- 🔴 다운 (응답 없음 / 에러)

🔴 발견 시 즉시 CEO + 영향 받는 부서장에게 알림.

저장: ~/Desktop/team-skills/리포트/data-dev/health-checks/{YYYY-MM-DD}.md
```

## 매주

### 2. 주간 스킬 카탈로그 점검 — 매주 월 7:17

**Cron**: `17 7 * * 1`

**프롬프트**:
```
이번 주 스킬 시스템 상태 점검:

1. 신규 스킬 추가/변경 (지난 1주) — `git log` 기반
2. SKILL-CATALOG.md 최신 상태 확인 → 미갱신 시 `./scripts/update-docs.sh` 자동 실행
3. 스킬 사용 빈도 (지난 4주) — 사용 0회 스킬 deprecate 후보 리스트
4. 트리거 키워드 충돌 검사 (다중 스킬이 같은 트리거)
5. 자동화 cron 카탈로그 (`automation-catalog.md`) 갱신

저장: ~/Desktop/team-skills/리포트/data-dev/skill-catalog-changes/{YYYY-MM-DD}.md
```

## 매월

### 3. API 사용량 / 한도 점검 — 매월 마지막 영업일 16:17

**Cron**: `17 16 25-31 * 5`

**프롬프트**:
```
이번 달 API 사용량 / 한도 점검:

- 네이버 검색광고 API (월 한도 vs 사용량)
- Gemini API (토큰 사용 / 비용)
- YouTube API (할당량)
- Reddit API (요청 수)
- Anthropic API (Claude 토큰)

각 API:
- 사용량 / 한도
- 다음 달 예상
- 임계치 (80%) 근접 알림
- 비용 트렌드

저장: ~/Desktop/team-skills/리포트/data-dev/api-usage/{YYYY-MM}.md
한도 80%↑ API는 즉시 CEO + 재무이사 알림.
```

## 즉시 대응 트리거 (cron 아님)

| 신호 | 임계치 | 대응 |
|---|---|---|
| MCP 서버 다운 | 2회 연속 헬스체크 실패 | 즉시 재시작 + CEO 알림 |
| API 한도 90%↑ | 월 한도 90% | 사용 줄이기 + CEO 알림 |
| 신규 스킬 충돌 | 트리거 키워드 중복 | 등록 거부 + 작성자에 알림 |
| Cafe24 데이터 수신 끊김 | 2시간 무응답 | 운영팀장 + CEO 알림 |

---

## 페이퍼클립 등록 우선순위

1. **1번(헬스체크)** — 첫 활성화
2. **2번(주간 카탈로그)**
3. **3번(월간 API 사용량)**
