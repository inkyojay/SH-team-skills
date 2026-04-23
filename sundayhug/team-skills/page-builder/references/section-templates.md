# 섹션 템플릿 레퍼런스

상세페이지에서 자주 사용되는 섹션 템플릿입니다.

---

## 1. 인트로 섹션

### 기본 인트로
```html
<div class="detail_section bg-color-dailycream" style="padding-bottom:0px;">
    <div class="sub_title font-w600 txtcenter color_dark_brown"
         style="font-size: 16px; letter-spacing: 2px; margin-bottom: 15px;">
        서브 타이틀
    </div>
    <div class="feature_title font-w600 txtcenter">
        메인 타이틀
    </div>
    <div class="desc_small font-w500 txtcenter"
         style="margin-top: 15px; font-size: 16px; color: #666; line-height: 1.8;">
        설명 텍스트
    </div>
    <div class="banner_top20_img" style="margin-top: 30px;">
        <img src="IMAGE_URL" alt="설명">
    </div>
</div>
```

---

## 2. 포인트 섹션 (POINT 01, 02...)

```html
<div class="detail_section" style="margin-bottom: 0px; margin-top: 50px; padding: 30px 15px;">
    <!-- POINT 태그 -->
    <div style="text-align: center; margin-bottom: 20px;">
        <span style="display: inline-block;
                     background: linear-gradient(135deg, #a38068 0%, #8b6b56 100%);
                     color: #fff; padding: 10px 24px; border-radius: 25px;
                     font-size: 14px; font-weight: 700; letter-spacing: 2px;
                     box-shadow: 0 4px 12px rgba(163, 128, 104, 0.3);">
            POINT 01
        </span>
    </div>
    <div class="title font-w700 txtcenter" style="font-size: 24px; margin-bottom: 10px; line-height: 1.4;">
        메인 타이틀
        <br><span style="color: #a38068;">강조 타이틀</span>
    </div>
    <div style="text-align: center; font-size: 14px; color: #888; line-height: 1.7; margin-bottom: 25px;">
        설명 텍스트
    </div>
    <!-- 콘텐츠 영역 -->
</div>
```

---

## 3. ABC 스타일 섹션 (A, B, C 포인트)

```html
<div class="detail_section" style="margin-top: 40px; margin-bottom: 0px;">
    <div class="sub_title font-w700 txtleft">
        <span class="desc_btn" style="background: #000000;">A</span>
    </div>
    <div class="title font-w700 txtleft" style="font-size: 26px; margin: 15px 0;">
        Anywhere
        <br> — 어디서든 익숙한
    </div>
    <div class="desc_small txtleft" style="line-height: 1.9;">
        <span class="point_color2" style="font-weight: 600;">강조 텍스트</span>
        <br><br>설명 텍스트
    </div>
    <div class="banner_top20_img">
        <img src="IMAGE_URL" alt="설명">
    </div>
</div>
```

---

## 4. 고민/말풍선 섹션

```html
<div class="detail_section" style="margin-bottom: 0px; margin-top: 0px; padding: 40px 20px;">
    <div style="text-align: center; margin-bottom: 15px;">
        <div style="font-size: 32px; font-weight: 700; color: #2d2420; line-height: 1.3; margin-bottom: 10px;">
            0~3세
            <br><span style="font-size: 24px; font-weight: 600;">수면이 가장 중요한 시기!</span>
        </div>
    </div>
    <div style="max-width: 600px; margin: 50px auto 0; display: flex; flex-direction: column; gap: 20px;">
        <!-- 고민 아이템들 (inline-patterns.md 참조) -->
    </div>
</div>
```

---

## 5. FAQ 섹션

```html
<div class="detail_section" style="margin-bottom: 0px; margin-top: 50px;">
    <div class="sub_title font-w700 txtleft">
        <span class="desc_btn" style="background: #000000;">FAQ</span>
    </div>
    <div class="title font-w700 txtleft" style="font-size: 28px; margin: 15px 0;">
        자주 묻는 질문
    </div>
</div>
<div class="detail_section" style="margin-top: 20px; margin-bottom: 30px;">
    <div style="max-width: 100%; margin: 0; text-align: left;">
        <!-- FAQ 아이템들 (inline-patterns.md 참조) -->
    </div>
</div>
```

---

## 6. 사이즈 가이드 섹션

```html
<div class="detail_section" style="margin-top: 50px;">
    <div class="sub_title txtleft font-w700 color_dark_brown">SIZE INFO</div>
    <div class="title font-w700 txtleft" style="font-size: 28px; margin: 15px 0;">
        제품 사이즈 가이드
    </div>
    <div class="desc_small txtleft" style="line-height: 1.9;">
        제품 설명
    </div>
    <div class="banner_top20_img">
        <img src="IMAGE_URL" alt="사이즈 이미지">
    </div>
    <div class="size_wrap2">
        <div class="sizeTable">
            <div class="size_cell sizetit">구분</div>
            <div class="size_cell sizetit">사이즈</div>
        </div>
        <div class="sizeTable">
            <div class="size_cell sizetit">가로 (W)</div>
            <div class="size_cell">00 cm</div>
        </div>
        <!-- 추가 행 -->
        <div class="sizetxt_wrap">
            <p class="sizetxt">※ 주의사항</p>
        </div>
    </div>
</div>
```

---

## 7. 구성품 섹션

