---
name: sundayhug-live-thumbnail
description: |
  SundayHug 쇼핑라이브/프로모션용 1:1 썸네일을 HTML/CSS 기반으로 제작하고 PNG로 정확히 출력하는 스킬.
  현재 확정된 스타일은 밝은 베이지톤 아기방/제품 사진을 배경으로, 좌측 하단에 검정 LIVE 일정 캡슐,
  PNG LIVE 배지, 작은 영문 키커, 큰 흰색 한글 타이틀을 배치하는 방식이다.

  특히 Chrome headless 캡처 시 하단 단색 바가 생기지 않도록 “더 크게 캡처 후 정확히 1:1 crop”하는
  출력 규칙을 반드시 따른다.
triggers:
  - "라이브 썸네일 만들어줘"
  - "쇼핑라이브 썸네일"
  - "썸네일 이미지 하나 만들어줘"
  - "라이브 배지 썸네일"
  - "1:1 고해상도 썸네일"
  - "SundayHug live thumbnail"
  - "블루밍데이즈 라이브 썸네일"
---

# sundayhug-live-thumbnail

SundayHug 라이브 커머스/프로모션용 정방형 썸네일을 만든다.

이 스킬은 이번에 확정한 스타일을 그대로 유지한다.

- 배경: 밝은 베이지/아이보리 톤 제품 라이프스타일 사진
- 상단 로고/상단 캠페인 배지: 기본적으로 넣지 않는다
- 정보 위치: 좌측 하단 집중
- LIVE 일정: 검정 pill 캡슐 + PNG LIVE 배지 + 흰색 굵은 날짜 텍스트
- 보조 문구: 작은 영문 대문자, 넓은 자간
- 메인 제목: 큰 흰색 굵은 한글, 2줄, 좌측 정렬
- 하단: 배경 사진이 끝까지 자연스럽게 이어져야 하며 금/갈/검정 단색 바가 보이면 실패

## 필수 원칙

1. 사용자가 “썸네일”이라고 하면 페이지를 수정하지 말고 이미지 1장 또는 이미지용 HTML을 만든다.
2. 결과물은 HTML 원본 + PNG 출력본을 함께 만든다.
3. LIVE 빨간 배지는 CSS로 재현하지 말고 PNG asset을 사용한다.
4. 배경 이미지는 `object-fit: cover`로 캔버스 전체를 덮는다.
5. Chrome headless에서 바로 `--window-size=1080,1080`로 찍지 않는다.
   - macOS Chrome headless는 실제 콘텐츠 하단이 약 87px 잘려 body/background가 단색 바처럼 찍힐 수 있다.
   - 반드시 더 높은 창으로 캡처한 뒤 정확히 1:1 crop한다.
6. 출력 후 vision 또는 픽셀 검사로 하단 단색 바가 없는지 확인한다.

## 기본 파일 위치

작업 예시 경로:

```text
~/Desktop/homepage/cafe/pages_1/event/bloomingdays-live-thumbnail.html
~/Desktop/homepage/cafe/pages_1/event/image/bloomingdays-live/bloomingdays-live-thumbnail.png
~/Desktop/homepage/cafe/pages_1/event/image/bloomingdays-live/bloomingdays-live-thumbnail-3240.png
```

팀스킬 결과물 규칙을 따를 때는 사용자에게 별도 경로 요청이 없으면:

```text
~/Desktop/team-skills/카드뉴스/sundayhug-live-thumbnail/{campaign-slug}/
```

에 저장한다.

## 필요한 asset

기본 LIVE 배지 PNG:

```text
/Users/inkyo/Desktop/templates/promotion/assets/live-badge.png
```

Cafe24 event 폴더에서 작업할 때는 해당 이벤트 이미지 폴더로 복사해서 상대경로로 참조한다.

예:

```bash
cp /Users/inkyo/Desktop/templates/promotion/assets/live-badge.png \
  /Users/inkyo/Desktop/homepage/cafe/pages_1/event/image/bloomingdays-live/live-badge.png
```

HTML에서는:

