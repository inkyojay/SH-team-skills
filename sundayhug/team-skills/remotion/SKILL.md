---
name: remotion-best-practices
description: Best practices for Remotion - Video creation in React
metadata:
  tags: remotion, video, react, animation, composition
---

## When to use

Use this skills whenever you are dealing with Remotion code to obtain the domain-specific knowledge.

## How to use

Read individual rule files for detailed explanations and code examples:

- [rules/3d.md](rules/3d.md) - 3D content in Remotion using Three.js and React Three Fiber
- [rules/animations.md](rules/animations.md) - Fundamental animation skills for Remotion
- [rules/assets.md](rules/assets.md) - Importing images, videos, audio, and fonts into Remotion
- [rules/audio.md](rules/audio.md) - Using audio and sound in Remotion - importing, trimming, volume, speed, pitch
- [rules/calculate-metadata.md](rules/calculate-metadata.md) - Dynamically set composition duration, dimensions, and props
- [rules/can-decode.md](rules/can-decode.md) - Check if a video can be decoded by the browser using Mediabunny
- [rules/charts.md](rules/charts.md) - Chart and data visualization patterns for Remotion
- [rules/compositions.md](rules/compositions.md) - Defining compositions, stills, folders, default props and dynamic metadata
- [rules/display-captions.md](rules/display-captions.md) - Displaying captions in Remotion with TikTok-style pages and word highlighting
- [rules/extract-frames.md](rules/extract-frames.md) - Extract frames from videos at specific timestamps using Mediabunny
- [rules/fonts.md](rules/fonts.md) - Loading Google Fonts and local fonts in Remotion
- [rules/get-audio-duration.md](rules/get-audio-duration.md) - Getting the duration of an audio file in seconds with Mediabunny
- [rules/get-video-dimensions.md](rules/get-video-dimensions.md) - Getting the width and height of a video file with Mediabunny
- [rules/get-video-duration.md](rules/get-video-duration.md) - Getting the duration of a video file in seconds with Mediabunny
- [rules/gifs.md](rules/gifs.md) - Displaying GIFs synchronized with Remotion's timeline
- [rules/images.md](rules/images.md) - Embedding images in Remotion using the Img component
- [rules/import-srt-captions.md](rules/import-srt-captions.md) - Importing .srt subtitle files into Remotion using @remotion/captions
- [rules/lottie.md](rules/lottie.md) - Embedding Lottie animations in Remotion
- [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - Measuring DOM element dimensions in Remotion
- [rules/measuring-text.md](rules/measuring-text.md) - Measuring text dimensions, fitting text to containers, and checking overflow
- [rules/sequencing.md](rules/sequencing.md) - Sequencing patterns for Remotion - delay, trim, limit duration of items
- [rules/tailwind.md](rules/tailwind.md) - Using TailwindCSS in Remotion
- [rules/text-animations.md](rules/text-animations.md) - Typography and text animation patterns for Remotion
- [rules/timing.md](rules/timing.md) - Interpolation curves in Remotion - linear, easing, spring animations
- [rules/transcribe-captions.md](rules/transcribe-captions.md) - Transcribing audio to generate captions in Remotion
- [rules/transitions.md](rules/transitions.md) - Scene transition patterns for Remotion
- [rules/trimming.md](rules/trimming.md) - Trimming patterns for Remotion - cut the beginning or end of animations
- [rules/videos.md](rules/videos.md) - Embedding videos in Remotion - trimming, volume, speed, looping, pitch
- [rules/parameters.md](rules/parameters.md) - Make a video parametrizable by adding a Zod schema
- [rules/maps.md](rules/maps.md) - Add a map using Mapbox and animate it

## Templates

Ready-to-use Remotion templates for common use cases.
전체 목록은 [templates/template-registry.md](templates/template-registry.md) 참조.

- [templates/meta-reels-ad](templates/meta-reels-ad/) - Meta(Instagram/Facebook) Reels 광고 영상 템플릿 (9:16, 1080x1920)
  - Config 기반 멀티씬 구조: `AdConfig`로 씬, 브랜드, 별점 등 설정
  - TTS 나레이션: `scripts/generate-tts.sh` (Supertone TTS) + `scripts/trim-audio.sh` (FFmpeg 무음 제거)
  - **나레이션 2가지 모드**: 통합 나레이션 (`config.narrationSrc` — 영상 전체에 스토리 1개) 또는 씬별 나레이션 (`scene.narrationSrc`)
  - BGM 지원: `config.bgmSrc`로 배경 음악 추가, 볼륨 조절 가능
  - 프로젝트 스캐폴딩: `scaffolding/` 폴더의 템플릿으로 빠르게 새 프로젝트 생성

- [templates/ugc-review](templates/ugc-review/) - UGC 리뷰형 광고 (30~45초)
  - 셀카 훅 → 네이버 검색 → 제품 시연 → 기능 소개 → CTA 흐름
  - 캐주얼 나레이션, 흰/노랑 볼드 자막, 키워드 하이라이트
  - 씬 타입별 전용 컴포넌트: SelfieHook, SearchScreen, DemoClip

- [templates/comparison](templates/comparison/) - 비교 추천형 광고 (45~60초)
  - 문제 제시 → 제품 비교 그리드 → 솔루션 시연 → 차별화 → CTA 흐름
  - 둥근 필(pill) 스타일 자막, 정보 전달형 톤
  - 2~4개 제품 비교 그리드 레이아웃, 추천 제품 하이라이트

- [templates/branded-showcase](templates/branded-showcase/) - 브랜드 공식형 광고 (30~45초)
  - 고정 헤더(로고+제품명+썸네일) + 하단 콘텐츠 순환 구조
  - 전문 나레이션, 컬러 하이라이트 자막 (키워드에 브랜드 컬러 배경)
  - 일관된 브랜드 아이덴티티 유지

- [templates/review-banner](templates/review-banner/) - 리뷰 배너형 광고 (5~10초)
  - 정적 컴포지트 레이아웃: 리뷰 카드(별점+말풍선) + 제품 배너
  - 짧은 피드 광고, 리타겟팅에 최적화
  - 순차 등장 애니메이션 + Ken Burns 배경 효과
