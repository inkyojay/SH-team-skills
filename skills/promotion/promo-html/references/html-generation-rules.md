# HTML 동적 생성 규칙

> Claude가 채널별 HTML을 생성할 때 반드시 따라야 할 규칙

## 필수 HTML 구조

모든 HTML 파일은 아래 구조를 따릅니다:

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width={W}">
  <style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

    :root {
      --sunday-beige: #F5E6D3;
      --hug-brown: #8B7355;
      --cream: #FAFAF7;
      --soft-gray: #E8E4DE;
      --text-deep: #8B7355;
      --text-dark: #333333;
      --text-mid: #666666;
      --text-light: #999999;
      --sale-red: #D4534A;
      --soft-pink: #F2D4C4;
      --misty-green: #C5D5C5;
    }

    * { margin: 0; padding: 0; box-sizing: border-box; }

    body {
      width: {W}px;
      height: {H}px;
      margin: 0;
      overflow: hidden;
      font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, sans-serif;
      background: var(--cream);
    }
    /* 채널별 커스텀 CSS */
  </style>
</head>
<body>
  <div class="container" style="width:{W}px; height:{H}px; position:relative;">
    <!-- 콘텐츠 -->
  </div>
</body>
</html>
```

## CSS 규칙

### 필수
- 모든 CSS는 `<style>` 태그 안에 인라인으로 작성
- CSS 변수(`:root`)를 사용하여 브랜드 컬러 참조
- `box-sizing: border-box` 전역 적용
- `body`에 정확한 `width`, `height` 지정
- `overflow: hidden` 적용

### 허용
- Pretendard 폰트 CDN `@import` (유일한 외부 리소스)
- Flexbox 레이아웃
- CSS Grid 레이아웃
- CSS 변수
- `calc()`, `min()`, `max()` 함수

### 금지
- 외부 CSS 파일 `<link>` 금지 (폰트 CDN 제외)
- 외부 JavaScript 금지
- `<script>` 태그 금지
- 애니메이션/트랜지션 금지
- `position: fixed` 금지
- `@media` 쿼리 금지 (고정 사이즈이므로 불필요)

## 이미지 처리

### 제품 이미지가 있는 경우
```html
<img src="{PRODUCT_IMAGE_PATH}" alt="{PRODUCT_NAME}"
     style="width:100%; height:100%; object-fit:cover; border-radius:8px;">
```
- `file://` 프로토콜로 로컬 이미지 참조
- `object-fit: cover` 또는 `contain` 사용

### 제품 이미지가 없는 경우
```html
<div style="width:100%; height:300px; background:var(--sunday-beige); border-radius:8px;
            display:flex; align-items:center; justify-content:center;">
  <span style="font-size:14px; color:var(--hug-brown);">SUNDAYHUG</span>
</div>
```
- 베이지 배경 플레이스홀더 사용
- 브랜드명 또는 제품명 텍스트 표시

## 사이즈 준수

- 모든 채널의 정확한 픽셀 사이즈를 `body`와 `.container`에 적용
- 콘텐츠가 지정 사이즈를 초과하지 않도록 `overflow: hidden` 적용
- 상대 단위(`%`, `em`)보다 절대 단위(`px`) 선호

## 브랜드 준수

### 색상
- 반드시 CSS 변수 또는 디자인 시스템의 HEX 값만 사용
- 팔레트 외 색상 절대 사용 금지
- 배경: `--cream`, `--sunday-beige`, `--warm-white` 중 선택
- 텍스트: `--text-deep`, `--text-dark`, `--text-mid`, `--text-light` 중 선택
- 강조: `--sale-red`, `--soft-pink`, `--misty-green` 중 선택

### 타이포그래피
- 폰트: Pretendard만 사용
- 계층: H1 > H2 > Body > Caption 4단계 준수
- 채널 사이즈에 따른 스케일링 적용 (design-system.md 참조)

## 레퍼런스 이미지 활용

1. 에이전트는 해당 채널의 레퍼런스 이미지를 Read 도구로 확인
2. 레이아웃 구조, 요소 배치, 비율을 참고
3. 컬러와 폰트는 반드시 브랜드 디자인 시스템 적용 (레퍼런스 색상 무시)
4. 레퍼런스를 그대로 복사하지 않고, 구조를 참고하여 새로 디자인

## 품질 체크리스트

HTML 생성 완료 후 자체 검증:

- [ ] `body` width/height가 채널 스펙과 정확히 일치하는가
- [ ] `@import` 폰트 CDN이 포함되어 있는가
- [ ] CSS 변수 블록(`:root`)이 포함되어 있는가
- [ ] 외부 CSS/JS 링크가 없는가 (폰트 CDN 제외)
- [ ] 사용된 모든 색상이 브랜드 팔레트에 포함되는가
- [ ] 텍스트가 컨테이너를 벗어나지 않는가
- [ ] 변수 플레이스홀더(`{{...}}`)가 남아있지 않는가
- [ ] 한글 텍스트가 올바르게 인코딩되어 있는가
