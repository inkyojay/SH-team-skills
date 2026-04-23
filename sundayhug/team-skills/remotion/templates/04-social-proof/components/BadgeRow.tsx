import React from "react";
import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { FONT, MOTION } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";
import type { BadgeItem } from "../types";

/**
 * 인증 뱃지 순차 등장 컴포넌트
 */
export const BadgeRow: React.FC<{
  badges: BadgeItem[];
  headline?: string;
  palette?: string;
  brandColor?: string;
}> = ({ badges, headline, palette, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(palette);
  const accent = brandColor ?? pal.accent;

  const headlineIn = spring({
    frame: frame - 5,
    fps,
    config: MOTION.spring,
  });

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${pal.bg} 0%, ${pal.bgWarm} 100%)`,
      }}
    >
      {/* 헤드라인 */}
      {headline && (
        <div
          style={{
            position: "absolute",
            top: "20%",
            left: 0,
            right: 0,
            textAlign: "center",
            opacity: interpolate(headlineIn, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(headlineIn, [0, 1], [20, 0])}px)`,
          }}
        >
          <span
            style={{
              fontSize: 52,
              fontWeight: 800,
              color: pal.text,
              fontFamily: FONT.body,
            }}
          >
            {headline}
          </span>
        </div>
      )}

      {/* 뱃지 그리드 */}
      <div
        style={{
          position: "absolute",
          top: headline ? "35%" : "25%",
          left: 60,
          right: 60,
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 28,
        }}
      >
        {badges.map((badge, i) => {
          const delay = 10 + i * 6;
          const badgeIn = spring({
            frame: frame - delay,
            fps,
            config: MOTION.springSnappy,
          });

          return (
            <div
              key={i}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 12,
                opacity: interpolate(badgeIn, [0, 1], [0, 1]),
                transform: `scale(${interpolate(badgeIn, [0, 1], [0, 1])})`,
              }}
            >
              {badge.iconSrc && (
                <Img
                  src={staticFile(badge.iconSrc)}
                  style={{
                    width: 80,
                    height: 80,
                    objectFit: "contain",
                  }}
                />
              )}
              <div
                style={{
                  background: "rgba(255,255,255,0.95)",
                  borderRadius: 20,
                  padding: "14px 28px",
                  boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
                  border: `2px solid ${accent}20`,
                }}
              >
                <span
                  style={{
                    fontSize: 26,
                    fontWeight: 700,
                    color: pal.text,
                    fontFamily: FONT.body,
                  }}
                >
                  {badge.text}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
