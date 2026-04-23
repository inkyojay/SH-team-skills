import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

/**
 * 제품 리빌 씬
 *
 * 훅 이후 하드 컷으로 전환되는 제품 공개 화면.
 * 캐주얼하지만 깔끔한 레이아웃.
 */
export const RevealScene: React.FC<{
  productName: string;
  caption: string;
  ctaText: string;
  ctaColor: string;
  bgColor: string;
  mediaSrc?: string;
  scale?: number;
}> = ({
  productName,
  caption,
  ctaText,
  ctaColor,
  bgColor,
  mediaSrc,
  scale = 1,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 제품명 등장 (약간의 zoom)
  const nameScale = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 150, mass: 0.6 },
    from: 1.2,
    to: 1,
  });

  const nameOpacity = interpolate(frame, [0, 6], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 캡션 등장 (약간 딜레이)
  const captionOpacity = interpolate(
    frame,
    [fps * 0.3, fps * 0.3 + 8],
    [0, 1],
    { extrapolateRight: "clamp" }
  );

  // CTA 등장
  const ctaProgress = spring({
    frame: frame - fps * 0.6,
    fps,
    config: { damping: 10, stiffness: 120, mass: 0.8 },
  });

  return (
    <AbsoluteFill
      style={{
        backgroundColor: bgColor,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 40 * scale,
      }}
    >
      {/* 제품 이미지 영역 */}
      <div
        style={{
          width: 600 * scale,
          height: 600 * scale,
          borderRadius: 32 * scale,
          backgroundColor: bgColor === "#FFF" || bgColor === "#FFFFFF"
            ? "#F5F5F5"
            : "rgba(255,255,255,0.1)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 100 * scale,
          opacity: nameOpacity,
          transform: `scale(${nameScale})`,
        }}
      >
        📦
      </div>

      {/* 제품명 */}
      <div
        style={{
          fontSize: 72 * scale,
          fontWeight: 800,
          color: bgColor === "#FFF" || bgColor === "#FFFFFF" ? "#1C1C1E" : "#FFF",
          fontFamily: "system-ui, -apple-system, sans-serif",
          textAlign: "center",
          opacity: nameOpacity,
          transform: `scale(${nameScale})`,
          padding: `0 ${40 * scale}px`,
        }}
      >
        {productName}
      </div>

      {/* 캡션 */}
      <div
        style={{
          fontSize: 36 * scale,
          color:
            bgColor === "#FFF" || bgColor === "#FFFFFF"
              ? "#666"
              : "rgba(255,255,255,0.7)",
          fontFamily: "system-ui, -apple-system, sans-serif",
          textAlign: "center",
          opacity: captionOpacity,
          padding: `0 ${60 * scale}px`,
          lineHeight: 1.4,
        }}
      >
        {caption}
      </div>

      {/* CTA Button */}
      <div
        style={{
          backgroundColor: ctaColor,
          borderRadius: 60 * scale,
          padding: `${24 * scale}px ${64 * scale}px`,
          opacity: ctaProgress,
          transform: `scale(${interpolate(ctaProgress, [0, 1], [0.8, 1])})`,
        }}
      >
        <span
          style={{
            fontSize: 40 * scale,
            fontWeight: 800,
            color: "#FFF",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {ctaText}
        </span>
      </div>
    </AbsoluteFill>
  );
};
