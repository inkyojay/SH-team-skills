import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import type { Tier } from "../types";
import { TIER_COLORS } from "../types";

const TIERS: Tier[] = ["S", "A", "B", "C", "F"];

/**
 * 티어 그리드 배경 - S/A/B/C/F 행을 렌더링
 * 각 행은 티어 레이블 + 아이템 슬롯 영역으로 구성
 */
export const TierGrid: React.FC<{
  children?: React.ReactNode;
}> = ({ children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 그리드가 나타나는 애니메이션 (0.3초)
  const gridOpacity = interpolate(frame, [0, fps * 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 220,
        left: 40,
        right: 40,
        display: "flex",
        flexDirection: "column",
        gap: 8,
        opacity: gridOpacity,
      }}
    >
      {TIERS.map((tier, i) => {
        const rowDelay = i * 3;
        const rowOpacity = interpolate(
          frame,
          [rowDelay, rowDelay + 6],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        );
        const rowSlide = interpolate(
          frame,
          [rowDelay, rowDelay + 6],
          [-30, 0],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        );

        return (
          <div
            key={tier}
            data-tier={tier}
            style={{
              display: "flex",
              alignItems: "stretch",
              minHeight: 110,
              opacity: rowOpacity,
              transform: `translateX(${rowSlide}px)`,
            }}
          >
            {/* 티어 레이블 */}
            <div
              style={{
                width: 100,
                backgroundColor: TIER_COLORS[tier],
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                borderRadius: "8px 0 0 8px",
              }}
            >
              <span
                style={{
                  fontSize: 56,
                  fontWeight: 900,
                  color: "#000",
                  fontFamily: "Impact, Arial Black, sans-serif",
                  textShadow: "1px 1px 2px rgba(0,0,0,0.3)",
                }}
              >
                {tier}
              </span>
            </div>

            {/* 아이템 슬롯 영역 */}
            <div
              style={{
                flex: 1,
                backgroundColor: `${TIER_COLORS[tier]}22`,
                borderRadius: "0 8px 8px 0",
                display: "flex",
                alignItems: "center",
                padding: "8px 12px",
                gap: 10,
                flexWrap: "wrap",
                minHeight: 110,
              }}
            />
          </div>
        );
      })}
      {children}
    </div>
  );
};
