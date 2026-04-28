---
name: live-page-builder
description: |
  네이버 쇼핑라이브 등 라이브 커머스 랜딩 페이지를 자동 생성하는 스킬.
  사용자와 대화로 라이브 전용 정보(호스트/일정/혜택/가격/쿠폰)를 받고, 사용자가 제공한
  상세페이지 HTML 경로를 참조해서 31개 라이브 섹션 템플릿(SynologyDrive 동기화) 중
  필요한 13~14개를 골라 모놀리식 라이브 페이지를 만든다.
  각 섹션은 600px 폭 standalone HTML로 생성되고 → Playwright로 정확한 콘텐츠 높이의
  PNG 추출 → 미리보기 그리드에서 다운로드. 12개 캠페인 팔레트 자동 매핑(시즌→팔레트).

  반드시 STEP 0 인터뷰 대화 먼저 진행 (한 번에 한 질문). 4가지 핵심 항목 확정 후
  요약 → 동의 → 빌드 순서. 인터뷰 답변은 `spec.json`으로 저장돼 재실행 시 활용 가능.

  다음 상황에서 반드시 이 스킬을 사용한다:
  - "라이브 페이지 만들어줘", "라이브 커머스 페이지", "쇼핑라이브 페이지" 요청
  - "네이버 라이브 프리미엄 페이지", "라이브 랜딩" 요청
  - 특정 캠페인 라이브 (예: "5월 가정의달 라이브") 페이지 제작 요청
  - 기존 `~/Desktop/output/상세페이지/네이버라이브_프리미엄/` 같은 결과물을 새로 만들고 싶을 때
triggers:
  - "라이브 페이지"
  - "라이브 페이지 만들어줘"
  - "라이브 커머스 페이지"
  - "쇼핑라이브 페이지"
  - "네이버 라이브"
  - "네이버 라이브 프리미엄"
  - "라이브 랜딩"
  - "live page"
  - "라이브 상세페이지"
---

# Live Page Builder

네이버 쇼핑라이브용 모놀리식 랜딩 페이지를 인터뷰 → 빌드 → PNG 추출까지 자동화.

## 입력 자료

| 자료 | 어디서 가져오나 | 비고 |
|---|---|---|
| **라이브 전용 정보** | 사용자 인터뷰 (호스트/일정/혜택/쿠폰/가격) | STEP 0 |
| **상세페이지 경로** | 사용자가 직접 제공 (예: `~/Desktop/output/상세페이지/sundayhug/sleepsack-silky-bamboo.html`) | 이미지 폴더 resolve 용 |
| **이미지** | 위 경로의 `images/{slug}/` 폴더에서 사용자가 골라서 알려줌 | 자동 추출 안 함 (v1) |
| **카피/USP** | 인터뷰에서 사용자가 직접 입력 (또는 "상세페이지 그 부분 가져와도 됩니다") | v1은 자동 추출 없음 |

## 실행 프로세스

### STEP 0 — 인터뷰 (반드시 먼저 실행)

→ 세부 가이드: `references/interview-flow.md`

**한 번에 한 질문, 자연스럽게**. promotion-planner 패턴과 동일.

**필수 10개 핵심 항목** (사용자가 모르면 옵션 제안):

1. **메인 제품**: "이번 라이브 메인 제품이 뭐예요?"
2. **상세페이지 경로**: "이 제품 상세페이지 HTML 경로 알려주세요"
3. **라이브 일정**: 날짜 / 시간 / 채널 (네이버/자사몰/카카오)
4. **호스트 정보**: 이름 / 역할 / 사진 경로 (없으면 스킵)
5. **라이브 타이틀**: 메인 헤드라인 + 서브 + 핵심 혜택 1줄
6. **가격**: 라이브 가격 / 정가 / 할인율
7. **쿠폰**: 코드 / 금액 / 조건 (없으면 스킵)
8. **라이브 혜택 4개**: 아이콘 + 제목 + 설명 + 태그 × 4개
9. **사은품**: 있으면 제목 + 설명 + 이미지 (없으면 스킵)
10. **캠페인 톤**: 시즌 + 분위기 → 12 팔레트 자동 매핑

