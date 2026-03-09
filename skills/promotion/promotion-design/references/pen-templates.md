# 채널별 .pen 디자인 템플릿

> 각 채널/포맷에 대한 batch_design 오퍼레이션 패턴
> 변수: `{HEADLINE}`, `{SUBTEXT}`, `{CTA}`, `{PERIOD}`, `{OFFER}`, `{PRODUCT_NAME}`, `{PRICE}`, `{DISCOUNT_PRICE}`

---

## 1. 인스타그램 스토리 (1080 x 1920)

```
// 캔버스 설정
frame=I("root", { tag:"div", w:1080, h:1920, bg:"#F5E6D3", layout:"column", position:"relative" })

// 상단 여백 + 브랜드
top=I(frame, { tag:"div", h:120, layout:"row", px:40, alignItems:"center", justifyContent:"center" })
brand=I(top, { tag:"span", text:"SUNDAYHUG", fontSize:16, fontWeight:"bold", color:"#8B7355", letterSpacing:2 })

// 메인 비주얼 영역 (제품 이미지)
visual=I(frame, { tag:"div", w:1080, h:900, bg:"#FAFAF7" })
// → 제품 이미지 삽입: G(visual, "ai", "...") 또는 사용자 이미지

// 프로모션 뱃지
badge=I(frame, { tag:"div", bg:"#D4534A", px:24, py:10, cornerRadius:20, alignSelf:"center", mt:-30, zIndex:10 })
I(badge, { tag:"span", text:"{OFFER}", fontSize:18, fontWeight:"bold", color:"#FFFFFF" })

// 텍스트 영역
textArea=I(frame, { tag:"div", flex:1, layout:"column", px:48, py:40, gap:16, alignItems:"center", justifyContent:"center" })
I(textArea, { tag:"h1", text:"{HEADLINE}", fontSize:40, fontWeight:"bold", color:"#8B7355", textAlign:"center" })
I(textArea, { tag:"p", text:"{SUBTEXT}", fontSize:18, color:"#666666", textAlign:"center" })
I(textArea, { tag:"p", text:"{PERIOD}", fontSize:14, color:"#999999" })

// CTA 영역
cta=I(frame, { tag:"div", h:180, layout:"column", alignItems:"center", justifyContent:"center", gap:12 })
ctaBtn=I(cta, { tag:"div", bg:"#8B7355", px:48, py:16, cornerRadius:8 })
I(ctaBtn, { tag:"span", text:"{CTA}", fontSize:18, fontWeight:"bold", color:"#FFFFFF" })
I(cta, { tag:"span", text:"↑ 스와이프하여 확인하기", fontSize:12, color:"#999999" })
```

---

## 2. 인스타그램 피드 (1080 x 1350)

```
frame=I("root", { tag:"div", w:1080, h:1350, bg:"#FAFAF7", layout:"column" })

// 상단 프로모션 정보
header=I(frame, { tag:"div", h:160, bg:"#F5E6D3", layout:"column", px:48, justifyContent:"center", gap:8 })
I(header, { tag:"span", text:"SUNDAYHUG", fontSize:12, fontWeight:"bold", color:"#8B7355", letterSpacing:2 })
I(header, { tag:"h1", text:"{HEADLINE}", fontSize:36, fontWeight:"bold", color:"#8B7355" })
I(header, { tag:"p", text:"{SUBTEXT}", fontSize:16, color:"#666666" })

// 비주얼 영역
visual=I(frame, { tag:"div", w:1080, h:700, bg:"#F5E6D3" })
// → 제품 이미지

// 혜택 영역
offer=I(frame, { tag:"div", flex:1, layout:"column", px:48, py:32, gap:16, alignItems:"center", justifyContent:"center" })
badge=I(offer, { tag:"div", bg:"#D4534A", px:20, py:8, cornerRadius:16 })
I(badge, { tag:"span", text:"{OFFER}", fontSize:16, fontWeight:"bold", color:"#FFFFFF" })
I(offer, { tag:"p", text:"{PERIOD}", fontSize:14, color:"#999999" })

// 하단 CTA
bottom=I(frame, { tag:"div", h:100, bg:"#8B7355", layout:"row", alignItems:"center", justifyContent:"center" })
I(bottom, { tag:"span", text:"{CTA}", fontSize:20, fontWeight:"bold", color:"#FFFFFF" })
```

