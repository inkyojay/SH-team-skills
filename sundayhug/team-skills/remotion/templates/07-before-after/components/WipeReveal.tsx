import React from "react";
import {
  AbsoluteFill,
  Img,
  Video,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { FONT, MOTION, BRAND } from "../../_shared/utils/brand";
import { getPalette } from "../../_shared/utils/palettes";

/**
 * clipPath Wipe 리빌 컴포넌트
 *
 * Before(채도 낮음) → After(풀 채도)를 clipPath로 슬라이드 전환합니다.
 */

const IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp", ".gif"];
const isImage = (src: string) =>
  IMAGE_EXTS.some((ext) => src.toLowerCase().endsWith(ext));

const Media: React.FC<{
  src: string;
  style?: React.CSSProperties;
}> = ({ src, style }) => {
  const { fps } = useVideoConfig();
  const baseStyle: React.CSSProperties = {
    width: "100%",
    height: "100%",
    objectFit: "cover",
    ...style,
  };
  return isImage(src) ? (
    <Img src={staticFile(src)} style={baseStyle} />
  ) : (
    <Video src={staticFile(src)} style={baseStyle} muted />
  );
};

export const WipeReveal: React.FC<{
  beforeSrc: string;
  afterSrc: string;
  beforeLabel?: string;
  afterLabel?: string;
  caption?: string;
  wipeDirection?: "horizontal" | "vertical";
  palette?: string;
  brandColor?: string;
}> = ({
  beforeSrc,
  afterSrc,
  beforeLabel = "BEFORE",
  afterLabel = "AFTER",
  caption,
  wipeDirection = "horizontal",
  palette,
  brandColor,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();
  const pal = getPalette(palette);
  const accent = brandColor ?? pal.accent;

  // wipe 진행: 처음 1초는 Before만, 이후 wipe
  const wipeStart = 30; // 1초 후 wipe 시작
  const wipeProgress = spring({
    frame: frame - wipeStart,
    fps,
    config: { damping: 22, stiffness: 80 },
  });

  const revealPct = interpolate(wipeProgress, [0, 1], [0, 100]);

  // 라벨 등장
  const beforeLabelIn = spring({
    frame: frame - 5,
    fps,
    config: MOTION.spring,
  });
  const afterLabelIn = spring({
    frame: frame - wipeStart - 10,
    fps,
    config: MOTION.springSnappy,
  });

  // 캡션
  const captionIn = spring({
    frame: frame - wipeStart - 20,
    fps,
    config: MOTION.spring,
  });

  const clipPath =
    wipeDirection === "horizontal"
      ? `inset(0 ${100 - revealPct}% 0 0)`
      : `inset(${100 - revealPct}% 0 0 0)`;

  return (
    <AbsoluteFill>
      {/* Before (채도 낮음) */}
      <AbsoluteFill style={{ filter: "saturate(0.3) brightness(0.85)" }}>
        <Media src={beforeSrc} />
      </AbsoluteFill>

      {/* After (풀 채도, clipPath로 리빌) */}
      <AbsoluteFill style={{ clipPath }}>
        <Media src={afterSrc} />
      </AbsoluteFill>

      {/* Wipe 라인 */}
      {revealPct > 0 && revealPct < 100 && (
        <div
          style={{
            position: "absolute",
            ...(wipeDirection === "horizontal"
              ? {
                  left: `${revealPct}%`,
                  top: 0,
                  bottom: 0,
                  width: 4,
                  transform: "translateX(-50%)",
                }
              : {
                  top: `${revealPct}%`,
                  left: 0,
                  right: 0,
                  height: 4,
                  transform: "translateY(-50%)",
                }),
            background: "#fff",
            boxShadow: "0 0 20px rgba(255,255,255,0.5)",
            zIndex: 10,
          }}
        />
      )}

      {/* 하단 그라데이션 */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(180deg, rgba(0,0,0,0) 60%, rgba(0,0,0,0.6) 100%)",
        }}
      />

      {/* Before 라벨 */}
      <div
        style={{
          position: "absolute",
          top: "42%",
          left: 60,
          opacity: interpolate(beforeLabelIn, [0, 1], [0, 1]),
          transform: `scale(${interpolate(beforeLabelIn, [0, 1], [0.8, 1])})`,
        }}
      >
        <div
          style={{
            background: "rgba(0,0,0,0.6)",
            borderRadius: 20,
            padding: "10px 24px",
          }}
        >
          <span
            style={{
              fontSize: 28,
              fontWeight: 700,
              color: "#fff",
              fontFamily: FONT.english,
              letterSpacing: 3,
            }}
          >
            {beforeLabel}
          </span>
        </div>
      </div>

      {/* After 라벨 */}
      {revealPct > 30 && (
        <div
          style={{
            position: "absolute",
            top: "42%",
            right: 60,
            opacity: interpolate(afterLabelIn, [0, 1], [0, 1]),
            transform: `scale(${interpolate(afterLabelIn, [0, 1], [0.8, 1])})`,
          }}
        >
          <div
            style={{
              background: accent,
              borderRadius: 20,
              padding: "10px 24px",
            }}
          >
            <span
              style={{
                fontSize: 28,
                fontWeight: 700,
                color: "#fff",
                fontFamily: FONT.english,
                letterSpacing: 3,
              }}
            >
              {afterLabel}
            </span>
          </div>
        </div>
      )}

      {/* 캡션 */}
      {caption && (
        <div
          style={{
            position: "absolute",
            bottom: 350,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            padding: "0 60px",
            opacity: interpolate(captionIn, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(captionIn, [0, 1], [20, 0])}px)`,
          }}
        >
          <p
            style={{
              fontSize: 48,
              fontWeight: 800,
              color: "#fff",
              fontFamily: FONT.body,
              textAlign: "center",
              textShadow: "0 4px 16px rgba(0,0,0,0.8)",
            }}
          >
            {caption}
          </p>
        </div>
      )}
    </AbsoluteFill>
  );
};
