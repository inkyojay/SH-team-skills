import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

/**
 * iOS 스타일 알림 배너 컴포넌트
 *
 * 위에서 슬라이드 인 → 유지 → 슬라이드 아웃
 */
export const IOSNotification: React.FC<{
  appName: string;
  title: string;
  body: string;
  appIcon?: string;
  appearFrame: number;
  stayDurationFrames: number;
  index: number;
  scale?: number;
}> = ({
  appName,
  title,
  body,
  appIcon = "\uD83D\uDCF1",
  appearFrame,
  stayDurationFrames,
  index,
  scale = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - appearFrame;
  if (localFrame < 0) return null;

  const exitFrame = stayDurationFrames;
  const totalDuration = exitFrame + fps * 0.5;
  if (localFrame > totalDuration) return null;

  // Slide in with spring
  const slideIn = spring({
    frame: localFrame,
    fps,
    config: { damping: 18, stiffness: 180, mass: 0.8 },
  });

  // Slide out
  const isExiting = localFrame > exitFrame;
  const exitProgress = isExiting
    ? interpolate(
        localFrame - exitFrame,
        [0, fps * 0.3],
        [0, 1],
        { extrapolateRight: "clamp" }
      )
    : 0;

  const translateY = interpolate(slideIn, [0, 1], [-200 * scale, 0]) -
    exitProgress * 200 * scale;
  const opacity = isExiting ? 1 - exitProgress : slideIn;

  return (
    <div
      style={{
        position: "absolute",
        top: (60 + index * 10) * scale,
        left: 24 * scale,
        right: 24 * scale,
        transform: `translateY(${translateY}px)`,
        opacity,
        zIndex: 100 - index,
      }}
    >
      <div
        style={{
          backgroundColor: "rgba(255, 255, 255, 0.95)",
          backdropFilter: "blur(40px)",
          WebkitBackdropFilter: "blur(40px)",
          borderRadius: 28 * scale,
          padding: `${20 * scale}px ${24 * scale}px`,
          boxShadow: `0 ${8 * scale}px ${32 * scale}px rgba(0,0,0,0.15)`,
        }}
      >
        {/* Header */}
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 10 * scale,
            marginBottom: 8 * scale,
          }}
        >
          {/* App Icon */}
          <div
            style={{
              width: 40 * scale,
              height: 40 * scale,
              borderRadius: 10 * scale,
              backgroundColor: "#F0F0F0",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 22 * scale,
            }}
          >
            {appIcon}
          </div>
          <span
            style={{
              fontSize: 24 * scale,
              color: "#8E8E93",
              fontWeight: 500,
              fontFamily: "system-ui, -apple-system, sans-serif",
              textTransform: "uppercase",
              letterSpacing: 0.5,
              flex: 1,
            }}
          >
            {appName}
          </span>
          <span
            style={{
              fontSize: 22 * scale,
              color: "#8E8E93",
              fontFamily: "system-ui, -apple-system, sans-serif",
            }}
          >
            now
          </span>
        </div>

        {/* Title */}
        <div
          style={{
            fontSize: 30 * scale,
            fontWeight: 700,
            color: "#1C1C1E",
            fontFamily: "system-ui, -apple-system, sans-serif",
            marginBottom: 4 * scale,
            lineHeight: 1.3,
          }}
        >
          {title}
        </div>

        {/* Body */}
        <div
          style={{
            fontSize: 28 * scale,
            color: "#6C6C70",
            fontFamily: "system-ui, -apple-system, sans-serif",
            lineHeight: 1.3,
            overflow: "hidden",
            textOverflow: "ellipsis",
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical" as const,
          }}
        >
          {body}
        </div>
      </div>
    </div>
  );
};
