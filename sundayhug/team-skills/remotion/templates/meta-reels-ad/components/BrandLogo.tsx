import React from "react";
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

/**
 * 브랜드 로고 뱃지 컴포넌트 (spring 스케일 애니메이션)
 *
 * 상단 중앙에 표시되며, 브랜드명과 색상을 파라미터로 받습니다.
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
        top: 80,
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
            fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
            letterSpacing: 4,
          }}
        >
          {brandName}
        </span>
      </div>
    </div>
  );
};
