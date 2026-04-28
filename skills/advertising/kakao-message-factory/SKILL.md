---
name: kakao-message-factory
description: 카카오톡 비즈니스 메시지(친구톡, 친구톡 캐러셀, 라이브 캐러셀)를 한 번의 인터뷰로 시각적으로 다양한 5~13개 변형을 자동 벌크 생성하는 스킬. 핵심은 "다양성 레시피"로 같은 사이즈 안에서 레이아웃 자체가 다른 템플릿을 섞어 진짜 다른 결과물을 출력 - wide-mix-5는 풀블리드/라이프스타일/이벤트분할/커머스카드/세일강조 5종 레이아웃을 800×600에서, carousel-mix-5는 단일/듀얼비교/TOP3/옵션쿠폰/세트 5세트 패턴을, live-carousel은 1080×1350 5카드 D-live 템플릿(--abc-bed/--portable-bed/default 자동 선택)을 사용. 시맨틱 슬롯 시스템(title/desc/price/discount/orig/category/badge 등)을 통해 사용자가 한 번 입력하면 17개 sundayhug 디자인 시스템 템플릿 중 적합한 클래스로 팩토리가 자동 매핑. 톤별 카피 자동 변형(emotional/informational/urgency/premium/soft) + 12 캠페인 팔레트(warm-spring/cool-summer/coral-sunset/midnight-luxe 등) + Gemini AI 이미지 변환 + 브라우저 실시간 편집 UI(텍스트/색상/글자크기/굵기/이미지 swap) 지원. PNG 변환 시 친구톡 2MB / 알림톡 500KB 자동 압축. 다음 상황에서 반드시 이 스킬을 사용한다 - "카카오톡 메시지", "친구톡 만들어줘", "카카오 캐러셀", "라이브 캐러셀", "카카오 예고 페이지", "비즈메시지 소재", "kakao bulk message", "친구톡 5종", "캐러셀 5세트", "라이브 방송 5카드", "카카오 메시지 다양한 스타일", "kakao message variations". 결과물은 ~/Desktop/team-skills/카카오메시지/{브랜드}/{캠페인}/ 에 저장.
---

# Kakao Message Factory v3 — 다양성 레시피 + 인터뷰 기반 자동 생성

## 🎯 v3 핵심: 진짜 시각적으로 다른 변형

**문제**: 같은 템플릿에 팔레트만 바꾸면 비슷해 보임.

**해결**: **다양성 레시피** — 같은 800×600 안에서 레이아웃 자체가 다른 5개 템플릿을 섞음.

```
wide-mix-5 레시피:
  변형 1 → 02-wide-image:A-product   (풀블리드 + 하단 정보바)
  변형 2 → 02-wide-image:B-lifestyle (라이프스타일 + 가격 오버레이)
  변형 3 → 02-wide-image:C-event     (분할형 이벤트)
  변형 4 → 06-commerce:A-standard    (커머스 카드)
  변형 5 → 06-commerce:C-sale        (세일 강조)
```

5개 모두 시각적으로 완전히 다른 레이아웃.

---

## 🎤 사용자 인터뷰 흐름 (Claude 자동 진행)

스킬 발동 시 Claude가 다음 순서로 질문:

### Q1~3: 캠페인 기본
```
Q1: 캠페인 이름? (출력 폴더명, 예: portable-crib_2026spring)
Q2: 메인 제품명?
Q3: 가격? (정가, 할인가, 할인율)
```

### Q4: 메시지 종류 (복수 가능)
```
☐ wide-mix-5     — 와이드 5종 (스타일 다양)
☐ wide-premium-5 — 프리미엄 와이드 5종 (다크 톤)
☐ wide-soft-3   — 감성 와이드 3종
☐ carousel-mix-5 — 캐러셀 5세트 (단일/듀얼/TOP3/옵션/세트)
☐ feed-mix-3    — 카루셀 피드 3종 (디테일/라이프/스토리)
☐ live-carousel — 1080×1350 5카드 라이브 방송
```

### Q5~7: 카피/이미지
```
Q5: 메인 라이프스타일 이미지 경로?
Q6: 핵심 USP 3가지? (톤별 카피 자동 생성용)
Q7: 무드 선호? (자유/시즌/프리미엄/감성)
```

### Q8~13: 라이브 선택 시
```
Q8:  라이브 어떤 제품? (abc-bed / portable-bed / 일반)
Q9:  방송 일정?
Q10: 라이브 단독 가격?
Q11: 라이브 이벤트 (럭키드로우/구매인증/소통왕)?
Q12: 옵션 구성 (색상/사이즈)?
Q13: 추가 이미지 경로?
```

