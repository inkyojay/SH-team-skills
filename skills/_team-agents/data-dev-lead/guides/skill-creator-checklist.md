# 신규 스킬 등록 체크리스트

## 등록 전 검증

### 1. 중복 스킬 검사
- [ ] `SKILL-CATALOG.md`에서 비슷한 스킬 검색
- [ ] 비슷하면 기존 스킬 확장으로 가능한지 검토 (중복 방지)

### 2. 폴더 구조
- [ ] `skills/{category}/{name}/` 폴더 생성
- [ ] `SKILL.md` 진입점 작성
- [ ] 필요 시 `assets/`, `templates/`, `scripts/`, `guides/` 하위 폴더

### 3. SKILL.md frontmatter 필수 필드
```yaml
---
name: 스킬명 (kebab-case)
description: |
  무엇을 / 언제 / 어떻게 사용
  최소 3~5문장
triggers:
  - "한국어 트리거 1"
  - "영문 트리거 1"
  - (4~10개)
---
```

### 4. 트리거 키워드 충돌 검사
```bash
grep -r "트리거후보" skills/*/SKILL.md
```
- 다른 스킬에 같은 트리거 있는지 확인
- 충돌 시 키워드 변경 또는 통합 협의

### 5. 결과물 저장 경로
- [ ] CLAUDE.md 규칙 (`~/Desktop/team-skills/{카테고리}/`) 따름
- [ ] 절대경로 사용 시 `Path.home() / "Desktop"` 패턴
- [ ] `mkdir -p` 또는 `parents=True`로 자동 생성

### 6. 환경변수 / API 키
- [ ] 필요한 환경변수 SKILL.md 본문에 명시
- [ ] 신규 키 필요 시 `api-key-management.md`에도 추가
- [ ] 평문 노출 절대 X

### 7. 호환성 검사
- [ ] Python 스크립트는 `python3 -m py_compile` 통과
- [ ] Node 스크립트는 `node --check` 통과
- [ ] Bash 스크립트는 `bash -n` 통과

## 등록 절차

```bash
# 1. 폴더 + SKILL.md 작성 완료
# 2. 카탈로그 갱신
./scripts/update-docs.sh

# 3. SKILL-CATALOG.md / 사용가이드.html에 신규 항목 확인
grep "신규-스킬-이름" SKILL-CATALOG.md

# 4. 트리거 키워드 충돌 최종 확인
grep -h "^triggers" skills/*/SKILL.md | sort | uniq -c | sort -rn | head

# 5. 데이터팀장이 SKILL_DETAILS dict에 등록 (scripts/generate-catalog.py)
# - desc / usecases / capabilities / output 4종 추가
# - 사용가이드.html 우측 상세 패널에 표시되도록

# 6. 사용자에게 시범 호출 요청 (트리거 키워드로)
```

## 등록 후

- [ ] 영향 받는 에이전트의 `skills-map.md` 업데이트
- [ ] 필요 시 `INDEX.md`의 워크플로우 다이어그램 갱신
- [ ] Desktop 미러 갱신 (해당되면)

## 흔한 실수

1. **`./scripts/update-docs.sh` 빠뜨림** → 카탈로그 미갱신
2. **트리거 키워드 충돌** → 의도치 않은 스킬 발동
3. **결과물 저장 경로 위반** → 프로젝트 폴더에 저장됨 (Git 부담)
4. **환경변수 평문 하드코딩** → 보안 사고
5. **`SKILL_DETAILS` dict 누락** → 사용가이드.html에 풍부한 정보 안 보임

## 새 스킬을 만들기 전에 자문

1. 기존 스킬 + 호출 체인으로 가능한가? (가능하면 만들지 마라)
2. 사용 빈도가 분기 5회 이상인가? (미만이면 만들 가치 의문)
3. 다른 스킬과 트리거 충돌하지 않는가?
4. 결과물이 자동 평가 가능한가? (검증 어려우면 안정성 문제)
