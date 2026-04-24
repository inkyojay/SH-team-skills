---
name: meta-ad-factory
description: 메타(Facebook/Instagram) 광고 소재를 벌크로 자동 생성하는 스킬. 제품 URL + 이미지를 입력하면 ① USP 자동 분석 → ② 타겟/톤별 카피 매트릭스 생성 → ③ 메타 광고 규격별 HTML 크리에이티브 벌크 생성 → ④ 로컬 FastAPI 서버 기반 인터랙티브 preview-grid (카드별 📥 단건 PNG on-demand / ✏️ 텍스트+스타일 편집[색상·크기·굵기·배경] / 🖼 Gemini AI 이미지 교체) → ⑤ 필요 시 Playwright 일괄 PNG 변환까지. 다음 상황에서 반드시 이 스킬을 사용한다: "메타 광고 만들어줘", "페이스북 광고 소재", "인스타 광고", "광고 크리에이티브", "광고 소재 벌크", "광고 배너 만들어줘", "SNS 광고 이미지", "퍼포먼스 마케팅 소재", "DA 소재 제작", "메타 광고 카피", "광고 에셋 생성", "A/B 테스트 소재", "리타겟팅 광고 소재" 요청 시. 제품 이미지(로컬/CDN URL)와 카피만 있으면 제품당 21개 광고 소재를 한 번에 생성, 브라우저에서 바로 편집·교체 가능.
---

# Meta Ad Factory — 메타 광고 소재 벌크 생성 스킬

## 개요

제품 이미지(로컬 파일 또는 CDN URL) + 카피 → Python 엔진으로 HTML 크리에이티브 자동 생성 → Playwright headless Chromium으로 픽셀 퍼펙트 PNG 변환

**생성량**: 제품 1개당 **21개** 크리에이티브 (4 레이아웃 × 3 사이즈 × 3 톤, 스마트 조합)

---

## 핵심 파일 구조

```
skills/advertising/meta-ad-factory/
├── SKILL.md                          ← 이 파일
├── scripts/
│   ├── meta_ad_builder.py            ← 핵심 빌드 엔진 (직접 수정 금지)
│   ├── server.py                     ← 로컬 FastAPI (PNG/텍스트/AI 이미지 API)
│   ├── export_png.py                 ← Playwright 일괄 PNG 변환기 (CLI)
│   ├── rebuild_grids.py              ← preview-grid.html 단독 재생성
│   └── products/
│       ├── all_products.py           ← 제품 config 모음 (기존 16개)
│       ├── event_ads.py              ← 이벤트 광고 config (5개)
│       └── build_master.py           ← 마스터 대시보드 생성
├── references/
│   ├── meta-ad-specs.md
│   ├── layout-templates.md
│   ├── copy-frameworks.md
│   └── target-audiences.md
└── output/  (→ 실제 출력은 OUTPUT_BASE 경로)
```

**실제 출력 경로**: `~/Desktop/team-skills/광고카피/sundayhug-meta-bulk/{카테고리}/{제품슬러그}/` (각 팀원 로컬 Desktop)

---

## 전체 워크플로우

### STEP 0: 인풋 수집

사용자에게 다음을 확인한다:

1. **제품명 & 슬러그** (예: `butterfly-swaddle-cotton-mesh`)
2. **카테고리** (`newborn` / `sleeping-bags` / `sleep-products` / `daily-look` / `events`)
3. **이미지 소스** (다음 중 하나):
   - 로컬 파일: `~/Desktop/상세페이지 최종본/{경로}/*.webp`
   - CDN URL: `https://sundayhugkr.cafe24.com/skin-skin69/pdp/{경로}.webp`
   - 상세 HTML에서 `<img src>` 추출
4. **프로모션 정보** (선택): 이벤트 전용 광고의 경우 가격·날짜·혜택
5. **색상 팔레트** (선택):
   - 기본 제품: `COLORS = {"primary": "#1D9E75", "secondary": "#F5F0EB", "accent": "#FF6B35"}`
   - 이벤트 광고: `EVENT_COLORS = {"primary": "#C8A07C", "secondary": "#F5EADC", "accent": "#D4645C"}`

