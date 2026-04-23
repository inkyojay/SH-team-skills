import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  Sequence,
  interpolate,
} from "remotion";
import type { HookRevealConfig } from "./types";
import { HookText } from "./components/HookText";
import { RevealScene } from "./components/RevealScene";

/**
 * V05 - Scroll-Stop Hook + Reveal 광고
 *
 * 2단 구성 B급 감성 템플릿:
 * 1) 훅: 화면을 가득 채우는 충격적 대형 텍스트
 * 2) 하드 컷 (2프레임 흰색 플래시)
 * 3) 리빌: 제품 공개 + CTA
 *
 * @example
 * ```tsx
 * <Composition
 *   id="HookReveal"
 *   component={HookReveal}
 *   durationInFrames={30 * 12}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       hookText: "아기 재우는데\n10분이면 충분",
 *       hookEmoji: "😴",
 *       hookBgColor: "#000",
 *       revealProductName: "선데이허그 스와들스트랩",
 *       revealCaption: "특허받은 양팔 고정 설계로\n아기가 스스로 잠드는 기적",
 *       ctaText: "지금 바로 구매 →",
 *     },
 *   }}
 * />
 * ```
 */
export const HookReveal: React.FC<{ config: HookRevealConfig }> = ({
  config,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const scale = Math.min(width / 1080, height / 1920);
  const hookDuration = (config.hookDuration ?? 1.5) * fps;
  const enableFlash = config.enableFlash ?? true;
  const flashDuration = enableFlash ? 2 : 0; // 2프레임 플래시
  const revealStart = Math.round(hookDuration + flashDuration);

  const hookBgColor = config.hookBgColor ?? "#000";
  const hookTextColor = config.hookTextColor ?? "#FFF";
  const ctaColor = config.ctaColor ?? "#FF0050";
  const revealBgColor = config.revealBgColor ?? "#FFF";

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* Hook Scene */}
      <Sequence from={0} durationInFrames={Math.round(hookDuration)}>
        <HookText
          text={config.hookText}
          emoji={config.hookEmoji}
          bgColor={hookBgColor}
          textColor={hookTextColor}
          scale={scale}
        />
      </Sequence>

      {/* Flash Transition (2-frame white flash) */}
      {enableFlash && (
        <Sequence
          from={Math.round(hookDuration)}
          durationInFrames={flashDuration}
        >
          <AbsoluteFill style={{ backgroundColor: "#FFFFFF" }} />
        </Sequence>
      )}

      {/* Reveal Scene */}
      <Sequence from={revealStart}>
        <RevealScene
          productName={config.revealProductName}
          caption={config.revealCaption}
          ctaText={config.ctaText}
          ctaColor={ctaColor}
          bgColor={revealBgColor}
          mediaSrc={config.revealMediaSrc}
          scale={scale}
        />
      </Sequence>
    </AbsoluteFill>
  );
};
