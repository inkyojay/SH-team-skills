import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

/**
 * 02 감성 프리뷰 (플레이스홀더 기반)
 */

const BRAND_COLOR = "#8B7355";
const FONT_DISPLAY = "'Cormorant Garamond', Georgia, serif";
const FONT_BODY = "'Noto Sans KR', system-ui";
const BG = "#FAF7F4";

export const EmotionalSample: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: BG }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={180}>
          <KenBurnsMoodScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={210}>
          <QuoteScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={150}>
          <ProductScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 15 })} />
        <TransitionSeries.Sequence durationInFrames={120}>
          <CtaScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

const KenBurnsMoodScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], { extrapolateRight: "clamp" });
  const scale = interpolate(progress, [0, 1], [1.0, 1.08]);
  const textIn = spring({ frame: frame - 15, fps, config: { damping: 18, stiffness: 120 } });

  return (
    <AbsoluteFill>
      <div style={{ width: "100%", height: "100%", transform: `scale(${scale})`, background: "linear-gradient(135deg, #F2D4C4 0%, #E8C0A8 30%, #D4A888 60%, #C0907A 100%)" }}>
        <div style={{ position: "absolute", top: "30%", left: "50%", transform: "translateX(-50%)", fontSize: 160, opacity: 0.4 }}>🌙</div>
      </div>
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(0,0,0,0.3) 100%)" }} />
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 60%, rgba(0,0,0,0.5) 100%)" }} />
      <div style={{ position: "absolute", bottom: 380, left: 0, right: 0, textAlign: "center", padding: "0 80px", opacity: interpolate(textIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(textIn, [0, 1], [20, 0])}px)` }}>
        <p style={{ fontSize: 48, fontWeight: 700, color: "#fff", fontFamily: FONT_BODY, lineHeight: 1.5, textShadow: "0 2px 12px rgba(0,0,0,0.6)" }}>
          포근한 잠자리의 시작
        </p>
      </div>
    </AbsoluteFill>
  );
};

const QuoteScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const quoteIn = spring({ frame: frame - 10, fps, config: { damping: 22, stiffness: 80 } });
  const attrIn = spring({ frame: frame - 30, fps, config: { damping: 18, stiffness: 120 } });
  const quoteMarkIn = spring({ frame: frame - 5, fps, config: { damping: 18, stiffness: 120 } });

  return (
    <AbsoluteFill style={{ background: BG, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", padding: "0 80px" }}>
      <span style={{ fontSize: 160, fontWeight: 300, color: `${BRAND_COLOR}30`, fontFamily: FONT_DISPLAY, lineHeight: 0.8, opacity: interpolate(quoteMarkIn, [0, 1], [0, 1]), transform: `scale(${interpolate(quoteMarkIn, [0, 1], [0.5, 1])})`, marginBottom: -20 }}>"</span>
      <p style={{ fontSize: 44, fontWeight: 400, color: "#333", fontFamily: FONT_DISPLAY, textAlign: "center", lineHeight: 1.7, margin: 0, fontStyle: "italic", opacity: interpolate(quoteIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(quoteIn, [0, 1], [30, 0])}px)`, maxWidth: 900 }}>
        아이가 편안하면{"\n"}엄마도 편안해요
      </p>
      <p style={{ fontSize: 28, fontWeight: 500, color: BRAND_COLOR, fontFamily: FONT_BODY, marginTop: 32, opacity: interpolate(attrIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(attrIn, [0, 1], [10, 0])}px)` }}>
        — 30대 워킹맘
      </p>
    </AbsoluteFill>
  );
};

const ProductScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], { extrapolateRight: "clamp" });
  const scale = interpolate(progress, [0, 1], [1.0, 1.08]);
  const captionIn = spring({ frame: frame - 10, fps, config: { damping: 16, stiffness: 150 } });

  return (
    <AbsoluteFill>
      <div style={{ width: "100%", height: "100%", transform: `scale(${scale})`, background: "linear-gradient(135deg, #E8D5C0 0%, #D4C0A8 100%)" }}>
        <div style={{ position: "absolute", top: "25%", left: "50%", transform: "translateX(-50%)", fontSize: 140, opacity: 0.5 }}>🧸</div>
      </div>
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 60%, rgba(0,0,0,0.5) 100%)" }} />
      <div style={{ position: "absolute", bottom: 380, left: 0, right: 0, textAlign: "center", padding: "0 60px", opacity: interpolate(captionIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(captionIn, [0, 1], [30, 0])}px)` }}>
        <p style={{ fontSize: 56, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY, textShadow: "0 4px 16px rgba(0,0,0,0.6)" }}>스와들 스트랩</p>
        <p style={{ fontSize: 34, fontWeight: 500, color: "rgba(255,255,255,0.85)", fontFamily: FONT_BODY, marginTop: 8, textShadow: "0 2px 8px rgba(0,0,0,0.5)" }}>엄마 품처럼 포근하게</p>
      </div>
    </AbsoluteFill>
  );
};

const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logoIn = spring({ frame: frame - 5, fps, config: { damping: 14, stiffness: 180 } });
  const productIn = spring({ frame: frame - 15, fps, config: { damping: 16, stiffness: 150 } });
  const ctaIn = spring({ frame: frame - 25, fps, config: { damping: 14, stiffness: 180 } });

  return (
    <AbsoluteFill style={{ background: `linear-gradient(135deg, ${BG} 0%, #E8D5C0 100%)`, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
      <span style={{ fontSize: 40, fontWeight: 800, color: BRAND_COLOR, letterSpacing: 4, opacity: interpolate(logoIn, [0, 1], [0, 1]), transform: `scale(${interpolate(logoIn, [0, 1], [0.6, 1])})`, marginBottom: 16, fontFamily: FONT_BODY }}>SUNDAY HUG</span>
      <span style={{ fontSize: 56, fontWeight: 900, color: "#333", opacity: interpolate(productIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(productIn, [0, 1], [20, 0])}px)`, marginBottom: 40, fontFamily: FONT_BODY }}>스와들 스트랩</span>
      <div style={{ backgroundColor: BRAND_COLOR, borderRadius: 60, padding: "20px 64px", opacity: interpolate(ctaIn, [0, 1], [0, 1]), transform: `scale(${interpolate(ctaIn, [0, 1], [0.8, 1])})` }}>
        <span style={{ fontSize: 36, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY }}>지금 바로 구매하기</span>
      </div>
    </AbsoluteFill>
  );
};
