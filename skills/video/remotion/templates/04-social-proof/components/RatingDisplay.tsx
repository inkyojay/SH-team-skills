import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { StarRating } from "../../_shared/components/StarRating";
import { CountUp } from "../../_shared/components/CountUp";
import { FONT, MOTION } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";
import type { ReviewItem } from "../types";

/**
 * 별점 + 리뷰 수 디스플레이
 */
export const RatingDisplay: React.FC<{
  score: number;
  reviewCountText: string;
  featuredReview?: ReviewItem;
  palette?: string;
  brandColor?: string;
}> = ({ score, reviewCountText, featuredReview, palette, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(palette);
  const accent = brandColor ?? pal.accent;

  const scoreIn = spring({
    frame: frame - 5,
    fps,
    config: MOTION.springSnappy,
  });

  const reviewIn = spring({
    frame: frame - 30,
    fps,
    config: MOTION.spring,
  });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${pal.bg} 0%, ${pal.bgWarm} 100%)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "20%",
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 24,
        }}
      >
        {/* 숫자 점수 */}
        <div
          style={{
            opacity: interpolate(scoreIn, [0, 1], [0, 1]),
            transform: `scale(${interpolate(scoreIn, [0, 1], [0.5, 1])})`,
          }}
        >
          <span
            style={{
              fontSize: 140,
              fontWeight: 900,
              color: accent,
              fontFamily: FONT.english,
              letterSpacing: -4,
            }}
          >
            {score.toFixed(1)}
          </span>
        </div>

        {/* 별점 */}
        <StarRating
          score={score}
          size={56}
          filledColor="#F5A623"
          delay={10}
        />

        {/* 리뷰 수 */}
        <span
          style={{
            fontSize: 30,
            fontWeight: 500,
            color: pal.textSub,
            fontFamily: FONT.body,
            marginTop: 8,
            opacity: interpolate(scoreIn, [0, 1], [0, 1]),
          }}
        >
          {reviewCountText}
        </span>
      </div>

      {/* 대표 리뷰 */}
      {featuredReview && (
        <div
          style={{
            position: "absolute",
            bottom: "38%",
            left: 60,
            right: 60,
            opacity: interpolate(reviewIn, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(reviewIn, [0, 1], [30, 0])}px)`,
          }}
        >
          <div
            style={{
              background: "rgba(255,255,255,0.9)",
              borderRadius: 24,
              padding: "32px 36px",
              boxShadow: "0 8px 32px rgba(0,0,0,0.08)",
            }}
          >
            <p
              style={{
                fontSize: 30,
                fontWeight: 500,
                color: pal.text,
                fontFamily: FONT.body,
                lineHeight: 1.5,
                margin: 0,
              }}
            >
              "{featuredReview.text}"
            </p>
            {featuredReview.author && (
              <p
                style={{
                  fontSize: 24,
                  fontWeight: 400,
                  color: pal.textSub,
                  fontFamily: FONT.body,
                  marginTop: 12,
                  textAlign: "right",
                }}
              >
                — {featuredReview.author}
              </p>
            )}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
