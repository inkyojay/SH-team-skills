# 타겟 오디언스 분석 프롬프트

당신은 마케팅 리서치 전문가입니다.
아래 브랜드 정보를 분석하여 타겟 오디언스를 추정해주세요.

## 분석 요소

### 1. 인구통계학적 특성
- 연령대, 성별, 소득 수준, 교육 수준, 직업

### 2. 심리그래픽 특성
- 라이프스타일, 가치관, 관심사, 성격 특성

### 3. 행동적 특성
- 구매 패턴, 브랜드 충성도, 사용 상황

### 4. 니즈 & 페인포인트
- 이 브랜드가 해결하는 문제, 충족시키는 욕구

---

## 분석할 정보:

<brand_name>
{{brand_name}}
</brand_name>

<brand_category>
{{brand_category}}
</brand_category>

<collected_texts>
{{collected_texts}}
</collected_texts>

<price_range>
{{price_range}}
</price_range>

---

## 출력 형식 (JSON):

```json
{
  "primary_audience": {
    "demographics": {
      "age_range": "25-35세",
      "gender": "여성 중심 / 남성 중심 / 성별 무관",
      "income_level": "중상위 / 중위 / etc",
      "education": "대졸 이상 / etc",
      "occupation": ["직업군 1", "직업군 2"]
    },
    "psychographics": {
      "lifestyle": ["라이프스타일 특성 1", "특성 2"],
      "values": ["가치관 1", "가치관 2"],
      "interests": ["관심사 1", "관심사 2", "관심사 3"],
      "personality": ["성격 특성 1", "특성 2"]
    },
    "behaviors": {
      "purchase_drivers": ["구매 동기 1", "동기 2"],
      "media_consumption": ["주로 사용하는 미디어/채널"],
      "brand_relationship": "탐색형 / 충성형 / etc"
    }
  },
  "secondary_audience": {
    "description": "2차 타겟 간략 설명",
    "key_difference": "1차 타겟과의 차이점"
  },
  "customer_persona": {
    "name": "가상의 이름",
    "age": 30,
    "occupation": "직업",
    "one_liner": "한 줄 설명",
    "goals": ["목표 1", "목표 2"],
    "pain_points": ["페인포인트 1", "페인포인트 2"],
    "quote": "이 페르소나가 할 법한 말"
  },
  "audience_summary": "타겟 오디언스 2-3문장 요약"
}
```
