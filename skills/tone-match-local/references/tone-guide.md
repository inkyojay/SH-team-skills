# 톤 매치 활용 가이드

## 강도별 효과

| 강도 | 효과 | 권장 |
|------|------|------|
| 20-30% | 미묘한 색감 변화 | 원본 유지하면서 살짝 통일 |
| 40-60% | 자연스러운 매칭 | 일반 상세페이지 톤 통일 |
| 70-80% | 확실한 변환 | 브랜드 톤앤매너 적용 (기본값) |
| 90-100% | 레퍼런스에 가깝게 | 동일 촬영 컷처럼 |

## 주의사항

- 상품 형태/색상은 보존됨 (톤만 변경)
- 흑백 레퍼런스 사용 시 흑백으로 변환됨
- 대량 처리 시 `--concurrency 1` 권장
- 출력은 항상 PNG

## 웹앱 vs 로컬 스킬 차이

| 항목 | 웹앱 (tone-match.tsx) | 로컬 스킬 (batch-tone-match.mjs) |
|------|----------------------|----------------------------------|
| 실행 환경 | Vercel 서버 | 로컬 CLI |
| 인증 | Supabase Auth | 불필요 |
| 크레딧 | DB 차감 | 불필요 (API 키 직접 사용) |
| 스토리지 | Supabase Storage | 로컬 파일 저장 |
| 배치 제한 | 최대 5장 | 제한 없음 (폴더 전체) |
| 브랜드 톤 | DB에서 조회 가능 | 로컬 파일만 |

## 사용 예시

```bash
# 기본 톤 매치
node batch-tone-match.mjs --reference ./ref.jpg --input ./product-photos

# 낮은 강도로 자연스럽게
node batch-tone-match.mjs --reference ./ref.jpg --input ./products --intensity 50

# 고품질 모델 + 순차 처리
node batch-tone-match.mjs --reference ./ref.jpg --input ./products --model gemini-3-pro --concurrency 1
```
