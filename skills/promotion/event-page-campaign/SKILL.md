---
name: event-page-campaign
description: Use when creating or restyling a Cafe24/SundayHug event page from visual reference images, preserving the original page, making a separate CSS/asset copy, checking mobile line breaks, exporting high-resolution mobile JPGs, splitting sections into JPG files, or creating a matching 1:1 live/event thumbnail.
triggers:
  - 이벤트 페이지 제작
  - 이벤트 페이지 리디자인
  - 레퍼런스 느낌으로 바꿔줘
  - 모바일 고해상도 JPG
  - 섹션별 JPG
  - 1:1 썸네일
  - 라이브 썸네일
  - Cafe24 이벤트 페이지
---

# Event Page Campaign

레퍼런스 이미지 기반으로 이벤트 페이지, 모바일 업로드용 JPG, 섹션별 JPG, 1:1 썸네일까지 한 번에 만드는 작업 스킬이다.

## 핵심 원칙

- 원본 HTML/CSS는 직접 수정하지 않는다. 반드시 `*-concept.html`, `*-hip.html`처럼 복사본을 만들고 CSS도 새 파일로 분리한다.
- 사용자가 공유한 레퍼런스는 색감, 여백, 타이포, 일러스트 밀도, 사진/그래픽 배치 방식으로 분해해서 적용한다.
- 기존 상품 사진과 브랜드 로고는 가능한 한 재사용하고, 부족한 장식 요소만 로컬 SVG/PNG로 만든다.
- 외부 URL 핫링크를 남기지 않는다. 모든 결과 페이지는 로컬 상대경로 asset으로 열려야 한다.
- 모바일 출력 전에 줄바꿈, 가격표/배지 돌출, 닫히지 않은 도형, 가로 overflow, 깨진 이미지를 먼저 잡는다.
- 최종 산출물은 사용자가 지정한 폴더가 없으면 `~/Desktop/team-skills/상세페이지/event-campaign/{campaign-slug}/`에 둔다.

## 작업 순서

1. 입력 확인: 원본 HTML 경로, 레퍼런스 이미지, 캠페인명/라이브 일정/가격/혜택, 썸네일 문구를 확인한다.
2. 복사본 생성: HTML을 새 이름으로 복사하고 새 CSS 파일을 링크한다. 기존 디자인 파일은 건드리지 않는다.
3. 무드 변환: 레퍼런스에서 팔레트, 폰트 느낌, 구획선, 일러스트, 사진 비율을 추출해 페이지에 적용한다.
4. 모바일 정리: 390px, 430px, 535px 폭에서 텍스트 줄바꿈과 요소 돌출을 확인한다. 긴 한국어 문장은 `<br>` 또는 `word-break: keep-all; overflow-wrap: break-word;`로 정리한다.
5. 시각 검수: 브라우저 또는 Playwright로 깨진 이미지, 가로 overflow, 흐린 출력, 닫히지 않은 SVG path를 확인한다.
6. JPG 출력: `scripts/export-event-assets.mjs`로 전체 모바일 JPG와 섹션별 JPG를 만든다.
7. 썸네일: 같은 톤앤매너로 정방형 HTML을 만들고 2160px 이상 JPG로 출력한다.

## 내보내기 스크립트

처음 한 번만 의존성을 설치한다.

```bash
cd /Users/inkyo/Projects/team-skills/skills/promotion/event-page-campaign/scripts
npm install
```

전체 모바일 JPG와 섹션별 JPG:

```bash
node /Users/inkyo/Projects/team-skills/skills/promotion/event-page-campaign/scripts/export-event-assets.mjs \
  --html "/path/to/event-page.html" \
  --mode all \
  --mobile-width 430 \
  --scale 3 \
  --quality 92
```

정방형 썸네일 JPG:

```bash
node /Users/inkyo/Projects/team-skills/skills/promotion/event-page-campaign/scripts/export-event-assets.mjs \
  --html "/path/to/thumbnail-square.html" \
  --mode thumb \
  --thumb-size 1080 \
  --scale 2 \
  --quality 92
```

주요 옵션:

| 옵션 | 기본값 | 설명 |
|---|---:|---|
| `--mode` | `all` | `page`, `sections`, `thumb`, `all` |
| `--out` | 자동 | 결과 폴더. 미지정 시 Desktop/team-skills 하위에 생성 |
| `--mobile-width` | `430` | 모바일 CSS viewport 폭 |
| `--scale` | `3` | deviceScaleFactor. 430px x 3 = 1290px JPG |
| `--quality` | `92` | JPG 품질 |
| `--section-selector` | 자동 | 섹션 분할 셀렉터 |
| `--strict` | off | 깨진 이미지/가로 overflow 발견 시 실패 코드 반환 |

## 결과물 구조

```text
~/Desktop/team-skills/상세페이지/event-campaign/{campaign-slug}/
├── mobile/
│   └── {slug}-mobile.jpg
├── sections/
│   ├── 01-hero.jpg
│   ├── 02-benefit.jpg
│   └── ...
├── thumbnail/
│   └── {slug}-thumbnail-square.jpg
└── export-report.json
```

## 품질 체크

- 모바일 전체 JPG 폭은 최소 `1290px` 이상으로 만든다.
- Cafe24 업로드가 부담되면 전체 1장 대신 `sections/*.jpg`를 사용한다.
- `export-report.json`의 `brokenImages`가 비어 있어야 한다.
- `horizontalOverflow`가 `false`여야 한다. 장식 구름/별이 화면 밖으로 나가면 실제 업로드 이미지에서도 어색하게 보인다.
- 버튼/가격표/라이브 일정 배지는 텍스트 길이에 따라 width가 늘어나도록 `inline-flex`, `width: fit-content`, `white-space: nowrap` 조합을 우선한다.
- 썸네일은 1:1 캔버스 안에서 LIVE 버튼, 날짜, 메인 타이틀이 잘리지 않아야 한다.

## 함께 쓰기 좋은 스킬

- `sundayhug-live-thumbnail`: 이미 확정된 SundayHug 쇼핑라이브 썸네일 스타일을 그대로 재사용할 때
- `pdp-section-capture`: PDP HTML을 섹션별 고해상도 이미지로 자를 때
- `tone-match-local`: 제품 이미지를 레퍼런스 톤에 맞춰 일괄 보정할 때
