import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Sequence,
} from "remotion";

import type { CountdownConfig } from "./types";
import { CountdownCard } from "./components/CountdownCard";

/**
 * V07 - Countdown Listicle
 *
 * "이걸 안 쓰는 3가지 이유" 스타일 역순 카운트다운.
 * 각 항목이 큰 숫자 줌인 + 텍스트 슬라이드업으로 등장하며,
 * #1은 플래시 + 더 큰 텍스트 + 긴 홀드로 드라마틱하게 연출.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="CountdownAd"
 *   component={Countdown}
 *   durationInFrames={30 * 20}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       title: "이걸 안 쓰는 3가지 이유",
 *       items: [
 *         { number: 3, text: "매일 밤 아기가 깬다" },
 *         { number: 2, text: "기저귀 갈기가 불편하다" },
 *         { number: 1, text: "실크보다 부드러운 촉감을 모른다" },
 *       ],
 *       ctaText: "지금 바로 체험하세요",
 *     },
 *   }}
 * />
 * ```
 */
export const Countdown: React.FC<{ config: CountdownConfig }> = ({
  config,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgColor = config.bgColor ?? "#0d0d0d";
  const itemDuration = config.itemDurationSeconds ?? 4;
  const titleDurationFrames = Math.round(fps * 2.5);
  const itemDurationFrames = Math.round(itemDuration * fps);

  // #1 아이템은 1.5배 길게
  const sortedItems = [...config.items].sort(
    (a, b) => b.number - a.number,
  );
  const isTopItem = (item: (typeof sortedItems)[0]) =>
    item.number ===
    Math.min(...config.items.map((i) => i.number));

  // 타이틀 하드컷
  const titleOpacity = interpolate(frame, [0, 2], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 큰 숫자 표시 (타이틀의 숫자)
  const maxNumber = Math.max(...config.items.map((i) => i.number));

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor }}>
      {/* 타이틀 카드 */}
      <Sequence durationInFrames={titleDurationFrames} layout="none">
        <AbsoluteFill
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            opacity: titleOpacity,
          }}
        >
          {/* 배경 큰 숫자 */}
          <span
            style={{
              position: "absolute",
              fontSize: 500,
              fontWeight: 900,
              fontFamily: "Impact, sans-serif",
              color: "rgba(255,255,255,0.06)",
              lineHeight: 1,
            }}
          >
            {maxNumber}
          </span>

          {/* 타이틀 텍스트 */}
          <h1
            style={{
              fontSize: 56,
              fontWeight: 900,
              color: "#fff",
              fontFamily: "Arial Black, sans-serif",
              textAlign: "center",
              padding: "0 60px",
              lineHeight: 1.4,
              margin: 0,
              zIndex: 2,
              textShadow: "0 4px 16px rgba(0,0,0,0.6)",
            }}
          >
            {config.title}
          </h1>
        </AbsoluteFill>
      </Sequence>

      {/* 카운트다운 아이템 */}
      {sortedItems.map((item, i) => {
        const isTop = isTopItem(item);
        const duration = isTop
          ? Math.round(itemDurationFrames * 1.5)
          : itemDurationFrames;
        const startFrame =
          titleDurationFrames + i * itemDurationFrames;

        return (
          <Sequence
            key={item.number}
            from={startFrame}
            durationInFrames={duration}
            layout="none"
          >
            <AbsoluteFill style={{ backgroundColor: bgColor }}>
              <CountdownCard
                number={item.number}
                text={item.text}
                mediaSrc={item.mediaSrc}
                isTop={isTop}
                numberColor={config.numberColor}
              />
            </AbsoluteFill>
          </Sequence>
        );
      })}

      {/* CTA */}
      {config.ctaText && (() => {
        const ctaStart =
          titleDurationFrames +
          sortedItems.reduce((sum, item, i) => {
            const isTop = isTopItem(item);
            return (
              sum +
              (i < sortedItems.length - 1
                ? itemDurationFrames
                : isTop
                  ? Math.round(itemDurationFrames * 1.5)
                  : itemDurationFrames)
            );
          }, 0);
        const ctaOpacity = interpolate(
          frame - ctaStart,
          [0, fps * 0.3],
          [0, 1],
          { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
        );

        return (
          <Sequence from={ctaStart} layout="none">
            <AbsoluteFill
              style={{
                backgroundColor: bgColor,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                opacity: ctaOpacity,
              }}
            >
              <span
                style={{
                  fontSize: 48,
                  fontWeight: 800,
                  color: "#FFE66D",
                  fontFamily: "Arial Black, sans-serif",
                  textAlign: "center",
                  padding: "0 60px",
                  textShadow: "0 2px 12px rgba(0,0,0,0.6)",
                }}
              >
                {config.ctaText}
              </span>
            </AbsoluteFill>
          </Sequence>
        );
      })()}
    </AbsoluteFill>
  );
};
