import React from "react";
import {
  AbsoluteFill,
  Img,
  Video,
  useVideoConfig,
  useCurrentFrame,
  interpolate,
  staticFile,
} from "remotion";

/**
 * 아기 사진/비디오 배경 영역 컴포넌트
 *
 * 제품 사용 이미지 또는 비디오를 배경으로 표시합니다.
 * 살짝 줌인하는 Ken Burns 효과를 적용합니다.
 */
export const BabyPhoto: React.FC<{
  src: string;
  isVideo?: boolean;
  videoStartFrom?: number;
  durationInFrames?: number;
}> = ({ src, isVideo = false, videoStartFrom = 0, durationInFrames = 180 }) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  // Ken Burns: 살짝 줌인
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.06], {
    extrapolateRight: "clamp",
  });

  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ opacity }}>
      {isVideo ? (
        <Video
          src={staticFile(src)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${scale})`,
          }}
          startFrom={videoStartFrom * fps}
          muted
        />
      ) : (
        <Img
          src={staticFile(src)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${scale})`,
          }}
        />
      )}
      {/* 전체 반투명 오버레이 */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background:
            "linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.15) 40%, rgba(0,0,0,0.5) 100%)",
        }}
      />
    </AbsoluteFill>
  );
};
