import React from "react";
import { AbsoluteFill, Video, useVideoConfig, staticFile } from "remotion";

/**
 * 셀카/미러 훅 씬 컴포넌트
 *
 * UGC 리뷰 영상의 첫 씬으로, 카메라를 직접 보며
 * 시청자 관심을 끄는 셀카 스타일 영상을 표시합니다.
 * 약간의 비네팅 효과로 포커스를 줍니다.
 */
export const SelfieHook: React.FC<{
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
            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 50%, rgba(0,0,0,0.65) 100%)",
        }}
      />
      {children}
    </AbsoluteFill>
  );
};
