# Meta Reels 광고 템플릿 (Remotion)

Config 기반 멀티씬 세로형 릴스/스토리 광고 영상 템플릿입니다.
TTS 나레이션 + 비디오 클립 + 자막을 조합하여 15초 광고를 생성합니다.

## 규격

| 항목 | 값 |
|------|-----|
| 해상도 | 1080×1920 |
| 비율 | 9:16 (세로) |
| FPS | 30 |
| 권장 길이 | 6~15초 |

## 아키텍처

```
AdConfig (types.ts)
  ├── scenes[] → TransitionSeries (비디오 + 자막)
  ├── brand    → BrandLogo 컴포넌트
  └── rating   → RatingBadge 컴포넌트

나레이션은 TransitionSeries 바깥에 절대 프레임으로 배치
(씬 전환 시 오디오 겹침 방지)
```

### 핵심 패턴: 나레이션 외부 배치

TransitionSeries 내부에 Audio를 넣으면 씬 전환 시 오디오가 겹칩니다.
나레이션을 TransitionSeries **바깥**에 절대 프레임으로 배치하여 해결합니다:

```tsx
<AbsoluteFill>
  <TransitionSeries>{/* 비디오 + 자막만 */}</TransitionSeries>
  {/* 나레이션: 절대 타이밍 */}
  <Sequence from={sceneStarts[i] + delay}>
    <Narration src="audio/scene1.mp3" />
  </Sequence>
</AbsoluteFill>
```

`utils/timing.ts`의 `calculateSceneStarts()`가 TransitionSeries 오버랩을 고려하여 각 씬의 절대 시작 프레임을 자동 계산합니다.

## 파일 구조

```
meta-reels-ad/
├── MetaReelsAd.tsx          # 메인 컴포넌트 (config → 멀티씬 렌더링)
├── types.ts                 # AdConfig, SceneConfig 타입
├── components/
│   ├── Caption.tsx          # 흰색 볼드 자막 (spring 애니메이션)
│   ├── BrandLogo.tsx        # 브랜드 로고 뱃지 (파라미터화)
│   ├── RatingBadge.tsx      # 별점 뱃지 (파라미터화)
│   ├── VideoClip.tsx        # 비디오 + 그라데이션 래퍼
│   └── Narration.tsx        # Audio 래퍼
├── utils/
│   └── timing.ts            # 씬 시작 프레임 계산 유틸
├── scaffolding/             # 프로젝트 스캐폴딩 템플릿
│   ├── package.json.template
│   ├── tsconfig.json.template
│   ├── Root.tsx.template
│   └── index.ts.template
├── scripts/
│   ├── generate-tts.sh      # Google Cloud TTS 생성
│   └── trim-audio.sh        # FFmpeg 오디오 트리밍
└── README.md                # 이 문서
```

## 사용법

### 1. 프로젝트 스캐폴딩

```bash
npx create-video@latest my-ad --blank
cd my-ad
npm install @remotion/transitions
```

`scaffolding/` 폴더의 템플릿 파일들을 참고하여 프로젝트를 구성합니다.
`{{BRAND_NAME}}`, `{{BRAND_COLOR}}`, `{{COMPOSITION_ID}}` 등의 플레이스홀더를 교체하세요.

### 2. AdConfig 정의

`types.ts`의 `AdConfig` 인터페이스에 맞게 광고 설정을 작성합니다:

```tsx
import type { AdConfig } from "./types";

const myAdConfig: AdConfig = {
  brand: { name: "MY BRAND", color: "#5a7d65" },
  rating: { score: "4.9", reviewCount: "227개 리뷰" },
  transitionDurationFrames: 8,
  scenes: [
    {
      videoSrc: "hook.mp4",
      durationSeconds: 3,
      caption: { line1: "후킹 카피", line2: "서브 카피" },
      narrationSrc: "audio/scene1.mp3",
      showBrandLogo: true,
    },
    {
      videoSrc: "problem.mp4",
      durationSeconds: 2,
      caption: { line1: "문제 제기" },
      narrationSrc: "audio/scene2.mp3",
    },
    // ... 추가 씬
  ],
};
```

