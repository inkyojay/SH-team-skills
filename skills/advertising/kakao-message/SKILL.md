---
name: kakao-message
description: 카카오톡 메시지 배너 제작. 이미지형/캐러셀형/리스트형 등 다양한 카카오 비즈메시지용 배너 템플릿을 제공합니다. "카카오 메시지 배너", "카톡 배너", "비즈메시지 이미지" 요청 시 사용.
triggers:
  - "카카오 메시지 배너"
  - "카톡 배너"
  - "비즈메시지"
  - "카카오 광고"
---

# Kakao Message Banner Creator

카카오톡 비즈메시지용 배너 템플릿 모음입니다.

## 사전 요구사항

```bash
pip install playwright
playwright install chromium
```

## 메시지 유형별 스펙

| 유형 | 사이즈 | 비율 | 용도 |
|------|--------|------|------|
| 와이드 이미지형 | 800×600 | 4:3 | 단일 상품/이벤트 홍보 |
| 캐러셀 피드형 | 800×400 | 2:1 | 슬라이드 카드 |
| 캐러셀 커머스 인트로 | 800×1100 | 8:11 | 캐러셀 첫 장 |
| 캐러셀 커머스 아이템 | 800×800 | 1:1 | 상품 상세 카드 |
| 리스트형 | 800×400 | 2:1 | 다중 상품 나열 |

---

## 와이드 이미지형 템플릿 (800×600)

### 1. 프로모션 세일 (wide-promo-sale.html)

빨강-주황 그라데이션의 강렬한 세일 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{BADGE_TEXT}}` | 상단 뱃지 | MEGA SALE |
| `{{DISCOUNT}}` | 할인율 숫자 | 50 |
| `{{TITLE}}` | 메인 타이틀 | 전 상품 특가 |
| `{{SUBTITLE}}` | 서브 타이틀 | 겨울 시즌 한정 |
| `{{PERIOD}}` | 기간 | 1/20 ~ 1/31 |
| `{{PRODUCT_IMAGE}}` | 제품 이미지 | ./product.png |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 지금 쇼핑하기 |

**레이아웃:**
```
┌────────────────────────────────────┐
│ [MEGA SALE]                        │
│                                    │
│  50%        ┌──────────┐           │
│  전 상품 특가 │          │           │
│  겨울 시즌   │  제품    │           │
│  ─────────  │  이미지  │           │
│  1/20~1/31  │          │           │
│             └──────────┘           │
│       [지금 쇼핑하기]               │
└────────────────────────────────────┘
```

### 2. 신상품 프리미엄 (wide-new-product.html)

다크 배경의 프리미엄 신상품 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{BADGE_TEXT}}` | 상단 뱃지 | NEW ARRIVAL |
| `{{TITLE}}` | 메인 타이틀 | 2025 신상품 |
| `{{SUBTITLE}}` | 서브 타이틀 | 한정 수량 특가 |
| `{{FEATURE_1~3}}` | 특징 3개 | 프리미엄 소재 |
| `{{PRODUCT_IMAGE}}` | 제품 이미지 | ./product.png |
| `{{PRICE}}` | 가격 | 89,000 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 자세히 보기 |

### 3. 쿠폰 이벤트 (wide-coupon-event.html)

카카오 옐로우 컬러의 쿠폰 증정 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{BADGE_TEXT}}` | 상단 뱃지 | 한정 쿠폰 |
| `{{TITLE_1}}` | 타이틀 1줄 | 지금 가입하면 |
| `{{TITLE_2}}` | 타이틀 2줄 | 즉시 사용 쿠폰 증정! |
| `{{COUPON_VALUE}}` | 쿠폰 금액 | 5,000 |
| `{{COUPON_DESC}}` | 쿠폰 조건 | 3만원 이상 구매 시 |
| `{{COUPON_EXPIRE}}` | 유효기간 | ~1/31까지 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 쿠폰 받기 |

### 4. 미니멀 클린 (wide-minimal.html)

깔끔한 화이트 미니멀 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{BRAND_NAME}}` | 브랜드명 | BRAND NAME |
| `{{TITLE}}` | 메인 타이틀 | 시그니처 컬렉션 |
| `{{SUBTITLE}}` | 서브 타이틀 | 새로운 시작을 위한 |
| `{{PRODUCT_IMAGE}}` | 제품 이미지 | ./product.png |
| `{{CTA_TEXT}}` | 버튼 텍스트 | SHOP NOW |

### 5. 감성 라이프스타일 (wide-emotional.html)

