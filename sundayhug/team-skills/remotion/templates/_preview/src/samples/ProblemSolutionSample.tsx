import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig, interpolate, useCurrentFrame, spring } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

/**
 * 01 문제-해결 프리뷰 (플레이스홀더 기반)
 *
 * 실제 비디오 파일 없이 템플릿의 모션과 레이아웃을 확인합니다.
 */

const BRAND = { name: "SUNDAY HUG", color: "#8B7355" };
const BG_WARM = "#FAF7F4";

const springConfig = { damping: 16, stiffness: 150 };
const springSnappy = { damping: 14, stiffness: 180 };

export const ProblemSolutionSample: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1510" }}>
      <TransitionSeries>
        {/* 문제 씬 */}
        <TransitionSeries.Sequence durationInFrames={150}>
          <ProblemScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 10 })}
        />
        {/* 솔루션 씬 */}
        <TransitionSeries.Sequence durationInFrames={210}>
          <SolutionScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: 10 })}
        />
        {/* CTA 씬 */}
        <TransitionSeries.Sequence durationInFrames={120}>
          <CtaScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

const ProblemScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const textIn = spring({ frame: frame - 8, fps, config: springConfig });
  const shake = frame < 20 ? interpolate(frame, [0, 5, 10, 15, 20], [0, -3, 3, -2, 0]) : 0;

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #3a2820 0%, #2a1a12 50%, #1a0e08 100%)",
      }}
    >
      <AbsoluteFill style={{ background: "rgba(30,20,15,0.25)" }} />
      {/* 아기 실루엣 placeholder */}
      <div style={{ position: "absolute", top: "25%", left: "50%", transform: "translateX(-50%)", fontSize: 120, opacity: 0.3 }}>
        😢
      </div>
      <div
        style={{
          position: "absolute", bottom: 380, left: 0, right: 0,
          display: "flex", flexDirection: "column", alignItems: "center", padding: "0 60px",
          opacity: interpolate(textIn, [0, 1], [0, 1]),
          transform: `translateY(${interpolate(textIn, [0, 1], [40, 0])}px) translateX(${shake}px)`,
        }}
      >
        <p style={{ fontSize: 58, fontWeight: 900, color: "#fff", textAlign: "center", lineHeight: 1.4, margin: 0, textShadow: "0 4px 16px rgba(0,0,0,0.8)", fontFamily: "'Noto Sans KR', system-ui" }}>
          아기 등센서에 잠을 못 자나요?
        </p>
        <p style={{ fontSize: 36, fontWeight: 500, color: "rgba(255,255,255,0.8)", textAlign: "center", marginTop: 16, textShadow: "0 2px 8px rgba(0,0,0,0.6)", fontFamily: "'Noto Sans KR', system-ui" }}>
          매일 반복되는 수면 고민
        </p>
      </div>
    </AbsoluteFill>
  );
};

const SolutionScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 전환 오버레이 (처음 30프레임)
  const wipeProgress = spring({ frame, fps, config: { damping: 20, stiffness: 100 } });
  const wipeOut = interpolate(frame, [20, 30], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  const textIn = spring({ frame: frame - 12, fps, config: springSnappy });
  const productIn = spring({ frame: frame - 20, fps, config: springConfig });

  return (
    <AbsoluteFill
      style={{
        background: "linear-gradient(135deg, #F5E6D3 0%, #E8D5C0 50%, #D4C0A8 100%)",
      }}
    >
      {/* 제품 placeholder */}
      <div style={{ position: "absolute", top: "20%", left: "50%", transform: "translateX(-50%)", fontSize: 140, opacity: 0.5 }}>
        👶
      </div>

      {/* 전환 오버레이 */}
      {frame < 35 && (
        <AbsoluteFill style={{ opacity: interpolate(wipeOut, [0, 1], [1, 0]), zIndex: 50 }}>
          <div style={{ width: "100%", height: "100%", background: BG_WARM, clipPath: `circle(${interpolate(wipeProgress, [0, 1], [0, 150])}% at 50% 50%)` }} />
          <div style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", opacity: interpolate(wipeProgress, [0, 0.5], [0, 1], { extrapolateRight: "clamp" }) }}>
            <span style={{ fontSize: 52, fontWeight: 800, color: "#333", fontFamily: "'Noto Sans KR', system-ui" }}>해결책은?</span>
          </div>
        </AbsoluteFill>
      )}

      {/* 제품 배지 */}
      <div style={{ position: "absolute", bottom: 500, left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", padding: "0 60px", opacity: interpolate(textIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(textIn, [0, 1], [40, 0])}px)` }}>
        <div style={{ background: BRAND.color, borderRadius: 30, padding: "8px 28px", marginBottom: 20, opacity: interpolate(productIn, [0, 1], [0, 1]), transform: `scale(${interpolate(productIn, [0, 1], [0.8, 1])})` }}>
          <span style={{ fontSize: 24, fontWeight: 700, color: "#fff", fontFamily: "'Noto Sans KR', system-ui", letterSpacing: 2 }}>스와들 스트랩</span>
        </div>
        <p style={{ fontSize: 58, fontWeight: 900, color: "#333", textAlign: "center", lineHeight: 1.4, margin: 0, fontFamily: "'Noto Sans KR', system-ui" }}>
          포근한 감싸기로 깊은 잠을
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
      <span style={{ fontSize: 40, fontWeight: 800, color: "#fff", letterSpacing: 4, opacity: interpolate(logoIn, [0, 1], [0, 1]), transform: `scale(${interpolate(logoIn, [0, 1], [0.6, 1])})`, marginBottom: 16, fontFamily: "'Noto Sans KR', system-ui" }}>{BRAND.name}</span>
      <span style={{ fontSize: 56, fontWeight: 900, color: "#fff", opacity: interpolate(productIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(productIn, [0, 1], [20, 0])}px)`, marginBottom: 40, textShadow: "0 2px 12px rgba(0,0,0,0.5)", fontFamily: "'Noto Sans KR', system-ui" }}>스와들 스트랩</span>
      <div style={{ backgroundColor: BRAND.color, borderRadius: 60, padding: "20px 64px", opacity: interpolate(ctaIn, [0, 1], [0, 1]), transform: `scale(${interpolate(ctaIn, [0, 1], [0.8, 1])})` }}>
        <span style={{ fontSize: 36, fontWeight: 800, color: "#fff", fontFamily: "'Noto Sans KR', system-ui" }}>지금 바로 구매하기</span>
      </div>
    </AbsoluteFill>
  );
};
