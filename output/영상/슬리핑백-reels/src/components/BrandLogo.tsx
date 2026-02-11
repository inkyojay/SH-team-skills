import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

/**
 * 브랜드 로고 뱃지 (상단 중앙, 세이프존 내)
 */
export const BrandLogo: React.FC<{
  brandName: string;
  brandColor: string;
}> = ({ brandName, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const scale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 130, // 세이프존 상단 108px + 여유
        left: 60,
        right: 120,
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
            fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
            letterSpacing: 4,
          }}
        >
          {brandName}
        </span>
      </div>
    </div>
  );
};
