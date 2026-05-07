# API 키 관리 가이드

## 원칙

1. **모든 키는 환경변수** — `.env` 또는 쉘 프로파일 (`~/.zshrc`)
2. **절대 코드 / 로그 / 메시지에 평문 노출 금지**
3. **공유 시 안전 채널** (1Password / Bitwarden) 사용
4. **분기마다 사용량 점검**, 한도 80% 도달 시 알림

## 현재 키 카탈로그

### 사내 보유 (이미 설정)

| API | 환경변수 | 발급처 | 한도 | 사용 스킬 |
|---|---|---|---|---|
| 네이버 검색/광고 | MCP `naver-search` | 네이버 개발자 센터 | 일 25,000 호출 | trend-radar, product-scout, keyword-* |
| Gemini API | `GEMINI_API_KEY` | Google AI Studio | 분당 60 RPM (Free) | viral-shorts-maker, naver-blog-seo-writer, batch-image-transform, tone-match-local |
| Anthropic API | `ANTHROPIC_API_KEY` | Anthropic | 토큰 기반 | viral-shorts-maker, content-pipeline |

### 신규 발급 필요 (모두 무료)

| API | 환경변수 | 발급 URL | 사용 스킬 |
|---|---|---|---|
| YouTube Data API v3 | `YOUTUBE_API_KEY` | console.cloud.google.com | trend-radar |
| Instagram Graph API | `INSTAGRAM_ACCESS_TOKEN` | Meta Business Suite | trend-radar, content-pipeline |
| Pinterest API v5 | `PINTEREST_ACCESS_TOKEN` | developers.pinterest.com | trend-radar, product-scout |
| Reddit API | `REDDIT_CLIENT_ID` / `REDDIT_SECRET` | reddit.com/prefs/apps | trend-radar, product-scout |

### 선택 (유료)

| API | 환경변수 | 비용 | 사용 스킬 |
|---|---|---|---|
| Apify | `APIFY_API_TOKEN` | 무료 ~ $49/월 | product-scout (1688/Amazon) |
| SerpAPI | `SERPAPI_KEY` | $75/월 | trend-radar (Google Trends) |

## 신규 키 발급 SOP

1. 발급 URL에서 키 생성
2. 사용량 한도 / 비용 모델 확인
3. `.env` 또는 `~/.zshrc`에 환경변수로 추가
4. CLAUDE.md API 키 표에 추가
5. 영향 받는 스킬의 SKILL.md에 환경변수 명시
6. 분기 점검 catalog에 등록

## 키 회전 (Rotation) 룰

- **개인 노트북에만 저장** — 클라우드 / GitHub / 슬랙 X
- **6개월 1회 회전** (보안 권장)
- **퇴사 / 외주 종료 시 즉시 회전**
- **노출 의심 시** 즉시 회전 + 발급처 통보

## 트러블슈팅

| 증상 | 원인 가능성 | 해결 |
|---|---|---|
| `401 Unauthorized` | 키 만료 / 권한 없음 | 발급처에서 갱신 |
| `429 Too Many Requests` | 한도 초과 | 호출 빈도 줄이기 / 한도 증액 |
| `403 Forbidden` | API 비활성화 | 발급처에서 enable 확인 |
| `Network Error` | MCP 서버 다운 | 헬스체크 후 재시작 |

## 사용량 모니터링

매월 `cron.md` 3번 실행으로 한도 / 사용량 자동 체크.
80% 도달 시 즉시 CEO + 재무이사에 알림 (비용 영향).