**선택 추가**: 번들 딜, 세트 구성, FAQ, 리뷰 통계/샘플, 신뢰 배지, 인증 마크.

**요약 + 동의 게이트**: 모든 항목 정리 후 "이대로 빌드 시작할까요? (Y/N)" → Y만 다음 단계.

### STEP 1 — Spec 작성

인터뷰 답변을 `LiveSpec` dict 구조로 정리:
```python
{
  "campaign_slug": "2026-05-가정의달-실키밤부",
  "product_name": "실키밤부 슬리핑백",
  "palette": "warm-spring",
  "active_sections": ["01-live-hero", "02-trust-bar", ...],   # 프리미엄 프리셋 14개 또는 사용자 조정
  "copy": {
    "live_title_html": "엄마들의 꿀잠 시크릿<br>실키밤부 라이브 특가",
    "host_name": "사라쌤",
    "schedule_date": "2026.05.10 (일)",
    "live_benefits": [{"icon":"🎁","title":"...","desc":"...","tag":"..."}, ...],
    ...
  },
  "pdp_path": "/Users/inkyo/Desktop/output/상세페이지/sundayhug/sleepsack-silky-bamboo.html",
  "image_dir": "/Users/inkyo/Desktop/output/상세페이지/sundayhug/images/sleepsack-silky-bamboo/"
}
```

JSON으로 임시 저장 후 빌드 명령 실행.

### STEP 2 — 빌드

```bash
~/.pyenv/versions/3.12.12/bin/python3 \
  skills/promotion/live-page-builder/scripts/build_live.py \
  --spec /tmp/spec.json
```

생성물:
- `~/Desktop/output/상세페이지/라이브/{slug}/spec.json` (재실행/재편집용)
- `~/Desktop/output/상세페이지/라이브/{slug}/previews/<sec>_600w_<palette>.html` (활성 섹션마다)
- `~/Desktop/output/상세페이지/라이브/{slug}/previews/preview-grid.html` (그리드 + PNG 다운로드 버튼)

**chevron** mustache 라이브러리 사용 (의존성: `pip install chevron`).

### STEP 3 — PNG 추출

```bash
~/.pyenv/versions/3.12.12/bin/python3 \
  skills/promotion/live-page-builder/scripts/export_png.py \
  --campaign 2026-05-가정의달-실키밤부

# 특정 섹션만
... --sections 01-live-hero,15-review,19-faq
```

각 섹션 → 600×{콘텐츠 실제 높이} PNG → `final/` 폴더.
Playwright headless Chromium, `body.scrollHeight` 측정 후 `clip` 으로 정확히 자름 (흰 여백 없음).

### STEP 4 — 미리보기 + 다운로드

```bash
open ~/Desktop/output/상세페이지/라이브/{slug}/previews/preview-grid.html
```

각 섹션 카드:
- iframe 미리보기
- 🟢 **PNG 다운로드** 버튼 (클릭 = `final/*.png` 다운로드)
- ⚫ HTML 새 창 (편집/검사용)

**텍스트 수정**: `previews/<sec>.html` 직접 편집 → `export_png.py` 다시 실행 → 그리드에서 새로 다운로드.

## 출력 구조

```
~/Desktop/output/상세페이지/라이브/{campaign-slug}/
├── spec.json                                          # 인터뷰 답변 (재실행용)
├── previews/
│   ├── preview-grid.html                              # 그리드 + PNG 다운로드 버튼
│   ├── 01-live-hero_600w_warm-spring.html
│   ├── 02-trust-bar_600w_warm-spring.html
│   └── ... (활성 섹션 14개)
└── final/
    ├── 01-live-hero_600w_warm-spring.png              # 600×{auto height}
    ├── 02-trust-bar_600w_warm-spring.png
    └── ...
```

## 31개 섹션 카탈로그

→ 세부 표: `references/section-catalog.md`

