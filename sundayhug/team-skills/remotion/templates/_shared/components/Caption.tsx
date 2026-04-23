import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { FONT, MOTION } from "../utils/brand";
import type { VideoFormat } from "../types/common";
import { FORMAT_SPECS } from "../types/common";

/**
 * 공용 자막 컴포넌트
 *
 * 포맷에 따라 하단 위치를 세이프존 안으로 자동 조정합니다.
 */
export const Caption: React.FC<{
  line1: string;
  line2?: string;
  emoji?: string;
  size?: "large" | "medium" | "small";
  format?: VideoFormat;
  color?: string;
}> = ({ line1, line2, emoji, size = "large", format = "reels", color = "#fff" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: MOTION.spring,
  });

  const opacity = interpolate(progress, [0, 1], [0, 1]);
  const translateY = interpolate(progress, [0, 1], [30, 0]);

  const fontSize = size === "large" ? 64 : size === "medium" ? 54 : 44;

  const spec = FORMAT_SPECS[format];
  const bottomPx = spec.safeZone?.bottom
    ? Math.round(spec.height * (spec.safeZone.bottom / 100)) + 20
    : 80;

  const textStyle: React.CSSProperties = {
    fontSize,
    fontWeight: 900,
    color,
    fontFamily: FONT.body,
    textAlign: "center",
    lineHeight: 1.35,
    margin: 0,
    WebkitTextStroke: "2px rgba(0,0,0,0.3)",
    paintOrder: "stroke fill",
    textShadow: [
      "0 4px 12px rgba(0,0,0,0.9)",
      "0 2px 4px rgba(0,0,0,0.9)",
      "0 0 40px rgba(0,0,0,0.5)",
    ].join(", "),
    letterSpacing: -1,
  };

  return (
    <div
      style={{
        position: "absolute",
        bottom: bottomPx,
        left: 0,
        right: 0,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "0 50px",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      <p style={textStyle}>{line1}</p>
      {line2 && (
        <p style={{ ...textStyle, marginTop: 4 }}>
          {line2}
          {emoji && (
            <span style={{ marginLeft: 8, WebkitTextStroke: "0px" }}>
              {emoji}
            </span>
          )}
        </p>
      )}
      {!line2 && emoji && (
        <span style={{ ...textStyle, marginTop: 4, WebkitTextStroke: "0px" }}>
          {emoji}
        </span>
      )}
    </div>
  );
};
