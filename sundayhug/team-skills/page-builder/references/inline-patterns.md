# 인라인 스타일 패턴 레퍼런스

CSS 클래스로 커버되지 않는 인라인 스타일 패턴입니다.
상세페이지 제작 시 복사하여 사용하세요.

---

## 1. 이미지 오버레이 카드 (가장 많이 사용)

### 기본 구조
```html
<div style="position: relative; overflow: hidden;">
    <img src="IMAGE_URL" alt="설명"
         style="width: 100%; aspect-ratio: 4/3; object-fit: cover;">
    <!-- 그라데이션 오버레이 -->
    <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 50%;
                background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%);">
    </div>
    <!-- 텍스트 -->
    <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 20px; color: #fff;">
        <div style="font-size: 18px; font-weight: 700; line-height: 1.4;">제목
            <br><span style="font-weight: 400; font-size: 14px; opacity: 0.9;">부제목</span>
        </div>
    </div>
</div>
```

### 이미지 비율 옵션
- `aspect-ratio: 3/4` - 세로형
- `aspect-ratio: 4/3` - 가로형
- `aspect-ratio: 16/9` - 와이드
- `aspect-ratio: 16/10` - 준와이드
- `aspect-ratio: 1/1` - 정사각형

### 그라데이션 옵션
```css
/* 검정 (기본) */
linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%)

/* 브라운 */
linear-gradient(to top, rgba(163,128,104,0.8) 0%, rgba(163,128,104,0) 100%)

/* 진한 검정 */
linear-gradient(to top, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%)
```

---

## 2. 뱃지 & 태그

### STEP 뱃지 (이미지 좌상단)
```html
<div style="position: absolute; top: 10px; left: 10px; background: #a38068; color: #fff;
            padding: 4px 10px; font-size: 11px; font-weight: 600;">
    STEP 1
</div>
```

### POINT 태그 (라운드 그라데이션) ⭐ 주력
```html
<span style="display: inline-block;
             background: linear-gradient(135deg, #a38068 0%, #8b6b56 100%);
             color: #fff; padding: 10px 24px; border-radius: 25px;
             font-size: 14px; font-weight: 700; letter-spacing: 2px;
             box-shadow: 0 4px 12px rgba(163, 128, 104, 0.3);">
    POINT 01
</span>
```

### 텍스트 태그 (테두리)
```html
<span style="display: inline-block; border: 1px solid #2d2420; color: #2d2420;
             padding: 6px 20px; font-size: 12px; font-weight: 600; letter-spacing: 2px;">
    REVIEW EVENT
</span>
```

### 숫자 원형 뱃지
```html
<div style="width: 32px; height: 32px; background: #2d2420; color: #fff;
            border-radius: 50%; display: flex; align-items: center;
            justify-content: center; font-size: 14px; font-weight: 700;
            margin: 0 auto 12px;">
    A
</div>
```

### 수량 뱃지 (구성품용)
```html
<div style="display: inline-block; background: #2d2420; color: #fff;
            padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: 500;">
    1개
</div>
```

---

## 3. 고민/말풍선 섹션

### 왼쪽 프로필 + 오른쪽 말풍선
```html
<div style="display: flex; align-items: center; gap: 15px;">
    <!-- 프로필 원형 -->
    <div style="width: 70px; height: 70px; border-radius: 50%; flex-shrink: 0;
                background: linear-gradient(135deg, #ff8605 0%, #ff6b9d 100%);
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 4px 12px rgba(255, 134, 5, 0.3);">
        <span style="color: #fff; font-size: 24px; font-weight: 700;">01</span>
    </div>
    <!-- 말풍선 -->
    <div style="background: #f8f6f4; padding: 18px 20px; border-radius: 20px;
                flex: 1; position: relative;">
        <!-- 꼬리 -->
        <div style="position: absolute; left: -8px; top: 20px; width: 0; height: 0;
                    border-top: 8px solid transparent; border-bottom: 8px solid transparent;
                    border-right: 10px solid #f8f6f4;"></div>
        <div style="font-size: 14px; line-height: 1.6; color: #2d2420;">
            <span style="color: #ff8605; font-weight: 600;">강조 텍스트</span>
            <br>일반 텍스트
        </div>
    </div>
</div>
```

