#!/usr/bin/env python3
"""
스킬 카탈로그 & 사용 가이드 자동 생성기

사용법:
    python scripts/generate-catalog.py

출력:
    - SKILL-CATALOG.md (마크다운 카탈로그)
    - 사용가이드.html (HTML 가이드)
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 경로 설정
BASE_DIR = Path(__file__).parent.parent
SKILLS_DIR = BASE_DIR / "skills"
AGENTS_DIR = BASE_DIR / "agents"
TEMPLATES_DIR = BASE_DIR / "skills" / "video" / "remotion" / "templates"
OUTPUT_CATALOG = BASE_DIR / "SKILL-CATALOG.md"
OUTPUT_HTML = BASE_DIR / "사용가이드.html"

# 카테고리 한글 매핑
CATEGORY_NAMES = {
    "content-creation": "콘텐츠 제작",
    "video": "영상 제작",
    "advertising": "광고",
    "brand": "브랜드 관리",
    "marketing": "마케팅 전략",
    "tools": "유틸리티 도구",
    "design": "UI/UX 디자인",
    "frontend": "프론트엔드",
    "documents": "문서 도구"
}

CATEGORY_ICONS = {
    "content-creation": "📝",
    "video": "🎬",
    "advertising": "📢",
    "brand": "🏷️",
    "marketing": "📊",
    "tools": "🔧",
    "design": "🎨",
    "frontend": "💻",
    "documents": "📄"
}

CATEGORY_COLORS = {
    "content-creation": "#4CAF50",
    "video": "#9C27B0",
    "advertising": "#FF5722",
    "brand": "#2196F3",
    "marketing": "#FF9800",
    "tools": "#607D8B",
    "design": "#E91E63",
    "frontend": "#00BCD4",
    "documents": "#795548"
}

# 스킬 한국어 번역 (영어 스킬용)
SKILL_TRANSLATIONS = {
    # Marketing
    "ab-test-setup": "A/B 테스트 설계 및 실험 계획",
    "ab-test": "A/B 테스트 분석",
    "analytics-tracking": "애널리틱스 추적 설정",
    "competitor-alternatives": "경쟁사 비교 페이지 제작 (vs 페이지, 대안 페이지)",
    "competitor-analysis": "경쟁사 분석",
    "content-strategy": "콘텐츠 전략 수립 및 주제 기획",
    "copy-editing": "마케팅 카피 편집 및 개선",
    "copywriting": "마케팅 카피라이팅 (랜딩페이지, 홈페이지 등)",
    "email-sequence": "이메일 시퀀스 작성",
    "form-cro": "폼 최적화 (리드 캡처, 문의 폼 등)",
    "free-tool-strategy": "무료 툴 마케팅 전략",
    "launch-strategy": "런칭 전략 수립",
    "marketing-ideas": "마케팅 아이디어 140개 전술",
    "marketing-psychology": "마케팅 심리학 (70+ 멘탈 모델)",
    "onboarding-cro": "온보딩 최적화 (활성화율 개선)",
    "page-cro": "페이지 전환율 최적화 (CRO)",
    "paid-ads": "유료 광고 캠페인 (Google, Meta, LinkedIn 등)",
    "paywall-upgrade-cro": "페이월/업그레이드 화면 최적화",
    "popup-cro": "팝업/모달 최적화",
    "pricing-strategy": "가격 전략 수립",
    "product-marketing-context": "제품 마케팅 컨텍스트 문서 작성",
    "programmatic-seo": "프로그래매틱 SEO (대량 페이지 생성)",
    "referral-program": "추천 프로그램 설계",
    "schema-markup": "스키마 마크업 (구조화된 데이터)",
    "seo-audit": "SEO 감사 및 분석",
    "seo": "검색 엔진 최적화 (SEO) - 기술 SEO, 콘텐츠 전략, 키워드 분석",
    "signup-flow-cro": "회원가입 플로우 최적화",
    "social-content": "소셜 미디어 콘텐츠 제작",
    "canvas-design": "포스터/디자인 시각물 제작",
    "csv-analyzer": "CSV 데이터 분석",
    "data-report": "마케팅 데이터 분석 리포트",
    "review-management": "리뷰 관리",
    "social-media-designer": "소셜 미디어 디자인",
    "Social Media Designer": "플랫폼별 최적화된 소셜 미디어 그래픽 제작",
    "video-script": "영상 스크립트 작성",

    # Tools
    "hook-creator": "Claude Code 훅 생성",
    "skill-creator": "스킬 생성 가이드",
    "slash-command-creator": "슬래시 커맨드 생성",
    "subagent-creator": "서브에이전트 생성",
    "youtube-transcribe-skill": "유튜브 자막 추출",
    "youtube-collector": "유튜브 콘텐츠 수집",
    "capture-sections": "HTML 섹션별 이미지 캡처",
    "html-section-capture": "HTML 섹션별 이미지 변환",
    "html2img": "HTML을 이미지로 변환",
    "inline-css": "CSS 인라인 변환",
    "brainstorming": "창의적 작업 전 아이디어 브레인스토밍 도구",
    "crafting-effective-readmes": "효과적인 README 파일 작성 가이드",
    "release-skills": "스킬 릴리스 워크플로우 - 버전 관리 및 배포",
    "firecrawl": "웹 크롤링 및 스크래핑 도구",
    "nano-banana-pro": "Google Gemini 기반 이미지 생성/편집 도구",
    "apify-ultimate-scraper": "Apify 기반 웹 스크래핑 도구",
    "webapp-testing": "웹앱 테스트 도구",
    "feature-planner": "기능 계획 및 단계별 구현 전략 수립",

    # Documents
    "docx": "DOCX 문서 생성/편집/분석 도구",
    "pdf": "PDF 추출, 생성, 병합, 분할, 폼 처리 도구",
    "hwpx": "HWPX(아래아 한글) 문서 변환 도구",
    "pptx": "프레젠테이션(PPT) 생성/편집/분석 도구",
    "xlsx": "엑셀 스프레드시트 생성/편집/분석 도구",

    # Marketing (additional)
    "keyword-trend": "네이버 키워드 시즌 트렌드 분석",
    "keyword-optimizer": "네이버 키워드 최적화 + 시즌 트렌드 통합: 등급표(S/A/B/C/D) + 상품명 3안 + 태그 10개 + 월별 캘린더 + HTML 리포트",
    "new-product-planner": "신제품 기획 종합 도구 (시장조사~런칭 전략)",
    "gov-apply": "정부/기관 지원사업 신청서 대화형 작성 도구",

    # Video
    "remotion-best-practices": "Remotion 영상 제작 가이드",
    "reels-editor": "릴스 영상 편집 (9:16, 1080x1920)",

    # Content
    "card-news-creator": "카드뉴스 제작 (인스타그램 스타일)",
    "page-builder": "상세페이지 제작",

    # Brand
    "brand-dna": "브랜드 DNA 분석",
    "brand-dna-extractor": "웹사이트에서 브랜드 DNA 추출 및 무드보드 생성",
    "brand-guidelines": "브랜드 가이드라인 적용 (색상, 타이포그래피)",
    "brand-logo": "브랜드 로고 검색 및 다운로드",
    "brand-setup": "새 브랜드 초기 설정 마법사",
    "brand-updater": "브랜드 정보 업데이트 및 동기화",
    "product-analyzer": "제품 분석 리포트",

    # Advertising
    "meta-ads": "메타 광고 기획 및 제작",
    "meta-ad-image": "메타(인스타/페북) 광고 이미지 제작",
    "kakao-message": "카카오톡 비즈메시지 배너 제작",
    "live-banner": "쇼핑라이브 배너 제작 (네이버/카카오)",
    "smartstore-banner": "스마트스토어 배너 제작",
}

# 에이전트 한국어 번역
AGENT_TRANSLATIONS = {
    "brand-setup-wizard": "새 브랜드 초기 설정 마법사 - 질문을 통해 브랜드 정보 수집",
    "brand-updater": "브랜드 정보 업데이트 - 제품, 경쟁사, 캠페인 등 수정",
    "competitor-analyzer": "경쟁사 실시간 분석 - 제품, 가격, 마케팅, SNS, 리뷰 조사",
    "content-quality-reviewer": "콘텐츠 품질 검토 - 마케팅 콘텐츠 리뷰 및 개선점 제안",
    "data-report-analyzer": "데이터 분석 리포트 생성 - CSV, 엑셀, JSON 파일 분석",
    "market-researcher": "시장 및 트렌드 조사 - 소비자 인사이트, 기회 영역 발굴",
    "promotion-designer": "프로모션 디자인 실행 - .pen 파일 제작 (promotion-design 스킬에서 병렬 스폰)",
    "sundayhug-marketing-hub": "마케팅 총괄 오케스트레이터 - 스킬/에이전트 추천 및 워크플로우",
    "skill-orchestrator": "통합 오케스트레이터 - 사용자 의도 파악 및 스킬/에이전트 매칭",
}

# 스킬별 상세 정보 (사용 방법, 사례, 가능한 작업)
SKILL_DETAILS = {
    # 광고
    "meta-ad-factory": {
        "desc": "메타(인스타/페북) 광고 소재를 벌크 자동 생성. 제품당 21개 크리에이티브(4 레이아웃 × 3 사이즈 × 3 톤) + 로컬 서버 기반 인터랙티브 편집(📥 단건 PNG / ✏️ 텍스트·스타일 편집 / 🖼 AI 이미지 교체).",
        "usecases": [
            {"cmd": "메타 광고 만들어줘 [제품슬러그]", "note": "제품당 21개 소재 빌드"},
            {"cmd": "python3 server.py --slug swaddle-strap", "note": "브라우저에서 편집/다운로드"},
            {"cmd": "이미지 교체 / 카피 수정", "note": "preview-grid 각 카드 호버 버튼"},
        ],
        "capabilities": ["21개 소재 벌크 생성", "on-demand PNG 단건 다운로드", "텍스트+스타일(색/크기/굵기/배경) 편집", "Gemini AI 이미지 교체", "3개 사이즈(1:1/4:5/9:16)"],
        "output": "~/Desktop/team-skills/광고카피/sundayhug-meta-bulk/",
    },
    "naver-ads-reporter": {
        "desc": "네이버 검색광고 성과를 API로 조회해 캠페인/광고그룹/키워드/상품별 인터랙티브 HTML 리포트로 출력.",
        "usecases": [
            {"cmd": "네이버 광고 성과 리포트", "note": "기본 리포트 생성"},
            {"cmd": "지난 주 네이버 광고 분석", "note": "기간 지정"},
            {"cmd": "낭비 키워드 찾아줘", "note": "효율 분석"},
        ],
        "capabilities": ["노출/클릭/비용/전환 집계", "ROAS·CTR·CPC 계산", "WoW/MoM 비교", "이상치 탐지"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    # 마케팅 전략
    "new-product-planner": {
        "desc": "신제품 기획 종합 — 아이디어→시장조사→경쟁사→키워드→가격→마케팅→수익 시뮬레이션까지 13탭 HTML.",
        "usecases": [
            {"cmd": "신제품 기획해줘", "note": "전체 프로세스 대화형"},
            {"cmd": "이 제품 시장 조사해줘", "note": "시장 분석"},
            {"cmd": "신상품 수익 시뮬레이션", "note": "KPI 모델링"},
        ],
        "capabilities": ["브레인스토밍", "VOC·경쟁사 분석", "키워드 검색량", "가격/마케팅 전략", "13탭 리포트"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    "sundayhug-marketing-planner": {
        "desc": "썬데이허그 제품의 마케팅 전략을 USP→롱테일 키워드→채널별 액션플랜까지 자동 수립.",
        "usecases": [
            {"cmd": "마케팅 플랜 짜줘 [제품]", "note": "풀 플랜 생성"},
            {"cmd": "이 제품 롱테일 키워드 30개", "note": "키워드 발굴"},
            {"cmd": "주차별 액션플랜", "note": "캘린더 생성"},
        ],
        "capabilities": ["USP 자동 분석", "롱테일 키워드 30+", "채널별 콘텐츠 플랜", "비교 콘텐츠 전략"],
        "output": "~/Desktop/team-skills/",
    },
    "promotion-planner": {
        "desc": "프로모션 기획 + 인터랙티브 HTML. 시즌 매칭 → 월별 테마 → 채널별 액션플랜 → KPI까지.",
        "usecases": [
            {"cmd": "프로모션 기획해줘", "note": "기본 기획"},
            {"cmd": "여름 시즌 프로모션", "note": "시즌 특화"},
            {"cmd": "주차별 프로모션 플랜", "note": "상세 캘린더"},
        ],
        "capabilities": ["시즌 이벤트 매칭", "프로모션 유형 선정", "주차별 액션플랜", "KPI 목표"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    "competitive-intelligence": {
        "desc": "경쟁사 분석 & 시장 모니터링. 단일 심층분석 또는 전체 시장 모니터링 두 모드 지원.",
        "usecases": [
            {"cmd": "경쟁사 분석해줘 [브랜드]", "note": "단일 브랜드 심층"},
            {"cmd": "시장 모니터링 리포트", "note": "전체 시장"},
            {"cmd": "경쟁사 가격 변동", "note": "가격 추적"},
        ],
        "capabilities": ["제품 라인업·가격·프로모션", "리뷰/VOC 분석", "대비 비교", "트렌드 추적"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    "trend-radar": {
        "desc": "멀티소스 트렌드 데이터 수집·분석 (네이버/유튜브/인스타/레딧 등). 탭 구조 HTML 리포트.",
        "usecases": [
            {"cmd": "트렌드 분석해줘", "note": "종합 트렌드"},
            {"cmd": "이번 시즌 뭐가 뜨나", "note": "시즌 트렌드"},
            {"cmd": "육아 트렌드 리포트", "note": "카테고리 필터"},
        ],
        "capabilities": ["멀티소스 수집", "탭별 리포트", "content-pipeline/product-scout 연동"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    "product-scout": {
        "desc": "데이터 기반 신상품 기회 탐색 & 소싱 매칭. Go/Hold 액션 버튼 내장.",
        "usecases": [
            {"cmd": "신상품 기회 찾아줘", "note": "기회 스코어링"},
            {"cmd": "소싱 가능한 제품", "note": "매트릭스 출력"},
            {"cmd": "경쟁사 신규 제품", "note": "동향 추적"},
        ],
        "capabilities": ["기회 카드 TOP 10", "소싱 매트릭스", "경쟁사 동향", "Go/Hold 판단"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    "keyword-optimizer": {
        "desc": "네이버 키워드 최적화 + 시즌 트렌드 통합 스킬. 제품 하나에 대해 ① 시드 키워드 발굴 → ② 검색량/경쟁도 API 조회 → ③ DataLab 월별 트렌드 → ④ S/A/B/C/D 등급 스코어링 → ⑤ 스마트스토어 상품명 3안 (SEO 규칙 준수) → ⑥ 네이버 태그사전 기반 상품태그 10개 추천 → ⑦ 월별 마케팅 캘린더 → ⑧ Chart.js 트렌드 그래프 포함 HTML 통합 리포트까지 자동 생성.",
        "usecases": [
            {"cmd": "[상품] 키워드 최적화 해줘", "note": "전체 플로우 실행 → HTML 리포트"},
            {"cmd": "스마트스토어 상품명 추천", "note": "SEO 준수 3안 생성"},
            {"cmd": "상품태그 10개 추천", "note": "태그사전 등록 가능성 판단"},
        ],
        "capabilities": [
            "검색광고 API (시드 + 연관 키워드)",
            "DataLab 월별 시즌 트렌드",
            "S/A/B/C/D 등급 스코어링",
            "스마트스토어 상품명 3안 (50자/수식어 금지)",
            "상품태그 10개 + 대체 후보",
            "월별 마케팅 캘린더",
            "HTML 통합 리포트 (Chart.js)",
        ],
        "output": "~/Desktop/team-skills/리포트/YYYY-MM-DD_{상품}_키워드-최적화.html",
    },
    "keyword-trend": {
        "desc": '"언제 마케팅"할지 — 네이버 DataLab으로 월별 시즌 트렌드 분석, 성수기/피크 파악.',
        "usecases": [
            {"cmd": "이 키워드 시즌 트렌드", "note": "월별 검색량"},
            {"cmd": "성수기 찾아줘", "note": "피크 분석"},
            {"cmd": "마케팅 타이밍 분석", "note": "시즌 전략"},
        ],
        "capabilities": ["DataLab 월별 트렌드", "성수기/비수기 파악", "피크 시점 매칭"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    "instagram-reviewer": {
        "desc": "인스타그램 체험단 후보 발굴·검증. S~D 등급으로 참여율/자녀 연령 매칭 점수화.",
        "usecases": [
            {"cmd": "체험단 후보 찾아줘", "note": "해시태그 발굴"},
            {"cmd": "[해시태그] 인플루언서", "note": "해시태그 기반"},
            {"cmd": "체험단 검증", "note": "등급화"},
        ],
        "capabilities": ["해시태그 발굴", "유사 계정 추천", "S-D 등급 점수화", "자녀 연령 매칭"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    "content-pipeline": {
        "desc": "Trend Radar 인사이트 기반 멀티채널 콘텐츠 자동 기획·생산 파이프라인.",
        "usecases": [
            {"cmd": "콘텐츠 파이프라인 돌려줘", "note": "트렌드→콘텐츠 자동화"},
            {"cmd": "이 트렌드로 멀티채널 콘텐츠", "note": "여러 채널 동시"},
        ],
        "capabilities": ["트렌드 기반 기획", "멀티채널 자동 생산", "A/B 변형"],
        "output": "~/Desktop/team-skills/",
    },
    # 브랜드
    "product-analyzer": {
        "desc": "제품 분석 리포트 — 상세페이지/리뷰/스펙을 분석해 마케팅 포인트 도출.",
        "usecases": [
            {"cmd": "제품 분석해줘 [URL]", "note": "상세페이지 분석"},
            {"cmd": "USP 뽑아줘", "note": "소구점 추출"},
            {"cmd": "제품 리뷰 분석", "note": "VOC 분석"},
        ],
        "capabilities": ["상세페이지 파싱", "USP 추출", "리뷰 감성 분석", "마케팅 포인트"],
        "output": "~/Desktop/team-skills/리포트/",
    },
    # 유틸리티
    "batch-image-transform": {
        "desc": "Gemini AI로 상품 이미지 배경 교체/톤 변환을 배치로 일괄 처리. 3가지 모드(레퍼런스/HTML/프롬프트).",
        "usecases": [
            {"cmd": "이 이미지들 배경 카페로 바꿔줘", "note": "프롬프트 모드"},
            {"cmd": "레퍼런스 이미지 스타일 적용", "note": "레퍼런스 모드"},
            {"cmd": "상세페이지 컨셉으로 변환", "note": "HTML 모드"},
        ],
        "capabilities": ["Gemini Flash/Pro 사용", "3가지 입력 모드", "배치 처리", "4가지 비율"],
        "output": "~/Desktop/team-skills/기타/",
    },
    "tone-match-local": {
        "desc": "레퍼런스 이미지의 색감/톤/분위기를 상품 이미지에 일괄 적용. 구도·콘텐츠는 100% 보존.",
        "usecases": [
            {"cmd": "이 레퍼런스 톤으로 맞춰줘", "note": "톤 매칭"},
            {"cmd": "색감 통일해줘", "note": "일괄 적용"},
            {"cmd": "강도 70%로 톤 적용", "note": "강도 조절"},
        ],
        "capabilities": ["톤/색감 매칭", "0-100% 강도 조절", "구도 보존", "배치 처리"],
        "output": "~/Desktop/team-skills/기타/",
    },
    "pdp-section-capture": {
        "desc": "상세페이지 HTML을 디자인 단위 섹션별로 잘라 고해상도 PNG 시리즈로 출력. HTML 주석 기반.",
        "usecases": [
            {"cmd": "상세페이지 섹션별로 잘라줘", "note": "PNG 시리즈"},
            {"cmd": "이 HTML 이미지로 변환", "note": "섹션 캡처"},
        ],
        "capabilities": ["주석 기반 섹션 분할", "supersampling 고해상도", "IntersectionObserver 라이브 캡처"],
        "output": "~/Desktop/team-skills/상세페이지/",
    },
    # 문서 도구
    "docx": {
        "desc": "Word 문서 생성·편집·분석 도구. 템플릿 기반 자동 생성 지원.",
        "usecases": [
            {"cmd": "Word 문서 만들어줘", "note": "DOCX 생성"},
            {"cmd": "이 문서 편집해줘 [파일]", "note": "기존 문서 편집"},
        ],
        "capabilities": ["DOCX 생성/편집", "표/목차/헤더", "템플릿 지원"],
        "output": "~/Desktop/team-skills/기타/",
    },
    "xlsx": {
        "desc": "Excel 스프레드시트 생성·편집·분석 도구. 수식·차트·피벗 지원.",
        "usecases": [
            {"cmd": "엑셀 분석해줘 [파일]", "note": "데이터 분석"},
            {"cmd": "수익 시뮬레이션 엑셀", "note": "수식 생성"},
        ],
        "capabilities": ["수식/차트/피벗", "CSV 변환", "템플릿 보존"],
        "output": "~/Desktop/team-skills/기타/",
    },
    "pptx": {
        "desc": "PowerPoint 프레젠테이션 생성·편집·분석.",
        "usecases": [
            {"cmd": "PPT 만들어줘", "note": "새 프레젠테이션"},
            {"cmd": "이 내용으로 피치덱", "note": "피치덱 생성"},
        ],
        "capabilities": ["슬라이드 생성/편집", "레이아웃/템플릿", "차트 삽입"],
        "output": "~/Desktop/team-skills/기타/",
    },
    "pdf": {
        "desc": "PDF 추출·생성·병합·분할·폼 처리.",
        "usecases": [
            {"cmd": "이 PDF 분석해줘", "note": "텍스트/표 추출"},
            {"cmd": "PDF 병합해줘", "note": "여러 파일 합침"},
        ],
        "capabilities": ["텍스트/표 추출", "병합/분할", "폼 필드 채우기", "OCR"],
        "output": "~/Desktop/team-skills/기타/",
    },
    "hwpx": {
        "desc": "한글(HWP/HWPX) 문서 생성·읽기·편집.",
        "usecases": [
            {"cmd": "한글 문서 만들어줘", "note": "HWPX 생성"},
            {"cmd": "이 한글 파일 읽어줘", "note": "내용 추출"},
        ],
        "capabilities": ["HWPX 생성/편집", "OWPML", "한컴 호환"],
        "output": "~/Desktop/team-skills/기타/",
    },
}

# 에이전트별 상세 정보
AGENT_DETAILS = {
    "brand-setup-wizard": {
        "desc": "새 브랜드 초기 설정 마법사 — 질문을 통해 브랜드 정보를 수집하고 레퍼런스 파일 생성.",
        "usecases": [
            {"cmd": "브랜드 설정해줘", "note": "새 브랜드 설정"},
            {"cmd": "새 브랜드 추가", "note": "브랜드 추가"},
            {"cmd": "brand setup", "note": "영문 명령도 지원"},
        ],
        "workflow": ["질문 수집", "브랜드 정보 정리", "레퍼런스 파일 생성"],
    },
    "brand-updater": {
        "desc": "기존 브랜드의 제품·경쟁사·캠페인 등 특정 정보를 부분 수정.",
        "usecases": [
            {"cmd": "브랜드 수정해줘", "note": "부분 업데이트"},
            {"cmd": "경쟁사 업데이트", "note": "경쟁사만 수정"},
            {"cmd": "제품 추가해줘", "note": "제품 라인업 추가"},
        ],
        "workflow": ["변경 항목 선택", "사용자 입력 받기", "JSON/MD 부분 수정"],
    },
    "competitor-analyzer": {
        "desc": "웹 검색으로 경쟁 브랜드의 제품·가격·마케팅·SNS·리뷰 데이터를 실시간 수집·분석.",
        "usecases": [
            {"cmd": "경쟁사 분석해줘 [브랜드명]", "note": "특정 브랜드 분석"},
            {"cmd": "벤치마킹 리포트 만들어줘", "note": "비교 리포트"},
            {"cmd": "시장 조사해줘", "note": "시장 전체 조사"},
        ],
        "workflow": ["웹 검색", "데이터 수집", "분석", "리포트 생성"],
    },
    "content-quality-reviewer": {
        "desc": "생성된 마케팅 콘텐츠(상세페이지/광고/SNS)의 품질을 검토하고 개선점 제안.",
        "usecases": [
            {"cmd": "이 콘텐츠 검토해줘", "note": "품질 리뷰"},
            {"cmd": "피드백 줘", "note": "개선 포인트"},
            {"cmd": "품질 체크", "note": "체크리스트 기반"},
        ],
        "workflow": ["콘텐츠 파싱", "체크리스트 평가", "개선점 제시"],
    },
    "data-report-analyzer": {
        "desc": "CSV/엑셀/JSON 데이터 파일을 읽어 분석하고 인사이트를 도출해 리포트 생성.",
        "usecases": [
            {"cmd": "데이터 분석해줘 [파일]", "note": "기본 분석"},
            {"cmd": "매출 분석 리포트", "note": "재무 분석"},
            {"cmd": "광고 성과 분석", "note": "성과 리포트"},
        ],
        "workflow": ["데이터 읽기", "통계 분석", "시각화", "인사이트 도출"],
    },
    "market-researcher": {
        "desc": "시장/트렌드/소비자 인사이트를 웹 검색으로 조사. 베이비·육아 카테고리 특화.",
        "usecases": [
            {"cmd": "시장 조사해줘", "note": "종합 시장 분석"},
            {"cmd": "트렌드 분석", "note": "트렌드 리포트"},
            {"cmd": "기회 발굴", "note": "신규 기회 영역"},
        ],
        "workflow": ["키워드 기반 검색", "트렌드 수집", "인사이트 도출"],
    },
    "promotion-designer": {
        "desc": "특정 채널/포맷의 프로모션 디자인을 .pen 파일로 제작. promotion-design 스킬에서 병렬 스폰.",
        "usecases": [
            {"cmd": "프로모션 디자인해줘", "note": "메인 스킬에서 호출"},
        ],
        "workflow": [".pen 파일 열기", "batch_design 명령", "결과 저장"],
    },
    "skill-orchestrator": {
        "desc": "사용자 요청을 분석해 가장 적합한 스킬/에이전트를 추천하고 매칭.",
        "usecases": [
            {"cmd": "도와줘", "note": "무엇을 할 수 있는지 안내"},
            {"cmd": "뭐 할 수 있어?", "note": "가능한 작업 목록"},
            {"cmd": "마케팅 관련 작업해줘", "note": "의도 파악 후 매칭"},
        ],
        "workflow": ["의도 분석", "스킬/에이전트 매칭", "작업 위임", "결과 전달"],
    },
    "sundayhug-marketing-hub": {
        "desc": "썬데이허그 마케팅 업무 총괄 오케스트레이터. 복합 워크플로우 설계 및 실행.",
        "usecases": [
            {"cmd": "마케팅 도와줘", "note": "종합 지원"},
            {"cmd": "어떤 스킬 써야해?", "note": "스킬 추천"},
            {"cmd": "캠페인 기획해줘", "note": "복합 캠페인"},
        ],
        "workflow": ["요청 분석", "복합 워크플로우 설계", "스킬 체인 실행"],
    },
}

# 카테고리별 대표 예시 (사용자가 이해하기 쉬운 형태)
CATEGORY_EXAMPLES = {
    "content-creation": [
        "상세페이지 만들어줘",
        "카드뉴스 제작해줘",
        "제품 소개 페이지 작성"
    ],
    "video": [
        "릴스 영상 편집해줘",
        "Remotion으로 영상 만들어줘"
    ],
    "advertising": [
        "메타 광고 기획해줘",
        "광고 카피 써줘",
        "타겟 오디언스 분석"
    ],
    "brand": [
        "브랜드 분석해줘",
        "브랜드 아키타입 선정",
        "브랜드 네이밍"
    ],
    "marketing": [
        "랜딩페이지 CRO 분석",
        "마케팅 카피 작성",
        "가격 전략 세워줘",
        "이메일 시퀀스 만들어줘"
    ],
    "tools": [
        "HTML을 이미지로 변환",
        "이미지 생성해줘",
        "인포그래픽 만들어줘"
    ],
    "design": [
        "디자인 시스템 만들어줘",
        "컬러 팔레트 추천",
        "UI 컴포넌트 리뷰"
    ],
    "frontend": [
        "React 컴포넌트 만들어줘",
        "Tailwind로 스타일링",
        "반응형 레이아웃"
    ],
    "documents": [
        "PDF 생성해줘",
        "엑셀 분석해줘",
        "PPT 만들어줘",
        "한글(HWP) 문서 변환",
        "DOCX 편집해줘"
    ]
}


def parse_skill_md(skill_path: Path) -> dict:
    """SKILL.md 파일을 파싱하여 정보 추출"""
    skill_file = skill_path / "SKILL.md"
    if not skill_file.exists():
        return None

    content = skill_file.read_text(encoding="utf-8")

    # Frontmatter 파싱
    info = {
        "name": skill_path.name,
        "path": str(skill_path.relative_to(BASE_DIR)),
        "description": "",
        "triggers": []
    }

    # YAML frontmatter 추출
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)

        # name 추출
        name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
        if name_match:
            info["name"] = name_match.group(1).strip().strip('"\'')

        # 멀티라인 description 먼저 체크 (| 또는 > 로 시작하는 경우)
        desc_multi = re.search(r'^description:\s*[|>]\s*\n(.*?)(?=\n[a-z_]+:|\Z)', frontmatter, re.DOTALL | re.MULTILINE)
        if desc_multi:
            desc_lines = desc_multi.group(1).strip().split('\n')
            info["description"] = desc_lines[0].strip() if desc_lines else ""
        else:
            # description 추출 (한 줄짜리)
            desc_single = re.search(r'^description:\s*["\']?([^|\n][^\n]*)["\']?$', frontmatter, re.MULTILINE)
            if desc_single:
                info["description"] = desc_single.group(1).strip().strip('"\'')


        # triggers 추출
        triggers_match = re.search(r'triggers:\s*\n((?:\s*-\s*.+\n?)+)', frontmatter)
        if triggers_match:
            triggers = re.findall(r'-\s*["\']?(.+?)["\']?\s*$', triggers_match.group(1), re.MULTILINE)
            info["triggers"] = [t.strip('"\'') for t in triggers[:3]]

    # 본문에서 description 추출 (frontmatter에 없는 경우)
    if not info["description"]:
        body = re.sub(r'^---\n.*?\n---\n?', '', content, flags=re.DOTALL)
        # 첫 번째 일반 텍스트 단락 찾기
        lines = body.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-') and not line.startswith('*'):
                info["description"] = line[:100]
                break

    # description 정리 (frontmatter 잔재 제거)
    if info["description"]:
        info["description"] = re.sub(r'^---.*', '', info["description"]).strip()
        info["description"] = re.sub(r'^name:.*', '', info["description"]).strip()
        if len(info["description"]) > 80:
            info["description"] = info["description"][:80] + "..."
        # HTML-safe: escape <, >, & and strip HTML comment markers that would break the page layout
        info["description"] = (
            info["description"]
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    return info


def parse_agent_md(agent_path: Path) -> dict:
    """에이전트 .md 파일 파싱 - frontmatter 지원"""
    if not agent_path.exists():
        return None

    content = agent_path.read_text(encoding="utf-8")

    info = {
        "name": agent_path.stem.replace("-", " ").title(),
        "filename": agent_path.name,
        "description": "",
        "tools": [],
        "triggers": []
    }

    # YAML frontmatter 추출
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)

        # name 추출
        name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
        if name_match:
            info["name"] = name_match.group(1).strip().strip('"\'')

        # description 추출 (멀티라인 지원)
        desc_match = re.search(r'^description:\s*[|>]\s*\n(.*?)(?=\n[a-z_]+:|\Z)', frontmatter, re.DOTALL | re.MULTILINE)
        if desc_match:
            desc_lines = desc_match.group(1).strip().split('\n')
            # 첫 번째 의미있는 줄 사용
            info["description"] = desc_lines[0].strip() if desc_lines else ""
            # 트리거 문구 추출 (마지막 줄에 "~요청 시" 패턴이 있으면)
            for line in desc_lines:
                if '"' in line and '요청 시' in line:
                    triggers = re.findall(r'"([^"]+)"', line)
                    info["triggers"] = triggers[:4]
                    break
        else:
            # 한 줄짜리 description
            desc_match = re.search(r'^description:\s*["\']?([^\n]+)["\']?$', frontmatter, re.MULTILINE)
            if desc_match:
                desc = desc_match.group(1).strip().strip('"\'')
                info["description"] = desc

        # tools 추출
        tools_match = re.search(r'^tools:\s*(.+)$', frontmatter, re.MULTILINE)
        if tools_match:
            tools_str = tools_match.group(1).strip()
            if tools_str.startswith('['):
                # YAML 리스트 형식
                info["tools"] = [t.strip().strip('"\'') for t in tools_str.strip('[]').split(',') if t.strip() and t.strip() != '-']
            elif tools_str.startswith('-'):
                # YAML 블록 리스트 형식 (줄바꿈이 없어진 경우)
                info["tools"] = [t.strip().strip('"\'') for t in tools_str.split('-') if t.strip()]
            else:
                # 쉼표/공백으로 구분된 형식
                info["tools"] = [t.strip() for t in re.split(r'[,\s]+', tools_str) if t.strip() and t.strip() != '-']

        # tools가 멀티라인 YAML 리스트인 경우
        if not info["tools"]:
            tools_block_match = re.search(r'^tools:\s*\n((?:\s*-\s*.+\n?)+)', frontmatter, re.MULTILINE)
            if tools_block_match:
                tools_lines = tools_block_match.group(1).strip().split('\n')
                info["tools"] = [re.sub(r'^\s*-\s*', '', t).strip().strip('"\'') for t in tools_lines if t.strip()]

    # frontmatter에서 name을 못 찾았으면 제목에서 추출
    if info["name"] == agent_path.stem.replace("-", " ").title():
        title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        if title_match:
            info["name"] = title_match.group(1).strip()

    # description이 없으면 본문 첫 단락에서 추출
    if not info["description"]:
        body = re.sub(r'^---\n.*?\n---\n?', '', content, flags=re.DOTALL)
        lines = body.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#') and not line.startswith('-') and not line.startswith('|'):
                info["description"] = line[:100]
                break

    # description 길이 제한 및 정리
    if info["description"] and len(info["description"]) > 100:
        info["description"] = info["description"][:100] + "..."

    return info


def scan_skills() -> dict:
    """skills 폴더 스캔하여 모든 스킬 정보 수집"""
    skills = {}

    # 루트 레벨 스킬 자동 카테고리 매핑
    ROOT_SKILL_CATEGORIES = {
        "docx": "documents",
        "pdf": "documents",
        "hwpx": "documents",
        "pptx": "documents",
        "xlsx": "documents",
        "keyword-trend": "marketing",
        "new-product-planner": "marketing",
        "gov-apply": "tools",
    }

    for category_dir in SKILLS_DIR.iterdir():
        if not category_dir.is_dir():
            continue

        # 루트 레벨 스킬 (SKILL.md가 직접 있는 경우)
        if (category_dir / "SKILL.md").exists():
            skill_info = parse_skill_md(category_dir)
            if skill_info:
                cat = ROOT_SKILL_CATEGORIES.get(category_dir.name, "tools")
                if cat not in skills:
                    skills[cat] = []
                skills[cat].append(skill_info)
            continue

        category = category_dir.name
        if category not in skills:
            skills[category] = []

        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_info = parse_skill_md(skill_dir)
            if skill_info:
                skills[category].append(skill_info)

        # 이름순 정렬
        skills[category].sort(key=lambda x: x["name"])

    # 루트 레벨에서 추가된 카테고리도 정렬
    for cat in skills:
        skills[cat].sort(key=lambda x: x["name"])

    return skills


def scan_agents() -> list:
    """agents 폴더 스캔하여 모든 에이전트 정보 수집"""
    agents = []

    if not AGENTS_DIR.exists():
        return agents

    for agent_file in AGENTS_DIR.glob("*.md"):
        agent_info = parse_agent_md(agent_file)
        if agent_info:
            agents.append(agent_info)

    agents.sort(key=lambda x: x["name"])
    return agents


def scan_templates() -> list:
    """영상 템플릿 폴더 스캔하여 정보 수집"""
    templates = []

    if not TEMPLATES_DIR.exists():
        return templates

    for tpl_dir in sorted(TEMPLATES_DIR.iterdir()):
        if not tpl_dir.is_dir():
            continue

        readme = tpl_dir / "README.md"
        if not readme.exists():
            continue

        content = readme.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        # 첫 줄에서 제목 추출 (# 제거)
        name = tpl_dir.name
        title = name
        if lines and lines[0].startswith("#"):
            title = lines[0].lstrip("#").strip()

        # 두 번째 문단(빈 줄 다음 첫 텍스트)에서 설명 추출
        description = ""
        found_blank = False
        for line in lines[1:]:
            if not line.strip():
                found_blank = True
                continue
            if found_blank and line.strip() and not line.startswith("#") and not line.startswith("|"):
                description = line.strip()
                break

        # 권장 길이 추출 (README.md 또는 analysis.md)
        duration = "-"
        duration_match = re.search(r'권장\s*길이\s*\|\s*(.+?)\s*\|', content)
        if duration_match:
            duration = duration_match.group(1).strip()
        else:
            analysis = tpl_dir / "analysis.md"
            if analysis.exists():
                analysis_content = analysis.read_text(encoding="utf-8")
                dur_match = re.search(r'권장\s*길이\s*\|\s*(.+?)\s*\|', analysis_content)
                if dur_match:
                    duration = dur_match.group(1).strip()

        if len(description) > 60:
            description = description[:60] + "..."

        templates.append({
            "name": name,
            "title": title,
            "description": description,
            "duration": duration,
        })

    return templates


def generate_markdown_catalog(skills: dict, agents: list, templates: list = None) -> str:
    """마크다운 카탈로그 생성"""

    total_skills = sum(len(s) for s in skills.values())

    md = f"""# Team Skills Catalog

