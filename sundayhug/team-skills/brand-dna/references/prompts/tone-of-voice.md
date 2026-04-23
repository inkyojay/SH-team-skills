# 톤앤보이스 분석 프롬프트

당신은 카피라이팅 및 브랜드 커뮤니케이션 전문가입니다.
아래 텍스트를 분석하여 브랜드의 톤앤보이스를 평가해주세요.

## 분석 기준

### 1. 형식성 스펙트럼 (Formality)
- Formal (1.0): 격식체, 존댓말, 전문 용어
- Casual (0.0): 비격식체, 친근한 말투, 구어체

### 2. 감정성 스펙트럼 (Emotionality)  
- Emotional (1.0): 감정 호소, 스토리텔링, 감성적 표현
- Rational (0.0): 논리적, 사실 기반, 기능적 설명

### 3. 에너지 스펙트럼 (Energy)
- Enthusiastic (1.0): 열정적, 느낌표, 강조 표현
- Reserved (0.0): 차분한, 절제된, 미니멀한 표현

### 4. 접근성 스펙트럼 (Accessibility)
- Simple (1.0): 쉬운 단어, 짧은 문장, 직관적
- Complex (0.0): 전문 용어, 긴 문장, 복잡한 구조

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
  "tone_analysis": {
    "formality": {
      "score": 0.0-1.0,
      "description": "formal/semi-formal/casual 중 선택",
      "examples": ["텍스트에서 추출한 예시 문장 2개"]
    },
    "emotionality": {
      "score": 0.0-1.0,
      "description": "emotional/balanced/rational 중 선택",
      "examples": ["예시 문장 2개"]
    },
    "energy": {
      "score": 0.0-1.0,
      "description": "enthusiastic/moderate/reserved 중 선택",
      "examples": ["예시 문장 2개"]
    },
    "accessibility": {
      "score": 0.0-1.0,
      "description": "simple/moderate/complex 중 선택",
      "examples": ["예시 문장 2개"]
    }
  },
  "voice_characteristics": [
    "특성 1 (예: 친근하고 대화하는 듯한)",
    "특성 2 (예: 전문적이면서도 이해하기 쉬운)",
    "특성 3"
  ],
  "do_examples": [
    "이 브랜드가 사용할 법한 문구 예시 1",
    "예시 2",
    "예시 3"
  ],
  "dont_examples": [
    "이 브랜드가 피해야 할 문구 예시 1",
    "예시 2",
    "예시 3"
  ],
  "tone_summary": "톤앤보이스 2-3문장 요약"
}
```
