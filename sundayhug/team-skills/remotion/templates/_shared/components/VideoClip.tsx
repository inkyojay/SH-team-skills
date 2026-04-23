import React from "react";
import { AbsoluteFill, Video, Img, useVideoConfig, staticFile } from "remotion";

/**
 * 공용 비디오/이미지 클립 + 그라데이션 오버레이
 *
 * src 확장자가 이미지(.jpg, .png, .webp)이면 Img, 아니면 Video로 렌더링합니다.
 */
const IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".webp", ".gif"];

function isImage(src: string): boolean {
  const lower = src.toLowerCase();
  return IMAGE_EXTENSIONS.some((ext) => lower.endsWith(ext));
}

export const VideoClip: React.FC<{
  src: string;
  startFrom?: number;
  /** 하단 그라데이션 표시 여부 (기본 true) */
  showGradient?: boolean;
  /** 커스텀 오버레이 CSS */
  overlayStyle?: React.CSSProperties;
  children?: React.ReactNode;
}> = ({ src, startFrom = 0, showGradient = true, overlayStyle, children }) => {
  const { fps } = useVideoConfig();

  return (
    <AbsoluteFill>
      {isImage(src) ? (
        <Img
          src={staticFile(src)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
        />
      ) : (
        <Video
          src={staticFile(src)}
          style={{ width: "100%", height: "100%", objectFit: "cover" }}
          startFrom={startFrom * fps}
          muted
        />
      )}
      {showGradient && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background:
              "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.6) 100%)",
            ...overlayStyle,
          }}
        />
      )}
      {children}
    </AbsoluteFill>
  );
};