```html
<div class="detail_section bg-color-dailycream" style="margin-top: 50px; padding: 50px 20px;">
    <div class="sub_title font-w700 txtcenter">
        <span class="desc_btn" style="background: #000000;">구성품</span>
    </div>
    <div class="title font-w700 txtcenter" style="font-size: 32px; margin: 20px 0 50px 0;">
        제품 정보 & 케어 가이드
    </div>
    <div style="max-width: 900px; margin: 0 auto;">
        <div class="title font-w700 txtleft"
             style="font-size: 22px; margin-bottom: 25px; color: #2d2420;
                    padding-left: 15px; border-left: 4px solid #2d2420;">
            구성품
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
            <!-- 구성품 카드들 (inline-patterns.md 참조) -->
        </div>
    </div>
</div>
```

---

## 8. 리뷰 이벤트 섹션

```html
<div class="detail_section">
    <div style="background: #2d2420; padding: 40px 0px; text-align: center;">
        <div style="color: #fff; font-size: 24px; font-weight: 700; line-height: 1.5; margin-bottom: 15px;">
            소중한 후기를 남겨주세요
            <br><span style="color: #fff;">특별한 선물을 드립니다</span>
        </div>
    </div>
    <div style="background: #fff; padding: 40px 20px; text-align: center;">
        <div style="margin-bottom: 15px;">
            <span style="display: inline-block; border: 1px solid #2d2420; color: #2d2420;
                         padding: 6px 20px; font-size: 12px; font-weight: 600; letter-spacing: 2px;">
                REVIEW EVENT
            </span>
        </div>
        <div style="font-size: 22px; font-weight: 700; color: #2d2420; margin-bottom: 10px;">
            이벤트 제목
        </div>
        <div style="font-size: 14px; color: #666; line-height: 1.7; margin-bottom: 30px;">
            설명 텍스트
        </div>
        <!-- 사은품 카드들 (inline-patterns.md 참조) -->
    </div>
</div>
```

---

## 9. 추가 구매 상품 섹션

```html
<div class="detail_section">
    <div style="background: #2d2420; padding: 40px 0px; text-align: center;">
        <div style="color: #fff; font-size: 24px; font-weight: 700; line-height: 1.5;">
            추가 구매 구성 상품
        </div>
    </div>
    <div style="background: #fff; padding: 40px 20px; text-align: center;">
        <!-- 상품 카드들 -->
    </div>
</div>
```

---

## 10. 전문가 프로필 섹션

```html
<div class="detail_section bg-color-1" style="margin-top: 50px;">
    <div class="sub_title">
        <span class="color_coral">Designed with</span>
    </div>
    <div class="title font-w700 txtcenter" style="font-size: 28px; margin: 20px 0;">
        제품이 선택받는 이유
    </div>
    <div class="profile" style="margin-bottom: 10px; margin-top: 30px;">
        <img src="PROFILE_IMAGE_URL" alt="프로필">
    </div>
    <p class="desc_small txtcenter">
        <span class="font_16_600">전문가 이름</span>
    </p>
    <div class="desc_small" style="margin: 30px 15px; line-height: 1.9;">
        <span class="point_color2" style="font-size: 18px; font-weight: 600;">
            "인용문"
        </span>
        <br><br>본문 내용
    </div>
</div>
```

---

## 11. 브랜드 비전 섹션

```html
<div class="detail_section bg-color-dailycream" style="margin-bottom: 0px; margin-top: 50px; padding: 40px 20px;">
    <div class="feature_title font-serif font-w300 txtcenter color_dark_brown"
         style="font-size: 28px; line-height: 1.5; margin: 20px 0;">
        브랜드와 함께 아기의
        <br>건강한 성장을 지켜주세요
    </div>
    <div class="desc_small font-serif txtcenter" style="margin: 30px 15px; line-height: 1.9;">
        브랜드 스토리 텍스트
    </div>
    <div class="banner_top20_img" style="margin-top: 30px;">
        <img src="IMAGE_URL" alt="브랜드 이미지">
    </div>
</div>
```

---

## 12. 상품정보 제공고시 섹션

```html
<div class="detail_section" style="margin-top: 50px; padding: 30px 20px;">
    <div class="title font-w700 txtleft" style="font-size: 22px; margin-bottom: 25px; color: #2d2420;">
        상품정보 제공고시
    </div>
    <table style="width: 100%; border-collapse: collapse; text-align: left; border-top: 1px solid #ddd;">
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 15px; width: 30%; background: #f9f9f9; font-weight: 600; color: #555;">
                품명 / 모델명
            </td>
            <td style="padding: 15px; color: #333;">제품명</td>
        </tr>
        <!-- 추가 행 -->
    </table>
</div>
```

---

## 13. CTA 배너 링크 섹션

```html
<div class="detail_section" style="margin-bottom: 0px; margin-top: 30px;">
    <a href="URL" style="display: block; text-decoration: none;">
        <div style="background: #1a1a1a; padding: 18px 20px; text-align: center; border-radius: 8px;">
            <span style="color: #fff; font-size: 15px; font-weight: 600; letter-spacing: -0.3px;">
                링크 텍스트 →
            </span>
        </div>
    </a>
</div>
```

---

## 14. 최종 확신 카피 섹션

```html
<div class="detail_section" style="margin-top: 50px; margin-bottom: 0px; padding: 40px 20px; background: #f9f9f9;">
    <div class="title font-w700 txtcenter" style="font-size: 26px; line-height: 1.5; margin-bottom: 25px;">
        마무리 메시지
    </div>
    <div class="desc_small txtcenter" style="line-height: 1.9; color: #555; font-size: 16px;">
        설명 텍스트
        <br><br>
        <span class="point_color2" style="font-weight: 600; font-size: 17px;">
            강조 메시지
        </span>
    </div>
    <div class="banner_top20_img" style="margin-top: 30px;">
        <img src="IMAGE_URL" alt="이미지">
    </div>
</div>
```
