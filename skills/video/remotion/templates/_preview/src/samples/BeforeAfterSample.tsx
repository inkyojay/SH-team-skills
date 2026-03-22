import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

/**
 * 07 비포/애프터 프리뷰 (플레이스홀더 기반)
 */

const BRAND_COLOR = "#8B7355";
const FONT_BODY = "'Noto Sans KR', system-ui";
const FONT_EN = "'DM Sans', system-ui";
const springConfig = { damping: 16, stiffness: 150 };
const springSnappy = { damping: 14, stiffness: 180 };

export const BeforeAfterSample: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1510" }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={270}>
          <WipeScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 10 })} />
        <TransitionSeries.Sequence durationInFrames={120}>
          <CtaScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

const WipeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const wipeStart = 30;
  const wipeProgress = spring({ frame: frame - wipeStart, fps, config: { damping: 22, stiffness: 80 } });
  const revealPct = interpolate(wipeProgress, [0, 1], [0, 100]);

  const beforeLabelIn = spring({ frame: frame - 5, fps, config: springConfig });
  const afterLabelIn = spring({ frame: frame - wipeStart - 10, fps, config: springSnappy });
  const captionIn = spring({ frame: frame - wipeStart - 20, fps, config: springConfig });

  return (
    <AbsoluteFill>
      {/* Before (desaturated) */}
      <AbsoluteFill style={{ filter: "saturate(0.3) brightness(0.85)" }}>
        <AbsoluteFill style={{ background: "linear-gradient(135deg, #8B7B6B 0%, #6B5B4B 50%, #4B3B2B 100%)" }}>
          <div style={{ position: "absolute", top: "30%", left: "50%", transform: "translateX(-50%)", fontSize: 120, opacity: 0.4 }}>😴</div>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* After (full saturation, revealed by clipPath) */}
      <AbsoluteFill style={{ clipPath: `inset(0 ${100 - revealPct}% 0 0)` }}>
        <AbsoluteFill style={{ background: "linear-gradient(135deg, #F5E6D3 0%, #E8D0B8 50%, #D4BA9E 100%)" }}>
          <div style={{ position: "absolute", top: "30%", left: "50%", transform: "translateX(-50%)", fontSize: 120, opacity: 0.6 }}>😊</div>
        </AbsoluteFill>
      </AbsoluteFill>

      {/* Wipe line */}
      {revealPct > 0 && revealPct < 100 && (
        <div style={{ position: "absolute", left: `${revealPct}%`, top: 0, bottom: 0, width: 4, transform: "translateX(-50%)", background: "#fff", boxShadow: "0 0 20px rgba(255,255,255,0.5)", zIndex: 10 }} />
      )}

      {/* 하단 그라데이션 */}
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 60%, rgba(0,0,0,0.6) 100%)" }} />

      {/* Before label */}
      <div style={{ position: "absolute", top: "42%", left: 60, opacity: interpolate(beforeLabelIn, [0, 1], [0, 1]), transform: `scale(${interpolate(beforeLabelIn, [0, 1], [0.8, 1])})` }}>
        <div style={{ background: "rgba(0,0,0,0.6)", borderRadius: 20, padding: "10px 24px" }}>
          <span style={{ fontSize: 28, fontWeight: 700, color: "#fff", fontFamily: FONT_EN, letterSpacing: 3 }}>BEFORE</span>
        </div>
      </div>

      {/* After label */}
      {revealPct > 30 && (
        <div style={{ position: "absolute", top: "42%", right: 60, opacity: interpolate(afterLabelIn, [0, 1], [0, 1]), transform: `scale(${interpolate(afterLabelIn, [0, 1], [0.8, 1])})` }}>
          <div style={{ background: BRAND_COLOR, borderRadius: 20, padding: "10px 24px" }}>
            <span style={{ fontSize: 28, fontWeight: 700, color: "#fff", fontFamily: FONT_EN, letterSpacing: 3 }}>AFTER</span>
          </div>
        </div>
      )}

      {/* Caption */}
      <div style={{ position: "absolute", bottom: 350, left: 0, right: 0, display: "flex", justifyContent: "center", padding: "0 60px", opacity: interpolate(captionIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(captionIn, [0, 1], [20, 0])}px)` }}>
        <p style={{ fontSize: 48, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY, textAlign: "center", textShadow: "0 4px 16px rgba(0,0,0,0.8)" }}>
          스와들 하나로 달라지는 수면
        </p>
      </div>
    </AbsoluteFill>
  );
};

const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logoIn = spring({ frame: frame - 5, fps, config: springSnappy });
  const productIn = spring({ frame: frame - 15, fps, config: springConfig });
  const ctaIn = spring({ frame: frame - 25, fps, config: springSnappy });

  return (
    <AbsoluteFill style={{ background: "linear-gradient(135deg, #3a2820 0%, #2a1a12 100%)", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
      <span style={{ fontSize: 40, fontWeight: 800, color: "#fff", letterSpacing: 4, opacity: interpolate(logoIn, [0, 1], [0, 1]), marginBottom: 16, fontFamily: FONT_BODY }}>SUNDAY HUG</span>
      <span style={{ fontSize: 56, fontWeight: 900, color: "#fff", opacity: interpolate(productIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(productIn, [0, 1], [20, 0])}px)`, marginBottom: 40, fontFamily: FONT_BODY }}>스와들 스트랩</span>
      <div style={{ backgroundColor: BRAND_COLOR, borderRadius: 60, padding: "20px 64px", opacity: interpolate(ctaIn, [0, 1], [0, 1]), transform: `scale(${interpolate(ctaIn, [0, 1], [0.8, 1])})` }}>
        <span style={{ fontSize: 36, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY }}>지금 바로 구매하기</span>
      </div>
    </AbsoluteFill>
  );
};