### 오른쪽 프로필 + 왼쪽 말풍선
```html
<div style="display: flex; align-items: center; gap: 15px; flex-direction: row-reverse;">
    <!-- 프로필 원형 -->
    <div style="width: 70px; height: 70px; border-radius: 50%; flex-shrink: 0;
                background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
                display: flex; align-items: center; justify-content: center;
                box-shadow: 0 4px 12px rgba(255, 107, 53, 0.3);">
        <span style="color: #fff; font-size: 24px; font-weight: 700;">02</span>
    </div>
    <!-- 말풍선 -->
    <div style="background: #ede3d8; padding: 18px 20px; border-radius: 20px;
                flex: 1; position: relative;">
        <!-- 꼬리 (오른쪽) -->
        <div style="position: absolute; right: -8px; top: 20px; width: 0; height: 0;
                    border-top: 8px solid transparent; border-bottom: 8px solid transparent;
                    border-left: 10px solid #ede3d8;"></div>
        <div style="font-size: 14px; line-height: 1.6; color: #2d2420; text-align: right;">
            텍스트 내용
        </div>
    </div>
</div>
```

---

## 4. 알림/주의사항 박스

### 주의사항 박스 (오렌지)
```html
<div style="background: #fff3e0; border-left: 4px solid #ff8605;
            padding: 18px 20px; border-radius: 8px; text-align: left;">
    <div style="display: flex; align-items: flex-start; gap: 12px;">
        <div style="flex-shrink: 0; font-size: 18px; color: #ff8605; font-weight: 700;">⚠️</div>
        <div style="flex: 1;">
            <div style="font-size: 14px; font-weight: 600; color: #2d2420; margin-bottom: 8px;">
                주의사항
            </div>
            <div style="font-size: 13px; color: #666; line-height: 1.7;">
                내용
            </div>
        </div>
    </div>
</div>
```

### 다크 알림 바
```html
<div style="background: #2d2420; padding: 12px 15px;">
    <span style="font-size: 13px; color: #fff;">
        <strong>Q. 질문</strong> → 답변
    </span>
</div>
```

### CTA 그라데이션 배너
```html
<div style="background: linear-gradient(135deg, #ff8605 0%, #ff6b35 100%);
            padding: 18px 20px; text-align: center;">
    <div style="color: #fff; font-size: 20px; font-weight: 700; line-height: 1.4;">
        메시지
    </div>
</div>
```

### 강조 배경 박스
```html
<div style="background: #f5f0e8; padding: 15px; text-align: center;">
    <div style="font-size: 14px; color: #2d2420; line-height: 1.6;">
        <strong>강조</strong> 일반 텍스트
    </div>
</div>
```

---

## 5. FAQ 아이템

```html
<div style="border-bottom: 1px solid #eee; padding: 20px 15px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="flex: 1; text-align: left; font-weight: 600; font-size: 14px;">
            Q1. 질문 내용
        </span>
    </div>
    <div style="padding-top: 15px;">
        <div style="color: #666; line-height: 1.8; text-align: left; font-size: 14px;">
            답변 내용
        </div>
    </div>
</div>
```

---

## 6. 그리드 레이아웃

### 3열 그리드 (구성품)
```html
<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
    <div style="background: #fff; border-radius: 10px; padding: 20px;
                text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.06);">
        <!-- 원형 이미지 -->
        <div style="width: 80px; height: 80px; background: #f5f5f5; border-radius: 50%;
                    margin: 0 auto 15px; overflow: hidden;">
            <img src="IMAGE_URL" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div style="font-size: 14px; font-weight: 600; color: #2d2420; margin-bottom: 6px;">
            제목
        </div>
        <div style="font-size: 12px; color: #888; margin-bottom: 8px;">설명</div>
        <!-- 수량 뱃지 -->
        <div style="display: inline-block; background: #2d2420; color: #fff;
                    padding: 4px 12px; border-radius: 12px; font-size: 11px;">1개</div>
    </div>
</div>
```

