import React from "react";
import { AbsoluteFill, Video, useVideoConfig, staticFile } from "remotion";

/**
 * 문제 제시 씬 컴포넌트
 *
 * 소비자가 겪는 문제/고민을 배경 영상 위에 텍스트로 제시합니다.
 * 어두운 오버레이로 텍스트 가독성을 확보합니다.
 */
export const ProblemScene: React.FC<{
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
      {/* 전체 어두운 오버레이 (문제 제시 분위기) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background:
            "linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.2) 40%, rgba(0,0,0,0.7) 100%)",
        }}
      />
      {children}
    </AbsoluteFill>
  );
};
