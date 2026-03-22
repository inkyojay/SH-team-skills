import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";
import { FONT, MOTION } from "../utils/brand";

/**
 * 숫자 카운트업 애니메이션 컴포넌트
 *
 * 0에서 목표값까지 spring 기반으로 부드럽게 카운트합니다.
 */
export const CountUp: React.FC<{
  /** 목표 숫자 */
  target: number;
  /** 숫자 뒤에 붙는 접미사 (예: "+", "%", "만") */
  suffix?: string;
  /** 숫자 앞에 붙는 접두사 (예: "★", "₩") */
  prefix?: string;
  /** 소수점 자릿수 (기본 0) */
  decimals?: number;
  /** 폰트 크기 (기본 96) */
  fontSize?: number;
  /** 텍스트 색상 */
  color?: string;
  /** 등장 딜레이 (프레임) */
  delay?: number;
}> = ({
  target,
  suffix = "",
  prefix = "",
  decimals = 0,
  fontSize = 96,
  color = "#333",
  delay = 0,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    frame: frame - delay,
    fps,
    config: { ...MOTION.spring, mass: 0.8 },
  });

  const currentValue = interpolate(progress, [0, 1], [0, target]);
  const opacity = interpolate(progress, [0, 0.3], [0, 1], {
    extrapolateRight: "clamp",
  });
  const scale = interpolate(progress, [0, 1], [0.8, 1]);

  const displayValue =
    decimals > 0
      ? currentValue.toFixed(decimals)
      : Math.round(currentValue).toLocaleString();

  return (
    <div
      style={{
        display: "flex",
        alignItems: "baseline",
        justifyContent: "center",
        opacity,
        transform: `scale(${scale})`,
      }}
    >
      {prefix && (
        <span
          style={{
            fontSize: fontSize * 0.6,
            fontWeight: 700,
            color,
            fontFamily: FONT.body,
            marginRight: 8,
          }}
        >
          {prefix}
        </span>
      )}
      <span
        style={{
          fontSize,
          fontWeight: 900,
          color,
          fontFamily: FONT.english,
          letterSpacing: -2,
        }}
      >
        {displayValue}
      </span>
      {suffix && (
        <span
          style={{
            fontSize: fontSize * 0.5,
            fontWeight: 700,
            color,
            fontFamily: FONT.body,
            marginLeft: 4,
          }}
        >
          {suffix}
        </span>
      )}
    </div>
  );
};
