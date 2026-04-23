---
name: meta-ad-factory
description: 메타(Facebook/Instagram) 광고 소재를 벌크로 자동 생성하는 스킬. 제품 URL + 이미지를 입력하면 ① USP 자동 분석 → ② 타겟/톤별 카피 매트릭스 생성 → ③ 메타 광고 규격별 HTML 크리에이티브 벌크 생성 → ④ 미리보기 그리드 → ⑤ 선택한 소재만 최종 이미지(PNG) 변환까지 전체 파이프라인을 실행한다. 다음 상황에서 반드시 이 스킬을 사용한다: "메타 광고 만들어줘", "페이스북 광고 소재", "인스타 광고", "광고 크리에이티브", "광고 소재 벌크", "광고 배너 만들어줘", "SNS 광고 이미지", "퍼포먼스 마케팅 소재", "DA 소재 제작", "메타 광고 카피", "광고 에셋 생성", "A/B 테스트 소재", "리타겟팅 광고 소재" 요청 시. 제품 이미지와 URL만 있으면 수십 개의 광고 소재를 한 번에 생성 가능.
---

# Meta Ad Factory — 메타 광고 소재 벌크 생성 스킬

## 개요

제품 URL + 이미지 업로드 → USP 분석 → 카피 매트릭스 → HTML 크리에이티브 벌크 생성 → 미리보기 → 선택 소재 PNG 변환

## 전체 워크플로우

### STEP 0: 인풋 수집 (대화형)

사용자에게 다음을 확인한다:

1. **제품 정보**: URL 또는 직접 입력 (제품명, 가격, 핵심 특징)
2. **이미지**: 업로드된 이미지 확인 (`/mnt/user-data/uploads/` 체크)
3. **프로모션 정보** (선택): 할인율, 이벤트명, 기간
4. **타겟 오디언스** (선택): 기본값은 references/target-audiences.md 참조
5. **톤 선호** (선택): 감성 / 정보형 / 긴급성 / 전체

인풋이 충분하면 바로 STEP 1로 진행. URL이 있으면 `web_fetch`로 제품 정보 자동 추출.

### STEP 1: USP 분석

제품 정보에서 핵심 USP를 도출한다.

**분석 프레임워크:**
- **기능적 USP**: 소재, 기술, 특허, 규격 등 객관적 차별점
- **감성적 USP**: 사용 경험, 라이프스타일, 감정적 베네핏
- **사회적 USP**: 리뷰, 입소문, 전문가 추천, 수상 등 사회적 증거
- **경제적 USP**: 가격 대비 가치, 프로모션, 번들 혜택

**출력**: USP 3~5개를 도출하고, 각각에 대해:
- 한 줄 요약 (헤드라인용)
- 상세 설명 (본문용)  
- 키 비주얼 방향 제안

사용자에게 USP 분석 결과를 보여주고 확인/수정 받은 후 STEP 2로 진행.

### STEP 2: 카피 매트릭스 생성

`references/copy-frameworks.md`를 참조하여 카피 세트를 생성한다.

**매트릭스 구조**: USP × 톤 × CTA

| 요소 | 변형 |
|------|------|
| USP | STEP 1에서 도출한 3~5개 |
| 톤 | 감성(Emotional), 정보(Informational), 긴급(Urgency) |
| CTA | 구매하기, 더 알아보기, 할인 받기, 무료배송 |

**각 카피 세트 구성:**
- `primary_text`: 본문 (125자 이내 권장, 최대 3줄)
- `headline`: 헤드라인 (40자 이내 권장)
- `description`: 설명 (30자 이내 권장)
- `cta`: CTA 버튼 텍스트

카피 매트릭스를 표로 보여주고 확인 받은 후 STEP 3으로 진행.

### STEP 3: HTML 크리에이티브 벌크 생성

`references/layout-templates.md`와 `references/meta-ad-specs.md`를 참조하여 HTML 광고 소재를 생성한다.

**생성 규격:**

| 포맷 | 사이즈 | 용도 |
|------|--------|------|
| 1:1 | 1080×1080 | 피드 (FB/IG 공통) |
| 4:5 | 1080×1350 | IG 피드 최적 |
| 9:16 | 1080×1920 | 스토리/릴스 |

**레이아웃 타입:**

1. **hero-image**: 이미지 전면 + 텍스트 오버레이 (그라데이션 배경)
2. **split-horizontal**: 좌우 분할 (이미지 | 카피)
3. **split-vertical**: 상하 분할 (이미지 위 | 카피 아래)
4. **benefit-stack**: USP 아이콘/텍스트 나열 + 제품 이미지
5. **social-proof**: 리뷰/별점 강조 + 제품
6. **urgency**: 타임세일/한정수량 배지 + 카운트다운 느낌