Claude가 답변 종합 → `products/{slug}_campaign.py` 자동 생성 → 빌드 → 서버 시작 → 브라우저 오픈.

---

## 📂 핵심 파일 구조

```
skills/advertising/kakao-message-factory/
├── SKILL.md
├── scripts/
│   ├── kakao_factory.py            ← 빌드 엔진 (v3 build_campaign_v3)
│   ├── semantic_slots.py           ← 신규: 시맨틱→클래스 매핑 (17 템플릿)
│   ├── recipes.py                  ← 신규: 7개 다양성 레시피
│   ├── kakao_validator.py          ← 사이즈/용량/카피 검증
│   ├── sync_templates.py           ← Synology → 로컬 캐시
│   ├── export_png.py               ← Playwright PNG + 자동 압축
│   ├── server.py                   ← FastAPI 편집 서버 (실시간 텍스트/색/이미지 수정)
│   ├── .template-cache/            ← 26개 템플릿 + CSS
│   └── products/
│       └── portable_crib_v3_sample.py  ← v3 데모 샘플
└── references/
    ├── kakao-message-specs.md
    ├── kakao-copy-rules.md
    ├── kakao-template-map.md
    └── kakao-validation-checklist.md
```

**출력**: `~/Desktop/team-skills/카카오메시지/{brand}/{slug}/`

---

## ⚡ 사전 준비 (1회)

```bash
# 의존성
pip3 install beautifulsoup4 Pillow fastapi uvicorn playwright
playwright install chromium

# 템플릿 캐시 동기화
cd skills/advertising/kakao-message-factory/scripts
python3 sync_templates.py

# (선택) Gemini 이미지 변환 시
# .env에 GEMINI_API_KEY=... 설정
```

---

## 🚀 워크플로우

### STEP 1: Claude 인터뷰
```
사용자: "휴대용 아기침대로 카카오 메시지 다양한 스타일 만들어줘"
Claude: Q1~Q7 진행 → products/portable-crib_v3.py 자동 생성
```

### STEP 2: 빌드
```bash
python3 kakao_factory.py build products/portable-crib_v3.py
```

출력 (시각적으로 5+5+5 = 15+ 다른 결과):
```
~/Desktop/team-skills/카카오메시지/sundayhug/portable-crib_v3/
├── *_wide_*_02-wide-image_800x600.html        # 와이드 5종 (다른 레이아웃)
├── *_wide_*_06-commerce_800x600.html
├── *_A-standard_card01_05-carousel-commerce_800x800.html  # 캐러셀 단일
├── *_B-dual_card01_05-carousel-commerce_800x800.html      # 캐러셀 듀얼
├── *_C-triple_card01_05-carousel-commerce_800x800.html    # TOP 3
├── *_D-option_card01_05-carousel-commerce_800x800.html    # 옵션
├── *_E-bundle_card01_05-carousel-commerce_800x800.html    # 세트
├── *_live_card01_04-carousel-feed_1080x1350.html          # 라이브 5카드
├── ... (5장)
├── images/
└── preview-grid.html
```

### STEP 3: 브라우저 편집
```bash
python3 server.py --slug portable-crib_v3
# 자동 오픈: http://localhost:8765/preview/portable-crib_v3
```

**편집 모드 ON** 토글:
- 노란 점선 = 텍스트 클릭 → 텍스트/색/크기/굵기 수정
- 주황 점선 = 이미지 클릭 → Gemini AI 변환 프롬프트 입력
- 📥 PNG = on-demand 생성 + 자동 압축

### STEP 4: PNG 일괄 변환
```bash
python3 export_png.py ~/Desktop/team-skills/카카오메시지/sundayhug/portable-crib_v3
# 친구톡 ≤2MB / 알림톡 ≤500KB 자동 압축
```

---

## 🍳 레시피 카탈로그

| 레시피 | 타입 | 결과물 | 사이즈 |
|---|---|---|---|
| `wide-mix-5` | messages | 5개 (풀블/라이프/이벤트/커머스/세일) | 800×600 |
| `wide-premium-5` | messages | 5개 (다크/럭셔리 톤) | 800×600 |
| `wide-soft-3` | messages | 3개 (출산선물/신생아) | 800×600 |
| `carousel-mix-5` | carousels | 5세트 × 1~2 카드 = 8~13장 | 800×800 |
| `carousel-product-3` | carousels | 3세트 (단일/듀얼/TOP3) | 800×800 |
| `feed-mix-3` | carousels | 3세트 (디테일/라이프/스토리) × 2카드 = 6장 | 800×600 |
| `live-carousel` | live_carousel | 1세트 × 5카드 = 5장 | 1080×1350 |

