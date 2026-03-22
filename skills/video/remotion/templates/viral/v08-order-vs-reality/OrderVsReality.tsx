import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  Sequence,
  Img,
} from "remotion";

import type { OrderVsRealityConfig } from "./types";

/**
 * V08 - Order vs Reality
 *
 * "주문한 것" 스크린샷 → 드라마틱 트랜지션 → "받은 것" 리빌.
 * isMatch=true면 초록 체크 + 신뢰 메시지,
 * isMatch=false면 빨간 X + 코미디 리액션.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="OrderVsRealityAd"
 *   component={OrderVsReality}
 *   durationInFrames={30 * 15}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       orderImageSrc: "order-screenshot.png",
 *       realityImageSrc: "real-product.png",
 *       productName: "실키밤부 슬리핑백",
 *       isMatch: true,
 *       caption: "기대 = 현실 그 자체",
 *     },
 *   }}
 * />
 * ```
 */
export const OrderVsReality: React.FC<{
  config: OrderVsRealityConfig;
}> = ({ config }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const orderLabel = config.orderLabel ?? "주문한 것";
  const realityLabel = config.realityLabel ?? "받은 것";
  const realityImage = config.realityImageSrc ?? config.orderImageSrc;

  // 타이밍
  const orderHoldFrames = Math.round(fps * 3); // 주문 이미지 3초
  const transitionFrames = Math.round(fps * 0.5); // 트랜지션 0.5초
  const revealStart = orderHoldFrames + transitionFrames;
  const resultDelay = Math.round(fps * 1.5); // 리빌 후 1.5초에 결과

  // ─── Phase 1: "주문한 것" ───
  const orderOpacity = interpolate(frame, [0, 3], [0, 1], {
    extrapolateRight: "clamp",
  });

  // ─── Phase 2: 드라마틱 트랜지션 (줌 + 스핀 + 플래시) ───
  const transitionProgress = interpolate(
    frame,
    [orderHoldFrames, orderHoldFrames + transitionFrames],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
  const transitionScale = interpolate(transitionProgress, [0, 0.5, 1], [1, 3, 1]);
  const transitionRotation = interpolate(transitionProgress, [0, 1], [0, 360]);
  const flashOpacity = interpolate(
    transitionProgress,
    [0, 0.3, 0.5, 0.8, 1],
    [0, 0.9, 1, 0.9, 0],
  );

  // ─── Phase 3: "받은 것" 리빌 ───
  const revealProgress = spring({
    frame: frame - revealStart,
    fps,
    config: { damping: 12, stiffness: 100 },
  });

  // ─── Phase 4: 결과 (체크 or X) ───
  const resultFrame = revealStart + resultDelay;
  const resultProgress = spring({
    frame: frame - resultFrame,
    fps,
    config: { damping: 8, stiffness: 120, mass: 0.6 },
  });
  const resultScale = interpolate(resultProgress, [0, 1], [0, 1]);

  // 밈 스타일 텍스트 (Impact, 흰 글씨 + 검은 외곽선)
  const memeTextStyle: React.CSSProperties = {
    fontSize: 64,
    fontWeight: 900,
    fontFamily: "Impact, Arial Black, sans-serif",
    color: "#fff",
    textTransform: "uppercase",
    WebkitTextStroke: "3px #000",
    textShadow: "4px 4px 0 #000, -2px -2px 0 #000, 2px -2px 0 #000, -2px 2px 0 #000",
    letterSpacing: 3,
    textAlign: "center" as const,
  };

  return (
    <AbsoluteFill style={{ backgroundColor: "#111" }}>
      {/* Phase 1: 주문한 것 */}
      <Sequence durationInFrames={orderHoldFrames + transitionFrames} layout="none">
        <AbsoluteFill
          style={{
            opacity: orderOpacity,
            transform:
              frame >= orderHoldFrames
                ? `scale(${transitionScale}) rotate(${transitionRotation}deg)`
                : undefined,
          }}
        >
          {/* 라벨 */}
          <div
            style={{
              position: "absolute",
              top: 160,
              left: 0,
              right: 0,
              zIndex: 5,
              textAlign: "center",
            }}
          >
            <span style={memeTextStyle}>{orderLabel}</span>
          </div>

          {/* 이미지 */}
          <div
            style={{
              position: "absolute",
              top: 300,
              left: 60,
              right: 60,
              bottom: 300,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Img
              src={config.orderImageSrc}
              style={{
                maxWidth: "100%",
                maxHeight: "100%",
                objectFit: "contain",
                borderRadius: 16,
                border: "4px solid #333",
              }}
            />
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* 트랜지션 플래시 */}
      {frame >= orderHoldFrames && frame < revealStart && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundColor: "#fff",
            opacity: flashOpacity,
            zIndex: 100,
          }}
        />
      )}

      {/* Phase 3: 받은 것 리빌 */}
      <Sequence from={revealStart} layout="none">
        <AbsoluteFill
          style={{
            opacity: interpolate(revealProgress, [0, 0.3], [0, 1], {
              extrapolateRight: "clamp",
            }),
          }}
        >
          {/* 라벨 */}
          <div
            style={{
              position: "absolute",
              top: 160,
              left: 0,
              right: 0,
              zIndex: 5,
              textAlign: "center",
            }}
          >
            <span style={memeTextStyle}>{realityLabel}</span>
          </div>

          {/* 이미지 */}
          <div
            style={{
              position: "absolute",
              top: 300,
              left: 60,
              right: 60,
              bottom: 300,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Img
              src={realityImage}
              style={{
                maxWidth: "100%",
                maxHeight: "100%",
                objectFit: "contain",
                borderRadius: 16,
                border: `4px solid ${config.isMatch ? "#4CAF50" : "#F44336"}`,
              }}
            />
          </div>

          {/* 결과: 체크 or X */}
          {frame >= resultFrame && (
            <div
              style={{
                position: "absolute",
                bottom: 200,
                left: 0,
                right: 0,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 16,
                transform: `scale(${resultScale})`,
              }}
            >
              {/* 아이콘 */}
              <div
                style={{
                  width: 100,
                  height: 100,
                  borderRadius: "50%",
                  backgroundColor: config.isMatch ? "#4CAF50" : "#F44336",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: `0 0 30px ${config.isMatch ? "#4CAF50" : "#F44336"}80`,
                }}
              >
                <span
                  style={{
                    fontSize: 56,
                    fontWeight: 900,
                    color: "#fff",
                    lineHeight: 1,
                  }}
                >
                  {config.isMatch ? "\u2713" : "\u2717"}
                </span>
              </div>

              {/* 텍스트 */}
              <span
                style={{
                  fontSize: 44,
                  fontWeight: 800,
                  color: config.isMatch ? "#4CAF50" : "#F44336",
                  fontFamily: "Arial Black, sans-serif",
                  textShadow: "0 2px 8px rgba(0,0,0,0.6)",
                  textAlign: "center",
                  padding: "0 40px",
                }}
              >
                {config.isMatch
                  ? config.caption ?? "\u2713 \uae30\ub300 = \ud604\uc2e4"
                  : config.caption ?? "\u2717 \uae30\ub300 \u2260 \ud604\uc2e4"}
              </span>

              {/* 제품명 */}
              <span
                style={{
                  fontSize: 28,
                  fontWeight: 600,
                  color: "#aaa",
                  fontFamily: "Arial, sans-serif",
                }}
              >
                {config.productName}
              </span>
            </div>
          )}
        </AbsoluteFill>
      </Sequence>
    </AbsoluteFill>
  );
};
