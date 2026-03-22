import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Sequence,
} from "remotion";
import type { NotesAppConfig } from "./types";

/**
 * V01 - iPhone Notes App 타이핑 광고
 *
 * Apple Notes 앱의 UI를 재현한 B급 감성 템플릿.
 * 글자가 하나씩 타이핑되는 효과로 시선을 끌고,
 * 의도적 오타와 커서 깜빡임으로 자연스러움을 연출합니다.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="NotesApp"
 *   component={NotesApp}
 *   durationInFrames={30 * 8}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       lines: [
 *         { text: "아기가 밤에 안 자서", delay: 0 },
 *         { text: "이거 써봤는데", delay: 0.3 },
 *         { text: "진짜 효과 있음 ㄹㅇ", bold: true },
 *       ],
 *       brandName: "선데이허그",
 *       productName: "스와들스트랩",
 *       ctaText: "지금 바로 검색 🔍",
 *     },
 *   }}
 * />
 * ```
 */
export const NotesApp: React.FC<{ config: NotesAppConfig }> = ({ config }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const charSpeed = config.charSpeed ?? 0.06;
  const ctaColor = config.ctaColor ?? "#007AFF";

  // 각 줄의 시작 프레임과 타이핑 정보 계산
  const lineTimings = React.useMemo(() => {
    let currentFrame = 0;
    return config.lines.map((line) => {
      const delay = (line.delay ?? 0.3) * fps;
      const startFrame = currentFrame + delay;
      const typingDuration = line.text.length * charSpeed * fps;
      currentFrame = startFrame + typingDuration;
      return { startFrame, typingDuration, endFrame: currentFrame };
    });
  }, [config.lines, fps, charSpeed]);

  // 전체 타이핑 끝나는 프레임
  const allTypingEnd =
    lineTimings.length > 0
      ? lineTimings[lineTimings.length - 1].endFrame
      : 0;

  // 커서 깜빡임 (0.5초 주기)
  const cursorVisible =
    Math.floor((frame / fps) * 2) % 2 === 0 || frame < allTypingEnd;

  // 현재 활성 줄 인덱스
  const activeLineIndex = lineTimings.findIndex(
    (t) => frame < t.endFrame
  );
  const currentActiveIndex =
    activeLineIndex === -1 ? config.lines.length - 1 : activeLineIndex;

  // 스케일 계산 (반응형)
  const scale = Math.min(width / 1080, height / 1920);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#FFFFFF",
        fontFamily:
          '"SF Mono", "Menlo", "Monaco", "Courier New", monospace',
      }}
    >
      {/* Status Bar */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 88 * scale,
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "center",
          paddingBottom: 8 * scale,
          fontSize: 28 * scale,
          fontWeight: 600,
          fontFamily: "system-ui, -apple-system, sans-serif",
          color: "#000",
          zIndex: 10,
        }}
      >
        <span>9:41</span>
      </div>

      {/* Notes Header Bar */}
      <div
        style={{
          position: "absolute",
          top: 88 * scale,
          left: 0,
          right: 0,
          height: 100 * scale,
          backgroundColor: "#F6F2E8",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          padding: `0 ${32 * scale}px`,
          borderBottom: `1px solid #E5E0D5`,
        }}
      >
        <span
          style={{
            fontSize: 32 * scale,
            color: "#D4A017",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          ← 메모
        </span>
        <span
          style={{
            fontSize: 28 * scale,
            color: "#8E8E93",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {config.brandName ?? "메모"}
        </span>
        <span
          style={{
            fontSize: 32 * scale,
            color: "#D4A017",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          ✏️
        </span>
      </div>

      {/* Content Area */}
      <div
        style={{
          position: "absolute",
          top: (88 + 100) * scale,
          left: 0,
          right: 0,
          bottom: config.ctaText ? 160 * scale : 0,
          padding: `${48 * scale}px ${40 * scale}px`,
          display: "flex",
          flexDirection: "column",
          gap: 16 * scale,
        }}
      >
        {config.lines.map((line, i) => {
          const timing = lineTimings[i];
          if (frame < timing.startFrame) return null;

          const progress = Math.min(
            (frame - timing.startFrame) / timing.typingDuration,
            1
          );
          const visibleChars = Math.floor(progress * line.text.length);
          const displayText = line.text.substring(0, visibleChars);

          // 제품명 하이라이트
          let rendered: React.ReactNode = displayText;
          if (config.productName && displayText.includes(config.productName)) {
            const parts = displayText.split(config.productName);
            rendered = (
              <>
                {parts[0]}
                <span
                  style={{
                    backgroundColor: "#FFFF00",
                    padding: `0 ${4 * scale}px`,
                  }}
                >
                  {config.productName}
                </span>
                {parts.slice(1).join(config.productName)}
              </>
            );
          }

          const showCursor = i === currentActiveIndex && cursorVisible;

          return (
            <div
              key={i}
              style={{
                fontSize: (line.bold ? 48 : 40) * scale,
                fontWeight: line.bold ? 700 : 400,
                color: "#1C1C1E",
                lineHeight: 1.5,
                letterSpacing: -0.5,
              }}
            >
              {rendered}
              {showCursor && (
                <span
                  style={{
                    display: "inline-block",
                    width: 3 * scale,
                    height: (line.bold ? 48 : 40) * scale,
                    backgroundColor: "#007AFF",
                    marginLeft: 2 * scale,
                    verticalAlign: "text-bottom",
                  }}
                />
              )}
            </div>
          );
        })}
      </div>

      {/* CTA */}
      {config.ctaText && (
        <Sequence from={Math.round(allTypingEnd + fps * 0.5)}>
          <div
            style={{
              position: "absolute",
              bottom: 40 * scale,
              left: 40 * scale,
              right: 40 * scale,
              height: 100 * scale,
              backgroundColor: ctaColor,
              borderRadius: 20 * scale,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              opacity: interpolate(
                useCurrentFrame(),
                [0, 8],
                [0, 1],
                { extrapolateRight: "clamp" }
              ),
            }}
          >
            <span
              style={{
                color: "#FFFFFF",
                fontSize: 36 * scale,
                fontWeight: 700,
                fontFamily: "system-ui, -apple-system, sans-serif",
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
