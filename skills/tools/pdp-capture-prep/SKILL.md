---
name: pdp-capture-prep
description: SundayHug PDP(상세페이지) HTML·CSS를 이미지 캡처 최적화 상태로 일괄 변환. IntersectionObserver 기반 스크롤 리빌(.v/.on) 제거, 본문·라벨 폰트 1차(+2px) 키움, 원격 Cafe24 CSS 참조를 로컬 경로로 치환. `pdp-section-capture` 스킬 **실행 전에** 이 전처리를 돌리면 JS 없이 정적 렌더가 깔끔해지고(빈 섹션 없음) 이미지에 글씨가 더 잘 보임. 원본 CSS의 구조는 유지하면서 캡처 용도 최적화만 적용.
triggers: PDP 최적화, 캡처 전처리, .v 제거, 스크롤 리빌 제거, IntersectionObserver 정리, 폰트 키우기, Cafe24 CSS 로컬화, 이미지 다운로드 최적화, capture prep, 상세페이지 정적화
---

# PDP Capture Prep

SundayHug 상세페이지를 **이미지 캡처 최적화 상태**로 일괄 변환하는 전처리 스킬. `pdp-section-capture`(실제 이미지 출력) 실행 **전에** 돌려두면 결과물 품질이 크게 올라감.

## 언제 쓰는가

- Cafe24 업로드용 섹션 PNG를 대량으로 뽑기 전에 HTML/CSS를 한 번 최적화하고 싶을 때
- 상세페이지가 `IntersectionObserver` + `.v { opacity:0 }` 패턴으로 되어있어 JS 없으면 섹션이 빈 공간으로 렌더될 때
- 작은 모바일 폰트(11~15px)가 캡처에서 가독성 떨어져 1차(+2px)로 일괄 상향하고 싶을 때
- `abc/` 폴더 등에서 CSS가 `https://sundayhugkr.cafe24.com/skin-skin69/...` 원격 참조라 로컬 변경사항이 반영 안 될 때

## 무엇을 하는가 (4가지 작업)

### 1. HTML: IntersectionObserver `<script>` 제거
상세페이지 공통 인라인 스크립트:
```html
<script>
const io=new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}});
},{threshold:.1,rootMargin:'0px 0px -40px 0px'});
document.querySelectorAll('.v').forEach(el=>io.observe(el));
</script>
```
→ 완전 제거. 함수가 섞인 `<script>`는 손대지 않음(설정 가능한 disqualifier 리스트로 보호).

### 2. HTML: 원격 Cafe24 CSS → 로컬 경로
```
<link rel="stylesheet" href="https://sundayhugkr.cafe24.com/skin-skin69/product/details/styles.css">
↓
<link rel="stylesheet" href="../product/details/styles.css">
```
파일 위치에 따라 상대경로 자동 계산.

### 3. CSS: `.v` 리빌 규칙 제거
삭제 대상(주석 포함):
```css
/* ---------- Animations ---------- */
@keyframes rise { ... }
.pdp-absolute .v { opacity: 0 }
.pdp-absolute .v.on { animation: rise .55s ease-out forwards }
```
이후 `class="v"`는 CSS 규칙 매칭 없는 **dead class**로 무해하게 유지.

### 4. CSS: 1차(+2px) 폰트 상향
**데스크톱 베이스**: 새 override 블록 추가 (@media 직전)
- 라벨류(sec-label, sec-eyebrow, hero-tag 등): 16px
- 본문(sec-body, sec-desc, feat-desc 등): 19px
- cmp-list / cmp-hd / product-info-tbl / trust-bar-item: 16px
- mid-cta a: 15px / color-card-name: 12px

**모바일 `@media (max-width:480px)` 블록**: 같은 값으로 일치
- 라벨 12→16, 본문 15→19, cmp/tbl/trust 13→16, line-height 1.85→1.75

## 사용법

```bash
python3 /Users/inkyo/Projects/team-skills/skills/tools/pdp-capture-prep/scripts/optimize-pdp-for-capture.py \
  <project-root-dir> [--dry-run]
```

### 권장 워크플로우

```bash
# 1. 캡처 전처리
python3 /Users/inkyo/Projects/team-skills/skills/tools/pdp-capture-prep/scripts/optimize-pdp-for-capture.py \
  "/Users/inkyo/Desktop/상세페이지 local (최종본)"

# 2. 캡처 스킬 일괄 실행 (pdp-section-capture 이용한 batch 드라이버)
for html in $(grep -rl 'class="pdp-absolute"' <root> --include="*.html" | grep -v product/detail.html); do
  node .../render-sections-smart.mjs "$html" "$(dirname $html)/$(basename $html .html)_sections" .pdp-absolute 600 3 png 92 4
done
```

## 안전장치 (Idempotent)

이 스크립트는 **여러 번 돌려도 안전**:
- HTML IO script 제거: 이미 없으면 no-op
- CSS 리빌 블록 제거: 이미 없으면 no-op
- 1차 override 블록 추가: 기존 감지하면 스킵
- 모바일 폰트 값 업데이트: 이미 1차 값이면 no-op

## `--dry-run` 옵션

실제 파일 수정 없이 **변경될 내용만 리포트**:
```bash
python3 optimize-pdp-for-capture.py <root> --dry-run
```

## 검증된 효과

### Before (원본 CSS/HTML)
- 섹션 캡처 시 `.v` 요소가 빈 공간으로 나옴 (opacity:0 유지)
- 모바일 본문 15px → 이미지 축소 시 글자 흐릿
- `abc/` 페이지: Cafe24 원격 CSS 사용 → 로컬 변경 무시

### After (이 스킬 적용)
- 모든 섹션이 첫 페인트부터 정상 렌더
- 본문 19px / 라벨 16px → 이미지에서 선명하게 읽힘
- 모든 페이지가 로컬 CSS 참조 → 일관된 스타일

## 검증 완료 환경

- macOS (M1/Intel)
- Python 3.10+
- 테스트 대상: 59개 SundayHug PDP HTML (sleeping-bags, newborn, outlet, abc, set-products, daily-look, sleep-products)
- 결과: 4가지 작업 모두 idempotent, 2회 연속 실행 시 2번째는 변경 0건

## `pdp-section-capture`와의 관계

| 스킬 | 역할 | 실행 시점 |
|---|---|---|
| **pdp-capture-prep** (이 스킬) | CSS/HTML을 캡처 친화적으로 최적화 | 1단계 (전처리) |
| **pdp-section-capture** | 최적화된 페이지를 섹션별 PNG로 출력 | 2단계 (캡처) |

단발성 캡처면 `pdp-section-capture`만 써도 IntersectionObserver neuter로 동작 가능. 여러 번 캡처하거나 소스 파일 자체를 깨끗한 정적 상태로 보존하고 싶으면 이 스킬을 먼저 돌려서 **원본 자체를 최적화**하는 것이 효율적.
