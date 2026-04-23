import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";

/**
 * 상단 프로그레스 바 - 시청 유지율 향상용
 *
 * 메타 릴스에서 영상 길이를 시각적으로 보여줘 이탈률을 낮춥니다.
 * 브랜드 컬러를 사용하여 자연스럽게 브랜딩합니다.
 */
export const ProgressBar: React.FC<{
  color?: string;
  height?: number;
  topOffset?: number;
}> = ({ color = "#A8C5A0", height = 4, topOffset = 0 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const progress = interpolate(frame, [0, durationInFrames], [0, 100], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: topOffset,
        left: 0,
        right: 0,
        height,
        backgroundColor: "rgba(255,255,255,0.15)",
        zIndex: 100,
      }}
    >
      <div
        style={{
          width: `${progress}%`,
          height: "100%",
          backgroundColor: color,
          borderRadius: height / 2,
        }}
      />
    </div>
  );
};
