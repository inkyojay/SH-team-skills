import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

/**
 * 자막 컴포넌트 - 세이프존 내 하단 배치
 * 세이프존: 하단 320px 위에 배치
 */
export const Caption: React.FC<{
  line1: string;
  line2?: string;
  emoji?: string;
  size?: "large" | "medium" | "small";
}> = ({ line1, line2, emoji, size = "large" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 180 },
  });

  const opacity = interpolate(progress, [0, 1], [0, 1]);
  const translateY = interpolate(progress, [0, 1], [30, 0]);

  const fontSizeMap = { large: 64, medium: 54, small: 44 };
  const fontSize = fontSizeMap[size];

  const textStyle: React.CSSProperties = {
    fontSize,
    fontWeight: 900,
    color: "#fff",
    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
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
        bottom: 340, // 세이프존 하단 320px + 20px 여유
        left: 60, // 세이프존 좌 60px
        right: 120, // 세이프존 우 120px
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
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
