#!/usr/bin/env python3
"""
브랜드 DNA 리포트 빌드 스크립트

사용법:
    python build_report.py --brand "브랜드명" --data brand_data.json

결과:
    ../report/{브랜드명}/ 폴더에 정적 웹사이트 생성
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# 경로 설정
SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
TEMPLATE_DIR = PROJECT_ROOT.parent / "Brand Guidance Moodboard Template"
REPORT_OUTPUT_DIR = PROJECT_ROOT / "report"
BRAND_DATA_FILE = TEMPLATE_DIR / "src" / "app" / "data" / "brandData.ts"


def slugify(text: str) -> str:
    """브랜드명을 URL-safe 폴더명으로 변환"""
    import re
    # 영문, 숫자, 한글만 허용
    text = re.sub(r'[^\w\s가-힣-]', '', text)
    text = re.sub(r'[\s]+', '_', text)
    return text.lower()


def generate_brand_data_ts(data: dict) -> str:
    """BrandReportData JSON을 TypeScript 파일로 변환"""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    return f'''export interface BrandReportData {{
  meta: {{
    date: string;
    client: string;
    status: string;
    projectCode: string;
  }};
  summary: {{
    mainTitle: string;
    subTitle: string;
    description: string;
    insights: {{ label: string; icon: 'trending' | 'shield' | 'chart' }}[];
  }};
  identity: {{
    mission: string;
    vision: string;
    values: string[];
    archetype: {{ name: string; description: string; }};
    coreTraits: string[];
  }};
  personality: {{
    radarData: {{ subject: string; A: number; fullMark: number }}[];
    highlight: {{ title: string; score: number; }};
  }};
  tone: {{
    spectrum: {{ label: string; left: string; right: string; value: number }}[];
    guidelines: {{ dos: string[]; donts: string[]; }};
  }};
  visuals: {{
    colors: {{ role: string; name: string; hex: string; desc: string; textColor: string }}[];
    styleGuide: {{ title: string; description: string }}[];
  }};
  persona: {{
    name: string;
    role: string;
    imageUrl: string;
    quote: string;
    description: string;
    goals: string[];
    painPoints: string[];
    tags: string[];
  }};
  strategy: {{
    strengths: string[];
    opportunities: string[];
    watchOut: string[];
  }};
  moodboard: {{
    keywords: string[];
    images: string[];
  }};
}}

export const exampleData: BrandReportData = {json_str};
'''


def build_report(brand_name: str, data_file: str = None, data_dict: dict = None):
    """
    브랜드 리포트를 빌드하고 폴더에 저장

    Args:
        brand_name: 브랜드 이름
        data_file: JSON 데이터 파일 경로 (선택)
        data_dict: 직접 전달하는 데이터 딕셔너리 (선택)
    """
    print(f"\n{'='*50}")
    print(f"  Brand DNA Report Builder")
    print(f"  Brand: {brand_name}")
    print(f"{'='*50}\n")

    # 1. 데이터 로드
    if data_dict:
        data = data_dict
    elif data_file:
        print(f"[1/5] 데이터 로드: {data_file}")
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        print("[ERROR] data_file 또는 data_dict가 필요합니다.")
        sys.exit(1)

    # 메타 정보 업데이트
    if 'meta' not in data:
        data['meta'] = {}
    data['meta']['date'] = datetime.now().strftime('%Y-%m-%d')
    data['meta']['client'] = brand_name
    data['meta']['projectCode'] = f"{slugify(brand_name)}_DNA_{datetime.now().year}.json"

    # 2. brandData.ts 업데이트
    print(f"[2/5] 템플릿 데이터 업데이트: {BRAND_DATA_FILE}")

    # 백업
    backup_file = BRAND_DATA_FILE.with_suffix('.ts.backup')
    if BRAND_DATA_FILE.exists():
        shutil.copy(BRAND_DATA_FILE, backup_file)

    # 새 데이터 쓰기
    ts_content = generate_brand_data_ts(data)
    with open(BRAND_DATA_FILE, 'w', encoding='utf-8') as f:
        f.write(ts_content)

    # 3. npm install (필요시)
    print(f"[3/5] 의존성 확인...")
    node_modules = TEMPLATE_DIR / "node_modules"
    if not node_modules.exists():
        print("      npm install 실행 중...")
        subprocess.run(["npm", "install"], cwd=TEMPLATE_DIR, check=True)

    # 4. 빌드
    print(f"[4/5] 빌드 중...")
    result = subprocess.run(
        ["npm", "run", "build"],
        cwd=TEMPLATE_DIR,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"[ERROR] 빌드 실패:\n{result.stderr}")
        # 백업 복원
        if backup_file.exists():
            shutil.copy(backup_file, BRAND_DATA_FILE)
        sys.exit(1)

    # 5. 결과물 복사
    brand_slug = slugify(brand_name)
    output_dir = REPORT_OUTPUT_DIR / brand_slug
    dist_dir = TEMPLATE_DIR / "dist"

    print(f"[5/5] 결과물 저장: {output_dir}")

    # 기존 폴더 삭제
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # dist 복사
    shutil.copytree(dist_dir, output_dir)

    # JSON 데이터도 함께 저장
    json_output = output_dir / f"{brand_slug}_data.json"
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 백업 파일 정리
    if backup_file.exists():
        backup_file.unlink()

    print(f"\n{'='*50}")
    print(f"  빌드 완료!")
    print(f"{'='*50}")
    print(f"\n결과물 위치: {output_dir}")
    print(f"\n로컬에서 보기:")
    print(f"  1. 파일 직접 열기:")
    print(f"     open \"{output_dir}/index.html\"")
    print(f"\n  2. 로컬 서버로 보기 (권장):")
    print(f"     cd \"{output_dir}\"")
    print(f"     python -m http.server 8080")
    print(f"     # → http://localhost:8080")
    print()

    return output_dir


def main():
    parser = argparse.ArgumentParser(description='브랜드 DNA 리포트 빌드')
    parser.add_argument('--brand', required=True, help='브랜드 이름')
    parser.add_argument('--data', required=True, help='BrandReportData JSON 파일 경로')

    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"[ERROR] 데이터 파일을 찾을 수 없습니다: {args.data}")
        sys.exit(1)

    build_report(args.brand, data_file=args.data)


if __name__ == "__main__":
    main()
