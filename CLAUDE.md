# Team Skills 프로젝트 가이드

이 프로젝트는 마케팅 및 콘텐츠 제작을 위한 AI 스킬 & 에이전트 모음입니다.

## 폴더 구조

```
team-skills/
├── skills/                     # 모든 스킬 (카테고리별)
│   ├── content-creation/       # 콘텐츠 제작
│   ├── video/                  # 영상 제작
│   ├── advertising/            # 광고
│   ├── brand/                  # 브랜드 관리
│   ├── marketing/              # 마케팅 전략
│   └── tools/                  # 유틸리티 도구
├── agents/                     # AI 에이전트
├── commands/                   # 슬래시 커맨드
├── scripts/                    # 유틸리티 스크립트
├── SKILL-CATALOG.md            # 스킬 카탈로그 (자동 생성)
└── 사용가이드.html              # HTML 가이드 (자동 생성)
```

## 중요: 문서 자동 업데이트

스킬이나 에이전트를 추가/수정할 때 **반드시** 다음 명령을 실행하세요:

```bash
./scripts/update-docs.sh
```

또는 Python 스크립트 직접 실행:

```bash
python3 scripts/generate-catalog.py
```

이 명령은 다음을 자동으로 업데이트합니다:
- `SKILL-CATALOG.md` - 마크다운 카탈로그
- `사용가이드.html` - HTML 가이드

## 외부 스킬 설치하기 (GitHub 레포에서)

```bash
./scripts/install-skills.sh <repo> <category>
```

예시:
```bash
./scripts/install-skills.sh coreyhaines31/marketingskills marketing
./scripts/install-skills.sh vercel-labs/agent-skills tools
```

이 스크립트는 자동으로:
1. `npx skills add`로 스킬 다운로드
2. `skills/[카테고리]/`로 정리
3. 중복 스킬 스킵
4. 임시 폴더(`.agents/`, `.agent/`) 정리
5. 문서 자동 업데이트

## 새 스킬 직접 추가하기

1. 적절한 카테고리 폴더에 스킬 폴더 생성:
   ```
   skills/[카테고리]/[스킬명]/
   ```

2. `SKILL.md` 파일 작성 (frontmatter 필수):
   ```yaml
   ---
   name: 스킬명
   description: 스킬 설명
   triggers:
     - "트리거 문구1"
     - "트리거 문구2"
   ---
   ```

3. 문서 업데이트 실행:
   ```bash
   ./scripts/update-docs.sh
   ```

## 새 에이전트 추가하기

1. `agents/` 폴더에 `.md` 파일 생성
2. 문서 업데이트 실행

## 결과물 저장 규칙

**모든 스킬과 에이전트의 결과물은 반드시 각 팀원 로컬 `~/Desktop/team-skills/` 폴더에 저장합니다.**
(프로젝트 레포지토리에는 결과물을 저장하지 않음 — Git 용량 부담 방지)

| 작업 유형 | 저장 경로 | 예시 |
|----------|----------|------|
| 광고 카피 | `~/Desktop/team-skills/광고카피/` | `~/Desktop/team-skills/광고카피/swaddle-strap-copy.md` |
| 영상 소재 | `~/Desktop/team-skills/영상/` | `~/Desktop/team-skills/영상/reels-sleeping-bag.mp4` |
| 분석 리포트 | `~/Desktop/team-skills/리포트/` | `~/Desktop/team-skills/리포트/competitor-analysis.md` |
| 상세페이지 | `~/Desktop/team-skills/상세페이지/` | `~/Desktop/team-skills/상세페이지/product-landing.html` |
| 카드뉴스 | `~/Desktop/team-skills/카드뉴스/` | `~/Desktop/team-skills/카드뉴스/sleeping-bag-tips/` |
| 기타 | `~/Desktop/team-skills/기타/` | `~/Desktop/team-skills/기타/brand-guide.pdf` |

> 개별 스킬 폴더 내에 output을 만들지 마세요. 항상 사용자 Desktop의 `team-skills/` 하위에 저장하세요.
> Python: `Path.home() / "Desktop" / "team-skills" / "리포트"`
> 결과물 폴더가 없으면 스킬/스크립트가 자동 생성합니다 (`mkdir -p` 또는 `parents=True`).

## 카테고리 목록

| 카테고리 | 폴더 | 용도 |
|----------|------|------|
| 콘텐츠 제작 | `content-creation/` | 상세페이지, 카드뉴스, 라이브 페이지 |
| 영상 제작 | `video/` | 릴스 편집, Remotion |
| 광고 | `advertising/` | 배너, 메타 광고, 인스타, 카카오 |
| 브랜드 | `brand/` | 브랜드 분석, 제품 분석, 브랜드 가이드 |
| 마케팅 | `marketing/` | CRO, 카피, 전략 |
| 도구 | `tools/` | 유틸리티, 스킬 생성 |

## API 키 설정 가이드

일부 스킬은 외부 API 키가 필요합니다. 환경변수로 설정하세요.

### 보유 중인 키 (이미 설정됨)

| API | 환경변수 | 사용 스킬 |
|-----|---------|----------|
| 네이버 데이터랩 | MCP `naver-search`로 연동 | trend-radar, product-scout |
| 네이버 검색광고 | MCP `naver-search`로 연동 | trend-radar, product-scout |
| Gemini API | `GEMINI_API_KEY` | viral-shorts-maker, naver-blog-seo-writer |
| Claude API | `ANTHROPIC_API_KEY` | viral-shorts-maker, content-pipeline |

