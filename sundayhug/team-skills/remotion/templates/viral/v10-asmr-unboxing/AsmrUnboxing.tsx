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

import type { AsmrUnboxingConfig } from "./types";
import { UnboxLayer } from "./components/UnboxLayer";

/**
 * V10 - ASMR Unboxing
 *
 * 클로즈업 제품 샷을 느린 줌인으로 보여주는
 * ASMR 스타일 언박싱 영상. 미니멀 텍스트, 프리미엄 감성.
 *
 * - 각 레이어: 느린 줌인(1→1.05) + 소프트 페이드
 * - 최종 리빌: 뷰티샷 + 은은한 글로우
 * - 텍스트: 최소한, 제품명만 마지막에 표시
 *
 * @example
 * ```tsx
 * <Composition
 *   id="AsmrUnboxingAd"
 *   component={AsmrUnboxing}
 *   durationInFrames={30 * 20}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       layers: [
 *         { mediaSrc: "box-closeup.jpg", label: "unboxing", durationSeconds: 5 },
 *         { mediaSrc: "tissue-paper.jpg", durationSeconds: 4 },
 *         { mediaSrc: "product-reveal.jpg", label: "reveal", durationSeconds: 5 },
 *       ],
 *       productName: "실키밤부 슬리핑백",
 *       finalRevealSrc: "beauty-shot.jpg",
 *     },
 *   }}
 * />
 * ```
 */
export const AsmrUnboxing: React.FC<{
  config: AsmrUnboxingConfig;
}> = ({ config }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgColor = config.bgColor ?? "#0a0a0a";
  const warmIntensity = config.warmOverlayIntensity ?? 0.15;
  const fadeFrames = Math.round(fps * 0.8); // 소프트 페이드 0.8초

  // 레이어 시작 프레임 계산
  let accumulated = 0;
  const layerTimings = config.layers.map((layer) => {
    const start = accumulated;
    const duration = Math.round(layer.durationSeconds * fps);
    accumulated += duration;
    return { start, duration };
  });

  // 최종 리빌 시작 프레임
  const finalStart = accumulated;
  const finalDuration = Math.round(fps * 4); // 4초

  // 제품명 등장 (최종 리빌 1.5초 후)
  const nameDelay = finalStart + Math.round(fps * 1.5);
  const nameSpring = spring({
    frame: frame - nameDelay,
    fps,
    config: { damping: 20, stiffness: 100, mass: 0.8 },
  });
  const nameOpacity = interpolate(nameSpring, [0, 0.5], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor }}>
      {/* 언박싱 레이어 */}
      {config.layers.map((layer, i) => (
        <Sequence
          key={i}
          from={layerTimings[i].start}
          durationInFrames={layerTimings[i].duration}
          layout="none"
        >
          <AbsoluteFill>
            <UnboxLayer
              mediaSrc={layer.mediaSrc}
              label={layer.label}
              fadeInFrames={i === 0 ? 6 : fadeFrames}
            />
          </AbsoluteFill>
        </Sequence>
      ))}

      {/* 최종 리빌 (뷰티샷) */}
      {config.finalRevealSrc && (
        <Sequence
          from={finalStart}
          durationInFrames={finalDuration}
          layout="none"
        >
          <AbsoluteFill>
            {/* 이미지 */}
            <Img
              src={config.finalRevealSrc}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                opacity: interpolate(
                  frame - finalStart,
                  [0, fadeFrames],
                  [0, 1],
                  { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
                ),
              }}
            />

            {/* 글로우 효과 */}
            <div
              style={{
                position: "absolute",
                inset: 0,
                background:
                  "radial-gradient(ellipse at center, rgba(255,235,200,0.15) 0%, transparent 70%)",
                opacity: interpolate(
                  frame - finalStart,
                  [fadeFrames, fadeFrames + fps],
                  [0, 1],
                  { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
                ),
              }}
            />
          </AbsoluteFill>
        </Sequence>
      )}

      {/* 워밍 오버레이 (전체 영상) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundColor: `rgba(255, 180, 100, ${warmIntensity})`,
          mixBlendMode: "multiply",
          pointerEvents: "none",
        }}
      />

      {/* 하단 그라데이션 */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 400,
          background:
            "linear-gradient(transparent, rgba(0,0,0,0.6))",
          pointerEvents: "none",
        }}
      />

      {/* 제품명 (마지막에 등장, 미니멀) */}
      <div
        style={{
          position: "absolute",
          bottom: 160,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: nameOpacity,
        }}
      >
        <h2
          style={{
            fontSize: 36,
            fontWeight: 300,
            color: "rgba(255,255,255,0.9)",
            fontFamily: "'Helvetica Neue', Arial, sans-serif",
            letterSpacing: 6,
            margin: 0,
            textTransform: "uppercase",
          }}
        >
          {config.productName}
        </h2>
      </div>

      {/* 브랜드명 (좌하단, 매우 작고 절제) */}
      {config.brandName && (
        <div
          style={{
            position: "absolute",
            bottom: 80,
            left: 60,
            opacity: interpolate(
              frame - nameDelay - Math.round(fps * 0.5),
              [0, fps * 0.3],
              [0, 0.4],
              { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
            ),
          }}
        >
          <span
            style={{
              fontSize: 16,
              fontWeight: 300,
              color: "rgba(255,255,255,0.5)",
              fontFamily: "'Helvetica Neue', Arial, sans-serif",
              letterSpacing: 3,
            }}
          >
            {config.brandName}
          </span>
        </div>
      )}
    </AbsoluteFill>
  );
};
