import React from "react";
import { AbsoluteFill, Video, useVideoConfig, staticFile } from "remotion";

/**
 * 비디오 클립 + 그라데이션 오버레이 래퍼
 *
 * 하단 그라데이션으로 자막 가독성을 확보합니다.
 */
export const VideoClip: React.FC<{
  src: string;
  startFrom?: number;
  children?: React.ReactNode;
}> = ({ src, startFrom = 0, children }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      <Video
        src={staticFile(src)}
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
        startFrom={startFrom * fps}
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
            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.6) 100%)",
        }}
      />
      {children}
    </AbsoluteFill>
  );
};
