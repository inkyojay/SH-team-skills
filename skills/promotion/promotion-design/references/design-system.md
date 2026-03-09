# 썬데이허그 .pen 디자인 시스템

> 모든 프로모션 디자인 산출물에 적용되는 브랜드 디자인 시스템

## 브랜드 컬러

### Primary
| 이름 | HEX | 용도 |
|------|-----|------|
| 썬데이 베이지 | `#F5E6D3` | 주 배경, 강조 영역, 태그 |
| 허그 브라운 | `#8B7355` | 헤드라인, 아이콘, 액센트 |

### Secondary
| 이름 | HEX | 용도 |
|------|-----|------|
| 크림 | `#FAFAF7` | 전체 배경, 카드 내부 |
| 소프트 그레이 | `#E8E4DE` | 구분선, 비활성, footer |
| 웜 화이트 | `#FFFFFF` | 카드 배경, 텍스트 영역 |

### Text
| 이름 | HEX | 용도 |
|------|-----|------|
| 딥 브라운 | `#8B7355` | 헤드라인, 강조 텍스트 |
| 다크 그레이 | `#333333` | 제목, 중요 본문 |
| 미디엄 그레이 | `#666666` | 일반 본문 |
| 라이트 그레이 | `#999999` | 보조 텍스트, 캡션 |

### Accent (프로모션용)
| 이름 | HEX | 용도 |
|------|-----|------|
| 세일 레드 | `#D4534A` | 할인 강조, SALE 태그 |
| 소프트 핑크 | `#F2D4C4` | 포인트 배경, 하이라이트 |
| 미스티 그린 | `#C5D5C5` | 봄/자연 테마 포인트 |

---

## 타이포그래피

### 헤드라인 (H1)
```json
{ "fontSize": 48, "fontWeight": "bold", "color": "#8B7355", "letterSpacing": -0.5 }
```
- 사용: 프로모션명, 메인 카피
- 범위: 36-64px (캔버스 크기에 따라)

### 서브 헤드라인 (H2)
```json
{ "fontSize": 28, "fontWeight": "bold", "color": "#333333" }
```
- 사용: 섹션 제목, 보조 카피

### 본문 (Body)
```json
{ "fontSize": 16, "fontWeight": "normal", "color": "#666666", "lineHeight": 1.6 }
```
- 사용: 설명 텍스트, 상세 정보
- 범위: 14-18px

### 캡션 (Caption)
```json
{ "fontSize": 12, "fontWeight": "normal", "color": "#999999" }
```
- 사용: 부가 정보, 유의사항

### CTA 텍스트
```json
{ "fontSize": 16, "fontWeight": "bold", "color": "#FFFFFF" }
```
- 사용: 버튼 내 텍스트

### 할인 가격
```json
{ "fontSize": 32, "fontWeight": "bold", "color": "#D4534A" }
```
- 사용: 할인율, 할인 가격

---

## 레이아웃 원칙

### 여백 (Padding)
- **외부 여백**: 40-60px (캔버스 대비 충분한 여백)
- **섹션 간 여백**: 24-32px
- **카드 내부 패딩**: 20-24px
- **요소 간 간격**: 8-16px

### 정렬
- **텍스트**: 좌측 정렬 기본, 중앙 정렬은 히어로/CTA에만
- **이미지**: 중앙 정렬, 또는 텍스트와 좌우 배치
- **카드**: 그리드 정렬, 균등 간격

### Corner Radius
| 요소 | radius |
|------|--------|
| 카드 | 12-16px |
| 버튼 | 8-12px |
| 태그/뱃지 | 16-20px (pill) |
| 이미지 | 8-12px |
| 전체 프레임 | 0px (모서리 직각) |

### 그림자
```json
{ "shadowColor": "rgba(0,0,0,0.06)", "shadowOffsetX": 0, "shadowOffsetY": 2, "shadowBlur": 8 }
```
- 카드와 버튼에만 가볍게 적용
- 과도한 그림자 지양

---

## 컴포넌트 패턴

### 프로모션 뱃지
```
I(parent, { tag:"div", bg:"#D4534A", px:16, py:6, cornerRadius:16 })
I(badge, { tag:"span", text:"20% OFF", fontSize:14, fontWeight:"bold", color:"#FFFFFF" })
```

### 제품 카드
```
I(parent, { tag:"div", bg:"#FFFFFF", cornerRadius:12, p:16, layout:"column", gap:12, shadow:true })
// 제품 이미지 (사용자 제공 또는 G()로 생성)
I(card, { tag:"div", w:"100%", aspectRatio:1, cornerRadius:8, bg:"#F5E6D3" })
I(card, { tag:"span", text:"{PRODUCT_NAME}", fontSize:16, fontWeight:"bold", color:"#333333" })
I(card, { tag:"span", text:"{PRICE}", fontSize:14, color:"#999999", textDecoration:"line-through" })
I(card, { tag:"span", text:"{DISCOUNT_PRICE}", fontSize:20, fontWeight:"bold", color:"#D4534A" })
```

### CTA 버튼
```
I(parent, { tag:"div", bg:"#8B7355", px:32, py:14, cornerRadius:8, alignSelf:"center" })
I(btn, { tag:"span", text:"{CTA_TEXT}", fontSize:16, fontWeight:"bold", color:"#FFFFFF" })
```

### 정보 행 (라벨 + 값)
```
I(parent, { tag:"div", layout:"row", gap:8, alignItems:"center" })
I(row, { tag:"span", text:"{LABEL}", fontSize:14, color:"#999999", w:80 })
I(row, { tag:"span", text:"{VALUE}", fontSize:14, color:"#333333" })
```

### 인용 박스 (핵심 메시지)
```
I(parent, { tag:"div", bg:"#F5E6D3", p:24, cornerRadius:12, borderLeft:"4px solid #8B7355" })
I(quote, { tag:"span", text:""", fontSize:48, color:"#8B7355", opacity:0.3 })
I(quote, { tag:"p", text:"{MESSAGE}", fontSize:20, color:"#8B7355", fontWeight:"medium" })
```

### 채널 태그
```
I(parent, { tag:"div", bg:"#F5E6D3", px:12, py:6, cornerRadius:16 })
I(tag, { tag:"span", text:"{CHANNEL}", fontSize:12, color:"#8B7355" })
```

---

## 이미지 처리 규칙

1. **사용자 제공 이미지 우선**: `material_paths`에 경로가 있으면 해당 이미지 사용
2. **레퍼런스 이미지 참고**: 레이아웃과 스타일을 참고하되, 그대로 복사하지 않음
3. **AI 생성 (G() 오퍼레이션)**: 이미지가 없는 경우 G()로 생성
   - 프롬프트에 브랜드 톤 반영: "warm, soft, natural, baby care"
   - 스타일: "minimal, clean, warm beige tones"
4. **이미지 비율**: 원본 비율 유지, 필요시 crop

---

## 금지 사항

- 원색(빨강, 파랑, 초록) 대면적 사용 금지
- 과도한 그라디언트 금지
- 3종 이상의 폰트 사이즈 혼재 금지 (H1, H2, Body, Caption 4단계로 제한)
- 5px 이하의 작은 텍스트 금지
- 검정(#000000) 배경 금지
- 형광색/네온 컬러 사용 금지
