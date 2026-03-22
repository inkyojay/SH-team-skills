import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Img,
} from "remotion";

/**
 * 카운트다운 개별 카드 - 큰 숫자 줌인 + 텍스트 슬라이드업
 * #1 아이템은 플래시 + 더 큰 텍스트 + 긴 홀드
 */
export const CountdownCard: React.FC<{
  number: number;
  text: string;
  mediaSrc?: string;
  isTop: boolean;
  numberColor?: string;
}> = ({ number, text, mediaSrc, isTop, numberColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // 숫자 줌인: scale 3 → 1
  const numberScale = spring({
    frame,
    fps,
    config: { damping: 10, stiffness: 100, mass: 1.2 },
  });
  const numberScaleValue = interpolate(numberScale, [0, 1], [3, 1]);

  // 텍스트 슬라이드업 (숫자 후 0.4초)
  const textDelay = Math.round(fps * 0.4);
  const textProgress = spring({
    frame: frame - textDelay,
    fps,
    config: { damping: 14, stiffness: 150 },
  });
  const textY = interpolate(textProgress, [0, 1], [80, 0]);
  const textOpacity = interpolate(textProgress, [0, 0.6], [0, 1], {
    extrapolateRight: "clamp",
  });

  // #1 특별 플래시 효과
  const flashOpacity = isTop
    ? interpolate(frame, [0, 3, 8], [0.8, 0.8, 0], {
        extrapolateRight: "clamp",
      })
    : 0;

  const fontSize = isTop ? 280 : 220;
  const textSize = isTop ? 52 : 42;

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        position: "relative",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        overflow: "hidden",
      }}
    >
      {/* 배경 이미지 (선택) */}
      {mediaSrc && (
        <Img
          src={mediaSrc}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            opacity: 0.3,
          }}
        />
      )}

      {/* 어두운 오버레이 */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundColor: "rgba(0,0,0,0.5)",
        }}
      />

      {/* 플래시 (1번만) */}
      {isTop && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundColor: "#fff",
            opacity: flashOpacity,
            zIndex: 5,
          }}
        />
      )}

      {/* 숫자 */}
      <div
        style={{
          position: "relative",
          zIndex: 2,
          transform: `scale(${numberScaleValue})`,
        }}
      >
        <span
          style={{
            fontSize,
            fontWeight: 900,
            fontFamily: "Impact, Arial Black, sans-serif",
            color: "transparent",
            background: numberColor
              ? numberColor
              : isTop
                ? "linear-gradient(135deg, #FF6B6B, #FFE66D)"
                : "linear-gradient(135deg, #4ECDC4, #556270)",
            backgroundClip: "text",
            WebkitBackgroundClip: "text",
            WebkitTextFillColor: "transparent",
            textShadow: "none",
            lineHeight: 1,
          }}
        >
          {number}
        </span>
      </div>

      {/* 텍스트 */}
      <div
        style={{
          position: "relative",
          zIndex: 2,
          transform: `translateY(${textY}px)`,
          opacity: textOpacity,
          marginTop: 20,
          padding: "0 60px",
          textAlign: "center",
        }}
      >
        <p
          style={{
            fontSize: textSize,
            fontWeight: 800,
            color: "#fff",
            fontFamily: "Arial, sans-serif",
            lineHeight: 1.4,
            margin: 0,
            textShadow: "0 2px 8px rgba(0,0,0,0.8)",
          }}
        >
          {text}
        </p>
      </div>
    </div>
  );
};
