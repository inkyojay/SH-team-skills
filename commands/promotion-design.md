---
name: promotion-design
description: 썬데이허그 프로모션 디자인 제작. 확정된 기획서를 바탕으로 채널별 디자인 산출물을 논의하고, 병렬로 .pen 디자인 제작.
triggers:
  - "프로모션 디자인"
  - "프로모션 디자인 제작"
  - "디자인 제작"
  - "promotion design"
---

# 프로모션 디자인 제작 스킬

확정된 기획서(.json)를 바탕으로 디자인 산출물을 논의하고, `promotion-designer` 에이전트를 병렬 스폰하여 .pen 디자인을 제작합니다.

## Phase 1: 기획서 로딩

### 기획서 찾기

```
1. Glob으로 "{{WORKSPACE_DIR}}/output/*/plan.json" 검색
2. 여러 개면 사용자에게 선택 요청 (폴더명 = 프로젝트 슬러그)
3. 하나면 바로 로드
4. 없으면 "/promotion-plan 먼저 실행하세요" 안내
```

### 데이터 추출

JSON 파일을 Read로 읽어 핵심 정보를 추출합니다:

```
- promotion_name, slug
- concept, key_message, tone_manner
- products (이름, 가격, 할인가)
- offer (혜택)
- period (기간)
- channels (채널 목록)
- deliverables (예상 산출물)
- look_and_feel (디자인 방향)
- visual_references (룩앤필 레퍼런스 이미지)
- materials (디자인 소재 사진)
```

로드 후 사용자에게 요약 확인:

```markdown
## 기획서 로드 완료

**{promotion_name}**
- 컨셉: {concept}
- 기간: {period}
- 채널: {channels}
- 룩앤필: {look_and_feel}
- 레퍼런스: {visual_references 수}장
- 디자인 소재: {materials.photos 수}장
- 예상 산출물: {deliverables 수}개
```

### 룩앤필 + 소재 확인

plan.json에 `visual_references`가 있으면:
1. 각 레퍼런스 이미지를 Read로 열어 디자인 톤 파악
2. `look_and_feel` 방향 확인

plan.json에 `materials`가 있으면:
1. `materials.base_dir` 하위 사진들을 Glob으로 탐색
2. 각 사진을 Read로 열어 확인
3. `use_in` 매핑에 따라 채널별 사진 배정 확인

둘 다 없으면:
- 사용자에게 "레퍼런스 이미지나 소재 사진을 추가하시겠습니까?" 확인
- 없으면 브랜드 기본 스타일로 진행

## Phase 2: 디자인 논의

### 채널별 포맷 제시

`references/channel-specs.md`를 읽어 기획서의 채널 목록에 해당하는 포맷을 표로 제시합니다.

```markdown
## 제작 가능한 디자인

| # | 채널 | 포맷 | 사이즈 | 레퍼런스 수 |
|---|------|------|--------|-----------|
| 1 | 인스타그램 | 스토리 | 1080x1920 | 5장 |
| 2 | 네이버 | PC 배너 | 1920x860 | 3장 |
| ...

어떤 디자인을 제작할까요? (번호로 선택, 또는 전부)
```

### 레퍼런스 이미지 확인

사용자가 선택한 포맷의 레퍼런스 이미지를 Read 도구로 보여줍니다.
레퍼런스 이미지 경로: `{{WORKSPACE_DIR}}/{폴더경로}/{파일명}`

```markdown
이 스타일을 참고하여 디자인하겠습니다.
특별히 원하는 스타일이 있으면 알려주세요.
```

### 새 소재 수집

제품 사진 등 새로운 소재가 있는지 확인합니다:

```markdown
디자인에 사용할 제품 사진이 있으신가요?
- 있다면 파일 경로를 알려주세요
- 없으면 AI로 생성하겠습니다
```

## Phase 3: 산출물 확정

최종 디자인 목록을 테이블로 작성하고 사용자 확인을 받습니다.

```markdown
## 최종 디자인 목록

| # | 채널 | 포맷 | 사이즈 | 레퍼런스 | 출력파일 |
|---|------|------|--------|---------|---------|
| 1 | 인스타그램 | 스토리 | 1080x1920 | 프로모션 스토리 1.png | insta-story.pen |
| 2 | 네이버 | PC 배너 | 1920x860 | pc_메인배너.png | naver-pc.pen |
| ...

이대로 디자인 제작을 시작할까요?
```

## Phase 4: 병렬 디자인 실행

사용자 확인 후, 팀을 만들고 병렬로 디자인을 제작합니다.

### 팀 생성

```
TeamCreate:
  team_name: "promo-{slug}"
  description: "{promotion_name} 디자인 제작"
```

### 태스크 생성

산출물별로 TaskCreate:

