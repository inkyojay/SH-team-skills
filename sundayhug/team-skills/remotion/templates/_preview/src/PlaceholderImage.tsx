import React from "react";
import { AbsoluteFill } from "remotion";

/**
 * 플레이스홀더 이미지 컴포넌트
 *
 * 템플릿 프리뷰에서 실제 이미지/비디오 대신 사용합니다.
 * public/ 폴더에 파일이 없어도 프리뷰가 동작하도록 합니다.
 */
export const PlaceholderImage: React.FC<{
  label?: string;
  bgColor?: string;
  emoji?: string;
}> = ({ label = "Placeholder", bgColor = "#E8DDD0", emoji = "📷" }) => {
  return (
    <AbsoluteFill
      style={{
        background: `linear-gradient(135deg, ${bgColor} 0%, ${adjustColor(bgColor, -20)} 100%)`,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        gap: 20,
      }}
    >
      <span style={{ fontSize: 80 }}>{emoji}</span>
      <span
        style={{
          fontSize: 28,
          fontWeight: 600,
          color: "rgba(0,0,0,0.3)",
          fontFamily: "system-ui, sans-serif",
          letterSpacing: 2,
        }}
      >
        {label}
      </span>
    </AbsoluteFill>
  );
};

function adjustColor(hex: string, amount: number): string {
  const num = parseInt(hex.replace("#", ""), 16);
  const r = Math.min(255, Math.max(0, ((num >> 16) & 0xff) + amount));
  const g = Math.min(255, Math.max(0, ((num >> 8) & 0xff) + amount));
  const b = Math.min(255, Math.max(0, (num & 0xff) + amount));
  return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, "0")}`;
}
