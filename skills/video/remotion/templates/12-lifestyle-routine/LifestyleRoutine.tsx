import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { LifestyleRoutineConfig, LifestyleScene } from "./types";
import { calculateSceneStarts } from "../_shared/utils/timing";
import { StepCard } from "./components/StepCard";
import { VideoClip } from "../_shared/components/VideoClip";
import { Caption } from "../_shared/components/Caption";
import { CtaEndCard } from "../_shared/components/CtaEndCard";
import { Narration } from "../_shared/components/Narration";
import { getPalette } from "../_shared/utils/palettes";

/**
 * 12 라이프스타일/루틴 소구점 템플릿
 *
 * 스텝 번호 팝인 + 타임라인 연결선 + 프로그레스 닷으로
 * 일상 루틴 속 제품 사용 과정을 보여줍니다.
 * 20~30초 권장 (스텝이 많아 약간 길게)
 */
export const LifestyleRoutine: React.FC<{
  config: LifestyleRoutineConfig;
}> = ({ config }) => {
  const { fps } = useVideoConfig();
  const transitionDuration = config.transitionDurationFrames ?? 12;
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
  scene: LifestyleScene,
  config: LifestyleRoutineConfig,
): React.ReactNode {
  switch (scene.type) {
    case "intro":
      return (
        <VideoClip src={scene.mediaSrc}>
          <Sequence from={8} layout="none">
            <Caption
              line1={scene.title}
              line2={scene.subTitle}
              format={config.format}
            />
          </Sequence>
        </VideoClip>
      );
    case "step":
      return (
        <StepCard
          step={scene.step}
          totalSteps={scene.totalSteps}
          palette={config.palette}
          brandColor={config.brand.color}
        />
      );
    case "summary":
      return (
        <AbsoluteFill
          style={{
            background: `linear-gradient(180deg, ${getPalette(config.palette).bg} 0%, ${getPalette(config.palette).bgWarm} 100%)`,
          }}
        >
          {scene.mediaSrc && (
            <VideoClip src={scene.mediaSrc} showGradient={false} />
          )}
          <Sequence from={8} layout="none">
            <Caption
              line1={scene.summaryText}
              line2={scene.productName}
              format={config.format}
            />
          </Sequence>
        </AbsoluteFill>
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
