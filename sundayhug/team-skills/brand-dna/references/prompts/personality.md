# 브랜드 퍼스낼리티 분석 프롬프트

당신은 브랜드 전략 전문가입니다. 
아래 웹사이트에서 수집된 텍스트를 분석하여 브랜드 개성을 평가해주세요.

## 분석 프레임워크: Aaker의 브랜드 개성 5차원 모델

각 차원을 0.0 ~ 1.0 점수로 평가하고, 판단 근거를 제시하세요.

### 1. Sincerity (진실성)
- 정직함, 진정성, 건전함, 명랑함
- 가족적, 친근한, 믿을 수 있는 느낌
- 예시 브랜드: 코카콜라, 할마트, 홀푸드

### 2. Excitement (흥미로움)  
- 대담함, 활기참, 상상력, 최신성
- 젊고, 트렌디하고, 독특한 느낌
- 예시 브랜드: 나이키, MTV, 레드불

### 3. Competence (능력)
- 신뢰성, 지성, 성공적
- 전문적이고, 효율적이고, 리더십 있는 느낌
- 예시 브랜드: 마이크로소프트, 볼보, CNN

### 4. Sophistication (세련됨)
- 상류층, 매력적
- 고급스럽고, 세련되고, 우아한 느낌
- 예시 브랜드: 샤넬, 렉서스, 아메리칸 익스프레스

### 5. Ruggedness (강인함)
- 아웃도어, 터프함
- 남성적이고, 거친, 자연적인 느낌
- 예시 브랜드: 말보로, 리바이스, 할리데이비슨

---

## 분석할 텍스트:

<brand_name>
{{brand_name}}
</brand_name>

<collected_texts>
{{collected_texts}}
</collected_texts>

---

## 출력 형식 (JSON):

```json
{
  "personality": {
    "sincerity": {
      "score": 0.0-1.0,
      "keywords": ["관련 키워드 3개"],
      "evidence": "판단 근거 (수집된 텍스트에서 인용)"
    },
    "excitement": {
      "score": 0.0-1.0,
      "keywords": ["관련 키워드 3개"],
      "evidence": "판단 근거"
    },
    "competence": {
      "score": 0.0-1.0,
      "keywords": ["관련 키워드 3개"],
      "evidence": "판단 근거"
    },
    "sophistication": {
      "score": 0.0-1.0,
      "keywords": ["관련 키워드 3개"],
      "evidence": "판단 근거"
    },
    "ruggedness": {
      "score": 0.0-1.0,
      "keywords": ["관련 키워드 3개"],
      "evidence": "판단 근거"
    }
  },
  "dominant_personality": "가장 높은 점수의 차원",
  "personality_summary": "브랜드 개성 2-3문장 요약"
}
```
