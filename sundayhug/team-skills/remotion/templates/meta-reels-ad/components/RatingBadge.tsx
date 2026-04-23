import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

/**
 * 별점 뱃지 컴포넌트 (spring 스케일 애니메이션)
 *
 * 하단에 표시되며, 별점과 리뷰 수를 파라미터로 받습니다.
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
        bottom: 180,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 10,
        }}
      >
        <span
          style={{
            fontSize: 30,
            color: "#FFD700",
            textShadow: "0 2px 8px rgba(0,0,0,0.6)",
          }}
        >
          ★★★★★
        </span>
        <span
          style={{
            fontSize: 28,
            fontWeight: 800,
            color: "#fff",
            fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
            textShadow: "0 2px 8px rgba(0,0,0,0.6)",
          }}
        >
          {score} ({reviewCount})
        </span>
      </div>
    </div>
  );
};
