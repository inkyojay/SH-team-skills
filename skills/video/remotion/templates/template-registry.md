# Remotion 영상 템플릿 레지스트리

Meta(Instagram/Facebook) 광고 및 릴스용 Remotion 영상 템플릿 목록입니다.
소구점(Appeal Type)별로 분류되어 있으며, 각 템플릿은 3개 포맷(Reels/Square/Vertical)을 지원합니다.

## 소구점별 템플릿 목록

### 구현 완료

| # | 소구점 | 폴더 | 메인 컴포넌트 | 추천 길이 | 핵심 모션 |
|---|--------|------|-------------|----------|----------|
| 01 | 문제-해결 | `01-problem-solution/` | `ProblemSolution` | 15~20초 | 다크→브라이트 wipe, shake→spring |
| 02 | 감성 | `02-emotional/` | `Emotional` | 15~25초 | Ken Burns, 슬로우 fade, Garamond 인용구 |
| 04 | 사회적 증거 | `04-social-proof/` | `SocialProof` | 15~20초 | CountUp, 별점 순차, 뱃지 팝인 |
| 07 | 비포/애프터 | `07-before-after/` | `BeforeAfter` | 15~20초 | clipPath wipe, 채도 전환 |
| 12 | 라이프스타일 | `12-lifestyle-routine/` | `LifestyleRoutine` | 20~30초 | 스텝 팝인, 프로그레스 닷 |

### 기존 (범용)

| 템플릿 | 폴더 | 용도 | 추천 길이 | 커버 소구점 |
|--------|------|------|----------|-----------|
| Meta Reels Ad | `meta-reels-ad/` | 범용 멀티씬 | 6~15초 | 범용 (부분적 01) |
| UGC 리뷰형 | `ugc-review/` | UGC 리뷰 | 30~45초 | 03-UGC/후기 |
| 비교 추천형 | `comparison/` | 제품 비교 | 45~60초 | 08-비교 |
| 브랜드 공식형 | `branded-showcase/` | 브랜드 쇼케이스 | 30~45초 | 05-혜택/기능 (부분) |
| 리뷰 배너형 | `review-banner/` | 리뷰 배너 | 5~10초 | 04-사회적증거 (부분) |

### Phase 2 예정 (MEDIUM)

| # | 소구점 | 핵심 모션 |
|---|--------|----------|
| 06 | 권위/전문가 | 전문가 프로필 카드 + 인증 뱃지 슬라이드 |
| 09 | 가격/할인 | 할인율 대형 카운터 + 취소선 애니메이션 |
| 11 | 선물/언박싱 | 언박싱 리빌 (scale 0→1) + 구성품 그리드 |
| 13 | 세트/구성 | 구성품 조립 애니메이션 + 가격 비교 |
| 15 | FAQ/오해타파 | Myth→Fact 카드 플립 (rotateY) |

### Phase 3 예정 (SITUATIONAL)

| # | 소구점 | 핵심 모션 |
|---|--------|----------|
| 10 | 긴급성/희소성 | 카운트다운 타이머 + 재고 감소 바 |
| 14 | 시즌/컬렉션 | 시즌 무드 전환 + 라인업 슬라이드 |
| 05 | 혜택/기능 | branded-showcase 강화판 |

### B급/바이럴 템플릿 (`viral/`)

기존 소구점별 프리미엄 템플릿과 별도로, B급 감성·Ugly Ad·밈 스타일의 바이럴 템플릿입니다.
의도적으로 Lo-Fi, 날것, 유머러스한 톤을 사용합니다.

| # | 템플릿명 | 폴더 | 메인 컴포넌트 | 추천 길이 | 핵심 |
|---|---------|------|-------------|----------|------|
| V01 | iPhone 메모장 | `viral/v01-notes-app/` | `NotesApp` | 5~10초 | Notes UI, 타이핑 애니메이션 |
| V02 | 카톡 대화 | `viral/v02-kakao-chat/` | `KakaoChat` | 15~25초 | KakaoTalk UI, 말풍선 순차 등장 |
| V03 | 가짜 알림 | `viral/v03-fake-notification/` | `FakeNotification` | 10~20초 | iOS 알림 배너 슬라이드 |
| V04 | Ugly 후기 | `viral/v04-ugly-review/` | `UglyReview` | 15~25초 | 셀카캠, 볼드 캡션, 흔들림 |
| V05 | 훅+리빌 | `viral/v05-hook-reveal/` | `HookReveal` | 10~15초 | 충격 텍스트→플래시→제품 리빌 |
| V06 | 티어리스트 | `viral/v06-tier-list/` | `TierList` | 20~30초 | S/A/B/C/F 그리드, 아이템 배치 |
| V07 | 카운트다운 | `viral/v07-countdown/` | `Countdown` | 15~25초 | 역순 카운트, #1 극적 리빌 |
| V08 | 주문vs실물 | `viral/v08-order-vs-reality/` | `OrderVsReality` | 10~20초 | 기대→전환→실물 리빌 |
| V09 | 텍스트 폭탄 | `viral/v09-text-bomb/` | `TextBomb` | 5~8초 | 화면 80% 텍스트, 단색 배경 |
| V10 | ASMR 언박싱 | `viral/v10-asmr-unboxing/` | `AsmrUnboxing` | 15~25초 | 클로즈업, 레이어 리빌, 최소 텍스트 |

