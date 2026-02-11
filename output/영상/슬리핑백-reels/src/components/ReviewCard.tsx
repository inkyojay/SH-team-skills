import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

/**
 * 리뷰 카드 오버레이 (릴스 B용)
 * 반투명 화이트 카드 + 별점 + 리뷰 텍스트
 */
export const ReviewCard: React.FC<{
  text: string;
  rating?: number;
  direction?: "left" | "right" | "center";
}> = ({ text, rating = 5, direction = "left" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideIn = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 160 },
  });

  const translateX =
    direction === "center"
      ? 0
      : direction === "left"
        ? interpolate(slideIn, [0, 1], [-300, 0])
        : interpolate(slideIn, [0, 1], [300, 0]);

  const opacity = interpolate(slideIn, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: "absolute",
        top: 200,
        left: 60, // 세이프존
        right: 120, // 세이프존
        display: "flex",
        justifyContent: "center",
        opacity,
        transform: `translateX(${translateX}px)`,
      }}
    >
      <div
        style={{
          background: "rgba(255, 255, 255, 0.88)",
          borderRadius: 20,
          padding: "24px 36px",
          backdropFilter: "blur(8px)",
          boxShadow: "0 4px 16px rgba(0,0,0,0.12)",
          maxWidth: 700,
        }}
      >
        <div style={{ marginBottom: 8 }}>
          <span style={{ fontSize: 28, color: "#FFD700" }}>
            {"★".repeat(rating)}
          </span>
        </div>
        <p
          style={{
            fontSize: 36,
            fontWeight: 600,
            color: "#3E2723",
            fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
            lineHeight: 1.45,
            margin: 0,
          }}
        >
          "{text}"
        </p>
      </div>
    </div>
  );
};
