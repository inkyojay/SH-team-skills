import React from "react";
import { AbsoluteFill, Video, useVideoConfig, staticFile } from "remotion";

/**
 * 솔루션 시연 씬 컴포넌트
 *
 * 우리 제품이 문제를 해결하는 시연 영상을 표시합니다.
 * 하단 그라데이션 + 필 자막 조합.
 */
export const SolutionDemo: React.FC<{
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
      {/* 하단 그라데이션 */}
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
