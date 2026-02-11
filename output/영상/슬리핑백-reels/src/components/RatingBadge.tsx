import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

/**
 * 별점 뱃지 (세이프존 내 하단)
 */
export const RatingBadge: React.FC<{
  score: string;
  reviewCount: string;
}> = ({ score, reviewCount }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({
    frame,
    fps,
    config: { damping: 8, stiffness: 180 },
  });

  return (
    <div
      style={{
        position: "absolute",
        bottom: 420, // 세이프존 하단 320px + 자막 위
        left: 60,
        right: 120,
        display: "flex",
        justifyContent: "center",
        transform: `scale(${scale})`,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
        <span
          style={{
            fontSize: 30,
            color: "#FFD700",
            textShadow: "0 2px 8px rgba(0,0,0,0.6)",
          }}
        >
          {"★".repeat(5)}
        </span>
        <span
          style={{
            fontSize: 28,
            fontWeight: 800,
            color: "#fff",
            fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
            textShadow: "0 2px 8px rgba(0,0,0,0.6)",
          }}
        >
          {score} ({reviewCount})
        </span>
      </div>
    </div>
  );
};
