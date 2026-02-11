import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

/**
 * CTA 엔드카드
 */
export const CtaEndCard: React.FC<{
  brandName: string;
  brandColor: string;
  line1: string;
  line2?: string;
  price?: string;
}> = ({ brandName, brandColor, line1, line2, price }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoIn = spring({
    frame: frame - 5,
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  const textIn = spring({
    frame: frame - 15,
    fps,
    config: { damping: 14, stiffness: 160 },
  });

  const ctaIn = spring({
    frame: frame - 25,
    fps,
    config: { damping: 12, stiffness: 180 },
  });

  const ctaPulse = interpolate((frame - 30) % 30, [0, 15, 30], [0.3, 0.6, 0.3]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        background: "rgba(0,0,0,0.45)",
        zIndex: 20,
      }}
    >
      {/* 브랜드명 */}
      <span
        style={{
          fontSize: 36,
          fontWeight: 800,
          color: "#fff",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          letterSpacing: 4,
          opacity: interpolate(logoIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(logoIn, [0, 1], [0.6, 1])})`,
          marginBottom: 20,
        }}
      >
        {brandName}
      </span>

      {/* 메인 카피 */}
      <div
        style={{
          opacity: interpolate(textIn, [0, 1], [0, 1]),
          transform: `translateY(${interpolate(textIn, [0, 1], [20, 0])}px)`,
          textAlign: "center",
          marginBottom: 16,
          padding: "0 60px",
        }}
      >
        <p
          style={{
            fontSize: 48,
            fontWeight: 900,
            color: "#fff",
            fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
            textShadow: "0 2px 12px rgba(0,0,0,0.5)",
            lineHeight: 1.3,
            margin: 0,
          }}
        >
          {line1}
        </p>
        {line2 && (
          <p
            style={{
              fontSize: 40,
              fontWeight: 700,
              color: "#fff",
              fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
              textShadow: "0 2px 12px rgba(0,0,0,0.5)",
              margin: "8px 0 0",
            }}
          >
            {line2}
          </p>
        )}
      </div>

      {/* 가격 */}
      {price && (
        <span
          style={{
            fontSize: 32,
            fontWeight: 600,
            color: "rgba(255,255,255,0.85)",
            fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
            opacity: interpolate(textIn, [0, 1], [0, 1]),
            marginBottom: 30,
          }}
        >
          {price}
        </span>
      )}

      {/* CTA 버튼 */}
      <div
        style={{
          backgroundColor: brandColor,
          borderRadius: 60,
          padding: "20px 56px",
          opacity: interpolate(ctaIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(ctaIn, [0, 1], [0.8, 1])})`,
          boxShadow: `0 4px 20px rgba(0,0,0,0.3), 0 0 30px ${brandColor}${Math.round(ctaPulse * 255)
            .toString(16)
            .padStart(2, "0")}`,
        }}
      >
        <span
          style={{
            fontSize: 34,
            fontWeight: 800,
            color: "#fff",
            fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          }}
        >
          프로필 링크에서 확인하세요 👆
        </span>
      </div>
    </div>
  );
};