나눔명조 폰트의 감성적인 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{TITLE}}` | 메인 타이틀 | 일상에 스며드는 |
| `{{SUBTITLE}}` | 서브 타이틀 | 따뜻한 위로 |
| `{{DESCRIPTION}}` | 설명 텍스트 | 당신의 하루를... |
| `{{PRODUCT_IMAGE}}` | 배경 이미지 | ./lifestyle.jpg |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 더 알아보기 |

### 6. 글래스모피즘 그라데이션 (wide-gradient.html)

보라색 그라데이션의 트렌디한 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{BADGE_TEXT}}` | 상단 뱃지 | EVENT |
| `{{TITLE}}` | 메인 타이틀 | 특별한 혜택 |
| `{{SUBTITLE}}` | 서브 타이틀 | 오직 오늘만 |
| `{{BENEFIT_1~3}}` | 혜택 3개 | 무료 배송 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 혜택 받기 |

### 7. 고객 리뷰 (wide-review.html)

베스트 리뷰 강조 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{REVIEW_IMAGE}}` | 리뷰 이미지 | ./review.jpg |
| `{{REVIEW_TEXT}}` | 리뷰 내용 | 정말 좋아요! |
| `{{REVIEWER_NAME}}` | 리뷰어 이름 | 김**님 |
| `{{REVIEW_DATE}}` | 리뷰 날짜 | 2025.01.15 |
| `{{PRODUCT_THUMB}}` | 제품 썸네일 | ./thumb.png |
| `{{PRODUCT_NAME}}` | 제품명 | 시그니처 블랭킷 |
| `{{SALE_PRICE}}` | 할인가 | 39,000 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 상품 보러가기 |

---

## 캐러셀형 템플릿

### 8. 캐러셀 피드 (carousel-feed.html) - 800×400

이미지+정보 분할 레이아웃의 피드 카드.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{PRODUCT_IMAGE}}` | 제품 이미지 | ./product.jpg |
| `{{BADGE_TEXT}}` | 뱃지 텍스트 | BEST |
| `{{BRAND_NAME}}` | 브랜드명 | BRAND |
| `{{TITLE}}` | 제품명 | 시그니처 아이템 |
| `{{DESCRIPTION}}` | 설명 | 프리미엄 품질의... |
| `{{DISCOUNT}}` | 할인율 | 30 |
| `{{SALE_PRICE}}` | 할인가 | 69,000 |
| `{{ORIGINAL_PRICE}}` | 원가 | 99,000 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 구매하기 |

### 9. 캐러셀 커머스 인트로 (carousel-commerce-intro.html) - 800×1100

캐러셀 첫 장용 인트로 페이지.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{BADGE_TEXT}}` | 이벤트 뱃지 | 단독 특가 |
| `{{TITLE_LINE_1}}` | 타이틀 1줄 | 올해의 베스트 |
| `{{TITLE_LINE_2}}` | 타이틀 2줄 | 최대 50% 할인 |
| `{{SUBTITLE}}` | 서브 타이틀 | 지금 놓치면 후회해요 |
| `{{MAIN_IMAGE}}` | 메인 이미지 | ./main.png |
| `{{BENEFIT_ICON_1~3}}` | 혜택 아이콘 | 🚚 |
| `{{BENEFIT_TEXT_1~3}}` | 혜택 텍스트 | 무료배송 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 상품 보러가기 |

### 10. 캐러셀 커머스 아이템 (carousel-commerce-item.html) - 800×800

개별 상품 상세 카드.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{PRODUCT_IMAGE}}` | 제품 이미지 | ./product.png |
| `{{DISCOUNT}}` | 할인율 | 30 |
| `{{BRAND_NAME}}` | 브랜드명 | BRAND |
| `{{PRODUCT_NAME}}` | 제품명 | 프리미엄 블랭킷 |
| `{{PRODUCT_DESC}}` | 제품 설명 | 부드러운 촉감의... |
| `{{REVIEW_COUNT}}` | 리뷰 수 | 1,234 |
| `{{SALE_PRICE}}` | 할인가 | 69,000 |
| `{{ORIGINAL_PRICE}}` | 원가 | 99,000 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 구매하기 |

---

## 리스트형 템플릿

### 11. 리스트 아이템 (list-item.html) - 800×400

