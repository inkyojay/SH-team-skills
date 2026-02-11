import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

/**
 * 기능 하이라이트 텍스트 (릴스 A 데모 씬용)
 * 중앙에 큰 텍스트로 기능 포인트 표시
 */
export const FeatureText: React.FC<{
  icon: string;
  text: string;
}> = ({ icon, text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 200 },
  });

  const scale = interpolate(pop, [0, 1], [0.6, 1]);
  const opacity = interpolate(pop, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 60,
        right: 120,
        bottom: 340,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          background: "rgba(0,0,0,0.55)",
          borderRadius: 24,
          padding: "24px 40px",
          backdropFilter: "blur(8px)",
          display: "flex",
          alignItems: "center",
          gap: 16,
        }}
      >
        <span style={{ fontSize: 48 }}>{icon}</span>
        <span
          style={{
            fontSize: 40,
            fontWeight: 800,
            color: "#fff",
            fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
            textShadow: "0 2px 8px rgba(0,0,0,0.5)",
          }}
        >
          {text}
        </span>
      </div>
    </div>
  );
};
