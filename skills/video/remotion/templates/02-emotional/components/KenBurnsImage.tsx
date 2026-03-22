import React from "react";
import {
  AbsoluteFill,
  Img,
  Video,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { FONT, MOTION } from "../../_shared/utils/brand";

/**
 * Ken Burns 효과 이미지/비디오 컴포넌트
 *
 * 미묘한 줌/패닝으로 정적 이미지에 생동감을 부여합니다.
 * scale: 1.0 → 1.08 (가이드라인 준수)
 */

const IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".gif"];
const isImage = (src: string) =>
  IMAGE_EXTS.some((ext) => src.toLowerCase().endsWith(ext));

type Direction = "zoom-in" | "zoom-out" | "pan-left" | "pan-right";

export const KenBurnsImage: React.FC<{
  src: string;
  videoStartFrom?: number;
  direction?: Direction;
  /** 오버레이 텍스트 */
  overlayText?: string;
  children?: React.ReactNode;
}> = ({ src, videoStartFrom = 0, direction = "zoom-in", overlayText, children }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // 전체 씬에 걸친 느린 진행
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: "clamp",
  });

  const { from, to } = MOTION.kenBurns;

  let transform: string;
  switch (direction) {
    case "zoom-in":
      transform = `scale(${interpolate(progress, [0, 1], [from, to])})`;
      break;
    case "zoom-out":
      transform = `scale(${interpolate(progress, [0, 1], [to, from])})`;
      break;
    case "pan-left":
      transform = `scale(${to}) translateX(${interpolate(progress, [0, 1], [2, -2])}%)`;
      break;
    case "pan-right":
      transform = `scale(${to}) translateX(${interpolate(progress, [0, 1], [-2, 2])}%)`;
      break;
  }

  // 텍스트 등장
  const textIn = spring({
    frame: frame - 15,
    fps,
    config: MOTION.springGentle,
  });

  return (
    <AbsoluteFill>
      <div
        style={{
          width: "100%",
          height: "100%",
          transform,
          transformOrigin: "center center",
        }}
      >
        {isImage(src) ? (
          <Img
            src={staticFile(src)}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        ) : (
          <Video
            src={staticFile(src)}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
            startFrom={videoStartFrom * fps}
            muted
          />
        )}
      </div>

      {/* 부드러운 비네트 오버레이 */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(0,0,0,0.3) 100%)",
        }}
      />

      {/* 하단 그라데이션 */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.5) 100%)",
        }}
      />

      {/* 오버레이 텍스트 */}
      {overlayText && (
        <div
          style={{
            position: "absolute",
            bottom: 380,
            left: 0,
            right: 0,
            textAlign: "center",
            padding: "0 80px",
            opacity: interpolate(textIn, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(textIn, [0, 1], [20, 0])}px)`,
          }}
        >
          <p
            style={{
              fontSize: 48,
              fontWeight: 700,
              color: "#fff",
              fontFamily: FONT.body,
              lineHeight: 1.5,
              textShadow: "0 2px 12px rgba(0,0,0,0.6)",
            }}
          >
            {overlayText}
          </p>
        </div>
      )}

      {children}
    </AbsoluteFill>
  );
};
