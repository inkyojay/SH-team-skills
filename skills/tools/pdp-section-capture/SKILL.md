---
name: pdp-section-capture
description: SundayHug PDP(상세페이지) HTML을 디자인 단위 섹션별로 잘라 고해상도 PNG 시리즈로 출력. HTML 주석(`<!-- HERO -->` 등)을 섹션 라벨로 인식하고, divider는 자동 스킵, 작은 brand-quote(.eq)는 앞 섹션에 자동 병합. 사용자가 (1) 상세페이지를 섹션별 이미지로 떨어뜨려달라거나, (2) Cafe24 업로드용 PNG 분할이 필요하거나, (3) 글씨 흐림 없이 supersampling으로 또렷한 섹션 이미지를 원할 때 사용. html-section-capture(Python/Playwright)와 달리 SundayHug의 `.pdp-absolute` + 주석 라벨링 + supersampling + 라이브 섹션 캡쳐로 특화됨.
triggers: 상세페이지 캡쳐, PDP 캡쳐, 섹션 분리, Cafe24 PNG, supersampling, .pdp-absolute, 디테일 페이지 이미지화, detail page screenshot, section split, pdp section
---

# PDP Section Capture

SundayHug 상세페이지(`.pdp-absolute` 컨테이너 + HTML 주석 라벨링 패턴)를 디자인 단위로 잘라 supersampling 적용한 고해상도 PNG로 떨어뜨리는 작업 스킬.

## 언제 쓰는가

- 상세페이지 HTML을 Cafe24 업로드용 섹션별 이미지로 만들어야 할 때
- 직접 Puppeteer fullPage 캡쳐를 했더니 글씨가 흐릿하거나 섹션이 중간에 잘릴 때
- `team-skills/html-section-capture` (Python/Playwright)는 generic하게 `section`, `[class*="section"]` 같은 셀렉터로 찾아서 SundayHug PDP의 실제 디자인 단위와 안 맞을 때

## 사전 요구사항

```bash
# Node 22+ 추천
cd /tmp && mkdir -p screenshot-tool && cd screenshot-tool
npm init -y
npm install puppeteer sharp
```

또는 이미 설치된 곳(`/tmp/screenshot-tool/node_modules/`)이 있으면 그걸 그대로 사용.

## 핵심 사용법

```bash
node /Users/inkyo/Projects/team-skills/skills/tools/pdp-section-capture/scripts/render-sections-smart.mjs \
  <html-path> <out-dir> [container=.pdp-absolute] [cssWidth=600] [outScale=3] [format=png] [quality=92] [superScale=4]
```

**SundayHug 표준 권장값** (글씨 또렷하게 + 비율 정확하게 + Cafe24 업로드 적정 크기):

```bash
node /Users/inkyo/Projects/team-skills/skills/tools/pdp-section-capture/scripts/render-sections-smart.mjs \
  "/path/to/swaddle_cotton_mesh.html" \
  "/path/to/swaddle_cotton_mesh/sections" \
  .pdp-absolute 600 3 png 92 4
```

이게 최종 검증된 조합. **outScale 3 + superScale 4** = Chrome에서 2400px로 그린 다음 lanczos3로 1800px로 다운샘플 → 글자 가장자리 super-crisp.

## 결과 예시

`sections/` 폴더에 다음과 같이 생성:

```
01_HERO.png                                 1800x1200
02_BADGE-BAR.png                            1800x140
03_INTRO.png                                1800x3969
04_나비잠-자세란.png                          ...
...
21_PRODUCT-INFO.png
```

- 파일명: `NN_<HTML주석라벨>.png` (한글/영문 혼용 OK)
- 폭: `cssWidth × outScale` (600 × 3 = 1800px)
- 높이: 각 섹션의 실제 비율 그대로

## 적용된 규칙 (이게 깔끔한 결과의 비결)

### 1. HTML 주석 = 섹션 라벨 (최우선)
```html
<!-- HERO -->
<div class="hero v">...</div>

<!-- FEAT 01 : 코튼 메쉬 통기성 -->
<div class="feat v">...</div>
```
→ `01_HERO.png`, `07_FEAT-01-코튼-메쉬-통기성.png`

직계 자식의 직전 형제 노드를 거슬러 올라가 가장 가까운 주석을 라벨로 사용. 콜론은 dash로, 공백도 dash로 sanitize.

### 1-2. 주석 없는 페이지 자동 폴백 (class 기반)

HTML에 `<!-- LABEL -->` 주석이 없어도 동작. 라벨 선택 우선순위:

1. **HTML 주석 라벨** — 있으면 이것 우선
2. **`KNOWN_SECTION_CLASSES`** — SundayHug PDP 시맨틱 클래스 (`hero`, `badge-bar`, `sec`, `feat`, `fi`, `cmp`, `eq`, `notice`, `rv-section`, `faq-list`, `final-cta`, `product-info`, `wash-sec`, `mid-cta` 등)
3. **유틸리티 아닌 첫 클래스** — `SKIP_CLASSES` (`v`, `on`, `divider`, `soft`, `tight`, `inset`, `rev`, `center`, `tx-c` 등)를 건너뛴 첫 토큰
4. **원시 첫 클래스** 또는 태그명 — 최후