마케팅 및 콘텐츠 제작을 위한 스킬 모음입니다.

> 자동 생성됨: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 통계

| 항목 | 수량 |
|------|------|
| 총 스킬 | {total_skills}개 |
| 에이전트 | {len(agents)}개 |
| 카테고리 | {len(skills)}개 |

---

"""

    # 카테고리별 스킬 목록
    for category, skill_list in skills.items():
        category_name = CATEGORY_NAMES.get(category, category)
        icon = CATEGORY_ICONS.get(category, "📁")

        md += f"## {icon} {category_name} ({len(skill_list)}개)\n\n"
        md += "| 스킬 | 설명 |\n"
        md += "|------|------|\n"

        for skill in skill_list:
            # 한국어 번역이 있으면 사용
            if skill['name'] in SKILL_TRANSLATIONS:
                desc = SKILL_TRANSLATIONS[skill['name']]
            elif skill['description']:
                desc = skill['description']
            else:
                desc = '-'
            md += f"| `{skill['name']}` | {desc} |\n"

        md += "\n"

    # 영상 템플릿 섹션
    if templates:
        md += f"## 🎬 영상 템플릿 ({len(templates)}개)\n\n"
        md += "| 템플릿 | 설명 | 권장 길이 |\n"
        md += "|--------|------|---------|\n"
        for tpl in templates:
            md += f"| `{tpl['name']}` | {tpl['description'] or tpl['title']} | {tpl['duration']} |\n"
        md += "\n"

    # 에이전트 섹션
    md += "## 🤖 에이전트\n\n"
    md += "| 에이전트 | 설명 |\n"
    md += "|----------|------|\n"

    for agent in agents:
        desc = agent['description'] if agent['description'] else '-'
        md += f"| **{agent['name']}** | {desc} |\n"

    md += f"\n---\n\n*마지막 업데이트: {datetime.now().strftime('%Y-%m-%d')}*\n"

    return md


def generate_html_guide(skills: dict, agents: list, templates: list = None) -> str:
    """HTML 사용 가이드 생성 - 3컬럼 레이아웃 (사이드바 + 메인 + 상세패널)"""

    total_skills = sum(len(s) for s in skills.values())

    # JSON 데이터 준비
    skill_details_json = json.dumps(SKILL_DETAILS, ensure_ascii=False)
    agent_details_json = json.dumps(AGENT_DETAILS, ensure_ascii=False)
    category_names_json = json.dumps(CATEGORY_NAMES, ensure_ascii=False)

    # 사이드바 네비게이션 아이템 생성
    nav_items = f'<div class="nav-item active" data-cat="all"><span>전체</span><span class="badge">{total_skills}</span></div>\n'
    for category, skill_list in skills.items():
        category_name = CATEGORY_NAMES.get(category, category)
        nav_items += f'      <div class="nav-item" data-cat="{category}"><span>{category_name}</span><span class="badge">{len(skill_list)}</span></div>\n'
    nav_items += f'      <div class="nav-item" data-cat="templates"><span>영상 템플릿</span><span class="badge">{len(templates) if templates else 0}</span></div>\n'
    nav_items += f'      <div class="nav-item" data-cat="agents"><span>에이전트</span><span class="badge">{len(agents)}</span></div>'

    # 카테고리별 스킬 섹션 생성
    skill_sections = ""
    for category, skill_list in skills.items():
        category_name = CATEGORY_NAMES.get(category, category)
        icon = CATEGORY_ICONS.get(category, "📁")
        color = CATEGORY_COLORS.get(category, "#666")
        examples = CATEGORY_EXAMPLES.get(category, [])

        # 스킬 카드 생성
        skill_cards = ""
        for skill in skill_list:
            skill_key = skill['name']
            if skill_key in SKILL_TRANSLATIONS:
                desc = SKILL_TRANSLATIONS[skill_key]
            elif skill['description']:
                desc = skill['description']
            else:
                desc = "-"

            # 트리거 태그 생성
            trigger_tags = ""
            if skill.get('triggers'):
                trigger_tags = '<div class="skill-tags">' + ''.join(f'<span class="tag">{t}</span>' for t in skill['triggers'][:3]) + '</div>'

            skill_cards += f'''
        <div class="skill-card" data-name="{skill['name']}" data-cat="{category}">
          <div class="skill-header"><h3>{skill['name']}</h3><span class="arrow">▼</span></div>
          <div class="skill-desc">{desc}{trigger_tags}</div>
        </div>'''

        # 예시 태그
        example_tags = ''.join(f'<span class="example-tag">{ex}</span>' for ex in examples)

        skill_sections += f'''
    <section class="section" data-cat="{category}">
      <h3 class="section-title" style="border-color: {color}">{icon} {category_name} ({len(skill_list)})</h3>
      <div class="example-box">{example_tags}</div>
      <div class="skill-list">{skill_cards}
      </div>
    </section>'''

    # 영상 템플릿 섹션
    template_section = ""
    if templates:
        template_cards = ""
        for tpl in templates:
            template_cards += f'''
        <div class="skill-card" data-name="{tpl['name']}" data-cat="templates">
          <div class="skill-header"><h3>{tpl['name']}</h3><span class="arrow">▼</span></div>
          <div class="skill-desc">{tpl['description'] or tpl['title']}<div class="usage"><strong>권장 길이:</strong> {tpl['duration']}</div></div>
        </div>'''

        template_section = f'''
    <section class="section" data-cat="templates">
      <h3 class="section-title" style="border-color: #9C27B0">🎬 영상 템플릿 ({len(templates)})</h3>
      <div class="skill-list">{template_cards}
      </div>
    </section>'''

    # 에이전트 섹션
    agent_cards = ""
    for agent in agents:
        # 한글 번역 적용
        agent_key = agent.get('filename', '').replace('.md', '')
        if agent_key in AGENT_TRANSLATIONS:
            desc = AGENT_TRANSLATIONS[agent_key]
        elif agent['description']:
            desc = agent['description']
        else:
            desc = "-"

        # 트리거 태그 생성
        trigger_tags = ""
        if agent.get('triggers'):
            trigger_tags = '<div class="skill-tags" style="margin-top:8px"><span style="color:var(--muted);font-size:0.7rem;margin-right:6px">호출:</span>' + ''.join(f'<span class="tag">"{t}"</span>' for t in agent['triggers'][:4]) + '</div>'

        # 도구 태그 생성
        tools_info = ""
        if agent.get('tools'):
            tools_str = ', '.join(agent['tools'][:6])
            tools_info = f'<div class="usage" style="margin-top:10px"><strong>사용 도구:</strong> {tools_str}</div>'

        agent_cards += f'''
        <div class="skill-card" data-name="{agent['name']}" data-cat="agents">
          <div class="skill-header"><h3>{agent['name']}</h3><span class="arrow">▼</span></div>
          <div class="skill-desc">{desc}{trigger_tags}{tools_info}</div>
        </div>'''

    agent_section = f'''
    <section class="section" data-cat="agents">
      <h3 class="section-title" style="border-color: #607D8B">🤖 에이전트 ({len(agents)})</h3>
      <div class="example-box"><span class="example-tag">"광고 만들어줘"</span><span class="example-tag">"릴스 편집해줘"</span><span class="example-tag">"브랜드 분석해줘"</span><span class="example-tag">"경쟁사 조사해줘"</span></div>
      <div class="skill-list">{agent_cards}
      </div>
    </section>'''

    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>마케팅 스킬팩 가이드</title>
<style>
  @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  :root {{
    --primary: #A38068;
    --primary-light: #c4a68a;
    --bg: #0f0f1a;
    --card: #1a1a2e;
    --sidebar: #16213e;
    --border: rgba(255,255,255,0.1);
    --text: #eee;
    --muted: #888;
  }}
  body {{
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
  }}
  .container {{ display: flex; min-height: 100vh; }}

  /* Sidebar */
  .sidebar {{
    width: 260px;
    background: var(--sidebar);
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    overflow-y: auto;
    border-right: 1px solid var(--border);
    z-index: 100;
  }}
  .sidebar-header {{
    padding: 24px 20px;
    border-bottom: 1px solid var(--border);
  }}
  .sidebar-header h1 {{
    font-size: 1.1rem;
    color: var(--primary);
    margin-bottom: 4px;
  }}
  .sidebar-header p {{
    font-size: 0.75rem;
    color: var(--muted);
  }}
  .sidebar input {{
    width: calc(100% - 32px);
    margin: 16px;
    padding: 10px 14px;
    border: 1px solid var(--border);
    border-radius: 8px;
    background: rgba(255,255,255,0.05);
    color: var(--text);
    font-size: 0.85rem;
  }}
  .sidebar input::placeholder {{ color: var(--muted); }}
  .sidebar input:focus {{ outline: none; border-color: var(--primary); }}
  .nav-item {{
    display: flex;
    justify-content: space-between;
    padding: 12px 20px;
    cursor: pointer;
    font-size: 0.85rem;
    color: var(--muted);
    border-left: 3px solid transparent;
    transition: all 0.15s;
  }}
  .nav-item:hover {{ background: rgba(163,128,104,0.1); color: var(--text); }}
  .nav-item.active {{ border-left-color: var(--primary); color: var(--primary); background: rgba(163,128,104,0.15); }}
  .badge {{
    font-size: 0.7rem;
    background: rgba(255,255,255,0.1);
    padding: 2px 8px;
    border-radius: 10px;
  }}
  .stats-box {{
    margin: 20px 16px;
    padding: 16px;
    background: rgba(163,128,104,0.1);
    border-radius: 10px;
    display: flex;
    justify-content: space-around;
    text-align: center;
  }}
  .stat-num {{ font-size: 1.4rem; font-weight: 700; color: var(--primary); }}
  .stat-label {{ font-size: 0.7rem; color: var(--muted); }}

  /* Main */
  .main {{ margin-left: 260px; margin-right: 340px; padding: 32px; flex: 1; }}
  .header {{ margin-bottom: 32px; }}
  .header h2 {{ font-size: 1.5rem; margin-bottom: 8px; }}
  .header p {{ color: var(--muted); font-size: 0.9rem; }}

  /* Right Detail Panel */
  .detail-panel {{
    width: 320px;
    background: var(--sidebar);
    position: fixed;
    top: 0;
    right: 0;
    height: 100vh;
    overflow-y: auto;
    border-left: 1px solid var(--border);
    z-index: 100;
  }}
  .detail-header {{
    padding: 20px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .detail-header h2 {{
    font-size: 1rem;
    color: var(--primary);
  }}
  .help-btn {{
    background: rgba(163,128,104,0.2);
    border: none;
    color: var(--primary-light);
    padding: 6px 12px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.75rem;
  }}
  .help-btn:hover {{ background: rgba(163,128,104,0.4); }}
  .detail-content {{
    padding: 20px;
  }}
  .detail-empty {{
    text-align: center;
    padding: 60px 20px;
    color: var(--muted);
  }}
  .detail-empty .icon {{ font-size: 3rem; margin-bottom: 16px; opacity: 0.5; }}
  .detail-empty p {{ font-size: 0.85rem; }}
  .detail-title {{
    font-size: 1.1rem;
    color: var(--text);
    margin-bottom: 8px;
    font-family: 'Monaco', monospace;
  }}
  .detail-category {{
    font-size: 0.7rem;
    color: var(--primary);
    background: rgba(163,128,104,0.2);
    padding: 3px 10px;
    border-radius: 10px;
    display: inline-block;
    margin-bottom: 16px;
  }}
  .detail-desc {{
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.7;
    margin-bottom: 20px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
  }}
  .detail-section {{
    margin-bottom: 20px;
  }}
  .detail-section h4 {{
    font-size: 0.8rem;
    color: var(--text);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}
  .detail-list {{
    list-style: none;
  }}
  .detail-list li {{
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 8px;
    font-size: 0.8rem;
    color: var(--muted);
  }}
  .detail-list li:hover {{ border-color: var(--primary); }}
  .detail-list .cmd {{
    color: var(--primary-light);
    font-family: 'Monaco', monospace;
    display: block;
    margin-bottom: 4px;
  }}
  .detail-list .note {{
    font-size: 0.7rem;
    color: var(--muted);
  }}
  .detail-tools {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }}
  .detail-tools span {{
    background: rgba(255,255,255,0.05);
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 0.7rem;
    color: var(--muted);
  }}
  .try-btn {{
    width: 100%;
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    border: none;
    color: #fff;
    padding: 12px;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.85rem;
    margin-top: 20px;
  }}
  .try-btn:hover {{ opacity: 0.9; }}

  /* Modal */
  .modal-overlay {{
    display: none;
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(0,0,0,0.8);
    z-index: 1000;
    justify-content: center;
    align-items: center;
  }}
  .modal-overlay.show {{ display: flex; }}
  .modal {{
    background: var(--card);
    border-radius: 16px;
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
    border: 1px solid var(--border);
  }}
  .modal-header {{
    padding: 20px 24px;
    border-bottom: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .modal-header h3 {{
    font-size: 1.1rem;
    color: var(--primary);
  }}
  .modal-close {{
    background: none;
    border: none;
    color: var(--muted);
    font-size: 1.5rem;
    cursor: pointer;
  }}
  .modal-close:hover {{ color: var(--text); }}
  .modal-body {{
    padding: 24px;
  }}
  .modal-step {{
    display: flex;
    gap: 16px;
    margin-bottom: 24px;
  }}
  .modal-step .num {{
    background: var(--primary);
    color: #fff;
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    flex-shrink: 0;
  }}
  .modal-step .content h4 {{
    color: var(--text);
    font-size: 0.95rem;
    margin-bottom: 8px;
  }}
  .modal-step .content p {{
    color: var(--muted);
    font-size: 0.85rem;
    line-height: 1.6;
  }}
  .modal-step .content code {{
    background: rgba(163,128,104,0.2);
    color: var(--primary-light);
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'Monaco', monospace;
  }}
  .modal-examples {{
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    padding: 16px;
    margin-top: 16px;
  }}
  .modal-examples h5 {{
    color: var(--text);
    font-size: 0.85rem;
    margin-bottom: 12px;
  }}
  .modal-examples .example {{
    background: var(--sidebar);
    padding: 10px 14px;
    border-radius: 6px;
    margin-bottom: 8px;
    color: var(--primary-light);
    font-family: 'Monaco', monospace;
    font-size: 0.8rem;
  }}

  /* Usage box */
  .usage-box-main {{
    background: linear-gradient(135deg, var(--primary), var(--primary-light));
    padding: 20px 24px;
    border-radius: 12px;
    margin-bottom: 32px;
  }}
  .usage-box-main h3 {{ font-size: 0.95rem; margin-bottom: 12px; }}
  .usage-box-main .examples {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }}
  .usage-box-main .example {{
    background: rgba(255,255,255,0.2);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
  }}

  /* Sections */
  .section {{ margin-bottom: 40px; }}
  .section-title {{
    font-size: 1rem;
    color: var(--text);
    padding-bottom: 12px;
    margin-bottom: 16px;
    border-bottom: 2px solid var(--border);
  }}
  .example-box {{
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
    margin-bottom: 16px;
  }}
  .example-tag {{
    background: rgba(163,128,104,0.2);
    color: var(--primary-light);
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 0.75rem;
  }}
  .skill-list {{ display: flex; flex-direction: column; gap: 10px; }}
  .skill-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    transition: all 0.2s;
  }}
  .skill-card:hover {{ border-color: var(--primary); }}
  .skill-card.selected {{ border-color: var(--primary); background: rgba(163,128,104,0.1); }}
  .skill-header {{
    padding: 14px 18px;
    cursor: pointer;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }}
  .skill-header h3 {{
    font-size: 0.9rem;
    font-weight: 600;
    font-family: 'Monaco', 'Consolas', monospace;
    color: var(--primary-light);
  }}
  .skill-header .arrow {{ color: var(--muted); transition: transform 0.2s; font-size: 0.7rem; }}
  .skill-card.open .arrow {{ transform: rotate(180deg); }}
  .skill-desc {{
    padding: 0 18px;
    color: var(--muted);
    font-size: 0.85rem;
    max-height: 0;
    overflow: hidden;
    transition: all 0.3s;
  }}
  .skill-card.open .skill-desc {{ max-height: 500px; padding: 0 18px 16px; }}
  .skill-tags {{ display: flex; gap: 6px; flex-wrap: wrap; margin-top: 10px; }}
  .tag {{
    background: rgba(163,128,104,0.25);
    color: var(--primary-light);
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.7rem;
  }}
  .usage {{
    background: rgba(255,255,255,0.05);
    padding: 10px 12px;
    border-radius: 6px;
    margin-top: 10px;
    font-size: 0.8rem;
  }}
  .hidden {{ display: none !important; }}

  /* Footer */
  footer {{
    text-align: center;
    padding: 40px 20px;
    color: var(--muted);
    font-size: 0.75rem;
    border-top: 1px solid var(--border);
    margin-top: 40px;
  }}

  /* Responsive */
  @media (max-width: 1200px) {{
    .detail-panel {{ display: none; }}
    .main {{ margin-right: 0; }}
  }}
  @media (max-width: 768px) {{
    .sidebar {{ width: 100%; height: auto; position: relative; }}
    .main {{ margin-left: 0; margin-right: 0; padding: 20px; }}
    .container {{ flex-direction: column; }}
  }}
</style>
</head>
<body>
<div class="container">
  <aside class="sidebar">
    <div class="sidebar-header">
      <h1>마케팅 스킬팩</h1>
      <p>AI 마케팅 자동화 도구 모음</p>
    </div>
    <input type="text" id="search" placeholder="스킬 검색...">
    <div class="stats-box">
      <div><div class="stat-num">{total_skills}</div><div class="stat-label">스킬</div></div>
      <div><div class="stat-num">{len(agents)}</div><div class="stat-label">에이전트</div></div>
      <div><div class="stat-num">{len(templates) if templates else 0}</div><div class="stat-label">템플릿</div></div>
    </div>
    <nav>
      {nav_items}
    </nav>
  </aside>

  <main class="main">
    <div class="header">
      <h2>설치된 스킬 목록</h2>
      <p>각 스킬을 클릭하면 상세 설명을 볼 수 있습니다</p>
    </div>

    <div class="usage-box-main">
      <h3>💡 사용 방법</h3>
      <div class="examples">
        <span class="example">"상세페이지 만들어줘"</span>
        <span class="example">"메타 광고 기획해줘"</span>
        <span class="example">"랜딩페이지 CRO 분석"</span>
        <span class="example">"이메일 시퀀스 작성"</span>
      </div>
    </div>

{skill_sections}
{template_section}
{agent_section}

    <footer>
      자동 생성됨 · {datetime.now().strftime('%Y-%m-%d %H:%M')}
    </footer>
  </main>

  <aside class="detail-panel">
    <div class="detail-header">
      <h2>📋 상세 정보</h2>
      <button class="help-btn" onclick="showGuideModal()">❓ 사용법</button>
    </div>
    <div class="detail-content">
      <div class="detail-empty" id="detail-empty">
        <div class="icon">👆</div>
        <p>왼쪽에서 스킬이나 에이전트를<br>클릭하면 상세 정보가 표시됩니다</p>
      </div>
      <div id="detail-info" style="display:none;"></div>
    </div>
  </aside>
</div>

<!-- 사용 가이드 모달 -->
<div class="modal-overlay" id="guide-modal">
  <div class="modal">
    <div class="modal-header">
      <h3>📖 사용 가이드</h3>
      <button class="modal-close" onclick="closeGuideModal()">&times;</button>
    </div>
    <div class="modal-body">
      <div class="modal-step">
        <span class="num">1</span>
        <div class="content">
          <h4>터미널 열기</h4>
          <p>VS Code에서 <code>Ctrl + `</code> 또는 Mac 터미널 앱을 실행하세요.</p>
        </div>
      </div>
      <div class="modal-step">
        <span class="num">2</span>
        <div class="content">
          <h4>Claude 실행</h4>
          <p>터미널에서 <code>claude</code> 명령어를 입력하세요.</p>
        </div>
      </div>
      <div class="modal-step">
        <span class="num">3</span>
        <div class="content">
          <h4>자연어로 요청</h4>
          <p>원하는 작업을 자연어로 말하면 됩니다. 스킬 이름을 외울 필요 없어요!</p>
          <div class="modal-examples">
            <h5>예시 요청</h5>
            <div class="example">"상세페이지 만들어줘"</div>
            <div class="example">"메타 광고 소재 제작해줘"</div>
            <div class="example">"카카오 배너 만들어줘"</div>
            <div class="example">"브랜드 분석해줘"</div>
          </div>
        </div>
      </div>
      <div class="modal-step">
        <span class="num">4</span>
        <div class="content">
          <h4>파일 전달하기</h4>
          <p>이미지나 파일 경로를 함께 전달하면 해당 파일을 활용해 작업합니다.</p>
        </div>
      </div>
      <div class="modal-step">
        <span class="num">💡</span>
        <div class="content">
          <h4>결과물 위치</h4>
          <p>모든 결과물은 각 팀원 로컬 <code>~/Desktop/team-skills/</code> 폴더에 저장됩니다.</p>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
// 스킬/에이전트 상세 정보 데이터
const skillDetails = {skill_details_json};
const agentDetails = {agent_details_json};
const categoryNames = {category_names_json};

// 카드 클릭 시 상세 정보 표시
document.querySelectorAll('.skill-card').forEach(card => {{
  card.addEventListener('click', (e) => {{
    // 모든 카드의 선택 상태 해제
    document.querySelectorAll('.skill-card').forEach(c => c.classList.remove('selected'));
    card.classList.add('selected');
    card.classList.toggle('open');

    const name = card.dataset.name;
    const cat = card.dataset.cat;
    showDetail(name, cat);
  }});
}});

function showDetail(name, cat) {{
  const detailEmpty = document.getElementById('detail-empty');
  const detailInfo = document.getElementById('detail-info');

  // 스킬 또는 에이전트 정보 가져오기
  let info = skillDetails[name] || agentDetails[name];
  let isAgent = cat === 'agents';

  if (!info) {{
    // 기본 정보 생성
    info = {{
      desc: document.querySelector(`[data-name="${{name}}"] .skill-desc`)?.textContent || '설명 없음',
      usecases: [{{cmd: `"${{name}} 실행해줘"`, note: '기본 실행'}}],
      capabilities: [],
      workflow: [],
    }};
  }}

  const catName = isAgent ? '에이전트' : (categoryNames[cat] || cat);

  let usecasesHtml = info.usecases?.map(u => `
    <li>
      <span class="cmd">${{u.cmd}}</span>
      <span class="note">${{u.note}}</span>
    </li>
  `).join('') || '';

  let capabilitiesHtml = '';
  if (info.capabilities?.length) {{
    capabilitiesHtml = `
      <div class="detail-section">
        <h4>✨ 가능한 작업</h4>
        <div class="detail-tools">
          ${{info.capabilities.map(c => `<span>${{c}}</span>`).join('')}}
        </div>
      </div>
    `;
  }}

  let workflowHtml = '';
  if (info.workflow?.length) {{
    workflowHtml = `
      <div class="detail-section">
        <h4>⚙️ 작업 흐름</h4>
        <div class="detail-tools">
          ${{info.workflow.map((w, i) => `<span>${{i+1}}. ${{w}}</span>`).join('')}}
        </div>
      </div>
    `;
  }}

  let outputHtml = '';
  if (info.output) {{
    outputHtml = `
      <div class="detail-section">
        <h4>📁 결과물 위치</h4>
        <div class="detail-tools"><span>${{info.output}}</span></div>
      </div>
    `;
  }}

  detailInfo.innerHTML = `
    <div class="detail-title">${{name}}</div>
    <span class="detail-category">${{catName}}</span>
    <div class="detail-desc">${{info.desc}}</div>

    <div class="detail-section">
      <h4>💬 사용 예시</h4>
      <ul class="detail-list">${{usecasesHtml}}</ul>
    </div>

    ${{capabilitiesHtml}}
    ${{workflowHtml}}
    ${{outputHtml}}

    <button class="try-btn" onclick="copyCommand('${{name}}')">
      📋 명령어 복사하기
    </button>
  `;

  detailEmpty.style.display = 'none';
  detailInfo.style.display = 'block';
}}

function copyCommand(name) {{
  const info = skillDetails[name] || agentDetails[name];
  const cmd = info?.usecases?.[0]?.cmd || `"${{name}} 실행해줘"`;
  navigator.clipboard.writeText(cmd.replace(/"/g, ''));
  alert('명령어가 복사되었습니다!');
}}

// 모달 제어
function showGuideModal() {{
  document.getElementById('guide-modal').classList.add('show');
}}

function closeGuideModal() {{
  document.getElementById('guide-modal').classList.remove('show');
}}

document.getElementById('guide-modal').addEventListener('click', (e) => {{
  if (e.target.classList.contains('modal-overlay')) {{
    closeGuideModal();
  }}
}});

// 검색
document.getElementById('search').addEventListener('input', function() {{
  const q = this.value.toLowerCase();
  document.querySelectorAll('.skill-card').forEach(card => {{
    const name = card.dataset.name.toLowerCase();
    const desc = card.querySelector('.skill-desc')?.textContent.toLowerCase() || '';
    const match = name.includes(q) || desc.includes(q);
    card.classList.toggle('hidden', !match);
  }});
  document.querySelectorAll('.section').forEach(sec => {{
    const hasVisible = sec.querySelector('.skill-card:not(.hidden)');
    sec.classList.toggle('hidden', !hasVisible);
  }});
}});

// 카테고리 필터
document.querySelectorAll('.nav-item').forEach(item => {{
  item.addEventListener('click', function() {{
    document.querySelectorAll('.nav-item').forEach(i => i.classList.remove('active'));
    this.classList.add('active');
    const cat = this.dataset.cat;
    document.querySelectorAll('.section').forEach(sec => {{
      sec.classList.toggle('hidden', cat !== 'all' && sec.dataset.cat !== cat);
    }});
    document.querySelectorAll('.skill-card').forEach(card => card.classList.remove('hidden'));
    document.getElementById('search').value = '';
  }});
}});
</script>
</body>
</html>"""

    return html


