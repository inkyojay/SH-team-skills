# SundayHug PDP — Design Tokens (AI 컨텍스트 요약)

> 이 파일은 `pdp-builder` 스킬이 PDP HTML을 생성할 때 매번 읽는 톤앤매너 가이드다.
> 원본 마스터 CSS는 같은 디렉토리 `../assets/styles.css` (3,749줄, 67KB).

## 컨테이너 규칙

- **루트**: `<div class="pdp-absolute"> ... </div>` 안에 모든 섹션 배치
- **최대 너비**: 600px (`max-width: 600px; margin: 0 auto`)
- **모바일 우선**: 자체 reset + `box-sizing: border-box` + `overflow-x: hidden`
- **외부 폰트**: Google Fonts (CSS 내부에서 import 됨)

## 색상 팔레트 (CSS 변수)

| 토큰 | HEX | 용도 |
|---|---|---|
| `--accent` | `#C8A07C` | 메인 포인트 (탄(tan) 톤) |
| `--accent2` | `#B8956A` | 더 진한 포인트 |
| `--accent-light` | `#F0E6DA` | 하이라이트 배경 |
| `--bg` | `#FFFFFF` | 기본 배경 |
| `--bg-warm` | `#FAF7F4` | 웜 톤 섹션 (`.sec.warm`) |
| `--bg-warm2` | `#F5F0EB` | 더 진한 웜 |
| `--bg-cool` | `#F8F8FA` | 쿨 톤 (`.sec.cool`) |
| `--bg-soft` | `#F9F7F4` | 소프트 (`.sec.soft`) |
| `--bg-cream` | `#F5F1EC` | 크림 (`.sec.cream`) |
| `--bg-sage` | `#EEF2EE` | 세이지 그린 (`.sec.sage`) |
| `--bg-blush` | `#FBF5F3` | 블러시 핑크 (`.sec.blush`) |
| `--dark` | `#1A1A1A` | 본문 강조/제목 |
| `--dark2` | `#2C2C3A` | 서브 다크 |
| `--body` | `#444444` | 본문 |
| `--sub` | `#888888` | 서브 텍스트 |
| `--line` | `#EBEBEB` | 구분선 |
| `--line-warm` | `#E5DDD4` | 웜 구분선 |
| `--danger` | `#D4645C` | 경고/할인 강조 |

## 타이포그래피

- **디스플레이/장식**: `Cormorant Garamond` (영문 라벨, 우아한 헤더)
- **본문 한글**: `Noto Sans KR` (300/400/500/700)
- **본문 영문**: `DM Sans` (300/400/500)
- 클래스로 직접 지정 가능: `var(--font-en)` = DM Sans, `var(--font-display)` = Cormorant

## 섹션 컨테이너 (`.sec`)

| 변형 | 효과 |
|---|---|
| `.sec` | 기본 (흰 배경) |
| `.sec.warm` | `--bg-warm` 배경 |
| `.sec.warm2` | `--bg-warm2` 배경 |
| `.sec.cool` | `--bg-cool` 배경 |
| `.sec.soft` | `--bg-soft` 배경 |
| `.sec.cream` | `--bg-cream` 배경 |
| `.sec.sage` | `--bg-sage` 배경 |
| `.sec.blush` | `--bg-blush` 배경 |
| `.sec.dark` | 다크 배경 + 라이트 텍스트 |
| `.sec.bare` | 패딩 제거 |

`.sec` 자식 요소: `.sec-label` (영문 라벨) / `.sec-title` (메인 헤딩) / `.sec-desc` (본문) / `.sec-body` (긴 본문) / `.sec-img` / `.tx-center` 또는 `.tx-c` (가운데 정렬)

## 핵심 빌딩 블록

- `.hero` + `.hero-img` + `.hero-text` + `.hero-tag` + `.hero-sub` (또는 `.hero-eyebrow` + `<h1>`)
- `.trust-bar` 안에 `.trust-bar-item` 3개 (자동 구분선)
- `.badge-bar` 안에 `.badge-bar-item` (`.badge-bar-label` + `.badge-bar-sub`)
- `.bq` (brand quote, 큰 인용문 + `<small>SUNDAY HUG</small>`)
- `.fb-img` (full-bleed 이미지, 600px 가로 채움)
- `.fi` (inline 이미지, 둥근 모서리)
- `.thin-line` (얇은 가로 구분선, `.sec` 사이)
- `.hl` (인라인 하이라이트 — 본문 안 강조 텍스트)

## 섹션별 공통 패턴

- **FAQ**: `.faq-item` 안에 `.faq-q` + `.faq-a`
- **Step list**: `.step-list` 안에 `.step-item` (`.step-num` + `.step-title` + `.step-desc`)
- **Final CTA**: `.final-cta` 안에 `.final-cta-label` + `<h2>` + `<p>` + `.final-cta-note`
- **Wash/Care**: `.note-card` 안에 `.note-hd` + `.note-item` (strong + p)
- **2-col sub**: `.sub-2col` 안에 `.sub-2col-item` × 2

## HTML 주석 라벨링 규약 (필수)

각 섹션 시작 직전에 영문 대문자 주석을 넣는다. `pdp-section-capture` 스킬이 이 주석으로 섹션을 잘라낸다.

```html
<!-- HERO -->
<!-- TRUST BAR -->
<!-- INTRO -->
<!-- OVERVIEW -->
<!-- BRAND QUOTE -->
<!-- WHY {FEATURE} -->
<!-- FEAT 01 -- {feature_name} -->
<!-- FEAT 02 -- {feature_name} -->
<!-- USE CASE -->
<!-- FAQ -->
<!-- BRAND STORY -->
<!-- FINAL CTA -->
<!-- WASH & CARE -->
<!-- SPECS -->
```

## 스크롤 리빌 (선택)

- `.v` 클래스 = 초기 hidden, viewport 진입 시 `.on` 추가하여 fade-in
- 캡처용으로는 `pdp-capture-prep` 스킬이 자동 제거 — **생성 시점에는 그냥 `.v` 붙여둬도 무방**

## 절대 지키기

1. **`styles.css` 절대 수정 금지** — 12개 페이지가 공유하는 마스터다
2. 제품별 차이는 HTML 상단 인라인 `<style>` 블록에만 (예: `abc-cover.html`의 `.feat-hz`, `.comp-grid`, `.info-tbl`)
3. 이미지 URL은 Cafe24 절대 경로 사용 — `https://sundayhugkr.cafe24.com/skin-skin69/pdp/{category}/{slug}/images/{name}.webp`
4. 모든 텍스트는 한글 본문 + 영문 라벨/eyebrow 혼용 — 톤이 흔들리지 않게
