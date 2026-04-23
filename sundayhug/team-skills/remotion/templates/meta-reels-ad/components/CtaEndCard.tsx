import React from "react";
import { useCurrentFrame, useVideoConfig, spring, interpolate } from "remotion";

/**
 * CTA 엔드카드 컴포넌트
 *
 * 마지막 씬에 브랜드명 + 제품명 + CTA 버튼을 오버레이합니다.
 * 순차적 spring 애니메이션으로 시선을 유도합니다.
 */
export const CtaEndCard: React.FC<{
  brandName: string;
  brandColor: string;
  productName: string;
  ctaText?: string;
}> = ({ brandName, brandColor, productName, ctaText = "지금 바로 구매하기" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const logoIn = spring({
    frame: frame - 5,
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  const productIn = spring({
    frame: frame - 15,
    fps,
    config: { damping: 14, stiffness: 160 },
  });

  const ctaIn = spring({
    frame: frame - 25,
    fps,
    config: { damping: 12, stiffness: 180 },
  });

  const ctaPulse = interpolate(
    (frame - 30) % 30,
    [0, 15, 30],
    [0.3, 0.6, 0.3],
  );

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
      <span
        style={{
          fontSize: 40,
          fontWeight: 800,
          color: "#fff",
          fontFamily: "Pretendard, system-ui, sans-serif",
          letterSpacing: 4,
          opacity: interpolate(logoIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(logoIn, [0, 1], [0.6, 1])})`,
          marginBottom: 16,
        }}
      >
        {brandName}
      </span>

      <span
        style={{
          fontSize: 56,
          fontWeight: 900,
          color: "#fff",
          fontFamily: "Pretendard, system-ui, sans-serif",
          opacity: interpolate(productIn, [0, 1], [0, 1]),
          transform: `translateY(${interpolate(productIn, [0, 1], [20, 0])}px)`,
          marginBottom: 40,
          textShadow: "0 2px 12px rgba(0,0,0,0.5)",
        }}
      >
        {productName}
      </span>

      <div
        style={{
          backgroundColor: brandColor,
          borderRadius: 60,
          padding: "20px 64px",
          opacity: interpolate(ctaIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(ctaIn, [0, 1], [0.8, 1])})`,
          boxShadow: `0 4px 20px rgba(0,0,0,0.3), 0 0 30px ${brandColor}${Math.round(ctaPulse * 255).toString(16).padStart(2, "0")}`,
        }}
      >
        <span
          style={{
            fontSize: 36,
            fontWeight: 800,
            color: "#fff",
            fontFamily: "Pretendard, system-ui, sans-serif",
          }}
        >
          {ctaText}
        </span>
      </div>
    </div>
  );
};
