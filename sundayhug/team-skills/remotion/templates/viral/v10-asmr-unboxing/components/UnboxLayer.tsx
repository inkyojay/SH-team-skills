import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Img,
} from "remotion";

/**
 * 개별 언박싱 레이어 - 느린 줌인(1→1.05) + 소프트 페이드
 * ASMR 감성: 부드럽고 만족스러운 시각 경험
 */
export const UnboxLayer: React.FC<{
  mediaSrc: string;
  label?: string;
  /** 이전 레이어에서 페이드 인 시간 (프레임) */
  fadeInFrames: number;
}> = ({ mediaSrc, label, fadeInFrames }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // 느린 줌인: scale 1 → 1.05
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.05], {
    extrapolateRight: "clamp",
  });

  // 소프트 페이드 인
  const fadeIn = interpolate(frame, [0, fadeInFrames], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 레이블 등장 (0.8초 후)
  const labelDelay = Math.round(fps * 0.8);
  const labelOpacity = interpolate(
    frame - labelDelay,
    [0, fps * 0.5],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        opacity: fadeIn,
        overflow: "hidden",
      }}
    >
      {/* 이미지 + 줌인 */}
      <Img
        src={mediaSrc}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
        }}
      />

      {/* 워밍 오버레이 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "linear-gradient(180deg, transparent 60%, rgba(0,0,0,0.4) 100%)",
        }}
      />

      {/* 라벨 (최소한) */}
      {label && (
        <div
          style={{
            position: "absolute",
            bottom: 180,
            left: 0,
            right: 0,
            textAlign: "center",
            opacity: labelOpacity,
          }}
        >
          <span
            style={{
              fontSize: 24,
              fontWeight: 300,
              color: "rgba(255,255,255,0.8)",
              fontFamily: "'Helvetica Neue', Arial, sans-serif",
              letterSpacing: 4,
              textTransform: "uppercase",
            }}
          >
            {label}
          </span>
        </div>
      )}
    </div>
  );
};