```bash
# 레시피 전체 보기
python3 kakao_factory.py list-recipes
```

---

## 📝 Config 패턴 (Claude가 자동 작성)

```python
from kakao_factory import CampaignV3, SemanticData, build_campaign_v3

data = SemanticData(
    title="ABC 휴대용 아기침대",
    desc="5초 펴고 접고 · 크림/제이드/베이비핑크",
    discount=35, price=119000, orig=184000,
    badge="BEST", category="PORTABLE CRIB",
    sub="크림 · 제이드 · 베이비핑크 3컬러",
    date="2026.04.28(화) — 05.05(화)",
    images={
        "hero": "/path/lifestyle.jpg",
        "product": "/path/cream-product.jpg",
        "item1": "/path/cream.jpg",
        "item2": "/path/jade.jpg",
        "item3": "/path/pink.jpg",
        # D-live alt 매칭용
        "휴대용 아기침대": "/path/cream-product.jpg",
        "데일리 크림": "/path/cream.jpg",
    },
    items=[  # 캐러셀의 카드별 데이터
        {"title":"크림", "price":119000, "image":"/path/cream.jpg"},
        {"title":"제이드", "price":119000, "image":"/path/jade.jpg"},
        {"title":"핑크", "price":119000, "image":"/path/pink.jpg"},
    ],
    tone_overrides={
        "emotional":      {"title":"엄마 옆자리, 우리 아기 잠자리", "desc":"..."},
        "informational":  {"title":"...", "desc":"..."},
        "urgency":        {"title":"...", "desc":"..."},
        "premium":        {"title":"...", "desc":"..."},
        "soft":           {"title":"...", "desc":"..."},
    },
)

CAMPAIGN = CampaignV3(
    brand="sundayhug",
    campaign_slug="portable-crib_v3",
    recipes=["wide-mix-5", "carousel-mix-5", "live-carousel"],
    data=data,
    live_template_hint="portable-bed",  # D-live-carousel--portable-bed 자동 선택
)
```

---

## 🔧 자동 동작 정리

| 기능 | 동작 |
|---|---|
| 시맨틱 슬롯 매핑 | `title="X"` → 02-A는 `km-info-bar-name`, 06-A는 `km-commerce-name`, 06-C는 `km-title`로 자동 |
| 가격 자동 포맷 | `119000` → `119,000원` |
| 할인율 자동 % | `35` → `35%` |
| 줄바꿈 | `\n` → `<br>` |
| 톤별 fallback 카피 | `tone_overrides` 미지정 시 자동 prefix (`꿀잠 ` for soft, `오늘만 · ` for urgency) |
| CSS 인라인화 | self-contained HTML |
| 이미지 자동 복사 | 절대경로 → `images/` 하위 |
| D-live alt 매칭 | `images={"휴대용 아기침대": "/path"}` → 같은 alt 가진 `<img>` 자동 교체 |
| `data-editable` | 모든 치환 텍스트에 자동 부여 → 서버 편집 가능 |
| `data-image-key` | 모든 치환 이미지에 자동 부여 → AI 변환 대상 |
| 카드 자동 분리 | 캐러셀의 `.card`/`.km-card` 자동 감지 |

---

## 📌 검증 명령

```bash
# 사용 가능한 레시피
python3 kakao_factory.py list-recipes

# 사용 가능한 템플릿 + 사이즈
python3 kakao_factory.py list-templates

# 템플릿 클래스/이미지 스캔
python3 kakao_factory.py inspect 04-carousel-feed:D-live-carousel--portable-bed

# 카피 검열
python3 kakao_validator.py check-copy "지금 50% 할인"

# PNG 압축
python3 kakao_validator.py compress /path/to.png 500
```

---

## 🔗 Trigger Examples

- "휴대용 아기침대로 카카오 메시지 다양한 스타일 5종 만들어줘"
- "친구톡 5종 레이아웃 다 다르게"
- "카카오 캐러셀 5세트 (단일/듀얼/TOP3/옵션/세트)"
- "라이브 방송 예고 페이지 5장 (포터블 베드)"
- "kakao bulk message with diverse layouts"

---

## 📚 Reference

- [kakao-message-specs.md](./references/kakao-message-specs.md) — 8타입 사이즈/용량/카피 한도
- [kakao-copy-rules.md](./references/kakao-copy-rules.md) — 알림톡 금지어
- [kakao-template-map.md](./references/kakao-template-map.md) — 24베리에이션 가이드
- [kakao-validation-checklist.md](./references/kakao-validation-checklist.md) — 발송 전 체크
