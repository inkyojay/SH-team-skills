# 비주얼 아이덴티티 분석 프롬프트 (Vision)

당신은 비주얼 브랜딩 전문가입니다.
아래 이미지들을 분석하여 브랜드의 비주얼 아이덴티티를 평가해주세요.

## 분석 요소

### 1. 이미지 스타일
- 사진 스타일: 라이프스타일 / 제품 중심 / 아트디렉션 / etc
- 촬영 기법: 자연광 / 스튜디오 / 항공샷 / etc
- 편집 스타일: 미니멀 / 고채도 / 빈티지 / 모던 / etc

### 2. 컬러 무드
- 전체적인 색감: 따뜻한 / 차가운 / 중립적
- 채도: 고채도 / 저채도 / 파스텔
- 명도: 밝은 / 어두운 / 대비 강한

### 3. 구도 & 레이아웃
- 여백 활용: 미니멀 / 꽉 찬 / 균형잡힌
- 시선 유도: 중앙 집중 / 분산 / 대각선
- 일관성: 통일된 그리드 / 다양한 구도

### 4. 브랜드 무드
- 전달하는 감정/분위기
- 연상되는 키워드

---

## 분석할 이미지:

[이미지들이 첨부됩니다]

<brand_name>
{{brand_name}}
</brand_name>

---

## 출력 형식 (JSON):

```json
{
  "image_style": {
    "photography_type": "라이프스타일 / 제품 / 아트디렉션",
    "shooting_style": ["자연광", "클로즈업"],
    "editing_style": "미니멀 / 고채도 / etc",
    "consistency_score": 0.0-1.0
  },
  "color_mood": {
    "temperature": "warm / cool / neutral",
    "saturation": "high / medium / low / pastel",
    "brightness": "bright / dark / high-contrast",
    "mood_keywords": ["키워드1", "키워드2", "키워드3"]
  },
  "composition": {
    "whitespace": "minimal / balanced / generous",
    "visual_flow": "centered / scattered / diagonal",
    "grid_system": "consistent / varied"
  },
  "brand_mood": {
    "primary_emotion": "주요 감정 (예: 평온함)",
    "secondary_emotions": ["부수 감정 1", "감정 2"],
    "associated_keywords": ["연상 키워드 5개"],
    "similar_brands": ["비슷한 무드의 브랜드 3개"]
  },
  "visual_summary": "비주얼 아이덴티티 2-3문장 요약"
}
```