4개 상품 그리드 레이아웃.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{LIST_TITLE}}` | 리스트 제목 | 이번 주 베스트 |
| `{{ITEM_IMAGE_1~4}}` | 상품 이미지 | ./item1.png |
| `{{ITEM_BADGE_1~4}}` | 상품 뱃지 | BEST |
| `{{ITEM_NAME_1~4}}` | 상품명 | 시그니처 블랭킷 |
| `{{ITEM_DISCOUNT_1~4}}` | 할인율 | 30 |
| `{{ITEM_PRICE_1~4}}` | 가격 | 39,000 |

**레이아웃:**
```
┌────────────────────────────────────┐
│ 이번 주 베스트            전체보기 > │
├────────────────────────────────────┤
│ ┌────┐  ┌────┐  ┌────┐  ┌────┐   │
│ │BEST│  │NEW │  │HOT │  │SALE│   │
│ │    │  │    │  │    │  │    │   │
│ └────┘  └────┘  └────┘  └────┘   │
│ 상품1    상품2    상품3    상품4    │
│ 30%↓    25%↓    20%↓    35%↓    │
│ 39,000  45,000  32,000  28,000   │
└────────────────────────────────────┘
```

---

## 퀴즈/이벤트형 템플릿

### 12. 퀴즈 이벤트 (quiz-event.html) - 800×400

참여형 퀴즈 이벤트 템플릿.

**변수:**
| 변수 | 설명 | 예시 |
|------|------|------|
| `{{QUIZ_ICON}}` | 퀴즈 아이콘 | ❓ |
| `{{BADGE_TEXT}}` | 이벤트 뱃지 | 퀴즈 이벤트 |
| `{{QUESTION}}` | 퀴즈 질문 | OO의 정답은? |
| `{{HINT}}` | 힌트 | 힌트: ㅈㅁ |
| `{{PRIZE_TEXT}}` | 경품 안내 | 정답자 100명 쿠폰 증정 |
| `{{CTA_TEXT}}` | 버튼 텍스트 | 정답 맞추기 |
| `{{CTA_SUB}}` | 버튼 서브 텍스트 | 카카오톡에서 참여 |

---

## 색상 팔레트

| 용도 | 색상명 | HEX |
|------|--------|-----|
| 카카오 옐로우 | --kakao-yellow | `#FEE500` |
| 카카오 브라운 | --kakao-brown | `#3C1E1E` |
| 카카오 블랙 | --kakao-black | `#191919` |
| 강조 레드 | --accent-red | `#FF5A5A` |
| 강조 블루 | --accent-blue | `#5A9CFF` |
| 강조 그린 | --accent-green | `#00C73C` |
| 강조 오렌지 | --accent-orange | `#FF9500` |
| 강조 퍼플 | --accent-purple | `#9B59B6` |

## 파일 구조

```
kakao-message/
├── SKILL.md
└── assets/
    └── templates/
        ├── styles.css                    # 공통 스타일
        ├── wide-promo-sale.html          # 와이드 프로모 세일 (800×600)
        ├── wide-new-product.html         # 와이드 신상품 (800×600)
        ├── wide-coupon-event.html        # 와이드 쿠폰 (800×600)
        ├── wide-minimal.html             # 와이드 미니멀 (800×600)
        ├── wide-emotional.html           # 와이드 감성 (800×600)
        ├── wide-gradient.html            # 와이드 그라데이션 (800×600)
        ├── wide-review.html              # 와이드 리뷰 (800×600)
        ├── carousel-feed.html            # 캐러셀 피드 (800×400)
        ├── carousel-commerce-intro.html  # 캐러셀 인트로 (800×1100)
        ├── carousel-commerce-item.html   # 캐러셀 아이템 (800×800)
        ├── list-item.html                # 리스트 4상품 (800×400)
        └── quiz-event.html               # 퀴즈 이벤트 (800×400)
```

## V2 템플릿 (templates-v2/)

Sunday Hug 브랜드에서 발전시킨 고급 템플릿 세트입니다. 유형별 디렉토리 구조, 팔레트 시스템, 가이드 문서를 포함합니다.

- `templates-v2/` — 유형별 카카오 메시지 템플릿
- `templates-v2/GUIDE.md` — 사용 가이드
- `templates-v2/_base-styles.css` — 공통 스타일
- `templates-v2/_palettes.css` — 컬러 팔레트 시스템

공유 디자인 시스템: `skills/advertising/_design-system/` 참조

## 사용 예시

### Playwright로 PNG 생성

```python
from playwright.sync_api import sync_playwright

def render_kakao_banner(template_path, output_path, variables):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': 800, 'height': 600})

        # HTML 로드
        with open(template_path, 'r') as f:
            html = f.read()

        # 변수 치환
        for key, value in variables.items():
            html = html.replace(f'{{{{{key}}}}}', value)

        page.set_content(html)

        # 컨테이너만 캡처
        element = page.query_selector('[class*="wide-"], [class*="carousel-"], [class*="list-"], [class*="quiz-"]')
        element.screenshot(path=output_path)

        browser.close()

# 사용 예
render_kakao_banner(
    'wide-promo-sale.html',
    'output/sale-banner.png',
    {
        'BADGE_TEXT': 'MEGA SALE',
        'DISCOUNT': '50',
        'TITLE': '전 상품 특가',
        'SUBTITLE': '겨울 시즌 한정',
        'PERIOD': '1/20 ~ 1/31',
        'PRODUCT_IMAGE': './product.png',
        'CTA_TEXT': '지금 쇼핑하기'
    }
)
```
