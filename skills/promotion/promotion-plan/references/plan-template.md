# 프로모션 기획서 템플릿

## .pen 기획서 레이아웃 (1680 x 1188)

캔버스 사이즈: **1680 x 1188px** (A4 가로 비율)

### 구조

```
┌──────────────────────────────────────────────────┐
│ [Header] 56px                                    │
│  SUNDAYHUG 로고 | "프로모션 기획서" | 날짜        │
├──────────────────────────────────────────────────┤
│ [Hero Section] 200px                             │
│  프로모션명 (48-64px bold)                       │
│  한줄 컨셉 (18px)                                │
│  배경: #F5E6D3 (썬데이 베이지)                   │
├────────────────────┬─────────────────────────────┤
│ [Left Column]      │ [Right Column]              │
│ 780px              │ 780px                        │
│                    │                              │
│ ┌────────────────┐ │ ┌─────────────────────────┐ │
│ │ 기본정보       │ │ │ 핵심 메시지             │ │
│ │ - 기간         │ │ │ (인용 스타일 박스)       │ │
│ │ - 타겟         │ │ │ 큰 따옴표 + 메시지      │ │
│ │ - 목적         │ │ └─────────────────────────┘ │
│ │ - 톤앤매너     │ │                              │
│ └────────────────┘ │ ┌─────────────────────────┐ │
│                    │ │ 대상 제품               │ │
│ ┌────────────────┐ │ │ - 제품명 + 이미지       │ │
│ │ 혜택 구성      │ │ │ - 가격/할인 정보        │ │
│ │ - 할인율       │ │ └─────────────────────────┘ │
│ │ - 사은품       │ │                              │
│ │ - 쿠폰 등     │ │ ┌─────────────────────────┐ │
│ └────────────────┘ │ │ 산출물 목록             │ │
│                    │ │ - 채널별 디자인 리스트   │ │
│ ┌────────────────┐ │ │ - 체크박스 형태         │ │
│ │ 채널 계획      │ │ └─────────────────────────┘ │
│ │ - 채널 태그    │ │                              │
│ │ - 포맷 정보    │ │                              │
│ └────────────────┘ │                              │
├────────────────────┴─────────────────────────────┤
│ [Footer] 48px                                    │
│  "확정 후 /promotion-design 실행" | 상태: 기획중 │
└──────────────────────────────────────────────────┘
```

### 스타일 가이드

| 요소 | 스타일 |
|------|--------|
| 배경 | `#FAFAF7` (크림) |
| 헤더 배경 | `#8B7355` (허그 브라운) |
| 히어로 배경 | `#F5E6D3` (썬데이 베이지) |
| 프로모션명 | 48-64px, bold, `#8B7355` |
| 섹션 제목 | 20px, bold, `#8B7355` |
| 본문 | 14-16px, `#666666` |
| 인용 박스 | `#F5E6D3` 배경, 좌측 4px `#8B7355` 보더 |
| 카드 | `#FFFFFF` 배경, cornerRadius 12px, 미세 그림자 |
| 태그 | `#F5E6D3` 배경, cornerRadius 16px, 12px 패딩 |
| Footer | `#E8E4DE` 배경 |

### batch_design 골격