### 2열 Flex (비교/상품 카드)
```html
<div style="display: flex; gap: 15px;">
    <div style="flex: 1; border: 1px solid #e0e0e0; overflow: hidden;">
        <div style="aspect-ratio: 1/1; overflow: hidden;">
            <img src="IMAGE_URL" style="width: 100%; height: 100%; object-fit: cover;">
        </div>
        <div style="padding: 20px; border-top: 1px solid #e0e0e0;">
            <!-- 내용 -->
        </div>
    </div>
</div>
```

### 3열 Flex (특징 요약)
```html
<div style="display: flex; gap: 10px;">
    <div style="flex: 1; background: #f8f6f4; padding: 15px; text-align: center;">
        <div style="font-size: 13px; color: #a38068; font-weight: 600;">제목</div>
        <div style="font-size: 12px; color: #666; margin-top: 5px;">설명</div>
    </div>
</div>
```

### 비대칭 2열 (6:4)
```html
<div style="display: flex; gap: 8px; align-items: flex-end;">
    <div style="flex: 6; overflow: hidden;">
        <img src="IMAGE_URL" style="width: 100%; aspect-ratio: 3/4; object-fit: cover;">
    </div>
    <div style="flex: 4; overflow: hidden; margin-bottom: 30px;">
        <img src="IMAGE_URL" style="width: 100%; aspect-ratio: 3/4; object-fit: cover;">
    </div>
</div>
```

---

## 7. 상품정보 테이블

```html
<table style="width: 100%; border-collapse: collapse; text-align: left; border-top: 1px solid #ddd;">
    <tr style="border-bottom: 1px solid #eee;">
        <td style="padding: 15px; width: 30%; background: #f9f9f9;
                   font-weight: 600; color: #555;">항목</td>
        <td style="padding: 15px; color: #333;">내용</td>
    </tr>
</table>
```

---

## 8. 다크 헤더 섹션

```html
<div style="background: #2d2420; padding: 40px 0px; text-align: center;">
    <div style="color: #fff; font-size: 24px; font-weight: 700; line-height: 1.5; margin-bottom: 15px;">
        제목
        <br><span style="color: #fff;">부제목</span>
    </div>
</div>
```

---

## 9. 모드 비교 카드

```html
<div style="flex: 1; position: relative; overflow: hidden;">
    <img src="IMAGE_URL" style="width: 100%; aspect-ratio: 3/4; object-fit: cover;">
    <!-- 그라데이션 -->
    <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 60%;
                background: linear-gradient(to top, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 100%);">
    </div>
    <!-- STEP 뱃지 -->
    <div style="position: absolute; top: 10px; left: 10px; background: #a38068;
                color: #fff; padding: 4px 10px; font-size: 11px; font-weight: 600;">
        STEP 1
    </div>
    <!-- 텍스트 -->
    <div style="position: absolute; bottom: 0; left: 0; right: 0; padding: 15px; color: #fff;">
        <div style="font-size: 16px; font-weight: 700; margin-bottom: 6px;">모드명</div>
        <div style="font-size: 11px; opacity: 0.95; line-height: 1.5;">
            설명 텍스트
        </div>
    </div>
</div>
```

---

## 10. 장식 요소

### 구분선 + 텍스트
```html
<div style="display: flex; align-items: center; justify-content: center; gap: 12px;">
    <div style="flex: 1; max-width: 80px; height: 1px;
                background: linear-gradient(to right, transparent, #a38068);"></div>
    <span style="font-size: 16px; font-weight: 600; color: #2d2420; letter-spacing: 2px;">
        JUST <span style="color: #a38068; font-size: 22px; font-weight: 800;">30</span> SEC
    </span>
    <div style="flex: 1; max-width: 80px; height: 1px;
                background: linear-gradient(to left, transparent, #a38068);"></div>
</div>
```

### 세로 구분선
```html
<div style="font-size: 14px; color: #999; padding-bottom: 20px;
            border-bottom: 1px solid #e0e0e0; max-width: 200px; margin: 0 auto;">
    |
</div>
```
