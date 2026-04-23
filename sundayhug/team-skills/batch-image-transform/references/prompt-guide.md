# 프롬프트 가이드

## 이커머스 시나리오별 예시 프롬프트

### 라이프스타일
```
Bright modern living room with natural sunlight streaming through large windows, minimalist Scandinavian decor, light wood furniture, green plants in the background
```

### 스튜디오 (화이트)
```
Clean white studio background with soft diffused lighting, subtle shadow beneath product, professional product photography setup
```

### 스튜디오 (컬러)
```
Solid pastel pink background with soft even lighting, minimal shadow, clean and modern aesthetic
```

### 카페/F&B
```
Stylish cafe table with latte art, morning sunlight, marble countertop, fresh pastries, warm and inviting atmosphere
```

### 여름/트로피컬
```
Tropical beach setting with turquoise water, white sand, palm leaf shadows, golden hour sunlight, vacation atmosphere
```

### 겨울/코지
```
Cozy winter cabin interior, warm fireplace glow, knitted blankets, hot cocoa, snowfall visible through frosted windows
```

### 자연/아웃도어
```
Lush green garden with morning dew, soft natural light filtering through trees, wildflowers, fresh and organic feeling
```

### 도시/모던
```
Modern urban rooftop at sunset, city skyline in background, warm golden hour light, clean concrete and glass surfaces
```

### 럭셔리
```
Elegant marble surface with gold accents, soft ambient lighting, luxury boutique atmosphere, dark moody background
```

### 미니멀
```
Simple flat lay on textured linen fabric, overhead shot, natural window light casting soft shadows, neutral earth tones
```

## 비율 선택 가이드

| 비율 | 용도 | 권장 채널 |
|------|------|-----------|
| `1:1` | 정방형 | 인스타그램 피드, 쇼핑몰 썸네일, SNS 광고 |
| `9:16` | 세로형 | 인스타 릴스, 틱톡, 쇼츠, 스토리 |
| `16:9` | 가로형 | 유튜브 썸네일, 배너, 상세페이지 헤더 |

## 모델 선택 가이드

| 모델 | 소요 시간 | 품질 | 권장 용도 |
|------|-----------|------|-----------|
| `gemini-2.5-flash` | ~23초/장 | 좋음 | 대량 처리, 테스트, SNS용 |
| `gemini-3-pro` | ~45초/장 | 최고 | 상세페이지, 배너, 고해상도 필요 시 |

## 주의사항

- 한국어 프롬프트는 자동으로 영문 번역됨 (Gemini 2.0 Flash 사용)
- 상품 자체의 형태/색상은 최대한 보존됨
- 인물 포함 이미지는 `--appearance` 옵션으로 별도 제어 가능
- 대량 처리 시 429 에러 방지를 위해 `--concurrency 1` 권장