### STEP 1: ProductConfig 작성

`scripts/products/all_products.py` (기존 제품) 또는 `scripts/products/event_ads.py` (이벤트) 에 새 `ProductConfig`를 추가한다.

```python
from meta_ad_builder import Benefit, CopySet, ProductConfig, build_ads

NEW_PRODUCT = ProductConfig(
    brand="SUNDAY HUG",
    brand_name_ko="썬데이허그",
    product_name="제품명",
    product_slug="product-slug",        # 폴더명으로 사용
    category="newborn",                  # 카테고리
    colors=COLORS,                       # 팔레트
    images={
        # key → 로컬 경로 또는 CDN URL (둘 다 지원)
        "hero-main":   str(DESKTOP / "path/to/hero.webp"),
        "lifestyle-01": "https://sundayhugkr.cafe24.com/.../image.webp",
    },
    tone_image_pools={                   # 톤별 이미지 우선순위 (선택)
        "emotional":     ["lifestyle-01", "hero-main"],
        "informational": ["hero-main", "detail-01"],
        "urgency":       ["hero-main", "lifestyle-01"],
    },
    copies={
        "emotional": [
            CopySet("emotional", "헤드라인\n2줄 가능", "서브텍스트. 최대 2줄.", "CTA 버튼"),
            CopySet("emotional", "헤드라인 2", "서브텍스트 2", "CTA", badge="배지텍스트"),
        ],
        "informational": [
            CopySet("informational", "기능 헤드라인", "상세 설명.", "자세히 보기", badge="KC인증"),
        ],
        "urgency": [
            CopySet("urgency", "긴급 헤드라인!", "한정 수량/기간 메시지.", "지금 구매",
                    badge="D-DAY", urgency_label="TODAY ONLY"),
        ],
    },
    benefits=[                           # benefit-stack 레이아웃용 (최대 4개)
        Benefit("🎯", "USP 제목", "USP 설명"),
        Benefit("✅", "KC 인증", "안심 소재"),
    ],
    review={                             # social-proof 레이아웃용
        "text": "실제 리뷰 텍스트",
        "name": "리뷰어 · 출처",
    },
    price_label="19,000원",              # 선택
)
```

**카피 작성 가이드**:
- `headline`: 줄바꿈 `\n` 사용 가능, 2줄 권장
- `subtext`: 1~2문장, 구체적 수치/혜택 포함
- `badge`: 짧은 강조 문구 (예: "KC인증", "-30%", "LIVE 한정")
- `urgency_label`: urgency 레이아웃 상단 타이머 텍스트

### STEP 2: HTML 크리에이티브 빌드

```bash
cd /Users/inkyo/Projects/team-skills/skills/advertising/meta-ad-factory/scripts

# 새 제품 단독 빌드 (all_products.py에 추가된 경우)
python3 products/all_products.py product-slug

# 이벤트 광고 빌드
python3 products/event_ads.py abc-bed-live

# 전체 빌드
python3 products/all_products.py
```

**빌드 결과물** (제품 1개당):
```
output/.../product-slug/
├── previews/
│   ├── 01_hero-image_1080x1080_emotional.html
│   ├── 02_hero-image_1080x1080_informational.html
│   ├── ...                                        # 21개 HTML
│   └── preview-grid.html                          # 미리보기 그리드
├── copy.csv                                       # Meta 벌크 업로드용
└── build-meta.json                                # 빌드 메타데이터
```

**생성 조합 (21개)**:
| 레이아웃 | 사이즈 | 수량 |
|---------|--------|------|
| hero-image | 1:1, 4:5, 9:16 × 3톤 | 9개 |
| split-vertical | 4:5, 9:16 × 3톤 | 6개 |
| benefit-stack | 4:5, 9:16 × 2톤 (info+urgency) | 4개 |
| social-proof | 4:5, 9:16 × 1톤 (info) | 2개 |

