import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";
import { FONT, MOTION } from "../utils/brand";
import type { VideoFormat } from "../types/common";
import { FORMAT_SPECS } from "../types/common";

/**
 * 공용 브랜드 로고 뱃지 컴포넌트
 *
 * 상단 중앙에 표시되며, 세이프존을 자동으로 고려합니다.
 */
export const BrandLogo: React.FC<{
  brandName: string;
  brandColor: string;
  format?: VideoFormat;
}> = ({ brandName, brandColor, format = "reels" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({
    frame,
    fps,
    config: MOTION.spring,
  });

  const spec = FORMAT_SPECS[format];
  const topPx = spec.safeZone?.top
    ? Math.round(spec.height * (spec.safeZone.top / 100)) + 20
    : 80;

  return (
    <div
      style={{
        position: "absolute",
        top: topPx,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          background: "rgba(255,255,255,0.92)",
          borderRadius: 40,
          padding: "14px 32px",
          boxShadow: "0 8px 24px rgba(0,0,0,0.15)",
        }}
      >
        <span
          style={{
            fontSize: 26,
            fontWeight: 800,
            color: brandColor,
            fontFamily: FONT.body,
            letterSpacing: 4,
          }}
        >
          {brandName}
        </span>
      </div>
    </div>
  );
};