```html
<img src="./image/bloomingdays-live/live-badge.png" alt="LIVE">
```

## 확정 스타일 스펙: 1080 x 1080 기준

캔버스:

```css
html, body {
  margin: 0;
  width: 1080px;
  height: 1080px;
  overflow: hidden;
  background: #111518;
  font-family: Pretendard, "Apple SD Gothic Neo", "Noto Sans KR", sans-serif;
}

.sh-live-thumb {
  position: relative;
  width: 1080px;
  height: 1175px; /* 캡처 안정성용. 최종은 1080으로 crop */
  overflow: hidden;
  background: #111518;
}
```

배경 이미지:

```css
.bg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 50% 0%;
  filter: brightness(.88) contrast(.96) saturate(.92);
}
```

중요:
- 1080x1350 같은 세로형 이미지는 `object-position: 50% 0%`가 하단 단색 바 없이 자연스러웠다.
- 다른 이미지에서는 피사체 위치에 맞춰 조정하되, 하단이 body/background 색으로 보이면 실패다.

오버레이:

```css
.warm-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(0,0,0,.10) 0%,
    rgba(0,0,0,.10) 45%,
    rgba(0,0,0,.18) 100%
  );
}
```

하단 별도 gradient bar는 기본적으로 쓰지 않는다.
단색 바로 오해될 수 있기 때문이다.

LIVE 일정 캡슐:

```css
.schedule {
  position: absolute;
  left: 75px;
  top: 626px;
  width: 545px;
  height: 75px;
  display: block;
  border-radius: 38px;
  background: #111518;
  box-shadow: 0 5px 13px rgba(0,0,0,.25);
}

.live-label {
  position: absolute;
  left: 57px;
  top: 14px;
  width: 71px;
  height: 48px;
}

.live-label img {
  display: block;
  width: 71px;
  height: 48px;
  object-fit: contain;
}

.date {
  position: absolute;
  left: 148px;
  top: 0;
  height: 75px;
  display: flex;
  align-items: center;
  color: #fff;
  font-size: 40px;
  font-weight: 850;
  letter-spacing: -.8px;
  white-space: nowrap;
}
```

실측 기준:
- 검정 캡슐: 545 x 75px
- LIVE PNG 배지: 71 x 48px
- LIVE 왼쪽 여백: 57px
- LIVE와 날짜 사이: 약 20px
- 날짜 오른쪽 여백: 약 45px

키커/타이틀:

```css
.kicker {
  position: absolute;
  left: 94px;
  top: 726px;
  color: rgba(255,255,255,.82);
  font-size: 18px;
  font-weight: 900;
  letter-spacing: .18em;
  text-transform: uppercase;
  text-shadow: 0 2px 6px rgba(0,0,0,.24);
}

.title {
  position: absolute;
  left: 94px;
  top: 764px;
  color: #fff;
  font-size: 65px;
  font-weight: 900;
  line-height: 1.35;
  letter-spacing: -2.7px;
  text-shadow: 0 3px 6px rgba(0,0,0,.38), 0 7px 14px rgba(0,0,0,.18);
}
```

## 표준 HTML 구조

```html
<div class="sh-live-thumb">
  <img class="bg" src="./image/bloomingdays-live/hero-canopy.webp" alt="">
  <div class="warm-overlay"></div>

  <div class="schedule">
    <div class="live-label"><img src="./image/bloomingdays-live/live-badge.png" alt="LIVE"></div>
    <div class="date">5월 7일 (목) 오전 11시</div>
  </div>

  <div class="kicker">Blooming Days · Shopping Live</div>
  <div class="title">ABC 아기침대 라이브 혜택<br>+ 전용 악세사리 쿠폰 공개</div>
</div>
```

## 출력 방식: 하단 바 방지용 필수 절차

절대 다음처럼 바로 찍지 않는다:

```bash
# 금/갈/검정 단색 바가 생길 수 있음 — 금지
chrome --headless --window-size=1080,1080 --screenshot=out.png page.html
```

