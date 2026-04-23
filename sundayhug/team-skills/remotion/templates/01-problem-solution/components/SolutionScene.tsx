import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { VideoClip } from "../../_shared/components/VideoClip";
import { FONT, MOTION, BRAND } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";

/**
 * 솔루션 씬
 *
 * 밝은 톤 + spring 등장으로 솔루션의 긍정적 분위기를 표현합니다.
 */
export const SolutionScene: React.FC<{
  mediaSrc: string;
  videoStartFrom?: number;
  solutionText: string;
  subText?: string;
  productName?: string;
  palette?: string;
  brandColor?: string;
}> = ({
  mediaSrc,
  videoStartFrom,
  solutionText,
  subText,
  productName,
  palette,
  brandColor,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(palette);
  const accentColor = brandColor ?? pal.accent;

  // 메인 텍스트 spring
  const textIn = spring({
    frame: frame - 8,
    fps,
    config: MOTION.springSnappy,
  });

  // 제품명 spring (딜레이)
  const productIn = spring({
    frame: frame - 18,
    fps,
    config: MOTION.spring,
  });

  const opacity = interpolate(textIn, [0, 1], [0, 1]);
  const translateY = interpolate(textIn, [0, 1], [40, 0]);
  const scale = interpolate(textIn, [0, 1], [0.9, 1]);

  return (
    <AbsoluteFill>
      <VideoClip
        src={mediaSrc}
        startFrom={videoStartFrom}
        overlayStyle={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.1) 50%, rgba(0,0,0,0.5) 100%)",
        }}
      />
      {/* 텍스트 영역 */}
      <div
        style={{
          position: "absolute",
          bottom: 350,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          padding: "0 60px",
          opacity,
          transform: `translateY(${translateY}px) scale(${scale})`,
        }}
      >
        {productName && (
          <div
            style={{
              background: accentColor,
              borderRadius: 30,
              padding: "8px 28px",
              marginBottom: 20,
              opacity: interpolate(productIn, [0, 1], [0, 1]),
              transform: `scale(${interpolate(productIn, [0, 1], [0.8, 1])})`,
            }}
          >
            <span
              style={{
                fontSize: 24,
                fontWeight: 700,
                color: "#fff",
                fontFamily: FONT.body,
                letterSpacing: 2,
              }}
            >
              {productName}
            </span>
          </div>
        )}
        <p
          style={{
            fontSize: 58,
            fontWeight: 900,
            color: "#fff",
            fontFamily: FONT.body,
            textAlign: "center",
            lineHeight: 1.4,
            margin: 0,
            textShadow: "0 4px 16px rgba(0,0,0,0.6)",
          }}
        >
          {solutionText}
        </p>
        {subText && (
          <p
            style={{
              fontSize: 34,
              fontWeight: 500,
              color: "rgba(255,255,255,0.85)",
              fontFamily: FONT.body,
              textAlign: "center",
              marginTop: 16,
              textShadow: "0 2px 8px rgba(0,0,0,0.5)",
            }}
          >
            {subText}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};
