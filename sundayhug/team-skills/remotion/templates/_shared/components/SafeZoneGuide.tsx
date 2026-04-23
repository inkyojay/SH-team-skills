import React from "react";
import { AbsoluteFill, useVideoConfig } from "remotion";
import type { VideoFormat } from "../types/common";
import { FORMAT_SPECS } from "../types/common";

/**
 * 세이프존 가이드 오버레이 (개발용)
 *
 * 릴스 세이프존(상단 14%, 하단 35%)을 시각화합니다.
 * 프로덕션 빌드에서는 제거하세요.
 */
export const SafeZoneGuide: React.FC<{
  format?: VideoFormat;
  /** 가이드 표시 여부 (기본 true) */
  visible?: boolean;
}> = ({ format = "reels", visible = true }) => {
  const { height } = useVideoConfig();

  if (!visible) return null;

  const spec = FORMAT_SPECS[format];
  const topPct = spec.safeZone?.top ?? 0;
  const bottomPct = spec.safeZone?.bottom ?? 0;

  if (topPct === 0 && bottomPct === 0) return null;

  const guideStyle: React.CSSProperties = {
    position: "absolute",
    left: 0,
    right: 0,
    background: "rgba(255,0,0,0.12)",
    borderStyle: "dashed",
    borderColor: "rgba(255,0,0,0.4)",
    borderWidth: 0,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontSize: 18,
    color: "rgba(255,0,0,0.5)",
    fontFamily: "monospace",
    pointerEvents: "none",
  };

  return (
    <AbsoluteFill style={{ pointerEvents: "none", zIndex: 999 }}>
      {topPct > 0 && (
        <div
          style={{
            ...guideStyle,
            top: 0,
            height: `${topPct}%`,
            borderBottomWidth: 2,
          }}
        >
          SAFE ZONE TOP {topPct}%
        </div>
      )}
      {bottomPct > 0 && (
        <div
          style={{
            ...guideStyle,
            bottom: 0,
            height: `${bottomPct}%`,
            borderTopWidth: 2,
          }}
        >
          SAFE ZONE BOTTOM {bottomPct}%
        </div>
      )}
    </AbsoluteFill>
  );
};