#### B급 vs 프리미엄 차이점

| | 프리미엄 (소구점별) | B급/바이럴 (viral/) |
|---|---|---|
| 톤 | 세련, 부드러움 | Lo-fi, 날것, 유머 |
| 폰트 | Noto Sans KR + Cormorant | system-ui, monospace |
| 색상 | 팔레트 12종 | 순백/순흑 허용, 단색 배경 |
| 모션 | spring 14-18, Ken Burns | 글리치, 플래시, 하드컷 |
| 배경 | #FAF7F4 (웜 베이지) | #FFF, #000, 단색 |

#### HTML 이미지 광고 대응표

| Remotion 영상 | HTML 이미지 (meta-ads) | 포맷 |
|:---:|:---:|------|
| V01~V09 | v01~v09 | A-square, B-vertical, C-reels |
| V10 (ASMR) | - | 영상 전용 |

---

## 공유 컴포넌트 (`_shared/`)

### 컴포넌트

| 컴포넌트 | 파일 | 용도 |
|---------|------|------|
| Caption | `components/Caption.tsx` | 포맷별 세이프존 자동 조정 자막 |
| BrandLogo | `components/BrandLogo.tsx` | 상단 브랜드 로고 뱃지 |
| CtaEndCard | `components/CtaEndCard.tsx` | 순차 spring CTA 엔드카드 |
| Narration | `components/Narration.tsx` | 나레이션 오디오 래퍼 |
| VideoClip | `components/VideoClip.tsx` | 비디오/이미지 + 그라데이션 오버레이 |
| CountUp | `components/CountUp.tsx` | 숫자 카운트업 애니메이션 |
| StarRating | `components/StarRating.tsx` | 별점 순차 등장 |
| SafeZoneGuide | `components/SafeZoneGuide.tsx` | 세이프존 시각화 (개발용) |

### 유틸리티

| 유틸 | 파일 | 용도 |
|------|------|------|
| timing | `utils/timing.ts` | TransitionSeries 타이밍 계산 |
| palettes | `utils/palettes.ts` | 12 캠페인 팔레트 |
| brand | `utils/brand.ts` | 썬데이허그 브랜드 상수 + 모션 가이드 |

### 타입

| 타입 | 파일 | 내용 |
|------|------|------|
| BaseConfig | `types/common.ts` | 공통 Config 인터페이스 |
| VideoFormat | `types/common.ts` | reels / feed-square / feed-vertical |
| FormatSpec | `types/common.ts` | 포맷별 해상도 + 세이프존 |

---

## 소구점 매핑 가이드

| 마케팅 목적 | 1순위 | 2순위 | 3순위 |
|------------|-------|-------|-------|
| 신규 인지도 | 02-감성 | branded-showcase | 01-문제해결 |
| 제품 소개 | 01-문제해결 | 12-라이프스타일 | branded-showcase |
| 전환/구매 | 04-사회적증거 | 07-비포애프터 | ugc-review |
| 리타겟팅 | 07-비포애프터 | review-banner | 04-사회적증거 |
| 후기 활용 | ugc-review | 04-사회적증거 | review-banner |
| 루틴 제안 | 12-라이프스타일 | 02-감성 | 01-문제해결 |

## 3개 포맷

| 포맷 | 크기 | 용도 | 세이프존 |
|------|------|------|---------|
| Reels (9:16) | 1080×1920 | 릴스/스토리 | 상단 14%, 하단 35% |
| Feed Square (1:1) | 1080×1080 | 피드 정사각 | 없음 |
| Feed Vertical (4:5) | 1080×1350 | 피드 세로 | 없음 |

각 템플릿의 `format` prop으로 자동 조정됩니다.

## 공통 아키텍처

1. **Config 기반**: TypeScript 인터페이스로 씬/브랜드/팔레트 설정
2. **TransitionSeries**: 씬 전환은 `@remotion/transitions` fade 사용
3. **나레이션 외부 배치**: TransitionSeries 바깥에 절대 프레임으로 Audio 배치
4. **공유 타이밍**: `_shared/utils/timing.ts`의 `calculateSceneStarts()` 공유
5. **팔레트 시스템**: 12종 캠페인 팔레트로 톤 앤 매너 통일
6. **모션 가이드라인**: spring damping 14-18, stiffness 120-180 (부드러운 톤)

## 파일 구조 컨벤션

```
template-name/
├── TemplateName.tsx       # 메인 컴포넌트
├── types.ts               # Config 타입 정의
├── components/            # 전용 컴포넌트
├── README.md              # 사용법 + Config 예시
├── analysis.md            # 레퍼런스 영상 분석 (선택)
└── references/            # 레퍼런스 영상 (선택)
```
