---
name: batch-image-openai
description: |
  OpenAI gpt-image-2 모델로 이미지를 batch 생성/편집하는 스킬. 4가지 모드 지원 — (1) 생성: 빈 폴더에서 프롬프트로 새 이미지 N개, (2) 편집: 입력 폴더 이미지를 프롬프트로 일괄 변환, (3) 레퍼런스: 무드보드 이미지 분석 후 동일 스타일로 변환, (4) HTML: 상세페이지에서 자동 컨셉 추출 후 변환. 한글 프롬프트 자동 영문 번역, 1024×1024/1536×1024/1024×1536 사이즈, low/medium/high 품질, 투명 배경(PNG/WebP) 지원. 비용 사전 표시 (이미지당 medium $0.053), 동시 처리 가능. "이미지 생성", "OpenAI 이미지", "gpt-image", "DALL-E batch", "이미지 변환 OpenAI", "image generation batch", "openai 이미지 일괄" 요청 시 사용. Gemini 버전(batch-image-transform)과 동일 패턴이지만 OpenAI 모델 사용 — 텍스트 렌더링(한/중/일) 정확, 1K~4K 출력, 최대 16장 멀티 레퍼런스 지원이 특징.
---

# Batch Image OpenAI — gpt-image-2 batch 생성/편집

## 필수 요구사항

### 환경변수
- `OPENAI_API_KEY`: OpenAI API 키 (필수)
- `OPENAI_ORG`: 조직 ID (선택)

### 설치
```bash
cd skills/batch-image-openai/scripts
npm install
```

---

## 4가지 모드

| 모드 | 옵션 | 설명 |
|---|---|---|
| **A. Generate** | `--generate --prompt "..." --n 5` | 빈 폴더에서 프롬프트로 새 이미지 N개 생성 |
| **B. Edit** | `--edit --input <폴더> --prompt "..."` | 입력 폴더 이미지를 프롬프트로 일괄 변환 |
| **C. Reference** | `--edit --input <폴더> --reference <이미지>` | 레퍼런스 이미지 분석 → 같은 스타일로 변환 |
| **D. HTML** | `--edit --input <폴더> --html <file.html>` | 상세페이지에서 컨셉 추출 → 변환 |

---

## 사용 예

### Mode A — 새 이미지 생성
```bash
node openai-image.mjs \
  --generate \
  --prompt "감성적인 아기 침대 라이프스타일 컷, 따뜻한 자연광, 화이트크림 톤" \
  --n 5 \
  --size 1024x1536 \
  --quality medium \
  --output ./out
```

### Mode B — 입력 이미지 톤 변환
```bash
node openai-image.mjs \
  --edit \
  --input ./photos \
  --prompt "따뜻한 황금빛 자연광, 미니멀 라이프스타일"
```

### Mode C — 레퍼런스 이미지 매칭
```bash
node openai-image.mjs \
  --edit \
  --input ./photos \
  --reference ./mood-board.png
```

### Mode D — 상세페이지 톤에 맞춰
```bash
node openai-image.mjs \
  --edit \
  --input ./photos \
  --html ./detail.html
```

---

## 주요 옵션

| 옵션 | 기본값 | 설명 |
|---|---|---|
| `--model` | `gpt-image-2` | OpenAI 이미지 모델 |
| `--size` | `1024x1024` | `1024x1024` / `1536x1024` (가로) / `1024x1536` (세로) / `auto` |
| `--quality` | `medium` | `low` / `medium` / `high` / `auto` |
| `--n` | `1` | 생성 개수 (generate 모드) |
| `--concurrency` | `2` | 병렬 처리 수 |
| `--format` | `png` | `png` / `jpeg` / `webp` |
| `--transparent` | off | 투명 배경 (png/webp 만) |
| `--output` | `<input>-output` 또는 `./out` | 출력 폴더 |
| `--prompt-only` | off | 실제 호출 안 하고 생성될 프롬프트만 출력 |

---

## 가격 (gpt-image-2, 이미지당 USD)

| 사이즈 | low | medium | high |
|---|---|---|---|
| 1024×1024 | $0.006 | **$0.053** | $0.211 |
| 1024×1536 | $0.005 | $0.041 | $0.165 |
| 1536×1024 | $0.005 | $0.041 | $0.165 |

스킬은 실행 전 예상 비용을 자동으로 표시합니다. **default는 medium** — 비용/품질 밸런스 최적.

---

## 한글 프롬프트 처리

스킬이 자동으로:
1. 한글 감지
2. `gpt-4o-mini`로 영문 번역
3. gpt-image-2에 전달

별도 번역 작업 불필요. 한국어 그대로 입력하면 됨.

---

## 워크플로우

### 1단계: 환경 확인
- `OPENAI_API_KEY` 설정 확인
- 의존성 설치: `cd scripts && npm install`

### 2단계: 모드 판별
사용자 요청에서 자동 판별:
- "생성", "만들어줘", "create" → **Generate**
- "변환", "톤 바꿔", "transform" → **Edit + Prompt**
- 무드보드/레퍼런스 이미지 첨부 → **Edit + Reference**
- "이 상세페이지 톤으로" → **Edit + HTML**

### 3단계: 실행 + 비용 사전 안내
실행 전 예상 비용 출력 → 사용자가 진행 결정.

### 4단계: 결과물 저장
- `~/Desktop/team-skills/이미지생성/{캠페인명}/` 권장
- Mode B/C/D는 `<input>-output/` 자동 생성

---

## 결과물 저장 규칙

CLAUDE.md 규칙에 따라:
```bash
node openai-image.mjs --generate --prompt "..." --output ~/Desktop/team-skills/이미지생성/spring-collection
```

폴더가 없으면 자동 생성.

---

## Gemini 버전과의 차이

| 항목 | batch-image-transform (Gemini) | batch-image-openai (이 스킬) |
|---|---|---|
| 모델 | gemini-2.5-flash | gpt-image-2 |
| API 키 | `GOOGLE_AI_API_KEY` | `OPENAI_API_KEY` |
| 모드 | edit (변환) 중심 | generate + edit (둘 다) |
| 텍스트 렌더링 | 보통 | 우수 (한/중/일 정확) |
| 출력 해상도 | 1024×1024 | 1024 / 1536 / 4K |
| 가격 (1024 medium) | $0.039 | $0.053 |

용도에 따라 선택 — 변환만 필요하면 Gemini 버전이 더 저렴, 텍스트가 들어가는 디자인이나 새 이미지 생성은 이 스킬.

---

## Trigger Examples

- "OpenAI로 아기침대 라이프 컷 5장 만들어줘"
- "이 사진들 황금빛 톤으로 변환 (gpt-image-2)"
- "레퍼런스 이미지 무드 따라서 일괄 변환"
- "상세페이지 톤에 맞춰 광고 이미지 새로 뽑기"
- "openai image batch 생성"
- "DALL-E batch 변환"

---

## Reference

- [prompt-guide.md](./references/prompt-guide.md) — 프롬프트 작성 팁 + 자주 쓰는 패턴
- OpenAI 공식 문서:
  - [gpt-image-2 모델](https://developers.openai.com/api/docs/models/gpt-image-2)
  - [Image generation guide](https://developers.openai.com/api/docs/guides/image-generation)
