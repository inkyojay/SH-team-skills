import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

/**
 * 둥근 필(pill) 스타일 자막 컴포넌트
 *
 * 반투명 둥근 배경 위에 텍스트를 표시합니다.
 * 스케일인 + 페이드 애니메이션.
 */
export const PillCaption: React.FC<{
  text: string;
  backgroundColor?: string;
  textColor?: string;
}> = ({
  text,
  backgroundColor = "rgba(0,0,0,0.65)",
  textColor = "#fff",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 160 },
  });

  const opacity = interpolate(progress, [0, 1], [0, 1]);
  const scale = interpolate(progress, [0, 1], [0.85, 1]);

  return (
    <div
      style={{
        position: "absolute",
        bottom: 300,
        left: 0,
        right: 0,
        display: "flex",
        justifyContent: "center",
        padding: "0 40px",
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      <div
        style={{
          background: backgroundColor,
          borderRadius: 40,
          padding: "18px 40px",
          backdropFilter: "blur(8px)",
        }}
      >
        <p
          style={{
            fontSize: 48,
            fontWeight: 800,
            color: textColor,
            fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
            textAlign: "center",
            lineHeight: 1.4,
            margin: 0,
            letterSpacing: -0.5,
          }}
        >
          {text}
        </p>
      </div>
    </div>
  );
};