```
// Header
header=I("root", { tag:"div", w:1680, h:56, bg:"#8B7355", layout:"row", px:40, alignItems:"center", justifyContent:"space-between" })
logo=I(header, { tag:"span", text:"SUNDAYHUG", fontSize:18, fontWeight:"bold", color:"#FFFFFF" })
title=I(header, { tag:"span", text:"프로모션 기획서", fontSize:14, color:"#FFFFFF" })
date=I(header, { tag:"span", text:"{DATE}", fontSize:12, color:"#FFFFFF", opacity:0.8 })

// Hero
hero=I("root", { tag:"div", w:1680, h:200, bg:"#F5E6D3", layout:"column", alignItems:"center", justifyContent:"center", gap:12 })
promoName=I(hero, { tag:"h1", text:"{PROMO_NAME}", fontSize:56, fontWeight:"bold", color:"#8B7355" })
concept=I(hero, { tag:"p", text:"{CONCEPT}", fontSize:18, color:"#8B7355", opacity:0.7 })

// Body (2 columns)
body=I("root", { tag:"div", w:1680, h:844, layout:"row", px:40, py:32, gap:40, bg:"#FAFAF7" })

// Left Column
left=I(body, { tag:"div", flex:1, layout:"column", gap:24 })
// ... 기본정보, 혜택, 채널 카드들

// Right Column
right=I(body, { tag:"div", flex:1, layout:"column", gap:24 })
// ... 핵심메시지, 제품, 산출물 카드들

// Footer
footer=I("root", { tag:"div", w:1680, h:48, bg:"#E8E4DE", layout:"row", px:40, alignItems:"center", justifyContent:"space-between" })
```

---

## .json 데이터 스키마

기획서와 함께 저장되는 구조화된 플랜 데이터:

```json
{
  "version": "1.0",
  "created_at": "2025-02-20T10:00:00Z",
  "updated_at": "2025-02-20T10:00:00Z",
  "status": "confirmed",

  "promotion_name": "봄 슬리핑백 특가",
  "slug": "spring-sleeping-bag-sale",
  "concept": "봄맞이 슬리핑백 전 라인업 20% 특가",
  "tone_manner": "따뜻하고 설레는 봄 느낌, 밝고 경쾌한 톤",
  "intent": "매출",
  "target_audience": "0-12개월 아기를 둔 신규 부모",
  "period": {
    "start": "2025-03-01",
    "end": "2025-03-15"
  },
  "key_message": "우리 아기 첫 봄잠, 썬데이허그 슬리핑백과 함께",

  "products": [
    {
      "name": "코지 슬리핑백",
      "price": 89000,
      "discount_price": 71200,
      "image": ""
    }
  ],

  "offer": {
    "type": "discount",
    "value": "20%",
    "description": "슬리핑백 전 라인업 20% 할인",
    "additional": "5만원 이상 무료배송"
  },

  "channels": ["인스타그램", "네이버", "자사몰", "카카오톡"],

  "deliverables": [
    {
      "channel": "인스타그램",
      "format": "스토리",
      "size": "1080x1920",
      "quantity": 1,
      "reference": "인스타그램/스토리/프로모션 스토리 1.png"
    },
    {
      "channel": "네이버",
      "format": "PC 배너",
      "size": "1920x860",
      "quantity": 1,
      "reference": "네이버 배너/피씨/pc_메인배너.png"
    }
  ],

  "project_dir": "{{WORKSPACE_DIR}}/output/spring-sleeping-bag-sale/",
  "pen_file": "{{WORKSPACE_DIR}}/output/spring-sleeping-bag-sale/plan.pen",
  "json_file": "{{WORKSPACE_DIR}}/output/spring-sleeping-bag-sale/plan.json"
}
```

### 필수 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `promotion_name` | string | 프로모션 이름 (한글) |
| `slug` | string | 파일명용 영문 슬러그 |
| `concept` | string | 한줄 컨셉 |
| `tone_manner` | string | 톤앤매너 |
| `intent` | string | 목적 (매출/인지도/재구매/신규유입) |
| `target_audience` | string | 타겟 고객 |
| `period` | object | 시작/종료일 |
| `key_message` | string | 핵심 메시지 |
| `products` | array | 대상 제품 목록 |
| `offer` | object | 혜택 구성 |
| `channels` | array | 사용 채널 목록 |
| `deliverables` | array | 예상 산출물 |

### 선택 필드

| 필드 | 타입 | 설명 |
|------|------|------|
| `hashtags` | array | 관련 해시태그 |
| `cta` | string | CTA 문구 |
| `notes` | string | 추가 메모 |
| `material_paths` | array | 사용자 제공 소재 경로 |