---

## 3. 네이버 모바일 배너 (750 x 1308)

```
frame=I("root", { tag:"div", w:750, h:1308, bg:"#F5E6D3", layout:"column" })

// 브랜드 + 프로모션 타입
top=I(frame, { tag:"div", h:80, layout:"row", px:32, alignItems:"center", justifyContent:"space-between" })
I(top, { tag:"span", text:"SUNDAYHUG", fontSize:14, fontWeight:"bold", color:"#8B7355" })
typeBadge=I(top, { tag:"div", bg:"#D4534A", px:12, py:4, cornerRadius:12 })
I(typeBadge, { tag:"span", text:"{OFFER}", fontSize:12, fontWeight:"bold", color:"#FFFFFF" })

// 메인 카피
titleArea=I(frame, { tag:"div", px:32, py:20, layout:"column", gap:8 })
I(titleArea, { tag:"h1", text:"{HEADLINE}", fontSize:32, fontWeight:"bold", color:"#8B7355" })
I(titleArea, { tag:"p", text:"{SUBTEXT}", fontSize:16, color:"#666666" })

// 비주얼 (제품)
visual=I(frame, { tag:"div", flex:1, mx:32, cornerRadius:12, bg:"#FAFAF7" })
// → 제품 이미지

// 기간 + CTA
bottom=I(frame, { tag:"div", h:140, layout:"column", px:32, py:24, gap:12, alignItems:"center" })
I(bottom, { tag:"p", text:"{PERIOD}", fontSize:14, color:"#999999" })
ctaBtn=I(bottom, { tag:"div", bg:"#8B7355", px:40, py:14, cornerRadius:8, w:"100%" , alignItems:"center" })
I(ctaBtn, { tag:"span", text:"{CTA}", fontSize:16, fontWeight:"bold", color:"#FFFFFF" })
```

---

## 4. 네이버 PC 배너 (1920 x 860)

```
frame=I("root", { tag:"div", w:1920, h:860, bg:"#F5E6D3", layout:"row" })

// 좌측: 텍스트 영역
left=I(frame, { tag:"div", w:860, h:860, layout:"column", px:80, justifyContent:"center", gap:20 })
I(left, { tag:"span", text:"SUNDAYHUG", fontSize:14, fontWeight:"bold", color:"#8B7355", letterSpacing:2, opacity:0.6 })
badge=I(left, { tag:"div", bg:"#D4534A", px:16, py:6, cornerRadius:16, alignSelf:"flex-start" })
I(badge, { tag:"span", text:"{OFFER}", fontSize:14, fontWeight:"bold", color:"#FFFFFF" })
I(left, { tag:"h1", text:"{HEADLINE}", fontSize:48, fontWeight:"bold", color:"#8B7355" })
I(left, { tag:"p", text:"{SUBTEXT}", fontSize:18, color:"#666666" })
I(left, { tag:"p", text:"{PERIOD}", fontSize:14, color:"#999999" })
ctaBtn=I(left, { tag:"div", bg:"#8B7355", px:36, py:14, cornerRadius:8, alignSelf:"flex-start", mt:8 })
I(ctaBtn, { tag:"span", text:"{CTA}", fontSize:16, fontWeight:"bold", color:"#FFFFFF" })

// 우측: 비주얼 영역
right=I(frame, { tag:"div", w:1060, h:860, bg:"#FAFAF7", position:"relative" })
// → 제품 이미지
```

---

## 5. 카카오톡 리스트형 (400 x 400)

