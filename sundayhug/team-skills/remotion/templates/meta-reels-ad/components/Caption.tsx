import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

/**
 * 흰색 볼드 자막 컴포넌트 (spring 애니메이션)
 *
 * 하단에 고정되며, 두꺼운 외곽선 + 드롭쉐도우로 가독성을 확보합니다.
 */
export const Caption: React.FC<{
  line1: string;
  line2?: string;
  emoji?: string;
  size?: "large" | "medium";
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

  const fontSize = size === "large" ? 64 : 54;

  const textStyle: React.CSSProperties = {
    fontSize,
    fontWeight: 900,
    color: "#fff",
    fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
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
        bottom: 300,
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