```
TaskCreate:
  subject: "{채널} {포맷} 디자인 제작"
  description: |
    채널: {channel}
    포맷: {format}
    사이즈: {width}x{height}
    레퍼런스: {reference_path}
    출력: {{WORKSPACE_DIR}}/output/{slug}/{output_filename}
    프로모션명: {promotion_name}
    핵심메시지: {key_message}
    혜택: {offer}
    기간: {period}
    톤앤매너: {tone_manner}
    소재경로: {material_path 또는 "없음"}
```

### 에이전트 스폰

각 산출물별로 `promotion-designer` 에이전트를 Task tool로 병렬 스폰합니다.

```
Task:
  subagent_type: "promotion-designer"
  team_name: "promo-{slug}"
  name: "designer-{n}"
  prompt: |
    당신은 promotion-designer 에이전트입니다.
    다음 디자인을 .pen 파일로 제작하세요.

    ## 디자인 정보
    - 채널: {channel}
    - 포맷: {format}
    - 사이즈: {width} x {height}
    - 레퍼런스 이미지: {{WORKSPACE_DIR}}/{reference_path}
    - 출력 경로: {{WORKSPACE_DIR}}/output/{slug}/{output_filename}

    ## 프로모션 컨텍스트
    - 프로모션명: {promotion_name}
    - 핵심 메시지: {key_message}
    - 혜택: {offer}
    - 기간: {period}
    - 톤앤매너: {tone_manner}
    - 대상 제품: {products}

    ## 룩앤필 방향
    - 전체 방향: {look_and_feel}
    {visual_references가 있으면 각각:}
    - 레퍼런스: {ref.path} — {ref.note}

    ## 디자인 소재 사진
    {이 채널에 배정된 소재 사진:}
    - {photo.category}: {materials.base_dir}/{photo.path} — {photo.description}
    (use_in에 이 채널이 포함되거나 "all"인 사진만 전달)

    ## 디자인 가이드
    1. 룩앤필 레퍼런스 이미지가 있으면 Read로 열어 색감/무드 파악
    2. 디자인 소재 사진이 있으면 Read로 열어 확인, .pen에 이미지 노드로 배치
    3. 채널 레퍼런스 이미지를 Read로 확인하여 스타일/레이아웃 파악
    4. references/pen-templates.md에서 해당 채널 템플릿 참조
    5. references/design-system.md의 브랜드 컬러/타이포 준수
    6. open_document("new")로 새 .pen 생성
    7. batch_design으로 디자인 구성 (소재 사진 포함)
    8. get_screenshot으로 결과 확인
    9. 태스크 완료 보고

    디자인 레퍼런스 파일 경로:
    - design-system: {{REPO_DIR}}/skills/promotion/promotion-design/references/design-system.md
    - pen-templates: {{REPO_DIR}}/skills/promotion/promotion-design/references/pen-templates.md
```

**중요**: 산출물이 여러 개면 가능한 한 병렬로 스폰합니다 (한 메시지에 여러 Task tool 호출).

## Phase 5: 검토

### 스크린샷 확인

각 에이전트가 완료하면:

1. 완성된 .pen 파일을 Pencil `get_screenshot`으로 캡처
2. 스크린샷을 사용자에게 제시
3. 피드백 수집

```markdown
## 디자인 결과

### 1. 인스타그램 스토리
[스크린샷]
- 파일: {slug}-insta-story.pen

### 2. 네이버 PC 배너
[스크린샷]
- 파일: {slug}-naver-pc.pen

수정이 필요한 부분이 있으면 알려주세요.
```

### 피드백 반영

수정 요청이 있으면:
1. 해당 .pen 파일을 `open_document`로 열기
2. `batch_design`의 Update(U) 오퍼레이션으로 수정
3. 다시 `get_screenshot`으로 확인

## Phase 6: 완료

모든 디자인이 확정되면:

```markdown
## 프로모션 디자인 완료

**{promotion_name}** 디자인이 완료되었습니다.

### 산출물
| # | 파일 | 채널 | 포맷 |
|---|------|------|------|
| 1 | insta-story.pen | 인스타그램 | 스토리 |
| 2 | naver-pc.pen | 네이버 | PC 배너 |
| ...

모든 파일 위치: `{{WORKSPACE_DIR}}/output/{slug}/`
```

팀을 해체합니다:
- 모든 에이전트에 shutdown_request 전송
- TeamDelete 실행

## 주의사항

- 기획서 JSON이 없으면 `/promotion-plan`으로 안내하세요
- 레퍼런스 이미지는 Read로 실제 확인 후 스타일을 파악하세요
- 병렬 에이전트는 서로 독립적으로 작업합니다 (교차 의존 없음)
- 디자인 시스템(`design-system.md`)의 브랜드 컬러/타이포를 반드시 준수하세요
- pen-templates.md의 변수({HEADLINE} 등)를 실제 값으로 치환하세요
- 팀 이름은 `promo-{slug}` 형식을 사용합니다