```
frame=I("root", { tag:"div", w:400, h:400, bg:"#FFFFFF", layout:"column", cornerRadius:0 })

// 비주얼 (상단 60%)
visual=I(frame, { tag:"div", w:400, h:240, bg:"#F5E6D3", position:"relative" })
// → 제품 이미지
badge=I(visual, { tag:"div", bg:"#D4534A", px:10, py:4, cornerRadius:10, position:"absolute", top:12, left:12 })
I(badge, { tag:"span", text:"{OFFER}", fontSize:11, fontWeight:"bold", color:"#FFFFFF" })

// 텍스트 (하단 40%)
textArea=I(frame, { tag:"div", flex:1, layout:"column", px:16, py:12, gap:6, justifyContent:"center" })
I(textArea, { tag:"span", text:"{PRODUCT_NAME}", fontSize:14, fontWeight:"bold", color:"#333333" })
priceRow=I(textArea, { tag:"div", layout:"row", gap:8, alignItems:"center" })
I(priceRow, { tag:"span", text:"{PRICE}", fontSize:12, color:"#999999", textDecoration:"line-through" })
I(priceRow, { tag:"span", text:"{DISCOUNT_PRICE}", fontSize:16, fontWeight:"bold", color:"#D4534A" })
```

---

## 6. 자사몰 모바일 배너 (720 x 950)

```
frame=I("root", { tag:"div", w:720, h:950, bg:"#F5E6D3", layout:"column" })

// 상단 브랜드
top=I(frame, { tag:"div", h:60, layout:"row", px:32, alignItems:"center" })
I(top, { tag:"span", text:"SUNDAYHUG", fontSize:12, fontWeight:"bold", color:"#8B7355", letterSpacing:2 })

// 카피 영역
titleArea=I(frame, { tag:"div", px:32, py:16, layout:"column", gap:8 })
I(titleArea, { tag:"h1", text:"{HEADLINE}", fontSize:28, fontWeight:"bold", color:"#8B7355" })
I(titleArea, { tag:"p", text:"{SUBTEXT}", fontSize:14, color:"#666666" })

// 비주얼
visual=I(frame, { tag:"div", flex:1, mx:24, my:12, cornerRadius:12, bg:"#FAFAF7" })
// → 제품 이미지

// 하단 혜택 + CTA
bottom=I(frame, { tag:"div", h:160, layout:"column", px:32, py:20, gap:12, alignItems:"center" })
badge=I(bottom, { tag:"div", bg:"#D4534A", px:16, py:6, cornerRadius:16 })
I(badge, { tag:"span", text:"{OFFER}", fontSize:14, fontWeight:"bold", color:"#FFFFFF" })
I(bottom, { tag:"p", text:"{PERIOD}", fontSize:12, color:"#999999" })
ctaBtn=I(bottom, { tag:"div", bg:"#8B7355", px:36, py:12, cornerRadius:8 })
I(ctaBtn, { tag:"span", text:"{CTA}", fontSize:14, fontWeight:"bold", color:"#FFFFFF" })
```

---

## 7. 자사몰 PC 배너 (1920 x 860)

```
frame=I("root", { tag:"div", w:1920, h:860, bg:"#FAFAF7", layout:"row" })

// 좌측 비주얼
left=I(frame, { tag:"div", w:960, h:860, bg:"#F5E6D3" })
// → 제품 라이프스타일 이미지

// 우측 텍스트
right=I(frame, { tag:"div", w:960, h:860, layout:"column", px:80, justifyContent:"center", gap:20 })
I(right, { tag:"span", text:"SUNDAYHUG", fontSize:14, fontWeight:"bold", color:"#8B7355", letterSpacing:2, opacity:0.6 })
I(right, { tag:"h1", text:"{HEADLINE}", fontSize:44, fontWeight:"bold", color:"#8B7355" })
I(right, { tag:"p", text:"{SUBTEXT}", fontSize:18, color:"#666666" })
divider=I(right, { tag:"div", w:60, h:2, bg:"#8B7355", opacity:0.3 })
badge=I(right, { tag:"div", bg:"#D4534A", px:16, py:6, cornerRadius:16, alignSelf:"flex-start" })
I(badge, { tag:"span", text:"{OFFER}", fontSize:14, fontWeight:"bold", color:"#FFFFFF" })
I(right, { tag:"p", text:"{PERIOD}", fontSize:14, color:"#999999" })
ctaBtn=I(right, { tag:"div", bg:"#8B7355", px:36, py:14, cornerRadius:8, alignSelf:"flex-start" })
I(ctaBtn, { tag:"span", text:"{CTA}", fontSize:16, fontWeight:"bold", color:"#FFFFFF" })
```

