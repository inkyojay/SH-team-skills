import React from "react";
import {
  Img,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  staticFile,
} from "remotion";

/**
 * 제품 정보 배너 컴포넌트
 *
 * 하단에 제품 이미지 + 제품명 + 가격/CTA를 배치합니다.
 * 슬라이드업 애니메이션으로 등장합니다.
 */
export const ProductBanner: React.FC<{
  imageSrc: string;
  productName: string;
  priceText?: string;
  ctaText?: string;
  brandColor?: string;
}> = ({
  imageSrc,
  productName,
  priceText,
  ctaText,
  brandColor = "#4A90D9",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 140 },
  });

  const translateY = interpolate(progress, [0, 1], [80, 0]);
  const opacity = interpolate(progress, [0, 1], [0, 1]);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        padding: "0 40px",
        opacity,
        transform: `translateY(${translateY}px)`,
      }}
    >
      <div
        style={{
          background: "rgba(255,255,255,0.95)",
          borderRadius: 24,
          padding: "20px 32px",
          display: "flex",
          alignItems: "center",
          gap: 24,
          boxShadow: "0 6px 24px rgba(0,0,0,0.12)",
          width: "100%",
          maxWidth: 960,
        }}
      >
        {/* 제품 이미지 */}
        <Img
          src={staticFile(imageSrc)}
          style={{
            width: 120,
            height: 120,
            objectFit: "contain",
            borderRadius: 16,
            flexShrink: 0,
          }}
        />

        {/* 제품 정보 */}
        <div style={{ flex: 1 }}>
          <p
            style={{
              fontSize: 32,
              fontWeight: 800,
              color: "#222",
              fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
              margin: 0,
              lineHeight: 1.3,
            }}
          >
            {productName}
          </p>
          {priceText && (
            <p
              style={{
                fontSize: 28,
                fontWeight: 600,
                color: brandColor,
                fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
                margin: "8px 0 0 0",
              }}
            >
              {priceText}
            </p>
          )}
        </div>

        {/* CTA 버튼 */}
        {ctaText && (
          <div
            style={{
              background: brandColor,
              borderRadius: 16,
              padding: "14px 24px",
              flexShrink: 0,
            }}
          >
            <span
              style={{
                fontSize: 24,
                fontWeight: 700,
                color: "#fff",
                fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
              }}
            >
              {ctaText}
            </span>
          </div>
        )}
      </div>
    </div>
  );
};
