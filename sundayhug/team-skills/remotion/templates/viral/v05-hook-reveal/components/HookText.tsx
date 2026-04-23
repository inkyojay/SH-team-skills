import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";

/**
 * 훅 텍스트 씬
 *
 * 화면 80%를 채우는 대형 텍스트 + 스케일 펄스 효과.
 * 시선을 강제로 붙잡는 역할.
 */
export const HookText: React.FC<{
  text: string;
  emoji?: string;
  bgColor: string;
  textColor: string;
  scale?: number;
}> = ({ text, emoji, bgColor, textColor, scale = 1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 즉시 등장 + 약간의 스케일 펄스
  const pulse = interpolate(
    Math.sin(frame * 0.15),
    [-1, 1],
    [0.97, 1.03]
  );

  // 첫 2프레임 약간의 글리치 오프셋
  const glitchX =
    frame < 3
      ? (Math.sin(frame * 17) * 15)
      : 0;
  const glitchY =
    frame < 3
      ? (Math.cos(frame * 13) * 10)
      : 0;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bgColor,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 20 * scale,
      }}
    >
      {emoji && (
        <span
          style={{
            fontSize: 120 * scale,
            transform: `translate(${glitchX}px, ${glitchY}px)`,
          }}
        >
          {emoji}
        </span>
      )}
      <div
        style={{
          fontSize: 96 * scale,
          fontWeight: 900,
          color: textColor,
          fontFamily: "system-ui, -apple-system, sans-serif",
          textAlign: "center",
          lineHeight: 1.1,
          padding: `0 ${60 * scale}px`,
          transform: `scale(${pulse}) translate(${glitchX}px, ${glitchY}px)`,
          wordBreak: "keep-all",
          maxWidth: "90%",
        }}
      >
        {text}
      </div>
    </AbsoluteFill>
  );
};
