import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

/**
 * 컬러 하이라이트 자막 컴포넌트
 *
 * 핵심 키워드에 브랜드 컬러 배경 하이라이트를 적용합니다.
 * 전문적인 브랜드 톤에 맞는 세련된 스타일.
 */
export const HighlightCaption: React.FC<{
  text: string;
  highlightWords?: string[];
  brandColor?: string;
}> = ({ text, highlightWords = [], brandColor = "#4A90D9" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 160 },
  });

  const opacity = interpolate(progress, [0, 1], [0, 1]);
  const translateY = interpolate(progress, [0, 1], [20, 0]);

  const renderText = () => {
    if (highlightWords.length === 0) return text;

    const regex = new RegExp(`(${highlightWords.join("|")})`, "g");
    const parts = text.split(regex);

    return parts.map((part, i) =>
      highlightWords.includes(part) ? (
        <span
          key={i}
          style={{
            background: brandColor,
            padding: "4px 12px",
            borderRadius: 8,
            color: "#fff",
          }}
        >
          {part}
        </span>
      ) : (
        <span key={i}>{part}</span>
      ),
    );
  };

  return (
    <div
      style={{
        position: "absolute",
        bottom: 280,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        padding: "0 50px",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      <p
        style={{
          fontSize: 48,
          fontWeight: 700,
          color: "#fff",
          fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
          textAlign: "center",
          lineHeight: 1.5,
          margin: 0,
          textShadow: [
            "0 3px 10px rgba(0,0,0,0.8)",
            "0 1px 3px rgba(0,0,0,0.9)",
          ].join(", "),
          letterSpacing: -0.5,
        }}
      >
        {renderText()}
      </p>
    </div>
  );
};
