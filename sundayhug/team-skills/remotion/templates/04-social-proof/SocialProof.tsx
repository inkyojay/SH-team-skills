import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { SocialProofConfig, SocialProofScene } from "./types";
import { calculateSceneStarts } from "../_shared/utils/timing";
import { StatsGrid } from "./components/StatsGrid";
import { RatingDisplay } from "./components/RatingDisplay";
import { BadgeRow } from "./components/BadgeRow";
import { VideoClip } from "../_shared/components/VideoClip";
import { Caption } from "../_shared/components/Caption";
import { CtaEndCard } from "../_shared/components/CtaEndCard";
import { Narration } from "../_shared/components/Narration";

/**
 * 04 사회적 증거 소구점 템플릿
 *
 * 숫자 카운트업, 별점, 인증 뱃지로 신뢰를 구축합니다.
 * 15~20초 권장
 */
export const SocialProof: React.FC<{ config: SocialProofConfig }> = ({
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
    <AbsoluteFill style={{ backgroundColor: "#FAF7F4" }}>
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
  scene: SocialProofScene,
  config: SocialProofConfig,
): React.ReactNode {
  switch (scene.type) {
    case "stats":
      return (
        <StatsGrid
          stats={scene.stats}
          palette={config.palette}
          brandColor={config.brand.color}
        />
      );
    case "rating":
      return (
        <RatingDisplay
          score={scene.score}
          reviewCountText={scene.reviewCountText}
          featuredReview={scene.featuredReview}
          palette={config.palette}
          brandColor={config.brand.color}
        />
      );
    case "badges":
      return (
        <BadgeRow
          badges={scene.badges}
          headline={scene.headline}
          palette={config.palette}
          brandColor={config.brand.color}
        />
      );
    case "reviews":
      // 리뷰 카루셀은 RatingDisplay를 변형하여 표시
      return (
        <RatingDisplay
          score={scene.reviews[0]?.rating ?? 5}
          reviewCountText={`${scene.reviews.length}개 리뷰`}
          featuredReview={scene.reviews[0]}
          palette={config.palette}
          brandColor={config.brand.color}
        />
      );
    case "cta":
      return (
        <CtaEndCard
          brandName={config.brand.name}
          brandColor={config.brand.color}
          productName={scene.productName}
          ctaText={scene.ctaText}
        />
      );
  }
}
