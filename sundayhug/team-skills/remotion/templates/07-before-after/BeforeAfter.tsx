import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { BeforeAfterConfig, BeforeAfterScene } from "./types";
import { calculateSceneStarts } from "../_shared/utils/timing";
import { WipeReveal } from "./components/WipeReveal";
import { VideoClip } from "../_shared/components/VideoClip";
import { Caption } from "../_shared/components/Caption";
import { CtaEndCard } from "../_shared/components/CtaEndCard";
import { Narration } from "../_shared/components/Narration";

/**
 * 07 비포/애프터 소구점 템플릿
 *
 * clipPath wipe로 전/후 비교를 극적으로 표현합니다.
 * 15~20초 권장
 */
export const BeforeAfter: React.FC<{ config: BeforeAfterConfig }> = ({
  config,
}) => {
  const { fps } = useVideoConfig();
  const transitionDuration = config.transitionDurationFrames ?? 10;

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
  scene: BeforeAfterScene,
  config: BeforeAfterConfig,
): React.ReactNode {
  switch (scene.type) {
    case "intro":
      return (
        <VideoClip src={scene.mediaSrc}>
          <Sequence from={8} layout="none">
            <Caption
              line1={scene.text}
              line2={scene.subText}
              format={config.format}
            />
          </Sequence>
        </VideoClip>
      );
    case "compare":
      return (
        <WipeReveal
          beforeSrc={scene.pair.beforeSrc}
          afterSrc={scene.pair.afterSrc}
          beforeLabel={scene.pair.beforeLabel}
          afterLabel={scene.pair.afterLabel}
          caption={scene.pair.caption}
          wipeDirection={scene.wipeDirection}
          palette={config.palette}
          brandColor={config.brand.color}
        />
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
