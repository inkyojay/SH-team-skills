# 브랜드 DNA 종합 분석 프롬프트

당신은 시니어 브랜드 전략가입니다.
아래 분석 결과들을 종합하여 브랜드 DNA 프로필을 완성해주세요.

## 종합할 분석 결과:

<brand_name>
{{brand_name}}
</brand_name>

<personality_analysis>
{{personality_analysis}}
</personality_analysis>

<tone_analysis>
{{tone_analysis}}
</tone_analysis>

<visual_analysis>
{{visual_analysis}}
</visual_analysis>

<color_analysis>
{{color_analysis}}
</color_analysis>

<target_audience>
{{target_audience}}
</target_audience>

<positioning_analysis>
{{positioning_analysis}}
</positioning_analysis>

---

## 출력 형식 (JSON):

```json
{
  "brand_dna_profile": {
    "brand_name": "브랜드명",
    "category": "카테고리",
    "one_liner": "브랜드를 한 문장으로 설명",
    
    "identity": {
      "mission": "추정 미션 (이 브랜드가 존재하는 이유)",
      "vision": "추정 비전 (이 브랜드가 지향하는 미래)",
      "core_values": ["핵심 가치 1", "가치 2", "가치 3"],
      "brand_essence": "한 단어로 표현하는 브랜드 핵심"
    },
    
    "personality": {
      "archetype": "브랜드 아키타입 (Hero, Caregiver, Creator, Ruler, Magician, Lover, Jester, Everyman, Innocent, Sage, Explorer, Outlaw 중)",
      "traits": ["성격 특성 1", "특성 2", "특성 3"],
      "human_comparison": "만약 이 브랜드가 사람이라면..."
    },
    
    "expression": {
      "visual_keywords": ["비주얼 키워드 5개"],
      "verbal_keywords": ["언어적 키워드 5개"],
      "emotional_keywords": ["감정적 키워드 5개"]
    },
    
    "strategy": {
      "target_summary": "타겟 한 줄 요약",
      "positioning_summary": "포지셔닝 한 줄 요약",
      "usp": "USP 한 줄",
      "competitive_edge": "경쟁 우위 한 줄"
    }
  },
  
  "executive_summary": {
    "headline": "헤드라인 (10단어 이내)",
    "summary": "브랜드 DNA 요약 (3-4문장)",
    "key_takeaways": [
      "핵심 인사이트 1",
      "핵심 인사이트 2",
      "핵심 인사이트 3"
    ]
  },
  
  "recommendations": {
    "strengths": ["강점 1", "강점 2"],
    "opportunities": ["기회 요소 1", "기회 요소 2"],
    "watch_outs": ["주의할 점 1", "주의할 점 2"]
  },
  
  "moodboard_keywords": ["무드보드에 들어갈 키워드 10개"]
}
```
