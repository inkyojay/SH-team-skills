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
    "keyword-optimizer": "키워드 최적화 분석",
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
    "brand-logo-finder": "브랜드 로고 검색 에이전트 - Brandfetch로 로고 검색 및 다운로드",
    "brand-setup-wizard": "새 브랜드 초기 설정 마법사 - 질문을 통해 브랜드 정보 수집",
    "brand-updater": "브랜드 정보 업데이트 - 제품, 경쟁사, 캠페인 등 수정",
    "competitor-analyzer": "경쟁사 실시간 분석 - 제품, 가격, 마케팅, SNS, 리뷰 조사",
    "content-quality-reviewer": "콘텐츠 품질 검토 - 마케팅 콘텐츠 리뷰 및 개선점 제안",
    "data-report-analyzer": "데이터 분석 리포트 생성 - CSV, 엑셀, JSON 파일 분석",
    "market-researcher": "시장 및 트렌드 조사 - 소비자 인사이트, 기회 영역 발굴",
    "meta-ad-creator": "메타 광고 이미지 자동 제작 - 2~3개 스타일 생성",
    "meta-ads-agent": "메타 광고 영상 제작 - 템플릿 선택부터 Remotion 프로젝트까지",
    "reels-editor-agent": "릴스 영상 편집 - 9:16 세로형 변환 및 자막 추가",
    "sundayhug-marketing-hub": "마케팅 총괄 오케스트레이터 - 스킬/에이전트 추천 및 워크플로우",
    "skill-orchestrator": "통합 오케스트레이터 - 사용자 의도 파악 및 스킬/에이전트 매칭",
}

# 스킬별 상세 정보 (사용 방법, 사례, 가능한 작업)
SKILL_DETAILS = {
    "page-builder": {
        "desc": "상세페이지, 랜딩페이지, 제품 소개 페이지를 HTML로 제작합니다.",
        "usecases": [
            {"cmd": "상세페이지 만들어줘", "note": "기본 상세페이지 제작"},
            {"cmd": "이 제품으로 랜딩페이지 만들어줘 [이미지]", "note": "이미지 기반 제작"},
            {"cmd": "경쟁사 A 스타일로 상세페이지", "note": "레퍼런스 참고 제작"},
        ],
        "capabilities": ["HTML 상세페이지 제작", "반응형 디자인", "SEO 최적화", "이미지 배치"],
        "output": "output/상세페이지/",
    },
    "card-news-creator": {
        "desc": "인스타그램 스타일의 카드뉴스를 제작합니다. 슬라이드형 콘텐츠에 최적화되어 있습니다.",
        "usecases": [
            {"cmd": "카드뉴스 만들어줘", "note": "기본 카드뉴스 제작"},
            {"cmd": "이 주제로 5장짜리 카드뉴스", "note": "장수 지정"},
            {"cmd": "육아 정보 카드뉴스 만들어줘", "note": "주제 지정"},
        ],
        "capabilities": ["인스타그램 최적화", "슬라이드 구성", "텍스트/이미지 배치", "브랜드 컬러 적용"],
        "output": "output/카드뉴스/",
    },
    "meta-ad-image": {
        "desc": "메타(인스타/페이스북) 광고용 이미지를 제작합니다. 다양한 템플릿을 활용합니다.",
        "usecases": [
            {"cmd": "메타 광고 이미지 만들어줘", "note": "기본 광고 이미지"},
            {"cmd": "이 제품 이미지로 인스타 광고 소재", "note": "이미지 기반"},
            {"cmd": "페북 광고 배너 3종 만들어줘", "note": "여러 버전 제작"},
        ],
        "capabilities": ["1080x1080 피드 광고", "1080x1920 스토리 광고", "다양한 레이아웃", "CTA 버튼 포함"],
        "output": "output/광고카피/",
    },
    "kakao-message": {
        "desc": "카카오톡 비즈메시지용 배너를 제작합니다. 이미지형, 캐러셀형, 리스트형을 지원합니다.",
        "usecases": [
            {"cmd": "카카오 메시지 배너 만들어줘", "note": "기본 배너"},
            {"cmd": "카톡 이미지형 배너", "note": "이미지형 제작"},
            {"cmd": "알림톡 캐러셀 배너 3장", "note": "캐러셀형 제작"},
        ],
        "capabilities": ["이미지형 배너", "캐러셀형 배너", "리스트형 배너", "규격 자동 적용"],
        "output": "output/광고카피/",
    },
    "reels-editor": {
        "desc": "영상을 인스타그램 릴스 포맷(9:16, 1080x1920)으로 편집합니다.",
        "usecases": [
            {"cmd": "릴스 영상 편집해줘 [영상파일]", "note": "세로형 변환"},
            {"cmd": "이 영상 릴스로 만들어줘", "note": "크롭 및 리사이즈"},
            {"cmd": "자막 넣어서 릴스 만들어줘", "note": "자막 추가"},
        ],
        "capabilities": ["9:16 세로 변환", "자막 추가", "인트로/아웃트로", "배경음악 추가"],
        "output": "output/영상/",
    },
    "brand-dna-extractor": {
        "desc": "웹사이트 URL에서 브랜드 DNA를 추출하고 무드보드 및 리포트를 생성합니다.",
        "usecases": [
            {"cmd": "브랜드 분석해줘 [URL]", "note": "웹사이트 분석"},
            {"cmd": "무드보드 만들어줘", "note": "무드보드 생성"},
            {"cmd": "브랜드 DNA 리포트", "note": "상세 리포트"},
        ],
        "capabilities": ["브랜드 컬러 추출", "무드보드 생성", "톤앤매너 분석", "인터랙티브 리포트"],
        "output": "output/리포트/",
    },
    "competitor-analysis": {
        "desc": "경쟁사를 분석하고 벤치마킹 리포트를 생성합니다.",
        "usecases": [
            {"cmd": "경쟁사 분석해줘", "note": "경쟁사 리서치"},
            {"cmd": "[브랜드명] 벤치마킹해줘", "note": "특정 브랜드 분석"},
            {"cmd": "시장 조사해줘", "note": "시장 분석"},
        ],
        "capabilities": ["경쟁사 제품 분석", "가격 비교", "마케팅 전략 분석", "SWOT 분석"],
        "output": "output/리포트/",
    },
    "copywriting": {
        "desc": "마케팅 카피를 작성합니다. 랜딩페이지, 홈페이지, 광고 카피 등을 지원합니다.",
        "usecases": [
            {"cmd": "광고 카피 써줘", "note": "광고 카피 작성"},
            {"cmd": "랜딩페이지 카피라이팅", "note": "랜딩페이지용"},
            {"cmd": "헤드라인 5개 만들어줘", "note": "헤드라인 다수 생성"},
        ],
        "capabilities": ["헤드라인 작성", "바디카피 작성", "CTA 문구", "USP 정리"],
        "output": "output/광고카피/",
    },
}