대신 더 높은 viewport로 찍고 crop한다.

1080 출력:

```bash
HTML="file:///path/to/thumbnail.html"
RAW="/tmp/live-thumb-1080-raw.png"
OUT="/path/to/live-thumbnail-1080.png"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --window-size=1080,1167 \
  --screenshot="$RAW" "$HTML"

python3 - <<'PY'
from PIL import Image
Image.open('/tmp/live-thumb-1080-raw.png').convert('RGB').crop((0,0,1080,1080)).save('/path/to/live-thumbnail-1080.png')
PY
```

3240 출력:

```bash
HTML="file:///path/to/thumbnail.html"
RAW="/tmp/live-thumb-3240-raw.png"
OUT="/path/to/live-thumbnail-3240.png"

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files \
  --force-device-scale-factor=3 \
  --window-size=1080,1167 \
  --screenshot="$RAW" "$HTML"

python3 - <<'PY'
from PIL import Image
Image.open('/tmp/live-thumb-3240-raw.png').convert('RGB').crop((0,0,3240,3240)).save('/path/to/live-thumbnail-3240.png')
PY
```

Pillow가 없으면:

```bash
python3 -m pip install --user pillow
```

## 검수 체크리스트

출력 후 반드시 확인한다.

1. 파일 크기
   ```bash
   sips -g pixelWidth -g pixelHeight out.png
   ```
   - 1080 출력: 1080 x 1080
   - 고해상도: 3240 x 3240

2. 하단 단색 바 검사
   - 금색/갈색/검정색 단색 수평 바가 보이면 실패.
   - 배경 이미지가 하단까지 자연스럽게 이어져야 한다.
   - 픽셀 검사 예:
     ```python
     from PIL import Image
     import numpy as np
     im = Image.open('out.png').convert('RGB')
     arr = np.array(im)
     bg = np.array([17,21,24])
     rows = ((arr == bg).all(axis=2)).mean(axis=1)
     print(next((i for i,v in enumerate(rows) if v > .99), None))
     # None이어야 정상
     ```

3. 시각 검수
   - LIVE 배지 PNG가 보이는가?
   - 검정 캡슐에 날짜 좌우 패딩이 충분한가?
   - 상단 SundayHug 로고/상단 Blooming Days 배지가 남아있지 않은가?
   - 텍스트가 이미지 경계에 닿거나 잘리지 않는가?

## 이번 확정 예시

확정된 최종 산출물:

```text
/Users/inkyo/Desktop/homepage/cafe/pages_1/event/bloomingdays-live-thumbnail.html
/Users/inkyo/Desktop/homepage/cafe/pages_1/event/image/bloomingdays-live/bloomingdays-live-thumbnail-from-html.png
/Users/inkyo/Desktop/homepage/cafe/pages_1/event/image/bloomingdays-live/bloomingdays-live-thumbnail-3240.png
```

확정 문구:

```text
LIVE 5월 7일 (목) 오전 11시
BLOOMING DAYS · SHOPPING LIVE
ABC 아기침대 라이브 혜택
+ 전용 악세사리 쿠폰 공개
```

## 흔한 실패와 수정

- 하단 금/갈/검정 바가 보임
  - 원인: Chrome headless viewport가 실제 콘텐츠보다 짧게 캡처됨, 또는 body/background 색 노출.
  - 수정: `--window-size=1080,1167`로 찍고 `crop((0,0,1080,1080))`.

- LIVE 빨간 라벨이 어색함
  - 원인: CSS로 직접 만든 라벨.
  - 수정: `live-badge.png` asset을 사용.

- 검정 캡슐이 글씨 대비 좁음
  - 수정: 캡슐 폭 545px 안팎, 날짜 오른쪽 여백 40~50px 확보.

- 상단 로고/캠페인 배지가 보임
  - 이 스타일에서는 제거한다. 정보는 하단에만 집중.

- 배경이 너무 어두움
  - 하단 별도 gradient를 끄고 전체 overlay를 `rgba(0,0,0,.10~.18)` 정도로 낮춘다.