### 3. TTS 나레이션 생성

**방법 A: 통합 나레이션 (권장)**

화면 텍스트와 별도로, 영상 전체를 하나의 스토리처럼 풀어주는 나레이션을 생성합니다.
화면 자막은 핵심 키워드 위주로, 나레이션은 자연스러운 이야기 흐름으로 구성하면 효과적입니다.

```bash
# 하나의 스토리 나레이션 생성
./scripts/generate-tts.sh "우리 아기가 밤새 안전하게 잘 수 있도록, 꿀잠 슬리핑백이 함께해요." public/audio/narration.mp3 e5f6fb1a53d0add87afb4f happy 1.1
```

Config에 통합 나레이션 + BGM 설정:
```ts
const myAdConfig: AdConfig = {
  narrationSrc: "audio/narration.mp3",
  narrationDelay: 3,
  bgmSrc: "audio/bgm.mp3",
  bgmVolume: 0.25,
  scenes: [
    // 씬별 narrationSrc 없이 사용
  ],
};
```

**방법 B: 씬별 나레이션**

각 씬에 개별 나레이션을 넣는 기존 방식입니다.

```bash
# Supertone TTS로 씬별 나레이션 생성
./scripts/generate-tts.sh "후킹 카피 텍스트" public/audio/scene1.mp3

# 앞뒤 무음 제거
./scripts/trim-audio.sh public/audio/scene1.mp3
```

### 4. 비디오 소스 준비

`public/` 폴더에 각 씬의 비디오 파일을 추가합니다.
- 9:16 세로 비디오 권장
- `videoStartFrom`으로 시작 지점 조절 가능 (초 단위)

### 5. 미리보기 & 렌더링

```bash
# 미리보기
npm run dev

# 렌더링
npx remotion render MyAd out/ad.mp4
```

## SceneConfig 옵션

| 필드 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `videoSrc` | string | (필수) | 비디오 파일명 |
| `videoStartFrom` | number | 0 | 비디오 시작 지점 (초) |
| `durationSeconds` | number | (필수) | 씬 길이 (초) |
| `caption` | object | (필수) | `{ line1, line2?, emoji? }` |
| `narrationSrc` | string | - | 씬별 나레이션 오디오 파일명 |
| `narrationDelay` | number | 5 | 씬별 나레이션 시작 딜레이 (프레임) |
| `captionDelay` | number | 5 | 자막 등장 딜레이 (프레임) |
| `showBrandLogo` | boolean | false | 브랜드 로고 표시 |
| `showRatingBadge` | boolean | false | 별점 뱃지 표시 |
| `ratingBadgeDelay` | number | 40 | 별점 뱃지 딜레이 (프레임) |

## AdConfig 옵션

| 필드 | 타입 | 기본값 | 설명 |
|------|------|--------|------|
| `narrationSrc` | string | - | 통합 나레이션 오디오 (씬별 narrationSrc보다 우선) |
| `narrationDelay` | number | 5 | 통합 나레이션 시작 딜레이 (프레임) |
| `bgmSrc` | string | - | 배경 음악 오디오 파일명 |
| `bgmVolume` | number | 0.3 | 배경 음악 볼륨 (0~1) |

## 15초 광고 구성 예시

| 씬 | 시간 | 역할 | 예시 |
|----|------|------|------|
| 1 | 0-3초 | 후킹 | "이불 밖으로 나오는 아이" |
| 2 | 3-5초 | 문제 제기 | "매번 걱정되시죠?" |
| 3 | 5-9초 | 솔루션 | "슬리핑백이 답이에요" |
| 4 | 9-12초 | 소재/혜택 | "실키밤부 원단이라 부드러워요" |
| 5 | 12-15초 | CTA | "꿀잠 슬리핑백 ✨" + 별점 |

## 관련 리소스

- [Remotion 베스트 프랙티스](../../rules/) - 규칙 파일 모음
- TTS: [Supertone API](https://docs.supertoneapi.com) (한국어 여성 Agatha 추천)
- 오디오 편집: [FFmpeg](https://ffmpeg.org/)
