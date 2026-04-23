---
name: batch-image-transform
description: |
  상품 이미지를 배치로 변환합니다. Gemini AI로 배경 교체/톤 변환을 일괄 처리합니다.
  "상품 이미지 변환해줘", "배치 이미지 변환", "이미지 일괄 변환" 요청 시 사용합니다.
---

# 배치 상품 이미지 변환 스킬

상품 이미지 폴더를 지정하면 Gemini AI로 배경 교체/장면 합성을 일괄 처리합니다.

## 필수 요구사항

### 환경변수
- `GOOGLE_AI_API_KEY`: Google AI Studio API 키

### 설치
```bash
cd content-marketing-team-main/.claude/skills/batch-image-transform/scripts
npm install
```

## 3가지 모드

| 모드 | 입력 | 설명 |
|------|------|------|
| A. 레퍼런스 | `--reference <이미지>` | 참조 이미지를 분석해서 동일 스타일로 변환 |
| B. HTML | `--html <파일>` | 상세페이지 HTML에서 촬영 컨셉 추출 후 변환 |
| C. 직접 프롬프트 | `--prompt "텍스트"` | 텍스트로 배경/장면 직접 지정 |

## 워크플로우

### 1단계: 환경 확인
- `GOOGLE_AI_API_KEY` 환경변수 존재 확인
- 입력 폴더에 이미지 파일(.jpg, .jpeg, .png, .webp) 존재 확인
- 필요시 `cd scripts && npm install` 실행

### 2단계: 모드 판별 및 실행

사용자 요청에서 모드를 판별합니다:

**Mode A - 레퍼런스 이미지 기반:**
```bash
node content-marketing-team-main/.claude/skills/batch-image-transform/scripts/batch-transform.mjs \
  --input ./product-photos \
  --reference ./reference.jpg \
  --output ./product-photos-output
```

**Mode B - HTML 상세페이지 기반:**
```bash
node content-marketing-team-main/.claude/skills/batch-image-transform/scripts/batch-transform.mjs \
  --input ./product-photos \
  --html ./detail-page.html \
  --output ./product-photos-output
```

**Mode C - 직접 프롬프트:**
```bash
node content-marketing-team-main/.claude/skills/batch-image-transform/scripts/batch-transform.mjs \
  --input ./product-photos \
  --prompt "Bright cafe table with natural sunlight, warm atmosphere" \
  --output ./product-photos-output
```

### 3단계: 선택 옵션

| 옵션 | 값 | 기본값 | 설명 |
|------|-----|--------|------|
| `--model` | `gemini-3-pro` / `gemini-2.5-flash` | `gemini-2.5-flash` | AI 모델 선택 |
| `--aspect-ratio` | `1:1` / `9:16` / `16:9` | `1:1` | 출력 비율 |
| `--appearance` | 텍스트 | (없음) | 인물 외모 프롬프트 |
| `--concurrency` | 숫자 | `2` | 동시 처리 수 |
| `--output` | 폴더 경로 | `<input>-output` | 출력 폴더 |

### 4단계: 결과 확인
- 출력 폴더에 `{원본이름}-transformed.png` 파일 생성
- 처리 결과 요약 (성공/실패 수, 소요 시간)

## 사용 예시

```bash
# 레퍼런스 이미지 스타일로 변환
"product-photos 폴더의 상품 사진들을 reference.jpg 스타일로 변환해줘"

# HTML 상세페이지 기반 변환
"product-photos 폴더 이미지들을 detail-page.html에 맞게 변환해줘"

# 직접 프롬프트로 변환
"product-photos 폴더 이미지들을 '밝은 카페 테이블 위, 자연광' 배경으로 변환해줘"

# 고품질 + 세로형
"product-photos 폴더를 gemini-3-pro 모델로, 9:16 비율로 변환해줘. 배경은 깔끔한 화이트 스튜디오"

# 전체 옵션
node scripts/batch-transform.mjs \
  --input ./product-photos \
  --prompt "Studio white background with soft lighting" \
  --model gemini-3-pro \
  --aspect-ratio 9:16 \
  --appearance "Young Korean woman, 20s, natural makeup" \
  --concurrency 1 \
  --output ./product-photos-vertical
```

## 참조 파일
- `references/prompt-guide.md`: 시나리오별 프롬프트 예시 및 비율 선택 가이드

## 주의사항

1. 한국어 프롬프트는 자동으로 영문 번역됩니다 (Gemini 2.0 Flash 사용)
2. 상품의 형태/색상/로고는 최대한 보존됩니다
3. 대량 처리 시 429 에러 방지를 위해 `--concurrency 1` 권장
4. `gemini-3-pro`: 고품질(~45초/장), `gemini-2.5-flash`: 빠름(~23초/장)
5. 출력은 PNG 형식
