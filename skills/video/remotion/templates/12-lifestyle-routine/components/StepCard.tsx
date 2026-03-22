import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { VideoClip } from "../../_shared/components/VideoClip";
import { FONT, MOTION } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";
import type { RoutineStep } from "../types";

/**
 * 루틴 스텝 카드
 *
 * 스텝 번호 팝인 + 타임라인 연결선 + 타이틀 슬라이드 + 프로그레스 닷
 */
export const StepCard: React.FC<{
  step: RoutineStep;
  totalSteps: number;
  palette?: string;
  brandColor?: string;
}> = ({ step, totalSteps, palette, brandColor }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const pal = getPalette(palette);
  const accent = brandColor ?? pal.accent;

  // 스텝 번호 팝인
  const numberIn = spring({
    frame: frame - 3,
    fps,
    config: MOTION.springSnappy,
  });

  // 타이틀 등장
  const titleIn = spring({
    frame: frame - 10,
    fps,
    config: MOTION.spring,
  });

  // 설명 등장
  const descIn = spring({
    frame: frame - 18,
    fps,
    config: MOTION.springGentle,
  });

  // 타임라인 연결선
  const lineIn = spring({
    frame: frame - 6,
    fps,
    config: MOTION.springGentle,
  });

  // 시간 라벨
  const timeIn = spring({
    frame: frame - 5,
    fps,
    config: MOTION.spring,
  });

  return (
    <AbsoluteFill>
      <VideoClip
        src={step.mediaSrc}
        startFrom={step.videoStartFrom}
        overlayStyle={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0.15) 40%, rgba(0,0,0,0.65) 100%)",
        }}
      />

      {/* 시간 라벨 (좌상단) */}
      {step.timeLabel && (
        <div
          style={{
            position: "absolute",
            top: 300,
            left: 50,
            opacity: interpolate(timeIn, [0, 1], [0, 1]),
            transform: `translateX(${interpolate(timeIn, [0, 1], [-20, 0])}px)`,
          }}
        >
          <div
            style={{
              background: "rgba(0,0,0,0.4)",
              borderRadius: 16,
              padding: "8px 20px",
              backdropFilter: "blur(8px)",
            }}
          >
            <span
              style={{
                fontSize: 24,
                fontWeight: 600,
                color: "#fff",
                fontFamily: FONT.english,
                letterSpacing: 2,
              }}
            >
              {step.timeLabel}
            </span>
          </div>
        </div>
      )}

      {/* 스텝 번호 (대형 원형 배지) */}
      <div
        style={{
          position: "absolute",
          bottom: 520,
          left: 60,
          opacity: interpolate(numberIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(numberIn, [0, 1], [0, 1])})`,
        }}
      >
        <div
          style={{
            width: 80,
            height: 80,
            borderRadius: "50%",
            background: accent,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: `0 4px 16px ${accent}60`,
          }}
        >
          <span
            style={{
              fontSize: 36,
              fontWeight: 900,
              color: "#fff",
              fontFamily: FONT.english,
            }}
          >
            {step.stepNumber}
          </span>
        </div>
      </div>

      {/* 타임라인 연결선 (스텝 번호 아래로 연장) */}
      {step.stepNumber < totalSteps && (
        <div
          style={{
            position: "absolute",
            bottom: 440,
            left: 99, // 스텝 번호 원 중앙 (left:60 + width:80/2 - lineWidth:2/2)
            width: 3,
            height: interpolate(lineIn, [0, 1], [0, 80]),
            background: `linear-gradient(180deg, ${accent}, ${accent}40)`,
            borderRadius: 2,
            opacity: interpolate(lineIn, [0, 1], [0, 0.7]),
          }}
        />
      )}

      {/* 타이틀 */}
      <div
        style={{
          position: "absolute",
          bottom: 420,
          left: 60,
          right: 60,
          opacity: interpolate(titleIn, [0, 1], [0, 1]),
          transform: `translateY(${interpolate(titleIn, [0, 1], [20, 0])}px)`,
        }}
      >
        <p
          style={{
            fontSize: 52,
            fontWeight: 800,
            color: "#fff",
            fontFamily: FONT.body,
            margin: 0,
            textShadow: "0 4px 16px rgba(0,0,0,0.6)",
          }}
        >
          {step.title}
        </p>
      </div>

      {/* 설명 */}
      {step.description && (
        <div
          style={{
            position: "absolute",
            bottom: 360,
            left: 60,
            right: 60,
            opacity: interpolate(descIn, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(descIn, [0, 1], [10, 0])}px)`,
          }}
        >
          <p
            style={{
              fontSize: 30,
              fontWeight: 400,
              color: "rgba(255,255,255,0.85)",
              fontFamily: FONT.body,
              margin: 0,
              textShadow: "0 2px 8px rgba(0,0,0,0.5)",
            }}
          >
            {step.description}
          </p>
        </div>
      )}

      {/* 프로그레스 닷 */}
      <div
        style={{
          position: "absolute",
          bottom: 300,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          gap: 12,
        }}
      >
        {Array.from({ length: totalSteps }, (_, i) => {
          const isActive = i + 1 === step.stepNumber;
          const isPast = i + 1 < step.stepNumber;

          const dotIn = spring({
            frame: frame - 25 - i * 2,
            fps,
            config: MOTION.spring,
          });

          return (
            <div
              key={i}
              style={{
                width: isActive ? 32 : 12,
                height: 12,
                borderRadius: 6,
                background: isActive
                  ? accent
                  : isPast
                    ? "rgba(255,255,255,0.7)"
                    : "rgba(255,255,255,0.3)",
                opacity: interpolate(dotIn, [0, 1], [0, 1]),
                transition: "width 0.3s",
              }}
            />
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