### STEP 3: 로컬 서버 시작 (인터랙티브 편집 모드)

```bash
cd skills/advertising/meta-ad-factory/scripts
python3 server.py --slug swaddle-strap
# → 브라우저가 자동으로 http://127.0.0.1:8765/preview/swaddle-strap 오픈
```

**서버 옵션**:
- `--slug <slug>` 특정 제품 자동 오픈 (생략 시 가장 최근 빌드된 제품)
- `--port 8765` 포트 변경
- `--no-open` 브라우저 자동 오픈 비활성화

**서버 모드에서 preview-grid 기능**:
- **🔍 필터**: 사이즈(1:1/4:5/9:16) · 레이아웃 · 톤
- **체크박스 선택**: 카드 클릭 → 선택/해제
- **모달 확대**: 더블클릭 / Shift+클릭
- **📥 전체 PNG 다운로드** (헤더 버튼): 선택/필터된 카드를 on-demand로 PNG 생성 → 순차 다운로드
- **카드별 호버 버튼** (왼쪽 상단):
  - **📥** 이 소재만 PNG 다운로드 (~5초)
  - **✏️** 텍스트 + 스타일 편집 모달
    - 텍스트 수정 (헤드라인 / 서브텍스트 / CTA / 배지 / 리뷰)
    - 필드별 **글자색** (color picker)
    - 필드별 **글자 크기** (px 입력)
    - 필드별 **글자 굵기** (Regular / Medium / Bold / Black)
    - CTA · 배지 한정 **배경색** (color picker)
    - 저장 시 원본 HTML 덮어쓰기 (해당 PNG 캐시 자동 무효화 → 재생성)
  - **🖼** AI 이미지 교체 (프롬프트 입력 → Gemini로 20~30초 변환 → 자동 반영)
- **📷 원본 사진 보기**: 소스 이미지 갤러리 (로컬 이미지는 `/src-image/{slug}/{key}` 로 서빙)
- **안전장치**: 첫 편집 시 `{filename}.bak` 자동 생성 (복구용)

### STEP 4 (선택): 대량 일괄 PNG 변환

서버 없이 CLI로 21개를 한번에 받고 싶으면:

```bash
python3 export_png.py --product swaddle-strap          # 단일 제품
python3 export_png.py --product swaddle-strap --zip    # ZIP 패키징
python3 export_png.py --all                             # 전체 제품 (수 분 소요)
```

**PNG 출력**: `~/Desktop/team-skills/광고카피/sundayhug-meta-bulk/{카테고리}/{슬러그}/final/*.png`
- 1080×1080 (1:1 피드), 1080×1350 (4:5 IG), 1080×1920 (9:16 릴스)

### STEP 5: 마스터 대시보드 생성

```bash
python3 products/build_master.py
```

출력:
- `output/.../index.html` — 전체 제품 랜딩 대시보드
- `output/.../all_copies.csv` — 통합 카피 CSV (Meta 광고 관리자 벌크 업로드용)
- `output/.../build-summary.json` — 통계

---

## preview-grid.html UI 업데이트 (rebuild_grids.py)

새 기능(다운로드 버튼, 원본 갤러리 등)을 기존 preview-grid에 적용하려면:

```bash
# 전체 재생성 (개별 광고 HTML 건드리지 않음, 빠름)
python3 rebuild_grids.py

# 특정 제품만
python3 rebuild_grids.py --slug product-slug
```

---

## 이미지 소스 처리 규칙

| 이미지 유형 | 처리 방식 | 예시 |
|------------|---------|------|
| 로컬 `.webp/.jpg/.png` | base64 인코딩 후 HTML에 임베드 | `str(DESKTOP / "path/hero.webp")` |
| CDN URL (`https://`) | URL 그대로 `<img src>` 참조 | `"https://sundayhugkr.cafe24.com/..."` |
| 상세페이지 HTML | `<img src>` 추출 → CDN URL로 변환 | `onerror` fallback URL 사용 |

