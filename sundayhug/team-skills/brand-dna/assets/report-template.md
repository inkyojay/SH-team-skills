# {{brand_name}} 브랜드 DNA 분석 리포트

> 분석일: {{date}}  
> URL: {{url}}

---

## Executive Summary

**{{headline}}**

{{summary}}

### 핵심 인사이트

{{#each key_takeaways}}
- {{this}}
{{/each}}

---

## 1. 브랜드 아이덴티티

### 미션
{{identity.mission}}

### 비전
{{identity.vision}}

### 핵심 가치
{{#each identity.core_values}}
- **{{this}}**
{{/each}}

### 브랜드 에센스
> "{{identity.brand_essence}}"

---

## 2. 브랜드 퍼스낼리티

### 브랜드 아키타입
**{{personality.archetype}}**

### 성격 특성
{{#each personality.traits}}
- {{this}}
{{/each}}

### 브랜드를 사람으로 표현한다면
{{personality.human_comparison}}

### Aaker 5차원 분석

| 차원 | 점수 | 키워드 |
|------|------|--------|
| Sincerity (진실성) | {{personality.sincerity.score}} | {{personality.sincerity.keywords}} |
| Excitement (흥미로움) | {{personality.excitement.score}} | {{personality.excitement.keywords}} |
| Competence (능력) | {{personality.competence.score}} | {{personality.competence.keywords}} |
| Sophistication (세련됨) | {{personality.sophistication.score}} | {{personality.sophistication.keywords}} |
| Ruggedness (강인함) | {{personality.ruggedness.score}} | {{personality.ruggedness.keywords}} |

---

## 3. 톤앤보이스

### 커뮤니케이션 스타일

| 스펙트럼 | 점수 | 설명 |
|----------|------|------|
| 형식성 | {{tone.formality.score}} | {{tone.formality.description}} |
| 감정성 | {{tone.emotionality.score}} | {{tone.emotionality.description}} |
| 에너지 | {{tone.energy.score}} | {{tone.energy.description}} |
| 접근성 | {{tone.accessibility.score}} | {{tone.accessibility.description}} |

### 보이스 특성
{{#each tone.voice_characteristics}}
- {{this}}
{{/each}}

### Do's (권장 표현)
{{#each tone.do_examples}}
- ✅ "{{this}}"
{{/each}}

### Don'ts (피해야 할 표현)
{{#each tone.dont_examples}}
- ❌ "{{this}}"
{{/each}}

---

## 4. 비주얼 아이덴티티

### 이미지 스타일
- **사진 유형**: {{visual.photography_type}}
- **촬영 스타일**: {{visual.shooting_style}}
- **편집 스타일**: {{visual.editing_style}}
- **일관성 점수**: {{visual.consistency_score}}

### 컬러 무드
- **색온도**: {{visual.color_mood.temperature}}
- **채도**: {{visual.color_mood.saturation}}
- **명도**: {{visual.color_mood.brightness}}
- **무드 키워드**: {{visual.color_mood.mood_keywords}}

### 브랜드 무드
- **주요 감정**: {{visual.brand_mood.primary_emotion}}
- **연상 키워드**: {{visual.brand_mood.associated_keywords}}
- **유사 브랜드**: {{visual.brand_mood.similar_brands}}

---

## 5. 컬러 시스템

### 컬러 팔레트

| 역할 | 색상 | 의미 |
|------|------|------|
| Primary | {{color.primary.hex}} {{color.primary.name}} | {{color.primary.psychology}} |
| Secondary | {{color.secondary.hex}} {{color.secondary.name}} | {{color.secondary.psychology}} |
| Accent | {{color.accent.hex}} {{color.accent.name}} | {{color.accent.psychology}} |

### 배색 조화
- **유형**: {{color.palette_harmony.type}}
- **조화 점수**: {{color.palette_harmony.harmony_score}}

### 컬러 인상
{{color.overall_impression.mood}}

---

## 6. 타겟 오디언스

### 1차 타겟

**인구통계**
- 연령: {{target.primary.demographics.age_range}}
- 성별: {{target.primary.demographics.gender}}
- 소득: {{target.primary.demographics.income_level}}
- 직업: {{target.primary.demographics.occupation}}

**심리그래픽**
- 라이프스타일: {{target.primary.psychographics.lifestyle}}
- 가치관: {{target.primary.psychographics.values}}
- 관심사: {{target.primary.psychographics.interests}}

### 고객 페르소나

> **{{target.persona.name}}** ({{target.persona.age}}세, {{target.persona.occupation}})
> 
> "{{target.persona.quote}}"
>
> **목표**: {{target.persona.goals}}
> **페인포인트**: {{target.persona.pain_points}}

---

## 7. 포지셔닝

### 가치 제안

**기능적 혜택**
{{#each positioning.functional_benefits}}
- {{this}}
{{/each}}

**감정적 혜택**
{{#each positioning.emotional_benefits}}
- {{this}}
{{/each}}

**핵심 약속**
> {{positioning.core_promise}}

### 포지셔닝 스테이트먼트
> {{positioning.positioning_statement}}

### 차별화 포인트 (USP)
**{{positioning.usp}}**

### 경쟁 우위
{{#each positioning.competitive_advantages}}
- {{this}}
{{/each}}

---

## 8. 브랜드 표현 키워드

### 비주얼 키워드
{{#each expression.visual_keywords}}
`{{this}}` 
{{/each}}

### 언어적 키워드
{{#each expression.verbal_keywords}}
`{{this}}` 
{{/each}}

### 감정적 키워드
{{#each expression.emotional_keywords}}
`{{this}}` 
{{/each}}

---

## 9. 전략적 권고사항

### 강점
{{#each recommendations.strengths}}
- ✅ {{this}}
{{/each}}

### 기회 요소
{{#each recommendations.opportunities}}
- 🚀 {{this}}
{{/each}}

### 주의할 점
{{#each recommendations.watch_outs}}
- ⚠️ {{this}}
{{/each}}

---

## 부록: 무드보드

[무드보드 이미지]

### 무드보드 키워드
{{#each moodboard_keywords}}
{{this}} | 
{{/each}}

---

*이 리포트는 Brand DNA Extractor에 의해 자동 생성되었습니다.*