| 분류 | 섹션 (★ = 프리미엄 프리셋 기본 포함) |
|---|---|
| 헤더 | ★ 01-live-hero, ★ 02-trust-bar |
| 일정 | ★ 03-schedule, ★ 04-countdown |
| 혜택/가격 | ★ 05-live-benefits, ★ 06-coupon, 07-bundle-deals, 08-price-compare, 09-set-contents |
| CTA | ★ 10-mid-cta, ★ 25-final-cta, 26-close |
| 신뢰 | ★ 11-host-recommendation, ★ 15-review, 16-social-proof, 21-guarantee, 22-cert-badges |
| 제품 | ★ 12-quick-showcase, ★ 13-lifestyle, 14-size-spec |
| 부가 | 17-gift-event, 18-target-persona, ★ 19-faq, 20-shipping |
| 브랜드 | 23-brand-quote, 24-brand-story |
| 상품 카드 | 28-product-banner, 29-product-grid, 30-collection-banner |
| 마무리 | ★ 27-footer, 31-channel-follow |

**프리미엄 프리셋 (기본 14개)**: 01, 02, 03, 04, 05, 06, 10, 11, 12, 13, 15, 19, 25, 27.

## 12개 팔레트 + 자동 매핑

→ 매핑 표: `references/interview-flow.md`의 시즌 매핑 섹션 참조.

| 월 | 자동 팔레트 |
|---|---|
| 1-2월 | gentle-winter |
| 3-5월 | warm-spring |
| 6월 | fresh-garden |
| 7-8월 | cool-summer |
| 9-10월 | cozy-autumn |
| 11월 | coral-sunset (블프) |
| 12월 | midnight-luxe (연말 다크) |

사용자가 직접 지정하면(`palette: "rose-dawn"`) 자동 매핑 무시.

## 슬롯(Mustache 변수) 처리 규칙

- `{{var}}` — 일반 텍스트 (HTML escape)
- `{{var_html}}` — `_html` 접미사는 raw HTML 허용 (build_live.py가 자동으로 `{{{var_html}}}` 변환). 예: `live_title_html`, `answer_html`
- `{{#배열}}...{{/배열}}` — 배열 반복. 비어있으면 섹션 자동 제외
- `{{?cond}}...{{/cond}}` — 조건부. chevron 표준은 아니라서 빌더가 `{{#cond}}`로 자동 변환

→ 전체 슬롯 사전: `references/slot-vocabulary.md`

## 의존성

- `chevron` (mustache renderer): `~/.pyenv/versions/3.12.12/bin/python3 -m pip install chevron`
- `playwright` (PNG 캡처)
- `bs4` (HTML 파싱 — 인터뷰에서 PDP에서 텍스트 발췌할 때만)
- 모두 `~/.pyenv/versions/3.12.12/bin/python3` 환경에 설치됨

## 한계 (v1 스코프)

- **이벤트 카드 모드 미지원** — 4장 짧은 카드는 v2에서. v1은 풀 라이브 페이지(13~14 섹션)만.
- **인터랙티브 텍스트 편집 미지원** — 모달 편집 없음. 사용자가 `previews/*.html`을 직접 편집 후 export 재실행.
- **상세페이지 자동 추출 미지원** — 인터뷰로 모든 텍스트 입력. PDP 자동 파싱은 v2.
- **Gemini 이미지 변환 미지원** — meta-ad-factory에는 있는 기능. 라이브에서는 사용자가 이미지 경로로 통제.

## 템플릿 동기화

SynologyDrive(`sundayhug-brand/templates/promotion/live-page/`)의 원본이 갱신되면:

```bash
SRC="$HOME/Library/CloudStorage/SynologyDrive-contents/스킬/sundayhug-brand/templates/promotion/live-page"
DEST="skills/promotion/live-page-builder/templates"
for f in _base-styles.css _palettes.css _guide-chrome.css GUIDE.md "기본 템플릿.html"; do
  cp "$SRC/$f" "$DEST/$f"
done
cp "$HOME/Library/CloudStorage/SynologyDrive-contents/스킬/sundayhug-brand/templates/promotion/_global-palettes.css" "$DEST/"
cp "$HOME/Library/CloudStorage/SynologyDrive-contents/스킬/sundayhug-brand/templates/promotion/_global-variables.css" "$DEST/"
for html in "$SRC"/sections/*.html; do cp "$html" "$DEST/sections/$(basename "$html")"; done
sed -i '' "s|'../_global-palettes.css'|'./_global-palettes.css'|" "$DEST/_palettes.css"
```
