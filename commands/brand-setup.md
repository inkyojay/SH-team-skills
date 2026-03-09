---
name: brand-setup
description: 새 브랜드 초기 설정 마법사
triggers:
  - "브랜드 설정"
  - "새 브랜드 추가"
  - "브랜드 초기화"
---

# 브랜드 설정 마법사

새 브랜드 초기 설정을 도와주는 마법사입니다.

## 트리거
- "브랜드 설정해줘"
- "새 브랜드 추가"
- "브랜드 초기화"

## 설정 프로세스

### Step 1: 기본 정보
- 브랜드명
- 카테고리
- 타겟 고객

### Step 2: 비주얼 아이덴티티
- 주요 컬러 (Primary, Secondary, Accent)
- 폰트 스타일
- 로고 정보

### Step 3: 브랜드 퍼스낼리티
- 핵심 가치
- 톤앤매너
- 권장/금지 표현

### Step 4: 제품 정보
- 주요 제품 라인업
- 가격대
- 차별화 포인트

### Step 5: 경쟁사 설정
- 주요 경쟁 브랜드
- 벤치마킹 포인트

## 출력 파일

```
.reference/brands/{brand-name}/
├── brand-guide.md      # 브랜드 가이드라인
├── products.json       # 제품 데이터베이스
├── competitors.md      # 경쟁사 분석
└── target-customers.md # 타겟 페르소나
```

## 완료 후
- 다른 스킬에서 브랜드 정보 자동 참조
- `/update`로 정보 수정 가능
