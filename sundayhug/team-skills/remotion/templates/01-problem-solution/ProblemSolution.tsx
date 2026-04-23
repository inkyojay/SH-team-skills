import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { ProblemSolutionConfig, ProblemSolutionScene } from "./types";
import { calculateSceneStarts } from "../_shared/utils/timing";
import { ProblemScene } from "./components/ProblemScene";
import { SolutionScene } from "./components/SolutionScene";
import { TransitionArrow } from "./components/TransitionArrow";
import { CtaEndCard } from "../_shared/components/CtaEndCard";
import { Narration } from "../_shared/components/Narration";

/**
 * 01 문제-해결 소구점 템플릿
 *
 * 다크 톤의 문제 제시 → wipe 전환 → 밝은 솔루션 → CTA
 * 15~20초 권장
 *
 * @example
 * ```tsx
 * <Composition
 *   id="ProblemSolution"
 *   component={ProblemSolution}
 *   durationInFrames={30 * 18}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{ config: myConfig }}
 * />
 * ```
 */
export const ProblemSolution: React.FC<{ config: ProblemSolutionConfig }> = ({
  config,
}) => {
  const { fps } = useVideoConfig();
  const transitionDuration = config.transitionDurationFrames ?? 10;
  const format = config.format ?? "reels";

  const sceneStarts = calculateSceneStarts(
    config.scenes,
    fps,
    transitionDuration,
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1510" }}>
      <TransitionSeries>
        {config.scenes.flatMap((scene, i) => {
          const durationInFrames = Math.round(scene.durationSeconds * fps);
          const isLast = i === config.scenes.length - 1;
          const elements: React.ReactNode[] = [];

          elements.push(
            <TransitionSeries.Sequence
              key={`scene-${i}`}
              durationInFrames={durationInFrames}
            >
              {renderScene(scene, config)}
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

      {/* BGM */}
      {config.bgmSrc && (
        <Audio
          src={staticFile(config.bgmSrc)}
          volume={config.bgmVolume ?? 0.3}
        />
      )}

      {/* 나레이션 */}
      {config.narrationSrc ? (
        <Sequence from={5} layout="none">
          <Narration src={config.narrationSrc} />
        </Sequence>
      ) : (
        config.scenes.map((scene, i) => {
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
        })
      )}
    </AbsoluteFill>
  );
};

function renderScene(
  scene: ProblemSolutionScene,
  config: ProblemSolutionConfig,
): React.ReactNode {
  switch (scene.type) {
    case "problem":
      return (
        <ProblemScene
          mediaSrc={scene.mediaSrc}
          videoStartFrom={scene.videoStartFrom}
          problemText={scene.problemText}
          subText={scene.subText}
          palette={config.palette}
        />
      );
    case "solution":
      return (
        <>
          {/* 전환 오버레이 (씬 시작 시 잠깐 표시) */}
          <Sequence from={0} durationInFrames={30} layout="none">
            <TransitionArrow
              palette={config.palette}
              brandColor={config.brand.color}
            />
          </Sequence>
          <SolutionScene
            mediaSrc={scene.mediaSrc}
            videoStartFrom={scene.videoStartFrom}
            solutionText={scene.solutionText}
            subText={scene.subText}
            productName={scene.productName}
            palette={config.palette}
            brandColor={config.brand.color}
          />
        </>
      );
    case "cta":
      return (
        <AbsoluteFill>
          {scene.mediaSrc && (
            <AbsoluteFill style={{ filter: "blur(8px) brightness(0.5)" }}>
              <img
                src={scene.mediaSrc}
                style={{ width: "100%", height: "100%", objectFit: "cover" }}
              />
            </AbsoluteFill>
          )}
          <CtaEndCard
            brandName={config.brand.name}
            brandColor={config.brand.color}
            productName={scene.productName}
            ctaText={scene.ctaText}
          />
        </AbsoluteFill>
      );
  }
}
