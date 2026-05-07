---
name: tone-match-local
description: |
  레퍼런스 이미지의 톤/색감을 상품 이미지에 배치(batch)로 적용하는 스킬.
  Gemini 이미지 모델을 사용하여 색감, 분위기, 컬러 그레이딩을 일괄 변환합니다.

  **실행 전 필수 확인**: 사용자에게 먼저 어떤 톤으로 변환할지 물어본다.
  - 사용자가 별도 레퍼런스 이미지를 지정하면 → 그 이미지로 처리
  - 별 대답이 없거나 "그냥 디폴트로 해줘" / "브랜드 톤으로 해줘" 등이면
    → `references/default-mood/` 폴더의 SundayHug 디폴트 무드 이미지(잔디밭 위 키즈 화이트 룩) 사용

  "톤 매치 해줘", "색감 맞춰줘", "톤앤매너 변환해줘" 요청 시 사용합니다.
triggers:
  - "톤 매치"
  - "톤앤매너 변환"
  - "색감 맞춰줘"
  - "브랜드 톤으로"
  - "이미지 톤 변환"
  - "tone match"
  - "color grading"
---

# Tone Match Local — 브랜드 톤 일괄 변환

레퍼런스 이미지의 색감/톤/분위기를 상품 이미지 폴더에 일괄 적용한다.

## 🚨 사용 전 필수 단계 (Step 0)

**스킬 발동 직후, 항상 사용자에게 먼저 물어본다:**

> "어떤 톤으로 변환할까요? 별도 레퍼런스 이미지가 있으면 경로/파일명 알려주세요. 특별한 답이 없으면 SundayHug 디폴트 브랜드 무드(잔디밭 키즈 화이트 룩)로 진행할게요."

`AskUserQuestion`으로 다음 4지선다를 권장:
1. **디폴트 브랜드 톤 사용 (Recommended)** — `references/default-mood/`의 무드 이미지
2. **새 레퍼런스 이미지 경로 입력** — 사용자가 절대경로 제공
3. **미디어 대시보드에서 고르기** — MCP `media-dashboard`로 검색
4. **조용히 디폴트로 진행** — 별 답 없이 바로 디폴트 사용

답이 모호하거나 "그냥 알아서" / "디폴트로" 류 응답이면 1번으로 fallback.

## 환경 요구사항

### 환경변수
- `GOOGLE_AI_API_KEY` — Google AI Studio API 키

### 설치 (최초 1회)
```bash
cd skills/tone-match-local/scripts
npm install
```

## 워크플로우

### Step 1. 사용자 톤 의도 확인 (위 Step 0)

### Step 2. 레퍼런스 이미지 결정
- **사용자 지정 시**: 그 경로 사용
- **디폴트 fallback**: `--reference` 인자 생략 → 스크립트가 자동으로 `references/default-mood/` 의 첫 이미지를 사용
- **디폴트가 비어있으면**: 사용자에게 "디폴트 무드 이미지가 아직 등록되지 않았습니다. `skills/tone-match-local/references/default-mood/` 폴더에 이미지를 넣어주세요"라고 안내

### Step 3. 입력 폴더/옵션 확인
- 입력 폴더에 이미지(.jpg, .jpeg, .png, .webp) 존재 확인
- 강도(intensity), 모델, 동시 처리 수 결정 (사용자 의견 우선, 미지정 시 기본값)

### Step 4. 실행

```bash
# 사용자 레퍼런스 사용
node skills/tone-match-local/scripts/batch-tone-match.mjs \
  --reference <레퍼런스 이미지 경로> \
  --input <상품 이미지 폴더>

# 디폴트 브랜드 톤 사용 (--reference 생략)
node skills/tone-match-local/scripts/batch-tone-match.mjs \
  --input <상품 이미지 폴더>
```

### Step 5. 옵션

| 옵션 | 값 | 기본값 | 설명 |
|------|-----|--------|------|
| `--reference` | 이미지 경로 | `references/default-mood/`의 첫 이미지 | 톤 레퍼런스 (생략 가능) |
| `--input` | 폴더 경로 | (필수) | 변환할 상품 이미지 폴더 |
| `--output` | 폴더 경로 | `<input>-toned` | 출력 폴더 |
| `--intensity` | `0-100` | `70` | 톤 변환 강도 |
| `--model` | `gemini-2.5-flash` / `gemini-3-pro` | `gemini-2.5-flash` | AI 모델 |
| `--concurrency` | 숫자 | `2` | 동시 처리 수 |

### Step 6. 결과 확인
- 출력 폴더에 `{원본이름}-toned.png` 생성
- 처리 결과 요약 (성공/실패 수)
- 결과는 `~/Desktop/team-skills/이미지/` 같은 사용자 Desktop 하위로 옮기는 게 일반적 (CLAUDE.md 규칙)

## 사용 예시

```bash
# 기본: 디폴트 브랜드 톤으로 일괄 변환
"product-photos 폴더 이미지를 우리 브랜드 톤으로 맞춰줘"
→ --reference 생략, --input ./product-photos

# 다른 레퍼런스 사용
"product-photos 폴더 이미지를 ./ref-warm.jpg 톤으로 맞춰줘"

# 강도 조절
"상품사진 톤 매치, 강도 50%로 약하게"

# 고품질 모델
"images/ 폴더 톤 변환. Gemini 3 Pro로 고품질"
```

## 디폴트 브랜드 톤 이미지 (Default Mood)

`references/default-mood/` 폴더의 첫 이미지를 사용한다.

**현재 디폴트 무드**: 잔디밭 위 키즈 화이트/크림 룩 — 자연광, 차분하고 자연스러운 어스 톤. SundayHug 브랜드 무드보드의 핵심 비주얼.

**디폴트 교체 방법**: `references/default-mood/` 안의 기존 이미지를 지우고 새 이미지를 넣으면 된다. 파일명은 자유.

## 참조 파일
- `references/tone-guide.md` — 강도별 효과 및 활용 가이드
- `references/default-mood/` — 디폴트 브랜드 무드 이미지 보관소
- `references/default-mood/README.md` — 디폴트 무드 관리 안내

## 주의사항

1. 상품의 형태/색상은 보존됩니다 (톤만 변경)
2. 흑백 레퍼런스 사용 시 흑백으로 변환됩니다
3. 대량 처리 시 429 에러 방지를 위해 `--concurrency 1` 권장
4. 출력은 PNG 형식
5. **Step 0 (사용자 의도 확인)을 절대 건너뛰지 말 것** — 잘못된 톤으로 수십 장 일괄 변환되면 비용/시간 손실 큼
