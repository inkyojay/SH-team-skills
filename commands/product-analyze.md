---
name: product-analyzer
description: 제품 분석 리포트
triggers:
  - "제품 분석"
  - "상품 리뷰"
  - "상세페이지 분석"
  - "이 제품 어때?"
---

# Product Analyzer

스마트스토어 상세페이지의 이미지를 분석하여 제품의 강점과 단점을 정리한 리포트를 생성합니다.

## 워크플로우

```
URL 입력 → 이미지 크롤링 → Claude Vision 분석 → JSON 생성 → React 웹 리포트
```

## Step 1: 크롤링

스마트스토어 상세페이지에서 이미지 추출:

```bash
python scripts/crawl_smartstore.py "https://smartstore.naver.com/store/products/123" --output /tmp/crawl_result.json
```

### 출력 형식

```json
{
  "product_info": {
    "url": "...",
    "store_name": "스토어명",
    "product_name": "제품명",
    "price": "가격",
    "category": "카테고리"
  },
  "images": [
    {
      "url": "이미지 URL",
      "base64": "base64 인코딩 데이터",
      "media_type": "image/jpeg",
      "type": "detail|thumbnail"
    }
  ],
  "image_count": 10
}
```

## Step 2: Claude Vision 분석

크롤링된 이미지를 Claude에 전달하여 분석:

```python
# 프롬프트 로드
prompt = read_file("references/prompts/product-analysis.md")
prompt = prompt.replace("{{product_name}}", crawl_result["product_info"]["product_name"])
prompt = prompt.replace("{{store_name}}", crawl_result["product_info"]["store_name"])
prompt = prompt.replace("{{price}}", crawl_result["product_info"]["price"])

# Claude Vision API 호출 (이미지 첨부)
images = [
    {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": img["media_type"],
            "data": img["base64"]
        }
    }
    for img in crawl_result["images"]
]

result = call_claude_with_images(prompt, images)
```

### 분석 항목

| # | 분석 영역 | 설명 |
|---|----------|------|
| 1 | 제품 개요 | 카테고리, 타겟 고객, 핵심 기능 |
| 2 | 강점 분석 | 기능/디자인/가격/차별화 (5-7개) |
| 3 | 단점 분석 | 기능 한계/정보 부족/우려 사항 (3-5개) |
| 4 | 기능별 분석 | 각 기능 1-5점 평가 |
| 5 | 경쟁 비교 | 유사 제품군 대비 비교 |
| 6 | 구매 추천 | 추천 점수 (1-10) 및 적합 고객 |

## Step 3: ProductReportData JSON 생성

AI 분석 결과를 아래 `ProductReportData` 인터페이스에 맞춰 JSON으로 변환:

```typescript
interface ProductReportData {
  meta: {
    date: string;           // "2026-01-14"
    productName: string;    // 제품명
    storeName: string;      // 스토어명
    productUrl: string;     // 원본 URL
    price: string;          // "89,000원"
  };
  overview: {
    category: string;
    targetAudience: string;
    coreFeatures: string[];
    summary: string;
  };
  strengths: {
    title: string;
    description: string;
    category: 'function' | 'design' | 'price' | 'unique';
    importance: 'high' | 'medium' | 'low';
  }[];
  weaknesses: {
    title: string;
    description: string;
    category: 'function' | 'info' | 'concern';
    severity: 'high' | 'medium' | 'low';
  }[];
  featureAnalysis: {
    feature: string;
    score: number;  // 1-5
    evidence: string;
    pros: string[];
    cons: string[];
  }[];
  competitorComparison: {
    aspect: string;
    thisProduct: string;
    competitors: string;
    verdict: 'advantage' | 'similar' | 'disadvantage';
  }[];
  recommendation: {
    score: number;  // 1-10
    summary: string;
    bestFor: string[];
    notFor: string[];
  };
  images: {
    thumbnail: string;
    detailImages: string[];
  };
}
```

## Step 4: 웹 리포트 빌드

제품별 정적 웹사이트 생성:

```bash
python scripts/build_product_report.py --product "제품명" --data /tmp/product_data.json
```

### 결과물 구조

```
report/
└── {제품명}/
    ├── index.html        # 메인 리포트 페이지
    ├── assets/           # CSS, JS
    └── {제품명}_data.json  # 원본 데이터
```

### 로컬에서 보기

```bash
# 방법 1: 파일 직접 열기
open "report/{제품명}/index.html"

# 방법 2: 로컬 서버 (권장)
cd "report/{제품명}"
python -m http.server 8080
# → http://localhost:8080
```

## 사용 예시

**입력**: "https://smartstore.naver.com/techstore/products/123456 이 제품 분석해줘"

**실행**:
1. `scripts/crawl_smartstore.py` - 상세페이지 이미지 추출
2. Claude Vision API - 이미지 분석
3. `ProductReportData` JSON 생성
4. `scripts/build_product_report.py` - 정적 사이트 빌드
5. `report/{제품명}/` 폴더에 결과물 저장
6. 로컬 URL 제공

## 리포트 섹션

6개 섹션의 인터랙티브 제품 분석 리포트:

1. **제품 개요** - 카테고리, 타겟 고객, 핵심 기능
2. **강점 분석** - 기능/디자인/가격/차별화 강점
3. **단점 / 개선점** - 기능 한계, 정보 부족, 우려 사항
4. **기능별 상세 분석** - 각 기능 점수 및 장단점
5. **경쟁 제품 비교** - 유사 제품군 대비 평가
6. **구매 추천** - 추천 점수 및 적합 고객

## 지원 플랫폼

- **네이버 스마트스토어** (`smartstore.naver.com`)

## 제한사항

- 상세페이지가 이미지로만 구성된 경우 분석 가능
- 최대 10개 이미지 분석 (API 비용 최적화)
- 동영상 콘텐츠는 분석 불가
- 로그인이 필요한 페이지는 접근 불가

## 파일 구조

```
product-analyzer/
├── SKILL.md                              # 이 문서
├── scripts/
│   ├── crawl_smartstore.py               # 크롤링 스크립트
│   └── build_product_report.py           # 빌드 스크립트
├── references/
│   └── prompts/
│       └── product-analysis.md           # 분석 프롬프트
├── report/                               # 생성된 리포트
└── Product Report Template/              # React 템플릿
```
