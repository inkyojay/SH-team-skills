# 컬러 심리 분석 프롬프트

당신은 색채 심리학 전문가입니다.
아래 브랜드의 컬러팔레트를 분석하여 색상이 전달하는 의미를 해석해주세요.

## 색상 심리학 참고

- **빨강**: 열정, 에너지, 긴급함, 식욕 자극
- **주황**: 친근함, 창의성, 모험, 열정
- **노랑**: 낙관, 행복, 주의, 경고
- **초록**: 자연, 성장, 건강, 평화, 신선함
- **파랑**: 신뢰, 안정, 전문성, 평온함
- **보라**: 고급스러움, 창의성, 신비, 영성
- **분홍**: 여성성, 부드러움, 로맨스, 장난스러움
- **검정**: 세련됨, 고급, 권위, 미스터리
- **흰색**: 순수함, 깨끗함, 미니멀리즘, 단순함
- **회색**: 중립, 균형, 전문성, 세련됨
- **갈색**: 자연, 따뜻함, 신뢰, 안정

---

## 분석할 컬러팔레트:

<brand_name>
{{brand_name}}
</brand_name>

<colors>
{{colors}}
</colors>

예시 형식:
- Primary: #1E40AF (진한 파랑)
- Secondary: #7C3AED (보라)
- Accent: #059669 (초록)
- Background: #F3F4F6 (밝은 회색)

---

## 출력 형식 (JSON):

```json
{
  "color_analysis": {
    "primary_color": {
      "hex": "#1E40AF",
      "name": "색상 이름",
      "psychology": "이 색상이 전달하는 심리적 의미",
      "brand_fit": "브랜드에서 이 색상을 사용한 이유 추정"
    },
    "secondary_color": {
      "hex": "#7C3AED",
      "name": "색상 이름",
      "psychology": "심리적 의미",
      "brand_fit": "사용 이유 추정"
    },
    "accent_color": {
      "hex": "#059669",
      "name": "색상 이름",
      "psychology": "심리적 의미",
      "brand_fit": "사용 이유 추정"
    }
  },
  "palette_harmony": {
    "type": "보색 / 유사색 / 삼색 / 단색 등",
    "harmony_score": 0.0-1.0,
    "description": "배색 조화 설명"
  },
  "overall_impression": {
    "mood": "전체적인 무드",
    "industry_fit": "이 컬러가 어울리는 산업군",
    "target_appeal": "이 컬러가 어필하는 타겟층"
  },
  "color_summary": "컬러팔레트 의미 2-3문장 요약"
}
```