# 에이전트별 상세 정보
AGENT_DETAILS = {
    "meta-ad-creator": {
        "desc": "제품 이미지를 분석하고 2~3개 스타일의 메타 광고 이미지를 자동 생성합니다.",
        "usecases": [
            {"cmd": "광고 만들어줘 [이미지폴더]", "note": "폴더 내 이미지로 광고 생성"},
            {"cmd": "메타 광고 제작", "note": "기본 광고 제작"},
            {"cmd": "인스타 광고 소재 3종", "note": "여러 버전 생성"},
        ],
        "workflow": ["이미지 분석", "템플릿 선택", "광고 이미지 생성", "PNG 변환"],
    },
    "reels-editor-agent": {
        "desc": "영상을 9:16 세로형으로 변환하고 자막, 인트로/아웃트로를 추가합니다.",
        "usecases": [
            {"cmd": "릴스 편집해줘 [영상파일]", "note": "영상 편집"},
            {"cmd": "릴스 광고 만들어줘", "note": "광고용 릴스"},
            {"cmd": "세로 영상으로 바꿔줘", "note": "포맷 변환"},
        ],
        "workflow": ["영상 분석", "크롭/리사이즈", "자막 생성", "인코딩"],
    },
    "competitor-analyzer": {
        "desc": "웹 검색으로 경쟁 브랜드의 제품, 가격, 마케팅, SNS, 리뷰 데이터를 수집하고 분석합니다.",
        "usecases": [
            {"cmd": "경쟁사 분석해줘 [브랜드명]", "note": "특정 브랜드 분석"},
            {"cmd": "벤치마킹 리포트 만들어줘", "note": "비교 리포트"},
            {"cmd": "시장 조사해줘", "note": "시장 전체 조사"},
        ],
        "workflow": ["웹 검색", "데이터 수집", "분석", "리포트 생성"],
    },
    "brand-setup-wizard": {
        "desc": "새 브랜드의 초기 설정을 도와주는 마법사입니다. 질문을 통해 브랜드 정보를 수집합니다.",
        "usecases": [
            {"cmd": "브랜드 설정해줘", "note": "새 브랜드 설정"},
            {"cmd": "새 브랜드 추가", "note": "브랜드 추가"},
            {"cmd": "brand setup", "note": "영문 명령도 지원"},
        ],
        "workflow": ["질문 수집", "브랜드 정보 정리", "레퍼런스 파일 생성"],
    },
    "skill-orchestrator": {
        "desc": "사용자의 요청을 분석하여 가장 적합한 스킬이나 에이전트를 추천하고 연결합니다.",
        "usecases": [
            {"cmd": "도와줘", "note": "무엇을 할 수 있는지 안내"},
            {"cmd": "뭐 할 수 있어?", "note": "가능한 작업 목록"},
            {"cmd": "마케팅 관련 작업해줘", "note": "의도 파악 후 매칭"},
        ],
        "workflow": ["의도 분석", "스킬/에이전트 매칭", "작업 위임", "결과 전달"],
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

        # description 추출 (한 줄짜리)
        desc_match = re.search(r'^description:\s*["\']?([^|\n][^\n]*)["\']?$', frontmatter, re.MULTILINE)
        if desc_match:
            info["description"] = desc_match.group(1).strip().strip('"\'')
        else:
            # 멀티라인 description
            desc_match = re.search(r'^description:\s*[|>]\s*\n(.*?)(?=\n[a-z_]+:|\Z)', frontmatter, re.DOTALL | re.MULTILINE)
            if desc_match:
                desc_lines = desc_match.group(1).strip().split('\n')
                info["description"] = desc_lines[0].strip() if desc_lines else ""

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
          <p>모든 결과물은 <code>output/</code> 폴더에 저장됩니다.</p>
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
