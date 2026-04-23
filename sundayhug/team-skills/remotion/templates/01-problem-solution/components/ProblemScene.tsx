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
 * 문제 제시 씬
 *
 * 다크 톤 오버레이 + 흔들림(shake) 모션으로 불안감을 표현합니다.
 */
export const ProblemScene: React.FC<{
  mediaSrc: string;
  videoStartFrom?: number;
  problemText: string;
  subText?: string;
  palette?: string;
}> = ({ mediaSrc, videoStartFrom, problemText, subText, palette }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(palette);

  // 텍스트 등장 spring
  const textIn = spring({
    frame: frame - 8,
    fps,
    config: MOTION.spring,
  });

  const opacity = interpolate(textIn, [0, 1], [0, 1]);
  const translateY = interpolate(textIn, [0, 1], [40, 0]);

  // 미세 흔들림 (문제 강조)
  const shake = frame < 20
    ? interpolate(frame, [0, 5, 10, 15, 20], [0, -3, 3, -2, 0])
    : 0;

  return (
    <AbsoluteFill>
      <VideoClip
        src={mediaSrc}
        startFrom={videoStartFrom}
        overlayStyle={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.15) 40%, rgba(0,0,0,0.7) 100%)",
        }}
      />
      {/* 다크 톤 필터 */}
      <AbsoluteFill
        style={{
          background: "rgba(30,20,15,0.25)",
          filter: "saturate(0.7)",
        }}
      />
      {/* 텍스트 */}
      <div
        style={{
          position: "absolute",
          bottom: 380,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          padding: "0 60px",
          opacity,
          transform: `translateY(${translateY}px) translateX(${shake}px)`,
        }}
      >
        <p
          style={{
            fontSize: 58,
            fontWeight: 900,
            color: "#fff",
            fontFamily: FONT.body,
            textAlign: "center",
            lineHeight: 1.4,
            margin: 0,
            textShadow: "0 4px 16px rgba(0,0,0,0.8)",
          }}
        >
          {problemText}
        </p>
        {subText && (
          <p
            style={{
              fontSize: 36,
              fontWeight: 500,
              color: "rgba(255,255,255,0.8)",
              fontFamily: FONT.body,
              textAlign: "center",
              marginTop: 16,
              textShadow: "0 2px 8px rgba(0,0,0,0.6)",
            }}
          >
            {subText}
          </p>
        )}
      </div>
    </AbsoluteFill>
  );
};
