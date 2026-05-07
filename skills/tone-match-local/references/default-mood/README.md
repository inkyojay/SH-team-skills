# Default Brand Mood — 디폴트 톤 레퍼런스

이 폴더의 **첫 번째 이미지 파일**(`.jpg` / `.jpeg` / `.png` / `.webp`)이 `tone-match-local` 스킬의 디폴트 브랜드 톤 레퍼런스가 된다.

`batch-tone-match.mjs`가 `--reference` 인자 없이 실행되면 자동으로 이 폴더에서 이미지를 찾아 사용한다.

## 현재 의도된 디폴트 무드

**잔디밭 위 키즈 화이트/크림 룩** — 자연광 / 어스 톤 / 차분 / 자연스러움. SundayHug 브랜드 무드보드 핵심 비주얼.

권장 파일명: `earth-grass-kids.jpg` (자유)

## 교체 방법

기존 이미지를 지우고 새 이미지를 넣으면 끝. 파일명은 무관하지만 의미 있는 이름 권장.

```bash
# 예: 기존 디폴트 교체
rm skills/tone-match-local/references/default-mood/*.jpg
cp ~/Desktop/new-mood.jpg skills/tone-match-local/references/default-mood/earth-grass-kids.jpg
```

## 디폴트 톤 선정 기준

1. **명확한 색감** — 색온도, 채도, 명도 톤이 일관되게 보여야 함
2. **노이즈 없음** — 너무 강한 그래픽 텍스트나 워터마크는 제외
3. **고해상도** — 최소 1024px 이상 권장 (Gemini 모델이 톤을 안정적으로 추출하기 위함)
4. **브랜드 톤과 일치** — SundayHug 의 어스/내추럴/크림 무드를 가장 잘 대표하는 1장

## 변경 시 주의

이 폴더의 이미지가 바뀌면 그 시점부터 모든 디폴트 호출에 즉시 반영된다.
대량 톤 변환 작업 직전에 의도하지 않은 교체가 일어나지 않도록 주의.
