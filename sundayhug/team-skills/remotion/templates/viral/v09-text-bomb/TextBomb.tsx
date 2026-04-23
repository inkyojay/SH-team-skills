import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

import type { TextBombConfig, FontStyle, BackgroundPattern } from "./types";

const FONT_MAP: Record<FontStyle, string> = {
  bold: "'Arial Black', 'Helvetica Neue', sans-serif",
  retro: "'Courier New', 'Monaco', monospace",
  handwritten: "'Comic Sans MS', 'Chalkboard SE', cursive",
  impact: "Impact, 'Arial Black', sans-serif",
};

/**
 * 배경 패턴 SVG 생성
 */
const getPatternStyle = (
  pattern: BackgroundPattern,
  textColor: string,
): React.CSSProperties => {
  const color = `${textColor}15`;
  switch (pattern) {
    case "dots":
      return {
        backgroundImage: `radial-gradient(${color} 2px, transparent 2px)`,
        backgroundSize: "30px 30px",
      };
    case "lines":
      return {
        backgroundImage: `repeating-linear-gradient(
          45deg,
          transparent,
          transparent 20px,
          ${color} 20px,
          ${color} 22px
        )`,
      };
    case "grid":
      return {
        backgroundImage: `
          linear-gradient(${color} 1px, transparent 1px),
          linear-gradient(90deg, ${color} 1px, transparent 1px)
        `,
        backgroundSize: "40px 40px",
      };
    default:
      return {};
  }
};

/**
 * V09 - Text Bomb / 배민 Style
 *
 * 화면의 80%를 차지하는 위트있는 텍스트 한 줄.
 * 솔리드 배경 + 미니멀 구성. 의도적 안티디자인.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="TextBombAd"
 *   component={TextBomb}
 *   durationInFrames={30 * 6}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       mainText: "잠 못 자는 아기는\n없습니다",
 *       subText: "잠 못 재우는 부모만 있을 뿐",
 *       brandName: "SUNDAYHUG",
 *       bgColor: "#FFE066",
 *       fontStyle: "impact",
 *     },
 *   }}
 * />
 * ```
 */
export const TextBomb: React.FC<{ config: TextBombConfig }> = ({ config }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const textColor = config.textColor ?? "#000";
  const fontStyle = config.fontStyle ?? "bold";
  const pattern = config.backgroundPattern ?? "none";

  // 메인 텍스트: spring scale (0.95 → 1) + fade
  const mainSpring = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 200, mass: 0.5 },
  });
  const mainScale = interpolate(mainSpring, [0, 1], [0.95, 1]);
  const mainOpacity = interpolate(mainSpring, [0, 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 서브 텍스트: 0.5초 후 등장
  const subDelay = Math.round(fps * 0.5);
  const subSpring = spring({
    frame: frame - subDelay,
    fps,
    config: { damping: 15, stiffness: 200, mass: 0.5 },
  });
  const subOpacity = interpolate(subSpring, [0, 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });
  const subScale = interpolate(subSpring, [0, 1], [0.95, 1]);

  // 브랜드명: 1초 후 등장
  const brandDelay = Math.round(fps * 1);
  const brandOpacity = interpolate(
    frame - brandDelay,
    [0, fps * 0.3],
    [0, 0.6],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  const patternStyle = getPatternStyle(pattern, textColor);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: config.bgColor,
        ...patternStyle,
      }}
    >
      {/* 메인 텍스트 (80% of frame width) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          padding: "0 10%",
        }}
      >
        <div
          style={{
            transform: `scale(${mainScale})`,
            opacity: mainOpacity,
            width: "100%",
            textAlign: "center",
          }}
        >
          <p
            style={{
              fontSize: 80,
              fontWeight: 900,
              color: textColor,
              fontFamily: FONT_MAP[fontStyle],
              lineHeight: 1.3,
              margin: 0,
              wordBreak: "keep-all",
              whiteSpace: "pre-wrap",
            }}
          >
            {config.mainText}
          </p>
        </div>

        {/* 서브 텍스트 */}
        {config.subText && (
          <div
            style={{
              transform: `scale(${subScale})`,
              opacity: subOpacity,
              marginTop: 30,
              textAlign: "center",
            }}
          >
            <p
              style={{
                fontSize: 36,
                fontWeight: 600,
                color: `${textColor}cc`,
                fontFamily: FONT_MAP[fontStyle],
                lineHeight: 1.5,
                margin: 0,
                whiteSpace: "pre-wrap",
              }}
            >
              {config.subText}
            </p>
          </div>
        )}
      </div>

      {/* 브랜드명 (우하단, 작고 절제된) */}
      <div
        style={{
          position: "absolute",
          bottom: 80,
          right: 60,
          opacity: brandOpacity,
        }}
      >
        <span
          style={{
            fontSize: 20,
            fontWeight: 600,
            color: `${textColor}88`,
            fontFamily: "Arial, sans-serif",
            letterSpacing: 2,
          }}
        >
          {config.brandName}
        </span>
      </div>
    </AbsoluteFill>
  );
};
