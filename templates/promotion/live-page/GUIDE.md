# 썬데이허그 라이브 프로모션 페이지 템플릿 가이드

> **이 파일을 가장 먼저 읽으세요.** 에이전트가 라이브 프로모션 페이지를 생성/수정할 때 필요한 모든 정보가 여기 있습니다.

---

## 개요

라이브 커머스(네이버 쇼핑라이브, 카카오 쇼핑라이브 등) 예고/상세 페이지를 위한 모바일 최적화 템플릿입니다.

- **31개 섹션** (필수 12개 + 선택 19개)
- **12개 캠페인 팔레트** (시즌 4종 + 무드 4종 + 스페셜 4종)
- **JS/애니메이션 없음** — 이미지로 변환되므로 모든 JS, CSS 애니메이션 사용 불가
- **모바일 퍼스트** — max-width 600px

---

## 중요 제약사항

### JS/애니메이션 완전 금지
이 템플릿은 HTML → 이미지 변환 용도입니다. 아래 항목은 **절대 사용하지 마세요**:

- `@keyframes`, `animation`, `transition` (CSS 애니메이션)
- `position: fixed` / `position: sticky` (이미지에서 의미 없음)
- JavaScript (아코디언, 카운트다운, 스크롤 애니메이션 등)
- `:hover` 효과 (무해하지만 이미지에 반영되지 않음)
- `.v` 클래스 (이전 버전의 스크롤 애니메이션 트리거 — 제거됨)

---

## 파일 구조

```
templates/promotion/live-page/
├── _base-styles.css             ← 전체 CSS (섹션 HTML에 <style>로 삽입)
├── _palettes.css                ← 12개 팔레트 변수 (함께 삽입)
├── _guide-chrome.css            ← 가이드 UI 전용 스타일 (가이드 헤더, 팔레트 바 등)
├── GUIDE.md                     ← 이 문서
├── template-guide.html          ← 비주얼 가이드 셸 (~80줄, fetch로 콘텐츠 로드)
├── template-guide-original.html ← 원본 모놀리식 가이드 (백업)
├── guide/                       ← 가이드 콘텐츠 (template-guide.html에서 로드)
│   ├── fullpage.html            ←   풀페이지 미리보기 콘텐츠
│   ├── catalog.html             ←   섹션 카탈로그 콘텐츠
│   └── guide.js                 ←   모드/팔레트 전환 + fetch 로딩
└── sections/                    ← 31개 섹션 HTML 조각
    ├── 01-live-hero.html
    ├── 02-trust-bar.html
    ├── 03-schedule.html
    ├── ...
    ├── 27-footer.html
    ├── 28-product-banner.html
    ├── 29-product-grid.html
    ├── 30-collection-banner.html
    └── 31-channel-follow.html
```

> **참고**: `template-guide.html`은 `fetch()`로 콘텐츠를 로드하므로 **HTTP 서버**를 통해 열어야 합니다.
> `file://` 프로토콜에서는 CORS 제한으로 작동하지 않습니다.
> 예: `npx serve .` 또는 `python3 -m http.server`

---

## 사용법

### 1단계: CSS 삽입
```html
<style>
  /* _base-styles.css 전체 내용 */
  /* _palettes.css 전체 내용 */
</style>
```

### 2단계: 팔레트 지정
```html
<body data-palette="warm-spring">
```
팔레트 미지정 시 기본(golden-hour와 동일) 적용.

### 3단계: 섹션 조합
필수 섹션을 기본으로, 선택 섹션을 캠페인에 맞게 추가합니다. 각 섹션 HTML 파일 상단 주석의 `{{variable}}` 플레이스홀더를 실제 데이터로 교체합니다.

---

## 31개 섹션 맵

