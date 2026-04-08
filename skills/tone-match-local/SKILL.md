---
name: tone-match-local
description: |
  레퍼런스 이미지의 톤/색감을 상품 이미지에 배치로 적용합니다.
  Gemini AI를 사용하여 색감, 분위기, 컬러 그레이딩을 일괄 변환합니다.
  "톤 매치 해줘", "색감 맞춰줘", "톤앤매너 변환해줘" 요청 시 사용합니다.
---

# 톤 매치 로컬 스킬

레퍼런스 이미지의 색감/톤/분위기를 상품 이미지 폴더에 일괄 적용합니다.

## 필수 요구사항

### 환경변수
- `GOOGLE_AI_API_KEY`: Google AI Studio API 키

### 설치
```bash
cd content-marketing-team-main/.claude/skills/tone-match-local/scripts
npm install
```

## 워크플로우

### 1단계: 환경 확인
- `GOOGLE_AI_API_KEY` 환경변수 존재 확인
- 레퍼런스 이미지 파일 존재 확인
- 입력 폴더에 이미지 파일(.jpg, .jpeg, .png, .webp) 존재 확인
- 필요시 `cd scripts && npm install` 실행

### 2단계: 실행

```bash
node content-marketing-team-main/.claude/skills/tone-match-local/scripts/batch-tone-match.mjs \
  --reference <레퍼런스 이미지> \
  --input <상품 이미지 폴더> \
  [옵션]
```

### 3단계: 선택 옵션

| 옵션 | 값 | 기본값 | 설명 |
|------|-----|--------|------|
| `--output` | 폴더 경로 | `<input>-toned` | 출력 폴더 |
| `--intensity` | `0-100` | `70` | 톤 변환 강도 |
| `--model` | `gemini-2.5-flash` / `gemini-3-pro` | `gemini-2.5-flash` | AI 모델 선택 |
| `--concurrency` | 숫자 | `2` | 동시 처리 수 |

### 4단계: 결과 확인
- 출력 폴더에 `{원본이름}-toned.png` 파일 생성
- 처리 결과 요약 (성공/실패 수)

## 사용 예시

```bash
# 기본 사용
"product-photos 폴더 이미지를 warm-tone.jpg 톤으로 맞춰줘"

# 강도 조절
"상품사진 톤 매치 해줘. 레퍼런스 ref.png, 강도 50%"

# 고품질 모델
"images/ 폴더를 brand-ref.jpg 색감으로 변환. 고품질 모델로"

# 전체 옵션
node scripts/batch-tone-match.mjs \
  --reference ./ref.jpg \
  --input ./products \
  --output ./toned \
  --intensity 50 \
  --model gemini-3-pro \
  --concurrency 1
```

## 참조 파일
- `references/tone-guide.md`: 강도별 효과 및 활용 가이드

## 주의사항

1. 상품의 형태/색상은 보존됩니다 (톤만 변경)
2. 흑백 레퍼런스 사용 시 흑백으로 변환됩니다
3. 대량 처리 시 429 에러 방지를 위해 `--concurrency 1` 권장
4. 출력은 PNG 형식
