import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { EmotionalConfig, EmotionalScene } from "./types";
import { calculateSceneStarts } from "../_shared/utils/timing";
import { KenBurnsImage } from "./components/KenBurnsImage";
import { QuoteCard } from "./components/QuoteCard";
import { VideoClip } from "../_shared/components/VideoClip";
import { Caption } from "../_shared/components/Caption";
import { CtaEndCard } from "../_shared/components/CtaEndCard";
import { Narration } from "../_shared/components/Narration";
import { getPalette } from "../_shared/utils/palettes";

/**
 * 02 감성 소구점 템플릿
 *
 * Ken Burns 풀블리드 + 슬로우 페이드 + 감성 인용구.
 * 15~25초 권장 (느린 템포)
 */
export const Emotional: React.FC<{ config: EmotionalConfig }> = ({
  config,
}) => {
  const { fps } = useVideoConfig();
  const transitionDuration = config.transitionDurationFrames ?? 15; // 감성은 전환이 더 느림
  const pal = getPalette(config.palette);

  const sceneStarts = calculateSceneStarts(
    config.scenes,
    fps,
    transitionDuration,
  );

  return (
    <AbsoluteFill style={{ backgroundColor: pal.bg }}>
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

      {config.bgmSrc && (
        <Audio
          src={staticFile(config.bgmSrc)}
          volume={config.bgmVolume ?? 0.3}
        />
      )}

      {config.narrationSrc ? (
        <Sequence from={5} layout="none">
          <Narration src={config.narrationSrc} />
        </Sequence>
      ) : (
        config.scenes.map((scene, i) => {
          if (!scene.narrationSrc) return null;
          return (
            <Sequence
              key={`narration-${i}`}
              from={sceneStarts[i] + (scene.narrationDelay ?? 5)}
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
  scene: EmotionalScene,
  config: EmotionalConfig,
): React.ReactNode {
  switch (scene.type) {
    case "mood":
      return (
        <KenBurnsImage
          src={scene.mediaSrc}
          videoStartFrom={scene.videoStartFrom}
          direction={scene.kenBurnsDirection}
          overlayText={scene.overlayText}
        />
      );
    case "quote":
      return (
        <QuoteCard
          quoteText={scene.quoteText}
          attribution={scene.attribution}
          backgroundColor={scene.backgroundColor}
          palette={config.palette}
          brandColor={config.brand.color}
        />
      );
    case "product":
      return (
        <KenBurnsImage src={scene.mediaSrc} videoStartFrom={scene.videoStartFrom}>
          <Sequence from={10} layout="none">
            <Caption
              line1={scene.caption}
              line2={scene.subCaption}
              format={config.format}
            />
          </Sequence>
        </KenBurnsImage>
      );
    case "cta":
      return (
        <AbsoluteFill>
          {scene.mediaSrc && (
            <AbsoluteFill style={{ filter: "blur(12px) brightness(0.4)" }}>
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
