---
name: detail-page-sections
description: 상세페이지 모듈형 섹션 템플릿 시스템 (27개 섹션)
triggers:
  - "상세페이지 만들어줘"
  - "상세페이지 섹션"
  - "detail page sections"
---

# 상세페이지 모듈형 섹션 시스템

27개의 재사용 가능한 섹션 템플릿으로 상세페이지를 조립합니다.

## 페이지 조립 흐름

[시선포착] → [신뢰확보] → [문제인식] → [해결책제시] → [구매유도] → [사회적증거] → [프로모션] → [상세정보] → [감성마무리] → [최종전환]

## 구조

- `sections/` — 27개 모듈형 HTML 섹션 템플릿
- `GUIDE.md` — 섹션별 설명 및 조립 가이드
- `_base-styles.css` — 공통 디자인 시스템 CSS
- `_animations.js` — 스크롤 애니메이션 라이브러리
- `template-guide.html` — 비주얼 가이드
- `scripts/` — CSS 빌드 자동화 도구

## 스크립트

- `scripts/_build_common_css.py` — 여러 HTML에서 CSS를 추출하여 _common.css로 병합
- `scripts/_apply_common_css.py` — HTML 파일들에 공통 CSS 적용 (인라인 스타일 제거)

## 사용법

1. `sections/` 에서 필요한 섹션 선택
2. 순서대로 조립하여 상세페이지 HTML 완성
3. `_base-styles.css` 링크 추가
4. 콘텐츠/이미지 교체
5. 필요시 `scripts/` 도구로 CSS 통합