**알려진 CDN 패턴 (sundayhugkr.cafe24.com)**:
```
/skin-skin69/pdp/newborn/{product}/images/hero-main.webp
/skin-skin69/pdp/newborn/butterfly-swaddle/{silky-bamboo|cotton-mesh}/image/hero-main-*.webp
/skin-skin69/pdp/sleeping-bags/sleepsack/{variant}/images/hero-01.webp
/skin-skin69/pdp/abc/abc-v2/images/intro-02-toddler.webp
/skin-skin69/pdp/abc/abc-mosquito-net/images/hero-01.webp
/skin-skin69/pdp/abc/abc-organizer/images/hero-01.webp
```

---

## 색상 팔레트

```python
# 기본 제품 광고
COLORS = {"primary": "#1D9E75", "secondary": "#F5F0EB", "accent": "#FF6B35"}

# 이벤트/프로모션 광고 (골든 앰버)
EVENT_COLORS = {"primary": "#C8A07C", "secondary": "#F5EADC", "accent": "#D4645C"}

# 플래시 세일 (충격가)
FLASH_COLORS = {"primary": "#D4645C", "secondary": "#FFF8F0", "accent": "#C8A07C"}

# 웰컴/신규 가입
WELCOME_COLORS = {"primary": "#1D9E75", "secondary": "#F5F0EB", "accent": "#C8A07C"}
```

---

## 릴스(9:16) 안전 영역

```
top: 108px    ← 상단 프로필 UI 영역
bottom: 320px ← 하단 CTA/캡션 영역
left: 60px
right: 120px
→ 안전 콘텐츠 영역: 900×1492px
```

`meta_ad_builder.py`의 `REELS_SAFE_PAD` 상수로 자동 적용됨.

---

## 신제품 추가 체크리스트

- [ ] `all_products.py` 또는 `event_ads.py`에 `ProductConfig` 추가
- [ ] 이미지 경로/URL 검증 (로컬 파일 존재 여부 또는 CDN URL 접근 가능 여부)
- [ ] 3개 톤(emotional/informational/urgency) 각 2~3개 카피 작성
- [ ] `benefits` 4개 작성 (benefit-stack 레이아웃용)
- [ ] `review` dict 작성 (social-proof 레이아웃용)
- [ ] `python3 products/{slug}.py` 빌드 실행 (HTML 21개만 생성, PNG는 서버에서 on-demand)
- [ ] `python3 server.py --slug {slug}` 서버 시작 → 브라우저에서 확인/편집
- [ ] 편집/이미지 교체 후 마음에 들면 카드의 📥 버튼으로 개별 PNG 다운로드
- [ ] (선택) `python3 export_png.py --product {slug}` 일괄 PNG 필요 시

## 서버 요구사항

```bash
pip install fastapi 'uvicorn[standard]' beautifulsoup4 python-multipart
# playwright는 이미 설치됨 (일괄 변환용과 공유)
```

AI 이미지 교체는 `.env`에 `GEMINI_API_KEY`가 설정되어 있고 Node.js가 PATH에 있어야 함
(`skills/batch-image-transform/scripts/batch-transform.mjs` 호출).

---

## 브랜드 기본값 (썬데이허그 SUNDAY HUG)

- 브랜드명: `SUNDAY HUG`
- 한국명: `썬데이허그`
- 프라이머리: `#1D9E75` (그린)
- 폰트: Noto Sans KR (Google Fonts CDN)
- 타겟: 신생아~24개월 영유아맘, 임신 후기 예비맘
- 톤: 따뜻하고 신뢰감 있는, 수면 전문 육아 브랜드

---

## 참조 파일

- `references/meta-ad-specs.md` — 메타 광고 규격, 텍스트 제한
- `references/layout-templates.md` — 레이아웃별 HTML/CSS 상세
- `references/copy-frameworks.md` — 톤별 카피 패턴
- `references/target-audiences.md` — 타겟 세그먼트 정의

**STEP 1 실행 전 반드시 `references/copy-frameworks.md`를 읽는다.**
**STEP 2 실행 전 반드시 `references/layout-templates.md`를 읽는다.**
