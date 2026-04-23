# Card News Creator GUI

Streamlit 기반 카드뉴스 생성 웹 인터페이스

## 빠른 시작

```bash
# 1. 의존성 설치
pip install -r requirements.txt
playwright install chromium

# 2. 실행
streamlit run app.py
```

## 내부 공유 방법

### 같은 네트워크 (WiFi) 내 공유
```bash
streamlit run app.py --server.address 0.0.0.0
```
- 터미널에 표시되는 **Network URL** (예: `http://192.168.x.x:8501`)을 팀원에게 공유

### ngrok으로 외부 공유
```bash
# ngrok 설치 (처음 1회)
brew install ngrok  # Mac
# 또는 https://ngrok.com/download

# 실행
ngrok http 8501
```
- ngrok이 제공하는 URL (예: `https://xxxx.ngrok.io`)을 공유

### Streamlit Community Cloud (무료)
1. GitHub에 코드 업로드
2. [share.streamlit.io](https://share.streamlit.io) 접속
3. GitHub repo 연결 → 자동 배포

## 기능

### 1. 콘텐츠 추출 (탭 1)
- YouTube URL → 자막 자동 추출
- 웹페이지 URL → 본문 텍스트 추출
- 직접 텍스트 입력

### 2. 카드 편집 (탭 2)
- 카드 유형: cover, content, info, summary
- 각 카드별 내용 편집
- AI 이미지 프롬프트 설정
- 개별 이미지 생성

### 3. 미리보기 & 내보내기 (탭 3)
- 전체 카드 미리보기
- 모든 이미지 일괄 생성
- JSON 구조 내보내기
- ZIP 파일로 이미지 다운로드

## 설정 (사이드바)

- **API 키**: Google Gemini API 키 입력
- **브랜드명**: 카드에 표시될 브랜드
- **색상 테마**: warm, cool, dark, minimal, vibrant
- **카드 수**: 5-12장 선택
- **이미지 스타일**: AI 이미지 생성 스타일 프롬프트

## 파일 구조

```
gui/
├── app.py           # 메인 Streamlit 앱
├── requirements.txt # 의존성 목록
└── README.md        # 이 파일
```

## 문제 해결

### API 키 오류
```bash
# API 키 재설정
python3 ../scripts/gemini_image_api.py --setup
```

### 포트 충돌
```bash
# 다른 포트로 실행
streamlit run app.py --server.port 8502
```

### 이미지 생성 실패
- 프롬프트를 더 단순하게 수정
- API 일일 한도 확인 (무료: 15 images/day)
