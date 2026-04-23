import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { FONT, MOTION } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";

/**
 * 감성 인용구 카드
 *
 * Cormorant Garamond 디스플레이 폰트로 인용구를 표시합니다.
 * 슬로우 페이드 + translateY 등장.
 */
export const QuoteCard: React.FC<{
  quoteText: string;
  attribution?: string;
  backgroundColor?: string;
  palette?: string;
  brandColor?: string;
}> = ({ quoteText, attribution, backgroundColor, palette, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(palette);
  const accent = brandColor ?? pal.accent;

  const quoteIn = spring({
    frame: frame - 10,
    fps,
    config: { damping: 22, stiffness: 80 }, // 매우 느리고 부드럽게
  });

  const attrIn = spring({
    frame: frame - 30,
    fps,
    config: MOTION.springGentle,
  });

  // 따옴표 장식
  const quoteMarkIn = spring({
    frame: frame - 5,
    fps,
    config: MOTION.springGentle,
  });

  const bgColor = backgroundColor ?? pal.bg;

  return (
    <AbsoluteFill
      style={{
        background: bgColor,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 80px",
      }}
    >
      {/* 큰 따옴표 장식 */}
      <span
        style={{
          fontSize: 160,
          fontWeight: 300,
          color: `${accent}30`,
          fontFamily: FONT.display,
          lineHeight: 0.8,
          opacity: interpolate(quoteMarkIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(quoteMarkIn, [0, 1], [0.5, 1])})`,
          marginBottom: -20,
        }}
      >
        "
      </span>

      {/* 인용구 */}
      <p
        style={{
          fontSize: 44,
          fontWeight: 400,
          color: pal.text,
          fontFamily: FONT.display,
          textAlign: "center",
          lineHeight: 1.7,
          margin: 0,
          fontStyle: "italic",
          opacity: interpolate(quoteIn, [0, 1], [0, 1]),
          transform: `translateY(${interpolate(quoteIn, [0, 1], [30, 0])}px)`,
          maxWidth: 900,
        }}
      >
        {quoteText}
      </p>

      {/* 출처 */}
      {attribution && (
        <p
          style={{
            fontSize: 28,
            fontWeight: 500,
            color: accent,
            fontFamily: FONT.body,
            marginTop: 32,
            opacity: interpolate(attrIn, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(attrIn, [0, 1], [10, 0])}px)`,
          }}
        >
          — {attribution}
        </p>
      )}
    </AbsoluteFill>
  );
};
