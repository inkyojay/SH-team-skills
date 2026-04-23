# PHASE 5 — 로컬 PC에서 네이버 API 실행 가이드

## 왜 로컬 PC에서 실행하나?

Claude 환경(claude.ai)에서는 네이버 검색광고 API 도메인(`api.searchad.naver.com`)에 대한 네트워크 접근이 차단될 수 있다. 이 경우 사용자의 로컬 PC에서 직접 스크립트를 실행하면 정확한 검색량 데이터를 확보할 수 있다.

## 사전 준비

### 1. Python 설치 확인
```bash
python --version
# Python 3.8 이상 필요
```
설치 안 되어 있으면: https://www.python.org/downloads/ 에서 다운로드

### 2. requests 라이브러리 설치
```bash
pip install requests
```

### 3. 네이버 검색광고 API 인증 정보 확인
- 네이버 검색광고 시스템 접속: https://searchad.naver.com/
- [도구] → [API 사용 관리]에서 확인:
  - API 라이선스 키 (Access License)
  - 시크릿 키 (Secret Key)
  - 고객 ID (Customer ID) — 광고 관리 화면 상단에 표시

## 실행 방법

### 기본 실행
```bash
python naver_keyword_search.py \
  --api-key "YOUR_API_KEY" \
  --secret-key "YOUR_SECRET_KEY" \
  --customer-id "YOUR_CUSTOMER_ID" \
  --keywords "아기 쿨매트 추천,냉감 슬리핑백,아기 냉감패드,국내산 아기 쿨매트" \
  --output keyword_results.json
```

### 키워드가 많은 경우 (파일로 입력)
키워드를 텍스트 파일에 한 줄에 하나씩 작성한 후:
```bash
# keywords.txt 만들기
아기 쿨매트 추천
냉감 슬리핑백 추천
아기 냉감패드
국내산 아기 쿨매트
아기 여름밤 자주 깨요
...

# 파일에서 읽어서 실행
python naver_keyword_search.py \
  --api-key "YOUR_API_KEY" \
  --secret-key "YOUR_SECRET_KEY" \
  --customer-id "YOUR_CUSTOMER_ID" \
  --keywords "$(cat keywords.txt | tr '\n' ',')" \
  --output keyword_results.json
```

## 결과 확인

실행 완료 후 `keyword_results.json` 파일이 생성된다. 이 파일에는:
- 키워드별 월간 PC/모바일 검색량
- 경쟁 정도 (높음/중간/낮음)
- 월평균 클릭수/클릭률
- 골든/성장/빅/니치 등급 자동 분류

## 결과를 Claude에 전달하는 방법

JSON 결과 파일을 다음 대화에서 Claude에게 공유하면 리포트를 업데이트할 수 있다:

1. **파일 업로드**: `keyword_results.json` 파일을 Claude 대화에 업로드
2. **복사 붙여넣기**: 콘솔에 출력된 결과 요약을 복사하여 전달
3. **리포트 연동**: "이 검색량 데이터로 리포트 업데이트해줘"라고 요청

## 자주 겪는 문제

| 문제 | 해결 방법 |
|------|---------|
| `HTTP 401` 에러 | API 키/시크릿 키 확인. 키에 앞뒤 공백이 없는지 체크 |
| `HTTP 403` 에러 | 고객 ID 확인. 검색광고 계정에 API 사용 권한이 활성화되어 있는지 확인 |
| `ModuleNotFoundError: requests` | `pip install requests` 실행 |
| 검색량이 `< 10`으로 나옴 | 정상. 매우 적은 검색량을 가진 키워드의 경우 네이버가 정확한 수치 대신 `< 10`으로 표시 |
| 일부 키워드 결과 없음 | 너무 긴 키워드나 특수문자가 포함된 경우 API가 인식하지 못할 수 있음 |
