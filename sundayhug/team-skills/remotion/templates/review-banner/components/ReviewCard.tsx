import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

/**
 * 리뷰 카드 (말풍선) 컴포넌트
 *
 * 별점 + 리뷰 텍스트를 말풍선 스타일로 표시합니다.
 * 스케일인 애니메이션으로 등장합니다.
 */
export const ReviewCard: React.FC<{
  rating: number;
  reviewText: string;
  reviewerName?: string;
}> = ({ rating, reviewText, reviewerName }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 160 },
  });

  const scale = interpolate(progress, [0, 1], [0.6, 1]);
  const opacity = interpolate(progress, [0, 1], [0, 1]);

  const stars = "★".repeat(rating) + "☆".repeat(5 - rating);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "0 50px",
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          background: "rgba(255,255,255,0.95)",
          borderRadius: 28,
          padding: "28px 36px",
          maxWidth: 900,
          boxShadow: "0 8px 32px rgba(0,0,0,0.15)",
        }}
      >
        {/* 별점 */}
        <div
          style={{
            fontSize: 32,
            color: "#FFD700",
            marginBottom: 12,
            textAlign: "center",
          }}
        >
          {stars}
        </div>

        {/* 리뷰 텍스트 */}
        <p
          style={{
            fontSize: 36,
            fontWeight: 600,
            color: "#333",
            fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
            textAlign: "center",
            lineHeight: 1.5,
            margin: 0,
          }}
        >
          &ldquo;{reviewText}&rdquo;
        </p>

        {/* 리뷰어 */}
        {reviewerName && (
          <p
            style={{
              fontSize: 24,
              fontWeight: 400,
              color: "#999",
              fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
              textAlign: "center",
              marginTop: 12,
              margin: "12px 0 0 0",
            }}
          >
            - {reviewerName}
          </p>
        )}
      </div>
    </div>
  );
};
