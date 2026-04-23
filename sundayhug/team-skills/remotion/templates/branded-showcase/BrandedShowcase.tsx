import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { BrandedShowcaseConfig } from "./types";
import { BrandHeader } from "./components/BrandHeader";
import { FeatureSlide } from "./components/FeatureSlide";
import { HighlightCaption } from "./components/HighlightCaption";
import { Narration } from "../meta-reels-ad/components/Narration";
import { calculateSceneStarts } from "../meta-reels-ad/utils/timing";

/**
 * 브랜드 공식형 광고 - 메인 컴포넌트
 *
 * 고정 헤더(로고+제품명+썸네일)가 상단에 유지되고,
 * 하단 콘텐츠 영역만 씬마다 전환됩니다.
 *
 * - 고정 헤더로 브랜드 일관성 유지
 * - 컬러 하이라이트 자막으로 핵심 키워드 강조
 * - 전문적인 톤의 브랜드 영상
 *
 * @example
 * ```tsx
 * <Composition
 *   id="BrandedShowcaseAd"
 *   component={BrandedShowcase}
 *   durationInFrames={30 * 40}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{ config: myShowcaseConfig }}
 * />
 * ```
 */
export const BrandedShowcase: React.FC<{
  config: BrandedShowcaseConfig;
}> = ({ config }) => {
  const { fps } = useVideoConfig();

  const transitionDuration = config.transitionDurationFrames ?? 8;

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

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* ─── 하단 콘텐츠 (TransitionSeries) ─── */}
      <TransitionSeries>
        {config.scenes.flatMap((scene, i) => {
          const durationInFrames = Math.round(scene.durationSeconds * fps);
          const captionDelay = scene.captionDelay ?? 8;
          const isLast = i === config.scenes.length - 1;

          const elements: React.ReactNode[] = [];

          elements.push(
            <TransitionSeries.Sequence
              key={`scene-${i}`}
              durationInFrames={durationInFrames}
            >
              <FeatureSlide
                src={scene.videoSrc}
                startFrom={scene.videoStartFrom}
              >
                <Sequence from={captionDelay} layout="none">
                  <HighlightCaption
                    text={scene.caption.text}
                    highlightWords={scene.caption.highlightWords}
                    brandColor={config.brand.color}
                  />
                </Sequence>
              </FeatureSlide>
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

      {/* ─── 고정 헤더 (항상 최상위) ─── */}
      <BrandHeader
        logoSrc={config.header.logoSrc}
        productName={config.header.productName}
        productImageSrc={config.header.productImageSrc}
        brandColor={config.brand.color}
      />

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
