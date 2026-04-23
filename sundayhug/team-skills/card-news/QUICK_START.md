# 카드뉴스 빠른 시작 가이드

## 설치 확인

```bash
# 필수 패키지
pip install youtube-transcript-api playwright requests pyyaml beautifulsoup4 PyPDF2

# Playwright 브라우저 설치
playwright install chromium
```

## 기본 사용법

### 1. YouTube 영상으로 카드뉴스 만들기

```
이 유튜브 영상으로 카드뉴스 만들어줘
https://www.youtube.com/watch?v=xxxxx
```

### 2. 웹페이지로 카드뉴스 만들기

```
이 블로그 글 카드뉴스로 변환해줘
https://blog.example.com/article
```

### 3. PDF로 카드뉴스 만들기

```
이 PDF 파일 카드뉴스로 만들어줘
~/documents/report.pdf
```

## 카드 구조

| 카드 | 내용 |
|------|------|
| 1 (표지) | 제목 + 부제목 |
| 2-8 (본문) | 핵심 내용 (6-7장) |
| 9 (요약) | 핵심 정리 |
| 10 (CTA) | 행동 유도 |

## 출력 위치

```
card-news/output/
├── project-name/
│   ├── card-01.png
│   ├── card-02.png
│   └── ...
```

## 브랜드 스타일

기본: Sunday Hug 스타일
- 메인 컬러: #A38068 (다크 브라운)
- 배경: #FFFBF5 (크림)

## 문제 해결

### 자막 추출 실패
- 자막이 없는 영상은 자동 생성 자막 사용
- 비공개 영상은 접근 불가

### 이미지 생성 실패
- Playwright 브라우저 설치 확인
- 나노바나 API 설정 확인