def main():
    print("🔍 스킬 스캔 중...")
    skills = scan_skills()

    print("🤖 에이전트 스캔 중...")
    agents = scan_agents()

    print("🎬 영상 템플릿 스캔 중...")
    templates = scan_templates()

    total_skills = sum(len(s) for s in skills.values())
    print(f"   - 발견된 스킬: {total_skills}개")
    print(f"   - 발견된 에이전트: {len(agents)}개")
    print(f"   - 발견된 템플릿: {len(templates)}개")

    # 마크다운 생성
    print("\n📝 마크다운 카탈로그 생성 중...")
    md_content = generate_markdown_catalog(skills, agents, templates)
    OUTPUT_CATALOG.write_text(md_content, encoding="utf-8")
    print(f"   ✅ {OUTPUT_CATALOG}")

    # HTML 생성
    print("\n🌐 HTML 가이드 생성 중...")
    html_content = generate_html_guide(skills, agents, templates)
    OUTPUT_HTML.write_text(html_content, encoding="utf-8")
    print(f"   ✅ {OUTPUT_HTML}")

    print(f"\n✨ 완료!")
    print(f"   총 {total_skills}개 스킬, {len(agents)}개 에이전트, {len(templates)}개 템플릿 문서화됨")


if __name__ == "__main__":
    main()
