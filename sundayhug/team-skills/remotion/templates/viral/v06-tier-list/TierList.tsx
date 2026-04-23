import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Sequence,
} from "remotion";

import type { TierListConfig, Tier } from "./types";
import { TierGrid } from "./components/TierGrid";
import { TierItem } from "./components/TierItem";

const TIER_ORDER: Tier[] = ["S", "A", "B", "C", "F"];

/**
 * V06 - Tier List / Ranking
 *
 * S/A/B/C/F 티어 그리드에 아이템을 하나씩 배치하는
 * B급 감성 랭킹 영상 템플릿.
 *
 * - 타이틀 하드컷 등장
 * - 빈 티어 그리드 표시
 * - 아이템이 오른쪽에서 슬라이드 인
 * - 브랜드 제품은 S티어 + 글로우/펄스
 *
 * @example
 * ```tsx
 * <Composition
 *   id="TierListAd"
 *   component={TierList}
 *   durationInFrames={30 * 25}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       title: "육아용품 티어표",
 *       items: [
 *         { name: "우리 브랜드", tier: "S", delay: 2 },
 *         { name: "A사 제품", tier: "B", delay: 4 },
 *         { name: "B사 제품", tier: "C", delay: 6 },
 *       ],
 *       brandHighlight: "우리 브랜드",
 *     },
 *   }}
 * />
 * ```
 */
export const TierList: React.FC<{ config: TierListConfig }> = ({ config }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const bgColor = config.bgColor ?? "#1a1a2e";

  // 타이틀: 하드컷 등장 (프레임 0에서 바로)
  const titleOpacity = interpolate(frame, [0, 2], [0, 1], {
    extrapolateRight: "clamp",
  });

  // 아이템별 티어 내 인덱스 계산
  const tierCounts: Record<Tier, number> = { S: 0, A: 0, B: 0, C: 0, F: 0 };

  const itemsWithMeta = config.items.map((item) => {
    const indexInTier = tierCounts[item.tier];
    tierCounts[item.tier]++;
    return {
      ...item,
      indexInTier,
      tierRowIndex: TIER_ORDER.indexOf(item.tier),
      enterFrame: Math.round((item.delay ?? 0) * fps),
    };
  });

  // 그리드 등장: 타이틀 후 1초
  const gridStartFrame = fps * 1;

  return (
    <AbsoluteFill style={{ backgroundColor: bgColor }}>
      {/* 타이틀 */}
      <div
        style={{
          position: "absolute",
          top: 80,
          left: 0,
          right: 0,
          textAlign: "center",
          opacity: titleOpacity,
        }}
      >
        <h1
          style={{
            fontSize: 64,
            fontWeight: 900,
            color: "#fff",
            fontFamily: "Impact, Arial Black, sans-serif",
            margin: 0,
            textTransform: "uppercase",
            letterSpacing: 4,
            textShadow: "0 4px 12px rgba(0,0,0,0.5)",
          }}
        >
          {config.title}
        </h1>
      </div>

      {/* 티어 그리드 + 아이템 */}
      <Sequence from={gridStartFrame} layout="none">
        <TierGrid>
          {itemsWithMeta.map((item, i) => (
            <TierItem
              key={i}
              name={item.name}
              imageSrc={item.imageSrc}
              tier={item.tier}
              enterFrame={item.enterFrame}
              isHighlight={config.brandHighlight === item.name}
              indexInTier={item.indexInTier}
              tierRowIndex={item.tierRowIndex}
            />
          ))}
        </TierGrid>
      </Sequence>

      {/* CTA */}
      {config.ctaText && (
        <Sequence
          from={Math.round(
            gridStartFrame +
              Math.max(...config.items.map((i) => (i.delay ?? 0) * fps)) +
              fps * 2,
          )}
          layout="none"
        >
          <div
            style={{
              position: "absolute",
              bottom: 120,
              left: 0,
              right: 0,
              textAlign: "center",
              opacity: interpolate(
                frame -
                  gridStartFrame -
                  Math.max(
                    ...config.items.map((i) => (i.delay ?? 0) * fps),
                  ) -
                  fps * 2,
                [0, fps * 0.3],
                [0, 1],
                { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
              ),
            }}
          >
            <span
              style={{
                fontSize: 36,
                fontWeight: 800,
                color: "#FFD700",
                fontFamily: "Arial Black, sans-serif",
                textShadow: "0 2px 8px rgba(0,0,0,0.6)",
              }}
            >
              {config.ctaText}
            </span>
          </div>
        </Sequence>
      )}
    </AbsoluteFill>
  );
};
