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
 * 고정 상단 헤더 컴포넌트
 *
 * 브랜드 로고 + 제품명 + 제품 썸네일을 상단에 고정 표시합니다.
 * 전체 영상 동안 유지되어 브랜드 인지도를 높입니다.
 */
export const BrandHeader: React.FC<{
  logoSrc: string;
  productName: string;
  productImageSrc?: string;
  brandColor: string;
}> = ({ logoSrc, productName, productImageSrc, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const slideDown = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 120 },
  });

  const translateY = interpolate(slideDown, [0, 1], [-120, 0]);
  const opacity = interpolate(slideDown, [0, 1], [0, 1]);

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 0,
        right: 0,
        zIndex: 10,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "60px 40px 30px",
        background:
          "linear-gradient(180deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0.3) 70%, rgba(0,0,0,0) 100%)",
        transform: `translateY(${translateY}px)`,
        opacity,
      }}
    >
      {/* 로고 */}
      <Img
        src={staticFile(logoSrc)}
        style={{
          height: 48,
          objectFit: "contain",
          marginBottom: 12,
        }}
      />

      {/* 제품명 */}
      <p
        style={{
          fontSize: 32,
          fontWeight: 700,
          color: "#fff",
          fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
          textAlign: "center",
          margin: 0,
          letterSpacing: 1,
        }}
      >
        {productName}
      </p>

      {/* 제품 썸네일 */}
      {productImageSrc && (
        <Img
          src={staticFile(productImageSrc)}
          style={{
            width: 160,
            height: 160,
            objectFit: "contain",
            marginTop: 16,
            borderRadius: 20,
            border: `3px solid ${brandColor}`,
            background: "rgba(255,255,255,0.1)",
          }}
        />
      )}
    </div>
  );
};
