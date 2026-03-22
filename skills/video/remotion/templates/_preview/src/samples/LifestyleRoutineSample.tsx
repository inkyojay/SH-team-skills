import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

/**
 * 12 라이프스타일/루틴 프리뷰 (플레이스홀더 기반)
 */

const BRAND_COLOR = "#8B7355";
const FONT_BODY = "'Noto Sans KR', system-ui";
const FONT_EN = "'DM Sans', system-ui";
const springConfig = { damping: 16, stiffness: 150 };
const springSnappy = { damping: 14, stiffness: 180 };
const springGentle = { damping: 18, stiffness: 120 };

const STEPS = [
  { num: 1, title: "목욕 후 보습", desc: "촉촉한 피부로 준비해요", time: "PM 7:30", emoji: "🛁", bg: "#E8F0F0" },
  { num: 2, title: "스와들 착용", desc: "엄마 품처럼 포근하게", time: "PM 7:45", emoji: "👶", bg: "#F5E6D3" },
  { num: 3, title: "꿀잠 시작", desc: "안정적인 수면으로", time: "PM 8:00", emoji: "🌙", bg: "#E8E0F0" },
];

export const LifestyleRoutineSample: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#FAF7F4" }}>
      <TransitionSeries>
        <TransitionSeries.Sequence durationInFrames={120}>
          <IntroScene />
        </TransitionSeries.Sequence>
        <TransitionSeries.Transition presentation={fade()} timing={linearTiming({ durationInFrames: 12 })} />
        {STEPS.flatMap((step, i) => {
          const elements: React.ReactNode[] = [];
          elements.push(
            <TransitionSeries.Sequence key={`step-${i}`} durationInFrames={150}>
              <StepScene step={step} />
            </TransitionSeries.Sequence>,
          );
          elements.push(
            <TransitionSeries.Transition key={`t-${i}`} presentation={fade()} timing={linearTiming({ durationInFrames: 12 })} />,
          );
          return elements;
        })}
        <TransitionSeries.Sequence durationInFrames={120}>
          <CtaScene />
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

const IntroScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const titleIn = spring({ frame: frame - 8, fps, config: springConfig });

  return (
    <AbsoluteFill style={{ background: "linear-gradient(135deg, #F5E6D3 0%, #E8D5C0 100%)" }}>
      <div style={{ position: "absolute", top: "25%", left: "50%", transform: "translateX(-50%)", fontSize: 120, opacity: 0.4 }}>✨</div>
      <div style={{ position: "absolute", bottom: 400, left: 0, right: 0, textAlign: "center", padding: "0 60px", opacity: interpolate(titleIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(titleIn, [0, 1], [30, 0])}px)` }}>
        <p style={{ fontSize: 56, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY, textShadow: "0 4px 16px rgba(0,0,0,0.3)", margin: 0 }}>우리 아기 취침 루틴</p>
        <p style={{ fontSize: 34, fontWeight: 500, color: "rgba(255,255,255,0.85)", fontFamily: FONT_BODY, marginTop: 12, textShadow: "0 2px 8px rgba(0,0,0,0.2)" }}>with 썬데이허그</p>
      </div>
    </AbsoluteFill>
  );
};

const StepScene: React.FC<{ step: typeof STEPS[0] }> = ({ step }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const numberIn = spring({ frame: frame - 3, fps, config: springSnappy });
  const lineIn = spring({ frame: frame - 6, fps, config: springGentle });
  const titleIn = spring({ frame: frame - 10, fps, config: springConfig });
  const descIn = spring({ frame: frame - 18, fps, config: springGentle });
  const timeIn = spring({ frame: frame - 5, fps, config: springConfig });

  return (
    <AbsoluteFill style={{ background: `linear-gradient(135deg, ${step.bg} 0%, ${adjustColor(step.bg, -15)} 100%)` }}>
      {/* Emoji placeholder */}
      <div style={{ position: "absolute", top: "22%", left: "50%", transform: "translateX(-50%)", fontSize: 140, opacity: 0.4 }}>{step.emoji}</div>

      {/* 하단 그라데이션 */}
      <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0) 40%, rgba(0,0,0,0.5) 100%)" }} />

      {/* Time label */}
      <div style={{ position: "absolute", top: 300, left: 50, opacity: interpolate(timeIn, [0, 1], [0, 1]), transform: `translateX(${interpolate(timeIn, [0, 1], [-20, 0])}px)` }}>
        <div style={{ background: "rgba(0,0,0,0.4)", borderRadius: 16, padding: "8px 20px", backdropFilter: "blur(8px)" }}>
          <span style={{ fontSize: 24, fontWeight: 600, color: "#fff", fontFamily: FONT_EN, letterSpacing: 2 }}>{step.time}</span>
        </div>
      </div>

      {/* Step number */}
      <div style={{ position: "absolute", bottom: 520, left: 60, opacity: interpolate(numberIn, [0, 1], [0, 1]), transform: `scale(${interpolate(numberIn, [0, 1], [0, 1])})` }}>
        <div style={{ width: 80, height: 80, borderRadius: "50%", background: BRAND_COLOR, display: "flex", alignItems: "center", justifyContent: "center", boxShadow: `0 4px 16px ${BRAND_COLOR}60` }}>
          <span style={{ fontSize: 36, fontWeight: 900, color: "#fff", fontFamily: FONT_EN }}>{step.num}</span>
        </div>
      </div>

      {/* Timeline connection line */}
      {step.num < 3 && (
        <div style={{ position: "absolute", bottom: 440, left: 99, width: 3, height: interpolate(lineIn, [0, 1], [0, 80]), background: `linear-gradient(180deg, ${BRAND_COLOR}, ${BRAND_COLOR}40)`, borderRadius: 2, opacity: interpolate(lineIn, [0, 1], [0, 0.7]) }} />
      )}

      {/* Title */}
      <div style={{ position: "absolute", bottom: 420, left: 60, right: 60, opacity: interpolate(titleIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(titleIn, [0, 1], [20, 0])}px)` }}>
        <p style={{ fontSize: 52, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY, margin: 0, textShadow: "0 4px 16px rgba(0,0,0,0.6)" }}>{step.title}</p>
      </div>

      {/* Description */}
      <div style={{ position: "absolute", bottom: 360, left: 60, right: 60, opacity: interpolate(descIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(descIn, [0, 1], [10, 0])}px)` }}>
        <p style={{ fontSize: 30, fontWeight: 400, color: "rgba(255,255,255,0.85)", fontFamily: FONT_BODY, margin: 0, textShadow: "0 2px 8px rgba(0,0,0,0.5)" }}>{step.desc}</p>
      </div>

      {/* Progress dots */}
      <div style={{ position: "absolute", bottom: 300, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 12 }}>
        {[1, 2, 3].map((n) => {
          const isActive = n === step.num;
          const isPast = n < step.num;
          const dotIn = spring({ frame: frame - 25 - n * 2, fps, config: springConfig });
          return (
            <div key={n} style={{ width: isActive ? 32 : 12, height: 12, borderRadius: 6, background: isActive ? BRAND_COLOR : isPast ? "rgba(255,255,255,0.7)" : "rgba(255,255,255,0.3)", opacity: interpolate(dotIn, [0, 1], [0, 1]) }} />
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
  const productIn = spring({ frame: frame - 15, fps, config: springConfig });
  const ctaIn = spring({ frame: frame - 25, fps, config: springSnappy });

  return (
    <AbsoluteFill style={{ background: "linear-gradient(135deg, #FAF7F4 0%, #F5E6D3 100%)", display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
      <span style={{ fontSize: 40, fontWeight: 800, color: BRAND_COLOR, letterSpacing: 4, opacity: interpolate(logoIn, [0, 1], [0, 1]), marginBottom: 16, fontFamily: FONT_BODY }}>SUNDAY HUG</span>
      <span style={{ fontSize: 56, fontWeight: 900, color: "#333", opacity: interpolate(productIn, [0, 1], [0, 1]), transform: `translateY(${interpolate(productIn, [0, 1], [20, 0])}px)`, marginBottom: 40, fontFamily: FONT_BODY }}>스와들 스트랩</span>
      <div style={{ backgroundColor: BRAND_COLOR, borderRadius: 60, padding: "20px 64px", opacity: interpolate(ctaIn, [0, 1], [0, 1]), transform: `scale(${interpolate(ctaIn, [0, 1], [0.8, 1])})` }}>
        <span style={{ fontSize: 36, fontWeight: 800, color: "#fff", fontFamily: FONT_BODY }}>지금 바로 구매하기</span>
      </div>
    </AbsoluteFill>
  );
};

function adjustColor(hex: string, amount: number): string {
  const num = parseInt(hex.replace("#", ""), 16);
  const r = Math.min(255, Math.max(0, ((num >> 16) & 0xff) + amount));
  const g = Math.min(255, Math.max(0, ((num >> 8) & 0xff) + amount));
  const b = Math.min(255, Math.max(0, (num & 0xff) + amount));
  return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, "0")}`;
}
