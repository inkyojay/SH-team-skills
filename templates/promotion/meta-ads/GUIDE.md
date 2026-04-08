# 썬데이허그 메타 광고 소재 템플릿 가이드

## 개요

Meta(Instagram/Facebook) 광고용 소재 템플릿 시스템. **소구점 유형(Appeal Type)** 기반으로 15개 타입 × 3개 포맷 변형 = **45개 HTML 템플릿**을 제공합니다.

- **채널**: Meta Ads (Facebook/Instagram Feed, Story, Reels)
- **CSS 프리픽스**: `.ma-`
- **HTML → 이미지 변환**: JavaScript/애니메이션 없음
- **팔레트**: 12종 (글로벌 팔레트 공유)

## 폴더 구조

```
templates/promotion/meta-ads/
├── _base-styles.css          ← .ma- 프리픽스 CSS
├── _palettes.css             ← 글로벌 팔레트 import + midnight-luxe 오버라이드
├── _guide-chrome.css         ← 가이드 UI
├── GUIDE.md                  ← 이 파일
├── template-guide.html       ← 15 타입 탭 + 12 팔레트 + 45 프리뷰
└── types/
    ├── 01-problem-solution/  ← 문제-해결
    ├── 02-emotional/         ← 감성
    ├── 03-ugc-testimonial/   ← 사용자 후기
    ├── 04-social-proof/      ← 사회적 증거
    ├── 05-benefit-feature/   ← 혜택/기능
    ├── 06-authority-expert/  ← 권위/전문가
    ├── 07-before-after/      ← 비포/애프터
    ├── 08-comparison/        ← 비교
    ├── 09-price-discount/    ← 가격/할인
    ├── 10-urgency-scarcity/  ← 긴급성/희소성
    ├── 11-gift-unboxing/     ← 선물/언박싱
    ├── 12-lifestyle-routine/ ← 라이프스타일/루틴
    ├── 13-bundle-set/        ← 세트/구성
    ├── 14-seasonal-collection/ ← 시즌/컬렉션
    └── 15-faq-mythbuster/    ← FAQ/오해타파
        각 폴더: A-feed-square.html (1080×1080)
                 B-feed-vertical.html (1080×1350)
                 C-story-reels.html (1080×1920)
```

## 10개 소구점 타입

| # | 타입 | 영문명 | 우선순위 | 핵심 레이아웃 |
|---|------|--------|----------|--------------|
| 01 | 문제-해결 | Problem-Solution | HIGH | 좌우/상하 분할 — 문제(어둡게) → 해결(밝게) |
| 02 | 감성 | Emotional | HIGH | 풀블리드 라이프스타일 사진 + 최소 텍스트 오버레이 |
| 03 | 사용자 후기 | UGC/Testimonial | HIGH | 후기 카드 + 별점 + 리뷰어 정보 + 제품 썸네일 |
| 04 | 사회적 증거 | Social Proof | HIGH | 통계 숫자 강조 + 신뢰 배지 + 리뷰 수 |
| 05 | 혜택/기능 | Benefit-Feature | MEDIUM | 제품 히어로 + 기능 카드 3~4개 |
| 06 | 권위/전문가 | Authority-Expert | MEDIUM | 전문가 프로필 + 인증 배지 + 추천 인용문 |
| 07 | 비포/애프터 | Before-After | MEDIUM | 50:50 분할 — Before(탈색) / After(선명) |
| 08 | 비교 | Comparison | MEDIUM | 비교 테이블/그리드 + 체크/X 마크 |
| 09 | 가격/할인 | Price-Discount | Situational | 할인율 대형 표시 + 취소선 원가 + CTA |
| 10 | 긴급성/희소성 | Urgency-Scarcity | Situational | 카운트다운 + 잔여 수량 + 볼드 CTA |
| 11 | 선물/언박싱 | Gift/Unboxing | MEDIUM | 기프트 패키지 비주얼 + 구성품 소개 + 포장 강조 |
| 12 | 라이프스타일/루틴 | Lifestyle/Routine | HIGH | 수면 루틴 스텝 + 라이프스타일 이미지 + 일상 제안 |
| 13 | 세트/구성 | Bundle/Set | MEDIUM | 구성품 그리드 + 개별/세트 가격 비교 + 절약 강조 |
| 14 | 시즌/컬렉션 | Seasonal/Collection | Situational | 시즌 무드 이미지 + 신상 라인업 + 컬렉션 소개 |
| 15 | FAQ/오해타파 | FAQ/Myth-Buster | MEDIUM | Myth→Fact 전환 또는 Q&A 카드 형식 |

## 3개 포맷 변형

