import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import type { AdConfig } from "./types";
import { calculateSceneStarts } from "./utils/timing";
import { Caption } from "./components/Caption";
import { BrandLogo } from "./components/BrandLogo";
import { RatingBadge } from "./components/RatingBadge";
import { VideoClip } from "./components/VideoClip";
import { Narration } from "./components/Narration";

/**
 * Meta Reels 광고 - Config 기반 멀티씬 컴포넌트
 *
 * AdConfig를 받아 자동으로 TransitionSeries를 구성합니다.
 * 나레이션은 TransitionSeries 바깥에 절대 프레임으로 배치하여
 * 씬 전환 시 오디오 겹침을 방지합니다.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="MyAd"
 *   component={MetaReelsAd}
 *   durationInFrames={30 * 15}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{ config: myAdConfig }}
 * />
 * ```
 */
export const MetaReelsAd: React.FC<{ config: AdConfig }> = ({ config }) => {
  const { fps } = useVideoConfig();

  const transitionDuration = config.transitionDurationFrames ?? 8;
  const sceneStarts = calculateSceneStarts(
    config.scenes,
    fps,
    transitionDuration,
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* ─── 비디오 + 자막 (TransitionSeries) ─── */}
      <TransitionSeries>
        {config.scenes.flatMap((scene, i) => {
          const durationInFrames = Math.round(scene.durationSeconds * fps);
          const captionDelay = scene.captionDelay ?? 5;
          const ratingBadgeDelay = scene.ratingBadgeDelay ?? 40;
          const isLast = i === config.scenes.length - 1;

          const elements: React.ReactNode[] = [];

          elements.push(
            <TransitionSeries.Sequence
              key={`scene-${i}`}
              durationInFrames={durationInFrames}
            >
              <VideoClip
                src={scene.videoSrc}
                startFrom={scene.videoStartFrom}
              >
                {scene.showBrandLogo && (
                  <Sequence from={captionDelay} layout="none">
                    <BrandLogo
                      brandName={config.brand.name}
                      brandColor={config.brand.color}
                    />
                  </Sequence>
                )}
                <Sequence from={captionDelay} layout="none">
                  <Caption
                    line1={scene.caption.line1}
                    line2={scene.caption.line2}
                    emoji={scene.caption.emoji}
                  />
                </Sequence>
                {scene.showRatingBadge && config.rating && (
                  <Sequence from={ratingBadgeDelay} layout="none">
                    <RatingBadge
                      score={config.rating.score}
                      reviewCount={config.rating.reviewCount}
                    />
                  </Sequence>
                )}
              </VideoClip>
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

      {/* ─── BGM ─── */}
      {config.bgmSrc && (
        <Audio src={staticFile(config.bgmSrc)} volume={config.bgmVolume ?? 0.3} />
      )}

      {/* ─── 나레이션 ─── */}
      {config.narrationSrc ? (
        /* 통합 나레이션: 하나의 스토리를 영상 전체에 재생 */
        <Sequence from={config.narrationDelay ?? 5} layout="none">
          <Narration src={config.narrationSrc} />
        </Sequence>
      ) : (
        /* 씬별 나레이션: 각 씬에 개별 오디오 배치 (하위 호환) */
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
