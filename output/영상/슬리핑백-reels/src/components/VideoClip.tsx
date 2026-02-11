import React from "react";
import { AbsoluteFill, Video, useVideoConfig, staticFile } from "remotion";

/**
 * 비디오 클립 + 하단 그라데이션 오버레이
 */
export const VideoClip: React.FC<{
  src: string;
  startFrom?: number;
  playbackRate?: number;
  children?: React.ReactNode;
}> = ({ src, startFrom = 0, playbackRate = 1, children }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      <Video
        src={staticFile(src)}
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
        startFrom={Math.round(startFrom * fps)}
        playbackRate={playbackRate}
        muted
      />
      {/* 하단 그라데이션 (텍스트 가독성) */}
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
