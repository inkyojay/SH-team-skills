import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { UgcReviewConfig } from "./types";
import { UgcCaption } from "./components/UgcCaption";
import { SelfieHook } from "./components/SelfieHook";
import { SearchScreen } from "./components/SearchScreen";
import { DemoClip } from "./components/DemoClip";
import { Narration } from "../meta-reels-ad/components/Narration";
import { calculateSceneStarts } from "../meta-reels-ad/utils/timing";

/**
 * UGC 리뷰형 광고 - 메인 컴포넌트
 *
 * 셀카 훅 → 검색 화면 → 제품 시연 → 기능 소개 → CTA 흐름으로
 * 자연스러운 UGC 스타일 광고를 구성합니다.
 *
 * - 씬 타입별로 적합한 컴포넌트를 자동 선택
 * - 강조 키워드 노랑 하이라이트 지원
 * - 빠른 컷 전환 (기본 4프레임)
 *
 * @example
 * ```tsx
 * <Composition
 *   id="UgcReviewAd"
 *   component={UgcReview}
 *   durationInFrames={30 * 38}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{ config: myUgcConfig }}
 * />
 * ```
 */
export const UgcReview: React.FC<{ config: UgcReviewConfig }> = ({
  config,
}) => {
  const { fps } = useVideoConfig();

  const transitionDuration = config.transitionDurationFrames ?? 4;
  const highlightColor = config.highlightColor ?? "#FFE53B";

  // Narration을 위한 절대 프레임 계산 (meta-reels-ad의 유틸 재사용)
  const scenesForTiming = config.scenes.map((s) => ({
    durationSeconds: s.durationSeconds,
    videoSrc: s.videoSrc,
    caption: { line1: s.caption.text },
  }));
  const sceneStarts = calculateSceneStarts(
    scenesForTiming,
    fps,
    transitionDuration,
  );

  const renderSceneContent = (
    scene: (typeof config.scenes)[0],
    children: React.ReactNode,
  ) => {
    switch (scene.type) {
      case "selfie-hook":
        return (
          <SelfieHook src={scene.videoSrc} startFrom={scene.videoStartFrom}>
            {children}
          </SelfieHook>
        );
      case "search-screen":
        return (
          <SearchScreen
            src={scene.videoSrc}
            startFrom={scene.videoStartFrom}
            searchQuery={config.searchOverlay?.searchQuery}
            platform={config.searchOverlay?.platform}
          >
            {children}
          </SearchScreen>
        );
      default:
        return (
          <DemoClip src={scene.videoSrc} startFrom={scene.videoStartFrom}>
            {children}
          </DemoClip>
        );
    }
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* ─── 비디오 + 자막 (TransitionSeries) ─── */}
      <TransitionSeries>
        {config.scenes.flatMap((scene, i) => {
          const durationInFrames = Math.round(scene.durationSeconds * fps);
          const captionDelay = scene.captionDelay ?? 5;
          const isLast = i === config.scenes.length - 1;

          const elements: React.ReactNode[] = [];

          elements.push(
            <TransitionSeries.Sequence
              key={`scene-${i}`}
              durationInFrames={durationInFrames}
            >
              {renderSceneContent(
                scene,
                <Sequence from={captionDelay} layout="none">
                  <UgcCaption
                    text={scene.caption.text}
                    highlightWords={scene.caption.highlightWords}
                    highlightColor={highlightColor}
                  />
                </Sequence>,
              )}
            </TransitionSeries.Sequence>,
          );

          if (!isLast) {
            elements.push(
              <TransitionSeries.Transition
                key={`transition-${i}`}
                presentation={fade()}
                timing={linearTiming({
                  durationInFrames: transitionDuration,
                })}
              />,
            );
          }

          return elements;
        })}
      </TransitionSeries>

      {/* ─── 나레이션: TransitionSeries 바깥에서 절대 타이밍 ─── */}
      {config.scenes.map((scene, i) => {
        if (!scene.narrationSrc) return null;
        const delay = scene.narrationDelay ?? 5;
        return (
          <Sequence
            key={`narration-${i}`}
            from={sceneStarts[i] + delay}
            layout="none"
          >
            <Narration src={scene.narrationSrc} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
