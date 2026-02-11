import React from "react";
import {
  AbsoluteFill,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";

/**
 * 이미지 슬라이드 + Ken Burns 효과
 * 사진 소스를 영상처럼 보여주는 컴포넌트
 */
export const ImageSlide: React.FC<{
  src: string;
  zoomDirection?: "in" | "out";
  zoomRange?: [number, number];
  backgroundColor?: string;
  children?: React.ReactNode;
}> = ({
  src,
  zoomDirection = "in",
  zoomRange = [1.0, 1.15],
  backgroundColor = "#000",
  children,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  const [from, to] =
    zoomDirection === "in" ? zoomRange : [zoomRange[1], zoomRange[0]];

  const scale = interpolate(frame, [0, durationInFrames], [from, to], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor }}>
      <Img
        src={staticFile(src)}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
          transform: `scale(${scale})`,
        }}
      />
      {/* 하단 그라데이션 */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background:
            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.65) 100%)",
        }}
      />
      {children}
    </AbsoluteFill>
  );
};