### 권장 흐름
```
[히어로] → [신뢰] → [방송일정] → [카운트다운] → [혜택] → [쿠폰]
→ [구매옵션] → [가격비교] → [세트구성] → [중간CTA]
→ [호스트추천] → [퀵쇼케이스] → [라이프스타일] → [사이즈/스펙]
→ [리뷰] → [SNS후기] → [사은품] → [타겟추천] → [FAQ]
→ [배송안내] → [구매보장] → [인증배지]
→ [브랜드인용문] → [브랜드스토리]
→ [제품배너] → [추천상품] → [컬렉션배너] → [채널팔로우]
→ [최종CTA] → [클로징] → [푸터]
```

### 전체 섹션 목록

| # | 파일명 | 섹션명 | 필수 | 배경 | 핵심 내용 |
|---|--------|--------|------|------|----------|
| 01 | 01-live-hero.html | Live Hero | ✅ | gradient | 호스트+방송제목+혜택, 정적 LIVE 뱃지 |
| 02 | 02-trust-bar.html | Trust Bar | ✅ | dark | 라이브 단독가/실시간 상담/즉시 발송 |
| 03 | 03-schedule.html | Schedule | ✅ | white | 방송 날짜/시간/채널 3칸 카드 |
| 04 | 04-countdown.html | Countdown | ✅ | warm | 정적 카운트다운 (애니메이션 없음) |
| 05 | 05-live-benefits.html | Live Benefits | ✅ | white | 2x2 혜택 그리드 |
| 06 | 06-coupon.html | Coupon | 선택 | warm | 전용 할인 쿠폰 카드 |
| 07 | 07-bundle-deals.html | Bundle Deals | ✅ | white | 단품/2+1/세트 옵션 카드 |
| 08 | 08-price-compare.html | Price Compare | 선택 | warm | 정가 vs 라이브가 비교표 |
| 09 | 09-set-contents.html | Set Contents | 선택 | white | 세트 구성품 비주얼 나열 |
| 10 | 10-mid-cta.html | Mid CTA | ✅ | gradient | 중간 구매 유도 |
| 11 | 11-host-recommendation.html | Host Rec. | 선택 | warm | 호스트 인용문 + 사진 |
| 12 | 12-quick-showcase.html | Quick Showcase | ✅ | white/warm | 셀링 포인트 좌우 교차 |
| 13 | 13-lifestyle.html | Lifestyle | 선택 | - | 풀블리드 감성 이미지 |
| 14 | 14-size-spec.html | Size & Spec | 선택 | warm | 사이즈표/소재 비교 |
| 15 | 15-review.html | Review | ✅ | white | 별점 통계 + 리뷰 |
| 16 | 16-social-proof.html | Social Proof | 선택 | warm | SNS 후기 카드 그리드 |
| 17 | 17-gift-event.html | Gift Event | 선택 | white | 사은품 안내 |
| 18 | 18-target-persona.html | Target | 선택 | warm | "이런 분께 추천" 체크리스트 |
| 19 | 19-faq.html | FAQ | 선택 | white | 정적 Q&A 리스트 (항상 열림) |
| 20 | 20-shipping.html | Shipping | ✅ | warm | 배송/교환/반품 2x2 카드 |
| 21 | 21-guarantee.html | Guarantee | 선택 | white | 무료반품/환불 보장 |
| 22 | 22-cert-badges.html | Cert Badges | 선택 | warm | KC인증/무형광 배지 그리드 |
| 23 | 23-brand-quote.html | Brand Quote | 선택 | dark | 감성 브랜드 인용문 |
| 24 | 24-brand-story.html | Brand Story | 선택 | warm | 브랜드 스토리 |
| 25 | 25-final-cta.html | Final CTA | ✅ | dark | 라이브 방송 중 구매하기 |
| 26 | 26-close.html | Close | ✅ | warm | 브랜드 클로징 메시지 |
| 27 | 27-footer.html | Footer | ✅ | dark | Designed for Families. |
| 28 | 28-product-banner.html | Product Banner | 선택 | 이미지 | 제품 이미지 배경 + 텍스트 오버레이 (5가지 스타일) |
| 29 | 29-product-grid.html | Product Grid | 선택 | white | 추천 상품 2열 카드 그리드 (가격/할인율) |
| 30 | 30-collection-banner.html | Collection Banner | 선택 | 이미지 | 컬렉션 링크 풀 이미지 배너 |
| 31 | 31-channel-follow.html | Channel Follow | 선택 | highlight | 카카오/SNS 채널 팔로우 CTA |

