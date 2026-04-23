import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { ComparisonConfig } from "./types";
import { PillCaption } from "./components/PillCaption";
import { ProblemScene } from "./components/ProblemScene";
import { ProductGrid } from "./components/ProductGrid";
import { SolutionDemo } from "./components/SolutionDemo";
import { Narration } from "../meta-reels-ad/components/Narration";
import { calculateSceneStarts } from "../meta-reels-ad/utils/timing";

/**
 * 비교 추천형 광고 - 메인 컴포넌트
 *
 * 문제 제시 → 제품 비교 → 솔루션 시연 → 차별화 → CTA 흐름으로
 * 논리적인 비교/추천 광고를 구성합니다.
 *
 * - 씬 타입별 전용 레이아웃 (문제/비교그리드/솔루션)
 * - 둥근 필(pill) 스타일 자막
 * - 부드러운 페이드 전환 (기본 10프레임)
 *
 * @example
 * ```tsx
 * <Composition
 *   id="ComparisonAd"
 *   component={Comparison}
 *   durationInFrames={30 * 55}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{ config: myComparisonConfig }}
 * />
 * ```
 */
export const Comparison: React.FC<{ config: ComparisonConfig }> = ({
  config,
}) => {
  const { fps } = useVideoConfig();

  const transitionDuration = config.transitionDurationFrames ?? 10;

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
      case "problem":
        return (
          <ProblemScene src={scene.videoSrc} startFrom={scene.videoStartFrom}>
            {children}
          </ProblemScene>
        );
      case "comparison":
        return (
          <ProductGrid
            products={scene.products ?? []}
            questionText={scene.questionText}
            brandColor={config.brand.color}
          >
            {children}
          </ProductGrid>
        );
      default:
        return (
          <SolutionDemo src={scene.videoSrc} startFrom={scene.videoStartFrom}>
            {children}
          </SolutionDemo>
        );
    }
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* ─── 비디오 + 자막 (TransitionSeries) ─── */}
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
              {renderSceneContent(
                scene,
                <Sequence from={captionDelay} layout="none">
                  <PillCaption
                    text={scene.caption.text}
                    backgroundColor={scene.caption.backgroundColor}
                    textColor={scene.caption.textColor}
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
