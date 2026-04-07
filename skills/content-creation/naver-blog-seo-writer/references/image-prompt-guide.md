# Google Gemini 이미지 생성 가이드

## 이미지 생성 API 설정

### 사용 API
**Google Gemini API** (generativelanguage.googleapis.com)
- 모델: `imagen-3.0-generate-002` (최신 Imagen 3)
- 한국어 프롬프트 지원
- Google AI Studio에서 API 키 발급

### API 키 발급 방법
1. https://aistudio.google.com 접속
2. "Get API key" 클릭
3. 프로젝트 생성 후 API 키 복사
4. 무료 티어: 분당 10회 요청 가능

---

## 블로그 이미지 유형별 프롬프트 패턴

### 유형 1: 대표 이미지 (도입부 직후)
글 전체를 대표하는 메인 이미지. 제품 or 주제 관련 고품질 이미지.

**프롬프트 패턴:**
```
[주제 핵심 명사], [분위기/스타일], [배경/환경], [조명], [구도],
상업용 제품 사진 스타일, 고해상도, 선명한, 따뜻한 색감
```

**예시 (신생아 슬리핑백):**
```
Cozy baby sleeping bag, soft pastel colors, white clean background,
natural soft lighting, close-up product shot,
commercial photography style, high resolution, warm tones,
no text overlay
```

### 유형 2: 정보형 이미지 (설명 내용 강조)
체크리스트, 비교표, 단계 설명 등 정보를 시각화.

**프롬프트 패턴:**
```
[설명 내용] infographic style, clean minimalist design,
[브랜드 컬러] accent color, white background, simple icons,
Korean-friendly design, no text (텍스트는 HTML에서 오버레이)
```

**예시 (사이즈 비교):**
```
Baby sleeping bag size comparison flat lay, 
small medium large sizes arranged neatly,
soft cream white background, minimal style,
top-down view, product photography
```

### 유형 3: 라이프스타일 이미지 (감성/공감 유도)
실제 사용 상황을 연출한 따뜻한 분위기 이미지.

**프롬프트 패턴:**
```
[상황 묘사], lifestyle photography, warm cozy atmosphere,
[시간대: morning/evening], soft natural light,
Korean family style, candid feeling, no faces shown
```

**예시 (아기 수면):**
```
Sleeping newborn baby in cozy sleeping bag, 
soft warm nursery room, morning light, 
pastel colors, serene peaceful atmosphere,
lifestyle photography, warm and tender mood,
top-down angle, no faces
```

### 유형 4: 소재/디테일 이미지 (제품 특징 강조)
소재 질감, 봉제, 디테일을 클로즈업한 이미지.

**프롬프트 패턴:**
```
Close-up texture of [소재 종류] fabric, 
soft and smooth, macro photography,
[컬러] tone, clean white background,
product detail shot, high clarity
```

**예시 (대나무 소재):**
```
Close-up bamboo cotton fabric texture, 
ultra soft and breathable material, 
macro photography, gentle green and cream tones,
clean white background, premium quality look
```

---

## 썬데이허그 브랜드 이미지 프롬프트 원칙

### 브랜드 무드
- **키워드**: cozy, gentle, safe, natural, premium, Korean baby brand
- **컬러 팔레트**: mint green (#1D9E75), warm cream, soft white
- **분위기**: 따뜻하고 안전한, 프리미엄하지만 친근한

### 브랜드 이미지 공통 프롬프트 접미어
```
, premium Korean baby brand style, soft mint green accent,
warm cream and white tones, clean minimal background,
cozy and safe atmosphere, high-end product photography
```

---

## 이미지 배치 계획표 (글 작성 전 결정)

| 위치 | 유형 | 프롬프트 핵심 | 역할 |
|------|------|--------------|------|
| 도입부 직후 | 대표 이미지 | 제품 전체 + 따뜻한 배경 | 첫인상, 클릭 유지 |
| 소제목 2 후 | 정보형 | 비교/설명 플랫레이 | 내용 시각화 |
| 소제목 4 후 | 라이프스타일 | 실사용 분위기 | 공감/감성 |
| 마무리 전 | 제품 디테일 | 소재/기능 클로즈업 | 구매 욕구 강화 |

---

## 이미지 사용 시 주의사항

1. **저작권**: Imagen 생성 이미지는 상업용 사용 가능 (Google AI 정책 기준)
2. **실제 아기 얼굴**: AI 생성 시 얼굴 없는 방식 권장 (프롬프트에 "no faces" 추가)
3. **파일명**: SEO를 위해 한국어 설명으로 저장 (예: 신생아-슬리핑백-소재-비교.jpg)
4. **이미지 크기**: 네이버 블로그 권장 크기 1200px × 800px (가로형)
5. **alt 텍스트**: 이미지 업로드 후 반드시 키워드 포함 설명 입력