---

## 12개 캠페인 팔레트

### 시즌 팔레트 (4종)
| 팔레트 | data-palette | 추천 캠페인 |
|--------|-------------|------------|
| 따뜻한 봄 | `warm-spring` | 봄 신상, 출산 선물 |
| 시원한 여름 | `cool-summer` | 여름 특가, 메쉬 라인 |
| 포근한 가을 | `cozy-autumn` | 추석 세트, 가을 신상 |
| 고요한 겨울 | `gentle-winter` | 크리스마스, 겨울 슬립백 |

### 무드 팔레트 (4종)
| 팔레트 | data-palette | 추천 캠페인 |
|--------|-------------|------------|
| 장밋빛 새벽 | `rose-dawn` | 여아 제품, 블러시 컬렉션 |
| 싱그러운 정원 | `fresh-garden` | 친환경, 밤부 라인 |
| 달빛 고요 | `moonlit-calm` | 수면 캠페인, 야간 라이브 |
| 볼터치 핑크 | `blush-touch` | 신생아, 출산 축하 |

### 스페셜 팔레트 (4종)
| 팔레트 | data-palette | 추천 캠페인 |
|--------|-------------|------------|
| 슬레이트 블루 | `slate-mood` | 남아 제품, 프리미엄 라인 |
| 골든 아워 | `golden-hour` | 브랜드 대표, 기본 라이브 |
| 코랄 선셋 | `coral-sunset` | 한정판, 콜라보, 기념일 |
| 미드나잇 럭스 | `midnight-luxe` | VIP 라이브, 프리미엄 세트 |

---

## 캠페인별 추천 조합

### 기본 라이브 (필수 섹션만, 12개)
```
01 → 02 → 03 → 04 → 05 → 07 → 10 → 12 → 15 → 20 → 25 → 26 → 27
```

### 풀 프로모션 (전체 31개)
```
01 ~ 31 전체 순서대로
```

### 세트 상품 특화 (18개)
```
01 → 02 → 03 → 04 → 05 → 07 → 08 → 09 → 10
→ 12 → 15 → 17 → 18 → 20 → 22 → 25 → 26 → 27
```

### 신뢰 강조 (브랜드 인지도 낮을 때, 20개)
```
01 → 02 → 03 → 04 → 05 → 07 → 10 → 11 → 12
→ 15 → 16 → 18 → 19 → 20 → 21 → 22 → 23 → 25 → 26 → 27
```

---

## 비주얼 가이드

`template-guide.html`을 HTTP 서버로 열면 (`npx serve .` 등):

1. **팔레트 탭 바**: 12개 팔레트를 탭으로 전환하며 완성된 풀페이지 미리보기
2. **섹션 카탈로그**: 31개 섹션 개별 미리보기 + 설명 + 필수/선택 태그 + 베리에이션

### 가이드 수정 시
- **섹션 내용 변경**: `guide/fullpage.html` 또는 `guide/catalog.html` 수정
- **가이드 UI 스타일 변경**: `_guide-chrome.css` 수정
- **섹션 CSS 변경**: `_base-styles.css` 수정
- **팔레트 변경**: `_palettes.css` 수정
- **원본 참고 필요 시**: `template-guide-original.html` 참조

---

## 변경 이력

| 버전 | 날짜 | 내용 |
|------|------|------|
| v3.0 | 2026-03-10 | 27→31 섹션 확장 (제품배너/추천그리드/컬렉션배너/채널팔로우), 실제 이미지 적용, 섹션별 베리에이션 추가 |
| v2.0 | 2026-03-10 | 14→27 섹션 확장, JS/애니메이션 완전 제거, Sticky Bar 삭제, FAQ 정적화, 비주얼 가이드 개편 |
| v1.0 | 2026-03-10 | 초기 버전 (14개 섹션) |
