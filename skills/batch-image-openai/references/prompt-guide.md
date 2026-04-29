# 프롬프트 작성 가이드 — gpt-image-2

## 핵심 원칙

gpt-image-2는 자연어 프롬프트를 잘 이해합니다. **추상적 형용사보다 구체적 묘사**가 효과적.

❌ "예쁜 사진"
✅ "오후 4시 황금빛 자연광이 창문으로 들어오는 미니멀 침실, 화이트크림 시트와 베이지 벽지"

---

## 5가지 구성 요소

좋은 프롬프트는 다음 5개 중 3개 이상 포함:

| 요소 | 예시 |
|---|---|
| **조명** | 황금빛 자연광 / 부드러운 노스라이트 / 백라이트 / 골든아워 |
| **색감** | 베이지/크림 톤 / 파스텔 핑크 / 모노크롬 / 어스톤 |
| **배경** | 미니멀 침실 / 한국 아파트 거실 / 흰 시클로라마 / 자연 배경 |
| **스타일** | 시네마틱 / 라이프스타일 / 스튜디오 / 다큐멘터리 |
| **분위기** | 따뜻한 / 차분한 / 활기찬 / 감성적 |

---

## 자주 쓰는 패턴 (썬데이허그용)

### 라이프스타일 (감성)
```
A cozy lifestyle photograph of a baby crib in a Korean apartment bedroom,
soft golden hour natural light from large windows, warm beige and cream
tones, minimalist Scandinavian interior, gentle atmosphere, photographed
on Sony A7IV with 35mm lens, f/2.8, shallow depth of field
```

### 제품샷 (스튜디오)
```
A clean studio product shot of a folding baby bed on white seamless
backdrop, soft diffused lighting from above, slight shadow underneath,
neutral color grade, commercial photography, sharp focus, 85mm macro
```

### 이벤트/시즌 (강조)
```
A spring promotional image with soft pink cherry blossom background,
baby crib in warm cream color, gentle morning light, pastel palette,
Korean editorial magazine style, dreamy bokeh
```

### 라이브 방송 썸네일
```
A vibrant live broadcast thumbnail showing a baby crib with cooling
mesh pad, energetic pose, NAVER LIVE badge mockup in upper right,
cool blue and white tones, summer freshness, high contrast
```

---

## 한글 입력 (자동 번역됨)

스킬이 한글을 자동으로 영문 번역하므로 한국어 그대로 작성해도 됨:

```
오후의 부드러운 자연광이 들어오는 미니멀 침실,
크림색 아기 침대가 중앙에 놓여있고,
베이지 톤의 따뜻한 분위기, 라이프스타일 사진
```

내부적으로 gpt-4o-mini가 영문 번역:
```
A minimalist bedroom with soft afternoon natural light pouring in,
a cream-colored baby crib placed in the center,
warm beige tone atmosphere, lifestyle photography style
```

---

## 텍스트 포함하기 (gpt-image-2의 강점)

gpt-image-2는 한국어/영문 텍스트를 **이미지 안에 정확하게** 렌더링할 수 있습니다.

### 사용 예
```
A promotional poster with the Korean text "봄 신상 35% OFF" in elegant
sans-serif typography at the top, with a baby crib photograph below,
spring pastel colors, professional layout
```

⚠️ 텍스트는 **5~7 단어 이내**로 짧게. 긴 문장은 깨질 수 있음.

---

## 투명 배경 (PNG)

배너/카드 합성용 투명 배경 이미지:
```bash
node openai-image.mjs --generate \
  --prompt "A floating baby crib product cutout, no shadow, isolated" \
  --transparent \
  --format png
```

또는 프롬프트에 명시:
```
"isolated on transparent background, no shadow, product cutout style"
```

---

## 비용 절감 팁

1. **테스트는 `--quality low`** ($0.006/장) — 컨셉 확인용
2. **본 작업은 `--quality medium`** ($0.053/장) — 대부분 충분
3. **인쇄/포스터만 `--quality high`** ($0.211/장)
4. **`--prompt-only`**로 실제 호출 전 프롬프트 검토 가능
5. 일괄 처리 시 **`--n 3~5`로 시작** → 결과 확인 후 추가

---

## 사이즈 선택 가이드

| 사이즈 | 용도 |
|---|---|
| **1024×1024** | 인스타 정사각, 카카오 캐러셀 커머스, 썸네일 |
| **1536×1024** | 가로 배너, 페이스북 광고, 카카오 와이드 이미지(축소 후 사용) |
| **1024×1536** | 인스타 세로, 카카오 캐러셀 피드, 핀터레스트 |
| **auto** | 모델이 프롬프트 보고 결정 (실험용) |

---

## 자주 묻는 질문

### Q. 한 번에 5장 생성 시 모두 다른가요?
A. 네. gpt-image-2는 같은 프롬프트라도 매 호출마다 다른 결과를 생성합니다 (시드 미지원).

### Q. Gemini 버전과 결과가 어떻게 달라요?
A. OpenAI는 텍스트 렌더링·라이팅 디테일에 강하고, Gemini는 자연스러운 배경 합성에 강합니다.

### Q. n=10 이상 한 번에 가능?
A. SDK의 n 파라미터는 1만 권장됩니다 (gpt-image-2). 스킬은 내부적으로 N번 병렬 호출.

### Q. 인물 사진도 가능?
A. 가능. 단 실존 인물·연예인 묘사는 정책상 거부될 수 있습니다.
