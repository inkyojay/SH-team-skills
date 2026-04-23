import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Sequence,
} from "remotion";
import type { UglyReviewConfig } from "./types";

/**
 * V04 - Ugly/Lo-Fi Review 광고
 *
 * TikTok/릴스 스타일의 볼드 캡션 리뷰 템플릿.
 * 카메라 쉐이크, 하드 컷, 의도적 "못생긴" 디자인.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="UglyReview"
 *   component={UglyReview}
 *   durationInFrames={30 * 20}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       reviewText: "진짜 써보고 깜놀함\n아기가 5분만에 잠듦\n이건 사기임 (좋은 의미로)",
 *       reviewerName: "육아맘 김**",
 *       productName: "스와들스트랩",
 *       bgColor: "#FF6B6B",
 *       rating: 5,
 *     },
 *   }}
 * />
 * ```
 */
export const UglyReview: React.FC<{ config: UglyReviewConfig }> = ({
  config,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const scale = Math.min(width / 1080, height / 1920);
  const shakeIntensity = config.shakeIntensity ?? 0.5;
  const highlightColor = config.highlightColor ?? "#FFFF00";
  const bgColor = config.bgColor ?? "#FF6B6B";
  const bgGradientEnd = config.bgGradientEnd;

  // 카메라 쉐이크 (의사 랜덤)
  const shakeX =
    Math.sin(frame * 0.7) * 6 * shakeIntensity +
    Math.cos(frame * 1.3) * 3 * shakeIntensity;
  const shakeY =
    Math.cos(frame * 0.9) * 5 * shakeIntensity +
    Math.sin(frame * 1.1) * 2 * shakeIntensity;
  const shakeRotate =
    Math.sin(frame * 0.5) * 0.3 * shakeIntensity;

  // 리뷰 텍스트를 줄 단위로 분리
  const lines = config.reviewText.split("\n").filter((l) => l.trim());

  // 각 줄이 등장하는 프레임 (하드 컷 — 즉시 등장)
  const lineInterval = Math.floor((fps * 15) / Math.max(lines.length, 1));
  const lineAppearFrames = lines.map((_, i) => i * lineInterval + fps * 0.5);

  // 별점 등장 프레임
  const ratingAppearFrame =
    lineAppearFrames.length > 0
      ? lineAppearFrames[lineAppearFrames.length - 1] + lineInterval * 0.5
      : fps;

  // 텍스트에서 제품명을 하이라이트 처리하는 헬퍼
  const renderHighlightedText = (text: string): React.ReactNode => {
    if (!text.includes(config.productName)) return text;
    const parts = text.split(config.productName);
    return (
      <>
        {parts[0]}
        <span
          style={{
            backgroundColor: highlightColor,
            padding: `${4 * scale}px ${8 * scale}px`,
            color: "#000",
          }}
        >
          {config.productName}
        </span>
        {parts.slice(1).join(config.productName)}
      </>
    );
  };

  // 텍스트 스트로크 스타일 (CSS text-stroke)
  const captionStyle: React.CSSProperties = {
    fontSize: 64 * scale,
    fontWeight: 900,
    color: "#FFFFFF",
    fontFamily: "system-ui, -apple-system, sans-serif",
    textAlign: "center" as const,
    lineHeight: 1.3,
    WebkitTextStroke: `${3 * scale}px #000`,
    paintOrder: "stroke fill",
    letterSpacing: -1,
    padding: `0 ${40 * scale}px`,
    wordBreak: "keep-all" as const,
  };

  return (
    <AbsoluteFill
      style={{
        background: bgGradientEnd
          ? `linear-gradient(180deg, ${bgColor} 0%, ${bgGradientEnd} 100%)`
          : bgColor,
        transform: `translate(${shakeX}px, ${shakeY}px) rotate(${shakeRotate}deg)`,
      }}
    >
      {/* 약간의 노이즈/그레인 오버레이 */}
      <AbsoluteFill
        style={{
          opacity: 0.04,
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)'/%3E%3C/svg%3E")`,
          backgroundSize: "256px 256px",
        }}
      />

      {/* 리뷰어 이름 (상단) */}
      <div
        style={{
          position: "absolute",
          top: 160 * scale,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
        }}
      >
        <div
          style={{
            backgroundColor: "rgba(0,0,0,0.5)",
            borderRadius: 40 * scale,
            padding: `${12 * scale}px ${32 * scale}px`,
            fontSize: 32 * scale,
            color: "#FFF",
            fontWeight: 600,
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          @{config.reviewerName}
        </div>
      </div>

      {/* 리뷰 캡션 (중앙) */}
      <div
        style={{
          position: "absolute",
          top: "30%",
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 24 * scale,
        }}
      >
        {lines.map((line, i) => {
          const appear = lineAppearFrames[i];
          // 하드 컷: 프레임 도달 시 즉시 100% 표시
          if (frame < appear) return null;

          return (
            <div key={i} style={captionStyle}>
              {renderHighlightedText(line)}
            </div>
          );
        })}
      </div>

      {/* 별점 (하단) */}
      {config.rating !== undefined && frame >= ratingAppearFrame && (
        <div
          style={{
            position: "absolute",
            bottom: config.ctaText ? 280 * scale : 200 * scale,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            gap: 8 * scale,
          }}
        >
          {Array.from({ length: 5 }, (_, i) => (
            <span
              key={i}
              style={{
                fontSize: 60 * scale,
                filter:
                  i < Math.floor(config.rating!)
                    ? "none"
                    : "grayscale(1) opacity(0.3)",
              }}
            >
              ⭐
            </span>
          ))}
        </div>
      )}

      {/* CTA */}
      {config.ctaText && (
        <Sequence from={Math.round(ratingAppearFrame + fps * 0.5)}>
          <div
            style={{
              position: "absolute",
              bottom: 120 * scale,
              left: 60 * scale,
              right: 60 * scale,
              backgroundColor: "#000",
              borderRadius: 16 * scale,
              padding: `${24 * scale}px`,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              border: `4px solid #FFF`,
            }}
          >
            <span
              style={{
                color: "#FFF",
                fontSize: 40 * scale,
                fontWeight: 800,
                fontFamily: "system-ui, -apple-system, sans-serif",
                letterSpacing: 1,
              }}
            >
              {config.ctaText}
            </span>
          </div>
        </Sequence>
      )}

      {/* 셀카캠 REC 표시 */}
      <div
        style={{
          position: "absolute",
          top: 100 * scale,
          right: 40 * scale,
          display: "flex",
          alignItems: "center",
          gap: 8 * scale,
          opacity: Math.floor(frame / (fps * 0.5)) % 2 === 0 ? 1 : 0.3,
        }}
      >
        <div
          style={{
            width: 16 * scale,
            height: 16 * scale,
            borderRadius: "50%",
            backgroundColor: "#FF0000",
          }}
        />
        <span
          style={{
            fontSize: 24 * scale,
            color: "#FFF",
            fontWeight: 700,
            fontFamily: "monospace",
          }}
        >
          REC
        </span>
      </div>
    </AbsoluteFill>
  );
};
