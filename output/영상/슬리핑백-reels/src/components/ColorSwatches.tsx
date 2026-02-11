import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
} from "remotion";

const COLORS = [
  { name: "화이트 크림", hex: "#FFF8F0" },
  { name: "오트 베이지", hex: "#D4C5A9" },
  { name: "베이비 핑크", hex: "#F4C2C2" },
  { name: "제이드 그린", hex: "#7DB9A0" },
  { name: "클라우드 블루", hex: "#A8C4E0" },
  { name: "블룸 라벤더", hex: "#B39DDB" },
];

/**
 * 6가지 컬러 스와치 쇼케이스
 * 순차적 등장 애니메이션
 */
export const ColorSwatches: React.FC<{
  highlightIndex?: number;
  showLabels?: boolean;
}> = ({ highlightIndex, showLabels = false }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

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
        padding: "0 80px",
      }}
    >
      {/* 2x3 그리드 */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: 24,
          justifyContent: "center",
          maxWidth: 700,
        }}
      >
        {COLORS.map((color, i) => {
          const delay = i * 4; // 각 컬러 4프레임 간격 순차 등장
          const s = spring({
            frame: frame - delay,
            fps,
            config: { damping: 10, stiffness: 200 },
          });
          const scale = interpolate(s, [0, 1], [0, 1]);
          const isHighlighted = highlightIndex === i;

          return (
            <div
              key={color.name}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 8,
                transform: `scale(${scale})`,
              }}
            >
              <div
                style={{
                  width: isHighlighted ? 160 : 140,
                  height: isHighlighted ? 160 : 140,
                  borderRadius: "50%",
                  backgroundColor: color.hex,
                  border: isHighlighted
                    ? "5px solid #fff"
                    : "3px solid rgba(255,255,255,0.6)",
                  boxShadow: isHighlighted
                    ? `0 0 30px ${color.hex}80, 0 4px 16px rgba(0,0,0,0.2)`
                    : "0 4px 12px rgba(0,0,0,0.15)",
                  transition: "all 0.3s",
                }}
              />
              {showLabels && (
                <span
                  style={{
                    fontSize: 22,
                    fontWeight: 600,
                    color: isHighlighted ? "#fff" : "rgba(255,255,255,0.8)",
                    fontFamily:
                      "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                    textShadow: "0 1px 4px rgba(0,0,0,0.5)",
                  }}
                >
                  {color.name}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