### 신규 발급 필요 (모두 무료)

| API | 환경변수 | 발급 URL | 사용 스킬 |
|-----|---------|---------|----------|
| YouTube Data API v3 | `YOUTUBE_API_KEY` | https://console.cloud.google.com | trend-radar |
| Instagram Graph API | `INSTAGRAM_ACCESS_TOKEN` | Meta Business Suite | trend-radar, content-pipeline |
| Pinterest API v5 | `PINTEREST_ACCESS_TOKEN` | https://developers.pinterest.com | trend-radar, product-scout |
| Reddit API | `REDDIT_CLIENT_ID` / `REDDIT_SECRET` | https://www.reddit.com/prefs/apps | trend-radar, product-scout |

### 선택 (유료, 필요 시)

| API | 환경변수 | 비용 | 사용 스킬 |
|-----|---------|------|----------|
| Apify (1688/Amazon) | `APIFY_API_TOKEN` | 무료~$49/mo | product-scout |
| SerpAPI (Google Trends) | `SERPAPI_KEY` | $75/mo | trend-radar |

### 설정 방법

```bash
# .env 또는 쉘 프로파일에 추가
export GEMINI_API_KEY="your-key"
export YOUTUBE_API_KEY="your-key"
export REDDIT_CLIENT_ID="your-id"
export REDDIT_SECRET="your-secret"
```

> 네이버 API는 MCP `naver-search` 서버로 이미 연동되어 있어 별도 설정 불필요.

## 브랜드별 작업 콘텐츠

상세페이지, 브랜드 스토리 등 브랜드별 작업 콘텐츠는 각 팀원 Desktop 하위에 브랜드 폴더로 관리합니다.

```
~/Desktop/team-skills/
├── 상세페이지/sundayhug/          # 상세페이지 HTML + images/
├── 브랜드가이드/sundayhug/pages/  # 브랜드 스토리 페이지
└── cafe24-skins/sundayhug/        # 카페24 스킨
```

상세페이지 작업 시:
- **편집**: `~/Desktop/team-skills/상세페이지/sundayhug/` 에서 직접 HTML 편집
- **프리뷰**: `cd ~/Desktop/team-skills/상세페이지/sundayhug && python3 -m http.server 8080`
- **이미지**: `~/Desktop/team-skills/상세페이지/sundayhug/images/` (상대경로로 참조)

## 미디어 대시보드 (MCP 연동)

미디어 에셋을 자연어로 관리할 수 있는 MCP 서버가 연동되어 있습니다.

### 접속 정보

- **대시보드 URL**: https://media-dashboard-production-7846.up.railway.app
- **MCP 서버**: `media-dashboard` (Claude Code에 글로벌 등록됨)

### 자연어 사용 예시

```
"products 폴더에 있는 사진 보여줘"
"manual 폴더 파일 목록"
"제품샷 검색해줘"
"이 파일들 AI로 분류해줘"
"인스타에서 새 게시물 가져와"
"abc-crib 폴더 사진으로 메타 광고 소재 만들어줘"
```

### MCP 도구 목록

| 도구 | 설명 | 예시 |
|------|------|------|
| `list_folders` | 폴더 목록 조회 | "폴더 보여줘" |
| `list_files` | 파일 목록 (폴더별 필터링) | "products 폴더 파일" |
| `get_file` | 파일 상세 정보 | "이 파일 정보 알려줘" |
| `search_media` | 미디어 검색 | "제품샷 검색" |
| `create_folder` | 폴더 생성 (하위 포함) | "새 폴더 만들어줘" |
| `move_files` | 파일 폴더 이동 | "이 파일 products로 옮겨" |
| `list_tags` | 태그 목록 | "태그 보여줘" |
| `tag_files` | 파일에 태그 추가 | "이 파일에 제품샷 태그 달아줘" |
| `classify_files` | AI 자동 분류 | "이 파일들 AI 분류해줘" |
| `classify_status` | AI 분류 큐 상태 | "분류 상태 확인" |
| `poll_instagram` | Instagram 미디어 가져오기 | "인스타에서 가져와" |
| `instagram_status` | Instagram 연결 상태 | "인스타 연결 상태" |
| `update_file` | 파일 메타데이터 수정 | "이 파일 설명 수정해줘" |

### 광고 소재 제작 워크플로우

1. 미디어 대시보드에서 소재 이미지 가져오기 (MCP)
2. `meta-ad-factory` 스킬로 광고 이미지 벌크 제작
3. 결과물은 `~/Desktop/team-skills/광고카피/` 에 저장

```
"abc-crib 폴더에서 제품 사진 가져와서 메타 광고 만들어줘"
```

### 팀원 설정 방법

1. `media-dashboard` 레포 clone
2. MCP 서버 의존성 설치:
   ```bash
   cd media-dashboard/mcp-server && npm install
   ```
3. Claude Code에 MCP 서버 등록:
   ```bash
   claude mcp add --scope user media-dashboard -- npx --prefix /path/to/media-dashboard/mcp-server tsx /path/to/media-dashboard/mcp-server/index.ts
   ```
4. Claude Code 재시작 후 사용 가능
