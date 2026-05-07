# Workflow A: 콘텐츠 검수 (Reviewer Mode)

> 사용자가 결과물(상세페이지/광고/SNS/카드뉴스/영상/패키징)을 제시하면 브랜드 실장이 9개 영역으로 평가하고 통과/수정 판정.

## 입력 형태 (모두 지원)

- HTML / MD / 이미지 파일 경로
- 텍스트 카피 (인스타 캡션, 블로그 본문 등)
- URL (자사몰 PDP, 인스타 게시물, 블로그 글)
- 이미지 캡처 (메타 광고 소재, 패키징 시안)
- 폴더 경로 (이미지 시리즈, 카드뉴스 묶음)

## 단계

### Step 1. 컨텍스트 로드

브랜드 실장은 다음을 매번 읽어 컨텍스트를 갱신:

1. `../guidance/quick-reference.md` (전체) — 1차 컨텍스트
2. `../checklists/pre-publish-review.md` (전체) — 50여 항목 체크리스트
3. `../checklists/brand-violations.md` (전체) — 위반 패턴 카탈로그

> 풀 가이드(`sundayhug-brand-guide.html` / `sundayhug-brand-project.md`)는 quick-reference로 부족할 때만 추가 로드 (예: TOG 시스템 디테일이 필요한 검수)

### Step 2. 검수 대상물 파악

```
- 채널/포맷: 인스타 피드 / 자사몰 PDP / 메타 광고 / 카드뉴스 / 블로그 / ...
- 카테고리: 제품 출시 / 시즌 컬러 / 프로모션 / 콘텐츠 / 검색 SEO / ...
- 캠페인 코드 (있다면): 어떤 브리프(creative-brief)에 속하는가
```

채널과 카테고리가 모호하면 사용자에게 한 번 묻는다 (`AskUserQuestion`).

### Step 3. 9개 영역 순차 평가

`pre-publish-review.md`의 9개 영역을 순차로 항목별 평가:

1. 🎨 Visual — 컬러 (5)
2. 🔤 Visual — 타이포그래피 (4)
3. 📷 Visual — 포토그래피 (5)
4. 🗣️ Voice — 어투 (5)
5. 🚫 Voice — 금지 표현 (5)
6. 💎 Brand Essence — 3축 정합 (5)
7. 🏷️ Tagline / Headline (3)
8. 🎯 타겟 적합성 (4)
9. 📦 채널별 톤 (4 sub-channels)

각 항목 PASS / WARN / FAIL 판정.

### Step 4. 판정 출력

#### FAIL (수정 필수)

```markdown
판정: 🔴 FAIL

위반 항목 (n개):

1. [Visual — 컬러 V-01]
   - 위치: HERO 배경
   - 문제: 형광 핑크 #FF00FF 사용
   - 수정: Blush #DEB5A8 또는 Soft Apricot #E8C9A8 권장

2. [Voice — 금지 표현 V-02]
   - 위치: 메인 카피
   - 문제: "대박 할인!!" 자극 어조
   - 수정: "이번 시즌 새로운 만남" 같은 평서문

3. ...

수정 후 재검수 부탁드립니다.

전체 점수: 41 / 50
```

#### WARN (주의)

```markdown
판정: 🟡 WARN

부분 충족 항목 (n개):

1. [영역] 항목 — 무엇이 / 어떻게 다듬으면 좋은지

[강점]
- (구체적으로 잘된 점 2~3개)

출고 가능하지만 다음 캠페인부터 개선 권장.

전체 점수: 46 / 50
```

#### PASS (출고 OK)

```markdown
판정: ✅ PASS

브랜드 정합도: 우수

[강점]
1. ...
2. ...
3. ...

[다음 단계 추천]
- 출고 채널: ...
- 시점: ...
- 후속 콘텐츠 추천: ...

전체 점수: 50 / 50
```

### Step 5. 위반 패턴 학습 (선택)

새로운 위반 패턴을 발견하면 `../checklists/brand-violations.md`에 V-XX로 추가 (사용자 승인 후).

### Step 6. 후속 액션 제안

검수 결과에 따라 다음 스킬 자동 추천:

| 상황 | 추천 다음 스킬 |
|---|---|
| 이미지 톤이 어긋남 | `tone-match-local` (디폴트 무드로) |
| 카피 톤이 어긋남 | `keyword-optimizer` (SEO + 카피 후보) |
| 상세페이지 구조 문제 | `pdp-builder`로 재생성 |
| 광고 소재 가변형 부족 | `meta-ad-factory` 21개 변형 빌드 |
| 캠페인 전체 재기획 | `creative-brief-template` 작성부터 다시 |

## 검수 모드 호출 트리거

> 사용자가 다음과 같이 말하면 자동 진입:

- "이거 톤 괜찮아?"
- "출고 전 검수해줘"
- "브랜드 가이드 맞춰서 봐줘"
- "이 카피 어때"
- "검수 한 번"
- "이거 우리 톤 맞아?"
- "review", "brand check"

## 검수 모드 출력 헤더

```
🔍 SundayHug 브랜드 검수 (Brand Director Review)
대상: [채널/포맷]
카테고리: [...]
─────────────────────────────────────────
```
