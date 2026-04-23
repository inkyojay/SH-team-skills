import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

/**
 * 04 사회적 증거 프리뷰 (플레이스홀더 기반)
 */

const BRAND_COLOR = "#8B7355";
const BG = "#FAF7F4";
const BG_WARM = "#F5E6D3";
const FONT_BODY = "'Noto Sans KR', system-ui";
const FONT_EN = "'DM Sans', system-ui";
const springConfig = { damping: 16, stiffness: 150 };
const springSnappy = { damping: 14, stiffness: 180 };

export const SocialProofSample: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: BG }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={180}>
          <StatsScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 10 })} />
        <TransitionSeries.Sequence durationInFrames={210}>
          <RatingScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 10 })} />
        <TransitionSeries.Sequence durationInFrames={150}>
          <BadgeScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 10 })} />
        <TransitionSeries.Sequence durationInFrames={120}>
          <CtaScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

const StatsScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const stats = [
    { target: 50000, suffix: "+", label: "누적 판매" },
    { target: 98, suffix: "%", label: "재구매율" },
  ];

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${BG} 0%, ${BG_WARM} 100%)` }}>
      <div style={{ position: "absolute", top: "25%", left: 60, right: 60, display: "flex", flexDirection: "column", gap: 60, alignItems: "center" }}>
        {stats.map((stat, i) => {
          const delay = i * 8;
          const progress = spring({ frame: frame - delay, fps, config: { ...springConfig, mass: 0.8 } });
          const value = interpolate(progress, [0, 1], [0, stat.target]);
          const labelIn = spring({ frame: frame - delay - 15, fps, config: springConfig });

          return (
            <div key={i} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
              <div style={{ display: "flex", alignItems: "baseline", opacity: interpolate(progress, [0, 0.3], [0, 1], { extrapolateRight: "clamp" }), transform: `scale(${interpolate(progress, [0, 1], [0.8, 1])})` }}>
                <span style={{ fontSize: 120, fontWeight: 900, color: BRAND_COLOR, fontFamily: FONT_EN, letterSpacing: -2 }}>
                  {Math.round(value).toLocaleString()}
                </span>
                <span style={{ fontSize: 60, fontWeight: 700, color: BRAND_COLOR, fontFamily: FONT_BODY, marginLeft: 4 }}>{stat.suffix}</span>
              </div>
              <span style={{ fontSize: 32, fontWeight: 600, color: "#333", fontFamily: FONT_BODY, opacity: interpolate(labelIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(labelIn, [0, 1], [10, 0])}px)` }}>
                {stat.label}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const RatingScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scoreIn = spring({ frame: frame - 5, fps, config: springSnappy });
  const reviewIn = spring({ frame: frame - 30, fps, config: springConfig });

  const stars = [1, 2, 3, 4, 5];

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${BG} 0%, ${BG_WARM} 100%)` }}>
      <div style={{ position: "absolute", top: "20%", left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", gap: 24 }}>
        <div style={{ opacity: interpolate(scoreIn, [0, 1], [0, 1]), transform: `scale(${interpolate(scoreIn, [0, 1], [0.5, 1])})` }}>
          <span style={{ fontSize: 140, fontWeight: 900, color: BRAND_COLOR, fontFamily: FONT_EN, letterSpacing: -4 }}>4.9</span>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          {stars.map((_, i) => {
            const starIn = spring({ frame: frame - 10 - i * 4, fps, config: springSnappy });
            return (
              <svg key={i} viewBox="0 0 24 24" width={56} height={56} style={{ opacity: interpolate(starIn, [0, 0.5], [0, 1], { extrapolateRight: "clamp" }), transform: `scale(${interpolate(starIn, [0, 1], [0, 1])})` }}>
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" fill="#F5A623" />
              </svg>
            );
          })}
        </div>
        <span style={{ fontSize: 30, fontWeight: 500, color: BRAND_COLOR, fontFamily: FONT_BODY, marginTop: 8, opacity: interpolate(scoreIn, [0, 1], [0, 1]) }}>3,842개 리뷰</span>
      </div>
      <div style={{ position: "absolute", bottom: "38%", left: 60, right: 60, opacity: interpolate(reviewIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(reviewIn, [0, 1], [30, 0])}px)` }}>
        <div style={{ background: "rgba(255,255,255,0.9)", borderRadius: 24, padding: "32px 36px", boxShadow: "0 8px 32px rgba(0,0,0,0.08)" }}>
          <p style={{ fontSize: 30, fontWeight: 500, color: "#333", fontFamily: FONT_BODY, lineHeight: 1.5, margin: 0 }}>"아이가 정말 편하게 잠들어요"</p>
          <p style={{ fontSize: 24, fontWeight: 400, color: BRAND_COLOR, fontFamily: FONT_BODY, marginTop: 12, textAlign: "right" }}>— 30대 워킹맘</p>
        </div>
      </div>
    </AbsoluteFill>
  );
};

const BadgeScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const headlineIn = spring({ frame: frame - 5, fps, config: springConfig });
  const badges = ["KC인증 완료", "네이버 1위", "맘카페 추천", "피부 저자극 테스트"];

  return (
    <AbsoluteFill style={{ background: `linear-gradient(180deg, ${BG} 0%, ${BG_WARM} 100%)` }}>
      <div style={{ position: "absolute", top: "22%", left: 0, right: 0, textAlign: "center", opacity: interpolate(headlineIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(headlineIn, [0, 1], [20, 0])}px)` }}>
        <span style={{ fontSize: 52, fontWeight: 800, color: "#333", fontFamily: FONT_BODY }}>검증된 품질</span>
      </div>
      <div style={{ position: "absolute", top: "38%", left: 60, right: 60, display: "flex", flexWrap: "wrap", justifyContent: "center", gap: 28 }}>
        {badges.map((text, i) => {
          const badgeIn = spring({ frame: frame - 10 - i * 6, fps, config: springSnappy });
          return (
            <div key={i} style={{ opacity: interpolate(badgeIn, [0, 1], [0, 1]), transform: `scale(${interpolate(badgeIn, [0, 1], [0, 1])})` }}>
              <div style={{ background: "rgba(255,255,255,0.95)", borderRadius: 20, padding: "14px 28px", boxShadow: "0 4px 16px rgba(0,0,0,0.08)", border: `2px solid ${BRAND_COLOR}20` }}>
                <span style={{ fontSize: 26, fontWeight: 700, color: "#333", fontFamily: FONT_BODY }}>{text}</span>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const CtaScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const logoIn = spring({ frame: frame - 5, fps, config: springSnappy });
  const ctaIn = spring({ frame: frame - 20, fps, config: springSnappy });

  return (
    <AbsoluteFill style={{ background: `linear-gradient(135deg, ${BG} 0%, ${BG_WARM} 100%)`, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
      <span style={{ fontSize: 40, fontWeight: 800, color: BRAND_COLOR, letterSpacing: 4, opacity: interpolate(logoIn, [0, 1], [0, 1]), marginBottom: 40, fontFamily: FONT_BODY }}>SUNDAY HUG</span>
      <div style={{ backgroundColor: BRAND_COLOR, borderRadius: 60, padding: "20px 64px", opacity: interpolate(ctaIn, [0, 1], [0, 1]), transform: `scale(${interpolate(ctaIn, [0, 1], [0.8, 1])})` }}>
        <span style={{ fontSize: 36, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY }}>지금 바로 구매하기</span>
      </div>
    </AbsoluteFill>
  );
};