| 변형 | 비율 | 사이즈 | 용도 | 세이프존 |
|------|------|--------|------|----------|
| A — Feed Square | 1:1 | 1080×1080 | 피드 기본 | 없음 |
| B — Feed Vertical | 4:5 | 1080×1350 | 피드 최적 (CTR +15%) | 없음 |
| C — Story/Reels | 9:16 | 1080×1920 | 스토리/릴스 | 상단 14%, 하단 35% 텍스트 금지 |

**설계 결정**: 기존 채널은 A/B/C가 콘텐츠 변형(Product/Lifestyle/Event)이지만, 메타 광고는 동일 소구점이 모든 배치(Feed/Story/Reels)에 서빙되므로 **포맷 변형**으로 구분합니다.

## CSS 클래스 요약 (.ma- 프리픽스)

### 프레임
- `.ma-frame` — 기본 프레임 컨테이너
- `data-type="feed-square"` — 1080×1080
- `data-type="feed-vertical"` — 1080×1350
- `data-type="story-reels"` — 1080×1920

### 타이포그래피
- `.ma-title` — 주제목 (64px, 700)
- `.ma-subtitle` — 부제목 (36px, 400)
- `.ma-label` — 영문 라벨 (22px, uppercase)
- `.ma-badge` — 둥근 뱃지 (pill)
- `.ma-quote` — 인용문 (디스플레이 폰트, 이탤릭)

### 가격
- `.ma-price` — 판매가 (56px, 700)
- `.ma-price-orig` — 원가 취소선 (28px)
- `.ma-discount` — 할인율 (56px, danger 색상)

### 레이아웃
- `.ma-split` — 좌우 분할
- `.ma-split-h` — 상하 분할
- `.ma-center` — 중앙 정렬 (그라데이션 배경)
- `.ma-hero-img` — 풀블리드 히어로 이미지
- `.ma-overlay` — 오버레이 (.bottom, .top, .full)

### 컴포넌트
- `.ma-cta-button` — CTA 버튼
- `.ma-brand-bar` / `.ma-brand-logo` — 브랜드 영역
- `.ma-stat` / `.ma-stat-number` / `.ma-stat-label` — 통계
- `.ma-review-card` — 리뷰 카드
- `.ma-feature-card` — 기능 카드
- `.ma-expert-profile` / `.ma-expert-avatar` — 전문가 프로필
- `.ma-comparison-row` — 비교 행
- `.ma-countdown` / `.ma-countdown-unit` — 카운트다운
- `.ma-check` / `.ma-cross` — 체크/X 마크
- `.ma-arrow` — 방향 화살표
- `.ma-strip` — 하단 스트립 바

## 사용법

### 1. 가이드에서 선택
`template-guide.html`을 브라우저에서 열어:
1. 원하는 팔레트 선택
2. 소구점 타입 탭 선택
3. A/B/C 포맷 중 필요한 것만 토글
4. **COPY JSON** 클릭 → 설정 복사

### 2. 프로모션 디자인 스킬과 연동
복사한 JSON을 `/promotion-design` 스킬에 붙여넣으면 자동으로 메타 광고 소재가 생성됩니다.

### 3. 독립 사용
각 `types/` 폴더의 HTML 파일을 직접 열어 개별 소재로 사용할 수 있습니다. 이미지 경로와 텍스트만 교체하면 됩니다.

## 팔레트

12개 캠페인 팔레트 (모든 채널 공통):

| 분류 | 팔레트 | 추천 용도 |
|------|--------|----------|
| 시즌 | warm-spring | 봄 신상, 출산 선물 |
| 시즌 | cool-summer | 여름 특가, 메쉬 라인 |
| 시즌 | cozy-autumn | 추석 세트, 가을 신상 |
| 시즌 | gentle-winter | 크리스마스, 겨울 슬립백 |
| 무드 | rose-dawn | 여아 제품, 블러시 컬렉션 |
| 무드 | fresh-garden | 친환경, 밤부 라인 |
| 무드 | moonlit-calm | 수면 캠페인, 야간 라이브 |
| 무드 | blush-touch | 신생아, 출산 축하 |
| 스페셜 | slate-mood | 남아 제품, 프리미엄 라인 |
| 스페셜 | golden-hour | 브랜드 대표 (기본값) |
| 스페셜 | coral-sunset | 한정판, 콜라보, 기념일 |
| 스페셜 | midnight-luxe | VIP, 프리미엄 세트 (다크) |

## 주의사항

- **JavaScript 금지**: HTML → 이미지 변환을 위해 정적 HTML만 사용
- **이미지 경로**: 독립 파일은 상대경로, 프로모션 디자인 스킬에서는 절대경로로 변환
- **세이프존 (C 변형)**: Story/Reels 9:16 포맷에서 상단 14%, 하단 35%에 핵심 텍스트 배치 금지
- **midnight-luxe**: 다크 배경이므로 텍스트 가독성 특별 주의 (_palettes.css에서 오버라이드 처리됨)
