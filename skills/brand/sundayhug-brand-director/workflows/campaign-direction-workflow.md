# Workflow B: 신규 캠페인 크리에이티브 방향성 설정 (Director Mode)

> 사용자가 신규 캠페인 의도를 제시하면 브랜드 실장이 컨셉/컬러/톤/비주얼 무드/스킬 체인을 담은 크리에이티브 브리프를 작성하고, 실행 순서를 가이드.

## 입력

- 캠페인 컨셉 (예: "봄 SS 컬러 드롭", "ABC 신제품 런칭", "출산선물 시즌 캠페인")
- 출시 시점 / 노출 기간
- 핵심 채널 (인스타, 자사몰, 메타, 네이버 블로그 등)
- (선택) 예산, 제약사항, KPI

## 단계

### Step 1. 컨텍스트 로드

검수 모드와 동일하지만, 크리에이티브 측을 더 깊이 보기 위해:

1. `../guidance/quick-reference.md` (전체)
2. `../guidance/sundayhug-brand-project.md` (10번 포지셔닝 맵 + 6번 패키징 + 7번 콘텐츠 3 Pillars 부분)
3. `../checklists/creative-brief-template.md` (전체) — 작성 양식

### Step 2. 캠페인 의도 파악 (대화)

부족한 정보가 있으면 `AskUserQuestion`으로 보완:

- 캠페인 메인 축은? (수면 과학 / 감성 디자인 / 프리미엄 경험)
- 시즌 컬러 드롭인가? (= Seasonal Accent 사용)
- 타겟 페르소나의 페인 포인트가 명확한가?
- KPI가 무엇인가? (전환율 / 도달 / 후기 / 검색량)

### Step 3. 크리에이티브 브리프 작성

`creative-brief-template.md`의 12개 섹션을 모두 채워서 브리프 1건 출력:

1. 캠페인 기본 정보
2. 캠페인 미션 한 줄
3. 3축 정합
4. 타겟 페르소나
5. 핵심 메시지 (메인 카피 / 서브 카피 / CTA / 금지)
6. 비주얼 디렉션 (컬러 + 무드 키워드 + 포토그래피 + 타이포)
7. 보이스 톤
8. 컨텐츠 산출물 매트릭스
9. 사용할 스킬 체인
10. KPI / 성공 기준
11. 위험 / 금기
12. 일정

저장 위치: `~/Desktop/team-skills/리포트/brand-briefs/{YYYY-MM-DD}_{캠페인코드}.md`

### Step 4. 컬러 / 무드 추천

**Brand DNA 기반 자동 추천 로직**:

| 캠페인 카테고리 | 추천 컬러 조합 | 추천 무드 |
|---|---|---|
| 시즌 컬러 드롭 (봄) | Cloud + Sage `#B5C4B1` + Soft Apricot `#E8C9A8` | Garden / Dawn |
| 시즌 컬러 드롭 (여름) | Warm Ivory + Misty Blue `#B3C5D3` | Dawn / Cool Breeze |
| 시즌 컬러 드롭 (가을) | Linen + Golden Hour `#D4A574` + Dusty Rose `#C09B8D` | Golden / Dusk |
| 시즌 컬러 드롭 (겨울) | Cloud + Slate Blue `#8A9BB0` + Moon | Moonlit / Dusk |
| 신제품 런칭 (수면) | Primary 5색 + Dusty Lavender `#C4B5CB` | Moonlit |
| 출산선물 캠페인 | Warm Ivory + Blush `#DEB5A8` + Linen | Garden / Golden |
| 프로모션 (절제 권장) | Primary 만, Accent 최소화 | Dusk |

### Step 5. 스킬 체인 가이드

브리프가 확정되면 다음 명령어를 순서대로 실행하도록 안내:

```bash
# 1. 키워드 SEO 발굴
"[제품명] 키워드 최적화 해줘"
# → keyword-optimizer 실행 → S/A/B/C/D 등급 + 상품태그

# 2. 사진 톤 통일 (시즌 컬러 무드 강할 경우 별도 레퍼런스 지정)
"product-photos 폴더 톤 매칭해줘. 봄 시즌 컬러 무드로"
# → tone-match-local Step 0에서 사용자 톤 의도 확인

# 3. 자사몰 PDP 생성
"[제품명] 상세페이지 만들어줘. 레퍼런스: [경쟁사 URL] + [캡처 이미지]"
# → pdp-builder

# 4. 메타 광고 21종
"메타 광고 만들어줘 [슬러그]"
# → meta-ad-factory

# 5. 시즌 마케팅 캘린더
"마케팅 플랜 짜줘 [제품]"
# → sundayhug-marketing-planner

# 6. 모든 산출물 검수
"이 산출물들 검수해줘"
# → 다시 brand-director (Reviewer Mode)
```

### Step 6. 실행 가능한 다음 액션 출력

```markdown
✅ 크리에이티브 브리프 작성 완료

저장 위치: ~/Desktop/team-skills/리포트/brand-briefs/2025-04-27_SS-DROP-001.md

🚦 다음 단계 (순차 실행 권장):

1. [keyword-optimizer]   "[ABC 블랭킷] 키워드 최적화 해줘"
2. [tone-match-local]    "product-photos 폴더 톤 매칭, 봄 무드로"
3. [pdp-builder]         "ABC 블랭킷 상세페이지 만들어줘. 레퍼런스: [URL]"
4. [meta-ad-factory]     "메타 광고 만들어줘 abc-blanket"
5. [marketing-planner]   "마케팅 플랜 짜줘 ABC 블랭킷"
6. [brand-director]      "산출물 검수해줘" ← 다시 이 스킬

각 단계 완료 후 자동으로 검수 단계 들어갑니다.
```

## 디렉터 모드 호출 트리거

- "신규 캠페인 기획"
- "[캠페인명] 크리에이티브 방향 잡아줘"
- "브리프 작성해줘"
- "이번 시즌 컬러 드롭 어떻게 갈까"
- "캠페인 디렉팅"
- "creative direction", "campaign brief"

## 디렉터 모드 출력 헤더

```
🎯 SundayHug 크리에이티브 디렉션 (Brand Director Briefing)
캠페인: [코드명]
기간: [시작 ~ 종료]
─────────────────────────────────────────
```