**생성 전략:**
- 모든 조합을 만들지 않는다. 스마트 조합으로 핵심 소재를 생성:
  - 이미지별 × 베스트 레이아웃 2~3개 × 사이즈 3개
  - 카피는 톤별로 로테이션
  - 예상 총 생성량: **15~30개**

**HTML 생성 규칙:**
- 각 소재는 독립된 HTML 파일 (inline CSS, 외부 의존성 없음)
- 이미지는 base64 인코딩으로 HTML에 임베드
- 한글 폰트: Google Fonts CDN (Pretendard or Noto Sans KR)
- 브랜드 컬러 적용 (기본: `#1D9E75` / 사용자 지정 가능)
- 파일명 규칙: `{번호}_{레이아웃}_{사이즈}_{톤}.html`

**미리보기 그리드 HTML 생성:**
- 모든 소재를 한 화면에서 볼 수 있는 그리드 뷰 HTML
- 소재별 체크박스로 선택 가능
- 필터: 사이즈별, 레이아웃별, 톤별
- 파일명: `preview-grid.html`

모든 HTML 파일을 `/home/claude/meta-ads/` 에 생성한 후 preview-grid.html을 `/mnt/user-data/outputs/`에 복사하여 사용자에게 제공.

### STEP 4: 사용자 선택 & 최종 이미지 변환

사용자가 미리보기에서 마음에 드는 소재를 선택하면:

**방법 A: Python Pillow로 PNG 변환** (기본)
```
1. 한글 폰트 설치 (Noto Sans KR)
2. 선택된 HTML의 레이아웃을 Pillow로 재구성
3. 이미지 + 텍스트 + 오버레이 합성
4. PNG로 출력
```

**방법 B: Gemini 이미지 생성 API** (사용자 API 키 필요)
```
1. HTML 소재의 구성 요소를 프롬프트로 변환
2. Gemini API로 고품질 이미지 생성
3. 제품 이미지는 원본 유지, 배경/분위기만 AI 생성
```

**방법 C: HTML 그대로 활용**
```
1. HTML 파일 자체를 최종 산출물로 제공
2. 사용자가 브라우저 스크린샷으로 직접 캡처
```

**출력물:**
- 선택된 소재의 최종 이미지 파일 (PNG)
- 카피 CSV 파일 (메타 광고 관리자 벌크 업로드용)
- 전체 에셋을 zip으로 패키징

### STEP 5: 카피 CSV 내보내기

메타 광고 관리자 벌크 업로드용 CSV를 생성한다.

```csv
ad_name,primary_text,headline,description,cta,image_file,size
```

## 핵심 생성 로직 (STEP 3 상세)

### HTML 크리에이티브 생성 프로세스

```
1. /mnt/user-data/uploads/ 에서 이미지 로드
2. 이미지를 base64로 인코딩
3. 각 조합(이미지 × 레이아웃 × 사이즈 × 카피)에 대해:
   a. references/layout-templates.md에서 해당 레이아웃 HTML 템플릿 로드
   b. 사이즈에 맞게 뷰포트/컨테이너 조정
   c. 카피 세트 삽입
   d. 이미지 base64 삽입
   e. 브랜드 컬러/폰트 적용
   f. 독립 HTML 파일로 저장
4. preview-grid.html 생성 (iframe으로 각 소재 임베드)
```

### Python 이미지 변환 프로세스 (STEP 4)

```bash
# 필요 패키지 설치
pip install Pillow --break-system-packages

# 한글 폰트 다운로드
wget -q "https://github.com/google/fonts/raw/main/ofl/notosanskr/NotoSansKR%5Bwght%5D.ttf" \
  -O /home/claude/NotoSansKR.ttf
```

```python
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import base64, io

# 이미지 로드 → 리사이즈 → 텍스트 오버레이 → 저장
```

## 브랜드 기본값 (썬데이허그)

- 프라이머리 컬러: `#1D9E75`
- 세컨더리 컬러: `#F5F0EB`
- 액센트: `#FF6B35`
- 폰트: Pretendard (대체: Noto Sans KR)
- 톤: 따뜻하고 신뢰감 있는, 육아 전문가 느낌

사용자가 다른 브랜드 제품을 요청하면 URL에서 컬러/톤을 자동 추출하거나 직접 지정 받는다.

## 참조 파일

- `references/meta-ad-specs.md` → 메타 광고 규격, 텍스트 제한, 권장사항
- `references/layout-templates.md` → 레이아웃별 HTML/CSS 템플릿
- `references/copy-frameworks.md` → 카피 생성 프레임워크, 톤별 가이드
- `references/target-audiences.md` → 타겟 오디언스 세그먼트 정의

**STEP 3 실행 전 반드시 `references/layout-templates.md`를 읽어야 한다.**
**STEP 2 실행 전 반드시 `references/copy-frameworks.md`를 읽어야 한다.**
