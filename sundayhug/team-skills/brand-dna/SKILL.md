---
name: brand-dna-extractor
description: 웹사이트에서 브랜드 DNA 추출 및 무드보드 생성
triggers:
  - "브랜드 분석"
  - "브랜드 DNA 추출"
  - "무드보드 만들어줘"
  - "이 사이트 분석해줘"
---

# Brand DNA Extractor

웹사이트에서 브랜드 DNA를 추출하여 인터랙티브 웹 리포트를 생성.

## 워크플로우

```
URL 입력 → 크롤링 → AI 분석 (7단계) → JSON 생성 → React 웹 리포트
```

## Step 1: 크롤링

```bash
python scripts/crawl.py "https://example.com" --output /tmp/crawl_result.json
```

## Step 2: AI 분석 파이프라인

7개 프롬프트 순차 실행. `references/prompts/` 참조:

| # | 분석 | 파일 | 입력 |
|---|------|------|------|
| 1 | 퍼스낼리티 | `personality.md` | 텍스트 |
| 2 | 톤앤보이스 | `tone-of-voice.md` | 텍스트 |
| 3 | 타겟 | `target-audience.md` | 텍스트+가격 |
| 4 | 비주얼 | `visual-identity.md` | 이미지 |
| 5 | 컬러 | `color-psychology.md` | 팔레트 |
| 6 | 포지셔닝 | `positioning.md` | 1-5 결과 |
| 7 | 종합 | `synthesis.md` | 전체 |

### 프롬프트 실행

```python
prompt = read_file("references/prompts/personality.md")
prompt = prompt.replace("{{brand_name}}", data["brand_name"])
prompt = prompt.replace("{{collected_texts}}", data["texts"])
result = call_claude(prompt)
```

## Step 3: BrandReportData JSON 생성

AI 분석 결과를 아래 `BrandReportData` 인터페이스에 맞춰 JSON으로 변환:

```typescript
interface BrandReportData {
  meta: {
    date: string;           // "2026-01-13"
    client: string;         // 브랜드명
    status: string;         // "FINAL"
    projectCode: string;    // "brandname_DNA_2026.json"
  };
  summary: {
    mainTitle: string;      // 핵심 메시지 (줄바꿈 가능)
    subTitle: string;
    description: string;    // 브랜드 요약 설명
    insights: { label: string; icon: 'trending' | 'shield' | 'chart' }[];
  };
  identity: {
    mission: string;
    vision: string;
    values: string[];       // ['혁신', '신뢰', '효율', '성장']
    archetype: { name: string; description: string; };
    coreTraits: string[];
  };
  personality: {
    radarData: { subject: string; A: number; fullMark: 100 }[];  // Aaker 5 dimensions
    highlight: { title: string; score: number; };
  };
  tone: {
    spectrum: { label: string; left: string; right: string; value: number }[];  // 0-100
    guidelines: { dos: string[]; donts: string[]; };
  };
  visuals: {
    colors: { role: string; name: string; hex: string; desc: string; textColor: string }[];
    styleGuide: { title: string; description: string }[];
  };
  persona: {
    name: string;
    role: string;
    imageUrl: string;       // Unsplash URL
    quote: string;
    description: string;
    goals: string[];
    painPoints: string[];
    tags: string[];
  };
  strategy: {
    strengths: string[];
    opportunities: string[];
    watchOut: string[];
  };
  moodboard: {
    keywords: string[];
    images: string[];       // 크롤링된 웹사이트 이미지 URLs (5-8장)
  };
}
```

### 무드보드 이미지 선택 가이드

크롤링 결과의 `images` 배열에서 무드보드용 이미지를 선택:

```python
# 크롤링 결과에서 이미지 선택 우선순위
crawl_result = json.load(open("/tmp/crawl_result.json"))

# 1. 제품 이미지 (product 관련)
product_images = [img for img in crawl_result["images"]
                  if "product" in img["url"].lower()]

# 2. 메인 비주얼 (medium/large 사이즈)
main_images = [img for img in crawl_result["images"]
               if "medium" in img["url"] or "large" in img["url"]]

# 3. OG 이미지 (브랜드 대표 이미지)
og_images = [img for img in crawl_result["images"]
             if img["type"] == "og_image"]

# 4. 아이콘/로고 제외
filtered = [img for img in main_images
            if not any(x in img["url"].lower() for x in ["icon", "logo", "svg"])]

# 최종 5-8장 선택
moodboard_images = filtered[:8]
```

**이미지 선택 기준:**
- 제품 이미지 우선 (브랜드 정체성 반영)
- medium/large 사이즈 선호 (고화질)
- 아이콘, 로고, SVG 제외
- OG 이미지 포함 (브랜드 대표 이미지)
- 다양한 제품/시각적 요소 포함

### JSON 파일 저장

```bash
# 분석 결과를 JSON 파일로 저장
report/{브랜드명}/{브랜드명}_data.json
```

## Step 4: 웹 리포트 빌드

브랜드별 정적 웹사이트 생성:

```bash
python scripts/build_report.py --brand "브랜드명" --data /tmp/brand_data.json
```

### 결과물 구조

```
report/
└── {브랜드명}/
    ├── index.html      # 메인 리포트 페이지
    ├── assets/         # CSS, JS, 이미지
    └── {브랜드명}_data.json  # 원본 데이터
```

### 로컬에서 보기

```bash
# 방법 1: 파일 직접 열기
open "report/{브랜드명}/index.html"

# 방법 2: 로컬 서버 (권장)
cd "report/{브랜드명}"
python -m http.server 8080
# → http://localhost:8080
```

### 개발 모드 (실시간 미리보기)

```bash
cd "Brand Guidance Moodboard Template"
npm install
npm run dev
# → http://localhost:5173
```

## 사용 예시

**입력**: "https://sundayhug.com 브랜드 DNA 분석해줘"

**실행**:
1. `scripts/crawl.py` 웹사이트 크롤링
2. 7개 프롬프트 순차 실행 (AI 분석)
3. `BrandReportData` JSON 생성
4. `scripts/build_report.py` 정적 사이트 빌드
5. `report/{브랜드명}/` 폴더에 결과물 저장
6. 로컬 URL 제공

## 결과물

### 폴더 구조

```
report/
├── sundayhug/
│   ├── index.html
│   ├── assets/
│   └── sundayhug_data.json
├── flex/
│   ├── index.html
│   ├── assets/
│   └── flex_data.json
└── ...
```

### 웹 리포트 섹션

7개 섹션의 인터랙티브 브랜드 분석 리포트:

1. **Executive Summary** - 브랜드 핵심 요약
2. **Brand Identity** - Mission/Vision/Values + Personality Radar Chart
3. **Tone & Voice** - 커뮤니케이션 스펙트럼 + Do/Don't 가이드
4. **Visual Identity** - Color System + Style Guide
5. **Target Persona** - 사용자 프로필 분석
6. **Strategic Recommendations** - SWOT 분석
7. **Visual Moodboard** - 크롤링된 실제 웹사이트 이미지 기반 무드보드
