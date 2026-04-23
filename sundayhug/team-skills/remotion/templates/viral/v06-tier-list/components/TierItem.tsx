import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Img,
} from "remotion";
import type { Tier } from "../types";
import { TIER_COLORS } from "../types";

/**
 * 개별 티어 아이템 - 오른쪽에서 슬라이드 인,
 * 브랜드 하이라이트 아이템은 글로우/펄스 효과
 */
export const TierItem: React.FC<{
  name: string;
  imageSrc?: string;
  tier: Tier;
  /** 등장 시작 프레임 */
  enterFrame: number;
  /** 브랜드 하이라이트 여부 */
  isHighlight?: boolean;
  /** 해당 티어 내 인덱스 (위치 계산) */
  indexInTier: number;
  /** 해당 티어의 행 인덱스 (S=0, A=1, ...) */
  tierRowIndex: number;
}> = ({
  name,
  imageSrc,
  tier,
  enterFrame,
  isHighlight = false,
  indexInTier,
  tierRowIndex,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - enterFrame,
    fps,
    config: { damping: 12, stiffness: 120, mass: 0.8 },
  });

  if (frame < enterFrame) return null;

  // 오른쪽에서 슬라이드 인
  const translateX = interpolate(progress, [0, 1], [400, 0]);
  const opacity = interpolate(progress, [0, 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 브랜드 하이라이트: 글로우 펄스
  const glowIntensity = isHighlight
    ? interpolate(
        Math.sin((frame - enterFrame) * 0.15),
        [-1, 1],
        [10, 25],
      )
    : 0;

  // 위치 계산: 티어 그리드 내 위치
  const top = 220 + tierRowIndex * 118 + 14;
  const left = 140 + 40 + indexInTier * 170 + 10;

  return (
    <div
      style={{
        position: "absolute",
        top,
        left,
        transform: `translateX(${translateX}px)`,
        opacity,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 4,
        zIndex: isHighlight ? 10 : 1,
      }}
    >
      <div
        style={{
          width: 150,
          height: 70,
          borderRadius: 12,
          backgroundColor: isHighlight ? TIER_COLORS[tier] : "#ffffff22",
          border: `3px solid ${TIER_COLORS[tier]}`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          overflow: "hidden",
          boxShadow: isHighlight
            ? `0 0 ${glowIntensity}px ${glowIntensity / 2}px ${TIER_COLORS[tier]}`
            : "none",
        }}
      >
        {imageSrc ? (
          <Img
            src={imageSrc}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : (
          <span
            style={{
              fontSize: 18,
              fontWeight: 800,
              color: isHighlight ? "#000" : "#fff",
              fontFamily: "Arial Black, sans-serif",
              textAlign: "center",
              padding: "0 6px",
              lineHeight: 1.2,
            }}
          >
            {name}
          </span>
        )}
      </div>
      {imageSrc && (
        <span
          style={{
            fontSize: 14,
            fontWeight: 700,
            color: "#fff",
            textAlign: "center",
            maxWidth: 150,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
          }}
        >
          {name}
        </span>
      )}
    </div>
  );
};
