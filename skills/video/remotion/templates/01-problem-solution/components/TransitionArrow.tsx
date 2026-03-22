import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { FONT, MOTION, BRAND } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";

/**
 * 문제→솔루션 전환 화살표 오버레이
 *
 * 다크→브라이트 wipe 전환 효과와 함께 전환 텍스트를 표시합니다.
 * TransitionSeries.Transition 대신 씬 시작부에 오버레이로 사용할 수 있습니다.
 */
export const TransitionArrow: React.FC<{
  /** 전환 텍스트 (예: "이제는 달라요", "해결책은?") */
  text?: string;
  palette?: string;
  brandColor?: string;
}> = ({ text = "해결책은?", palette, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const pal = getPalette(palette);
  const color = brandColor ?? pal.accent;

  // wipe 진행도
  const wipeProgress = spring({
    frame,
    fps,
    config: { damping: 20, stiffness: 100 },
  });

  // 텍스트 등장
  const textIn = spring({
    frame: frame - 5,
    fps,
    config: MOTION.springSnappy,
  });

  const textOpacity = interpolate(textIn, [0, 1], [0, 1]);
  const textScale = interpolate(textIn, [0, 1], [0.7, 1]);

  // wipe out (씬 후반부에 사라짐)
  const wipeOut = interpolate(frame, [20, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const overallOpacity = interpolate(wipeOut, [0, 1], [1, 0]);

  return (
    <AbsoluteFill
      style={{
        opacity: overallOpacity,
        zIndex: 50,
      }}
    >
      {/* 배경 wipe */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          background: pal.bg,
          clipPath: `circle(${interpolate(wipeProgress, [0, 1], [0, 150])}% at 50% 50%)`,
        }}
      />
      {/* 전환 텍스트 */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          opacity: textOpacity,
          transform: `scale(${textScale})`,
        }}
      >
        {/* 화살표 */}
        <svg
          width="80"
          height="80"
          viewBox="0 0 24 24"
          style={{ marginBottom: 24 }}
        >
          <path
            d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"
            fill={color}
          />
        </svg>
        <span
          style={{
            fontSize: 52,
            fontWeight: 800,
            color: pal.text,
            fontFamily: FONT.body,
          }}
        >
          {text}
        </span>
      </div>
    </AbsoluteFill>
  );
};
