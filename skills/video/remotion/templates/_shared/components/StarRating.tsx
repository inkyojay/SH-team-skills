import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { MOTION } from "../utils/brand";

/**
 * 별점 애니메이션 컴포넌트
 *
 * 별이 하나씩 순차적으로 등장하며 채워집니다.
 */
export const StarRating: React.FC<{
  /** 별점 (0~5) */
  score: number;
  /** 별 크기 (기본 48) */
  size?: number;
  /** 채워진 별 색상 */
  filledColor?: string;
  /** 빈 별 색상 */
  emptyColor?: string;
  /** 등장 딜레이 (프레임) */
  delay?: number;
  /** 별 간격 딜레이 (프레임, 기본 4) */
  stagger?: number;
}> = ({
  score,
  size = 48,
  filledColor = "#F5A623",
  emptyColor = "#E0D5C8",
  delay = 0,
  stagger = 4,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const totalStars = 5;

  return (
    <div style={{ display: "flex", gap: size * 0.2, justifyContent: "center" }}>
      {Array.from({ length: totalStars }, (_, i) => {
        const starDelay = delay + i * stagger;
        const progress = spring({
          frame: frame - starDelay,
          fps,
          config: MOTION.springSnappy,
        });

        const scale = interpolate(progress, [0, 1], [0, 1]);
        const opacity = interpolate(progress, [0, 0.5], [0, 1], {
          extrapolateRight: "clamp",
        });
        const isFilled = i < Math.floor(score);
        const isPartial = i === Math.floor(score) && score % 1 > 0;

        return (
          <div
            key={i}
            style={{
              width: size,
              height: size,
              opacity,
              transform: `scale(${scale})`,
              position: "relative",
            }}
          >
            {/* 빈 별 */}
            <svg
              viewBox="0 0 24 24"
              width={size}
              height={size}
              style={{ position: "absolute", top: 0, left: 0 }}
            >
              <path
                d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                fill={emptyColor}
              />
            </svg>
            {/* 채워진 별 */}
            {(isFilled || isPartial) && (
              <svg
                viewBox="0 0 24 24"
                width={size}
                height={size}
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  clipPath: isPartial
                    ? `inset(0 ${(1 - (score % 1)) * 100}% 0 0)`
                    : undefined,
                }}
              >
                <path
                  d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"
                  fill={filledColor}
                />
              </svg>
            )}
          </div>
        );
      })}
    </div>
  );
};