---

## 8. 카카오톡 캐로셀 (1080 x 1350)

```
frame=I("root", { tag:"div", w:1080, h:1350, bg:"#FAFAF7", layout:"column" })

// 상단 배경 + 카피
header=I(frame, { tag:"div", h:280, bg:"#F5E6D3", layout:"column", px:48, justifyContent:"center", gap:12 })
I(header, { tag:"span", text:"SUNDAYHUG", fontSize:12, fontWeight:"bold", color:"#8B7355", letterSpacing:2 })
I(header, { tag:"h1", text:"{HEADLINE}", fontSize:36, fontWeight:"bold", color:"#8B7355" })
I(header, { tag:"p", text:"{PERIOD}", fontSize:14, color:"#999999" })

// 제품 비주얼 (메인)
visual=I(frame, { tag:"div", flex:1, mx:40, my:20, cornerRadius:12, bg:"#FFFFFF" })
// → 제품 이미지

// 하단 정보
bottom=I(frame, { tag:"div", h:200, layout:"column", px:48, py:24, gap:12 })
I(bottom, { tag:"span", text:"{PRODUCT_NAME}", fontSize:20, fontWeight:"bold", color:"#333333" })
I(bottom, { tag:"p", text:"{SUBTEXT}", fontSize:14, color:"#666666" })
priceRow=I(bottom, { tag:"div", layout:"row", gap:12, alignItems:"center" })
I(priceRow, { tag:"span", text:"{PRICE}", fontSize:16, color:"#999999", textDecoration:"line-through" })
I(priceRow, { tag:"span", text:"{DISCOUNT_PRICE}", fontSize:24, fontWeight:"bold", color:"#D4534A" })
badge=I(bottom, { tag:"div", bg:"#D4534A", px:14, py:6, cornerRadius:12, alignSelf:"flex-start" })
I(badge, { tag:"span", text:"{OFFER}", fontSize:12, fontWeight:"bold", color:"#FFFFFF" })
```

---

## 변수 치환 규칙

| 변수 | 소스 (JSON) | 예시 |
|------|------------|------|
| `{HEADLINE}` | `promotion_name` 또는 커스텀 카피 | "봄 슬리핑백 특가" |
| `{SUBTEXT}` | `concept` 또는 `key_message` | "우리 아기 첫 봄잠을 위한 특별 할인" |
| `{CTA}` | 채널별 기본값 또는 커스텀 | "지금 바로 구매하기" |
| `{PERIOD}` | `period.start` ~ `period.end` | "3.1(금) - 3.15(토)" |
| `{OFFER}` | `offer.value` + `offer.type` | "20% OFF" |
| `{PRODUCT_NAME}` | `products[n].name` | "코지 슬리핑백" |
| `{PRICE}` | `products[n].price` (포맷팅) | "89,000원" |
| `{DISCOUNT_PRICE}` | `products[n].discount_price` | "71,200원" |

### 채널별 기본 CTA

| 채널 | 기본 CTA |
|------|---------|
| 인스타그램 스토리 | "스와이프하여 확인하기" |
| 인스타그램 피드 | "프로필 링크에서 확인하기" |
| 네이버 | "지금 바로 구매하기" |
| 자사몰 | "특가 상품 보러가기" |
| 카카오톡 | "자세히 보기" |
| 라이브 | "라이브 혜택 확인" |
