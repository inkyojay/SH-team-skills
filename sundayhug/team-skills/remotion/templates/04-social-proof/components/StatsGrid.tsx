import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { CountUp } from "../../_shared/components/CountUp";
import { FONT, MOTION } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";
import type { StatItem } from "../types";

/**
 * 통계 그리드 컴포넌트
 *
 * 2~4개의 통계 항목을 그리드로 배치하고 순차적으로 카운트업합니다.
 */
export const StatsGrid: React.FC<{
  stats: StatItem[];
  palette?: string;
  brandColor?: string;
}> = ({ stats, palette, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(palette);
  const accent = brandColor ?? pal.accent;

  const columns = stats.length <= 2 ? 1 : 2;

  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(180deg, ${pal.bg} 0%, ${pal.bgWarm} 100%)`,
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "18%",
          left: 60,
          right: 60,
          bottom: "40%",
          display: "grid",
          gridTemplateColumns: `repeat(${columns}, 1fr)`,
          gap: 40,
          alignContent: "center",
        }}
      >
        {stats.map((stat, i) => {
          const delay = i * 8;
          const labelIn = spring({
            frame: frame - delay - 15,
            fps,
            config: MOTION.spring,
          });

          return (
            <div
              key={i}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 12,
              }}
            >
              <CountUp
                target={stat.value}
                suffix={stat.suffix}
                prefix={stat.prefix}
                decimals={stat.decimals}
                fontSize={stats.length <= 2 ? 120 : 88}
                color={accent}
                delay={delay}
              />
              <span
                style={{
                  fontSize: 32,
                  fontWeight: 600,
                  color: pal.text,
                  fontFamily: FONT.body,
                  opacity: interpolate(labelIn, [0, 1], [0, 1]),
                  transform: `translateY(${interpolate(labelIn, [0, 1], [10, 0])}px)`,
                }}
              >
                {stat.label}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