예: `<div class="sec soft v">` → `sec` (KNOWN에서 매칭)  
예: `<div class="v feat">` → `feat` (KNOWN에서 매칭, `v` 스킵)  
예: `<div class="v some-random">` → `some-random` (유틸 `v` 스킵)

### 2. `<div class="divider">` 자동 스킵 (장식 구분선)

### 3. `<div class="eq">` (높이 < 400px) → **앞 섹션에 자동 병합**
브랜드 인용구가 독립 파일로 떨어지면 어색하므로, 바로 앞 섹션 끝에 자연스럽게 붙임.

### 4. 빈 주석 → 출력 안 됨
`<!-- TRUST POINTS -->` 다음에 실제 섹션 element가 없으면 그냥 무시 (정상 동작).

## 고해상도/선명도 비결 (이게 핵심)

### Supersampling (Chrome high-res render → lanczos3 downsample)
- `superScale=4` → Chrome이 2400px 폭으로 native render (subpixel AA 풍부하게 적용)
- `outScale=3` → lanczos3 커널로 1800px 폭으로 축소
- 4픽셀 → 1.78픽셀 평균화 → **글자 가장자리 매우 sharp + subpixel color fringe 자연 평균화로 사라짐**

### IntersectionObserver 무력화
페이지 inline JS가 `.v` 요소들을 처음에 opacity:0으로 숨기고 IO로 늦게 보여주는데, 이게 캡쳐 타이밍과 race가 남. `evaluateOnNewDocument`로 IO를 즉시 발화 버전으로 교체 → script가 `io.observe()` 호출하는 즉시 콜백이 동기 실행 → `.v` 요소가 첫 페인트부터 visible.

CSS도 belt-and-suspenders로 `.v { opacity: 1 !important; }` 강제.

### body 기본 margin 제거
브라우저 기본 `body { margin: 8px }` 때문에 좌우 8px 흰 띠가 생김. `html, body { margin: 0 !important; }` 강제 주입.

### 라이브 섹션 캡쳐 (이게 진짜 중요)
**❌ 안 좋은 방식**: fullPage PNG 한 번 떠놓고 좌표로 자름
- 측정 시점과 캡쳐 시점 사이에 이미지 로딩으로 layout shift 가능 → 섹션이 중간에 잘림

**✅ 적용된 방식**: 각 섹션을 `page.screenshot({ clip })`로 개별 캡쳐
- 캡쳐 직전에 `data-section-idx`로 element를 다시 찾아 라이브 bbox 측정
- 측정 ↔ 캡쳐 시점 동일 → 좌표 어긋날 일 없음
- 사전에 viewport를 docHeight로 고정해 fullPage reflow도 없음

### Aspect ratio 보존
sharp의 `resize({ width: X, fit: 'fill' })`이 한 axis만 줬을 때 height를 stretch할 수 있음. 명시적으로 `height: cssH × outScale`도 같이 넘겨야 비율 정확.

## 다른 컨테이너/디자인 패턴 적용

`.pdp-absolute` 외 다른 컨테이너면 3번째 인자로 셀렉터 전달:

```bash
node ... swaddle.html out/sections .pdp-modern 600 3 png 92 4
```

`<!-- LABEL -->` 주석 패턴이 없는 HTML이면 fallback으로 첫 클래스명을 라벨로 사용.

## 일괄 처리 패턴

여러 디테일 페이지를 한 번에:

```bash
for html in "/path/to/products"/*/swaddle_*.html; do
  base=$(basename "$html" .html)
  dir=$(dirname "$html")
  node /Users/inkyo/Projects/team-skills/skills/tools/pdp-section-capture/scripts/render-sections-smart.mjs \
    "$html" "$dir/sections" .pdp-absolute 600 3 png 92 4
done
```

## 트러블슈팅

| 증상 | 원인 | 해결 |
|---|---|---|
| 섹션이 중간에 잘림 | layout shift | 이미 라이브 캡쳐로 해결됨. 그래도 발생하면 wait 시간 늘리기 |
| 좌우에 흰 띠 | body margin | 이미 reset 주입됨. 다른 페이지면 inject CSS 확인 |
| 글씨 흐림 | 직출력 + grayscale AA | superScale을 outScale보다 1~2 단계 높게 |
| 비율 찌그러짐 | sharp resize 한 axis만 | height도 명시적으로 (이미 적용됨) |
| 한글 폰트 fallback | Google Fonts 늦게 로딩 | FontFaceSet.load() preload (이미 적용됨) |
| .v 요소가 빈 화면 | IntersectionObserver race | IO neuter (이미 적용됨) |

## 검증 완료된 환경

- macOS (M1/Intel)
- Node 22+
- Puppeteer headless (Chromium 번들)
- sharp (libvips lanczos3 커널)
- 테스트 HTML: `/Users/inkyo/Desktop/상세페이지 local (최종본)/newborn/butterfly-swaddle/cotton-mesh/swaddle_cotton_mesh.html`
- 결과: 21개 섹션, 1800px 폭, 비율 정상, 글씨 sharp
