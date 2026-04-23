import React from "react";
import { AbsoluteFill, Video, useVideoConfig, staticFile } from "remotion";

/**
 * 특징 소개 슬라이드 컴포넌트
 *
 * 헤더 아래 영역에 비디오/이미지를 표시하는 슬라이드.
 * 하단 그라데이션으로 자막 가독성을 확보합니다.
 */
export const FeatureSlide: React.FC<{
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
      {/* 상단 + 하단 그라데이션 (헤더/자막 가독성) */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: [
            "linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0) 25%)",
            "linear-gradient(0deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0) 40%)",
          ].join(", "),
        }}
      />
      {children}
    </AbsoluteFill>
  );
};
