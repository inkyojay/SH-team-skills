#!/usr/bin/env python3
"""
제품 분석 리포트 빌드 스크립트

사용법:
    python build_product_report.py --product "제품명" --data product_data.json

결과:
    ../report/{제품명}/ 폴더에 정적 웹사이트 생성
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
TEMPLATE_DIR = PROJECT_ROOT / "Product Report Template"
REPORT_OUTPUT_DIR = PROJECT_ROOT / "report"
PRODUCT_DATA_FILE = TEMPLATE_DIR / "src" / "app" / "data" / "productData.ts"


def slugify(text: str) -> str:
    """제품명을 URL-safe 폴더명으로 변환"""
    import re
    # 영문, 숫자, 한글만 허용
    text = re.sub(r'[^\w\s가-힣-]', '', text)
    text = re.sub(r'[\s]+', '_', text)
    return text.lower()


def generate_product_data_ts(data: dict) -> str:
    """ProductReportData JSON을 TypeScript 파일로 변환"""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)

    return f'''export interface ProductReportData {{
  meta: {{
    date: string;
    productName: string;
    storeName: string;
    productUrl: string;
    price: string;
  }};
  overview: {{
    category: string;
    targetAudience: string;
    coreFeatures: string[];
    summary: string;
  }};
  strengths: {{
    title: string;
    description: string;
    category: 'function' | 'design' | 'price' | 'unique';
    importance: 'high' | 'medium' | 'low';
  }}[];
  weaknesses: {{
    title: string;
    description: string;
    category: 'function' | 'info' | 'concern';
    severity: 'high' | 'medium' | 'low';
  }}[];
  featureAnalysis: {{
    feature: string;
    score: number;
    evidence: string;
    pros: string[];
    cons: string[];
  }}[];
  competitorComparison: {{
    aspect: string;
    thisProduct: string;
    competitors: string;
    verdict: 'advantage' | 'similar' | 'disadvantage';
  }}[];
  recommendation: {{
    score: number;
    summary: string;
    bestFor: string[];
    notFor: string[];
  }};
  images: {{
    thumbnail: string;
    detailImages: string[];
  }};
}}

export const exampleData: ProductReportData = {json_str};
'''


def build_report(product_name: str, data_file: str = None, data_dict: dict = None):
    """
    제품 분석 리포트를 빌드하고 폴더에 저장

    Args:
        product_name: 제품 이름
        data_file: JSON 데이터 파일 경로 (선택)
        data_dict: 직접 전달하는 데이터 딕셔너리 (선택)
    """
    print(f"\n{'='*50}")
    print(f"  Product Analysis Report Builder")
    print(f"  Product: {product_name}")
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
    data['meta']['productName'] = product_name

    # 2. productData.ts 업데이트
    print(f"[2/5] 템플릿 데이터 업데이트: {PRODUCT_DATA_FILE}")

    # 백업
    backup_file = PRODUCT_DATA_FILE.with_suffix('.ts.backup')
    if PRODUCT_DATA_FILE.exists():
        shutil.copy(PRODUCT_DATA_FILE, backup_file)

    # 새 데이터 쓰기
    ts_content = generate_product_data_ts(data)
    with open(PRODUCT_DATA_FILE, 'w', encoding='utf-8') as f:
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
            shutil.copy(backup_file, PRODUCT_DATA_FILE)
        sys.exit(1)

    # 5. 결과물 복사
    product_slug = slugify(product_name)
    output_dir = REPORT_OUTPUT_DIR / product_slug
    dist_dir = TEMPLATE_DIR / "dist"

    print(f"[5/5] 결과물 저장: {output_dir}")

    # 기존 폴더 삭제
    if output_dir.exists():
        shutil.rmtree(output_dir)

    # dist 복사
    shutil.copytree(dist_dir, output_dir)

    # JSON 데이터도 함께 저장
    json_output = output_dir / f"{product_slug}_data.json"
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
    parser = argparse.ArgumentParser(description='제품 분석 리포트 빌드')
    parser.add_argument('--product', required=True, help='제품 이름')
    parser.add_argument('--data', required=True, help='ProductReportData JSON 파일 경로')

    args = parser.parse_args()

    if not os.path.exists(args.data):
        print(f"[ERROR] 데이터 파일을 찾을 수 없습니다: {args.data}")
        sys.exit(1)

    build_report(args.product, data_file=args.data)


if __name__ == "__main__":
    main()
