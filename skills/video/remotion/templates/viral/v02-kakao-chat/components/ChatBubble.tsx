import React from "react";
import {
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";

/**
 * 카카오톡 스타일 채팅 버블
 *
 * isMe=true: 노란 버블 오른쪽 정렬
 * isMe=false: 흰 버블 왼쪽 정렬 + 프로필
 */
export const ChatBubble: React.FC<{
  sender: string;
  text: string;
  isMe: boolean;
  appearFrame: number;
  emoji?: string;
  imageSrc?: string;
  scale?: number;
}> = ({ sender, text, isMe, appearFrame, emoji, imageSrc, scale = 1 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - appearFrame;
  if (localFrame < 0) return null;

  const scaleAnim = spring({
    frame: localFrame,
    fps,
    config: { damping: 15, stiffness: 200, mass: 0.8 },
    from: 0.95,
    to: 1,
  });

  const opacity = interpolate(localFrame, [0, 4], [0, 1], {
    extrapolateRight: "clamp",
  });

  const profileColors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"];
  const colorIndex =
    sender.split("").reduce((a, c) => a + c.charCodeAt(0), 0) %
    profileColors.length;

  const timeStr = "오후 3:42";

  return (
    <div
      style={{
        display: "flex",
        flexDirection: isMe ? "row-reverse" : "row",
        alignItems: "flex-end",
        gap: 8 * scale,
        marginBottom: 12 * scale,
        padding: `0 ${24 * scale}px`,
        opacity,
        transform: `scale(${scaleAnim})`,
        transformOrigin: isMe ? "right bottom" : "left bottom",
      }}
    >
      {/* 프로필 (상대방만) */}
      {!isMe && (
        <div
          style={{
            width: 72 * scale,
            height: 72 * scale,
            borderRadius: 24 * scale,
            backgroundColor: profileColors[colorIndex],
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            fontSize: 28 * scale,
            color: "#FFF",
            fontWeight: 700,
            flexShrink: 0,
          }}
        >
          {sender.charAt(0)}
        </div>
      )}

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: isMe ? "flex-end" : "flex-start",
          maxWidth: "65%",
        }}
      >
        {/* 발신자 이름 (상대방만) */}
        {!isMe && (
          <span
            style={{
              fontSize: 24 * scale,
              color: "#555",
              marginBottom: 4 * scale,
              fontFamily: "system-ui, -apple-system, sans-serif",
            }}
          >
            {sender}
          </span>
        )}

        <div
          style={{
            display: "flex",
            flexDirection: isMe ? "row-reverse" : "row",
            alignItems: "flex-end",
            gap: 6 * scale,
          }}
        >
          {/* 버블 */}
          <div
            style={{
              backgroundColor: isMe ? "#FEE500" : "#FFFFFF",
              borderRadius: 16 * scale,
              padding: emoji
                ? `${16 * scale}px`
                : `${14 * scale}px ${18 * scale}px`,
              position: "relative",
            }}
          >
            {emoji ? (
              <span style={{ fontSize: 64 * scale }}>{emoji}</span>
            ) : imageSrc ? (
              <div
                style={{
                  width: 400 * scale,
                  height: 300 * scale,
                  borderRadius: 12 * scale,
                  backgroundColor: "#E0E0E0",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  fontSize: 24 * scale,
                  color: "#999",
                }}
              >
                📷 이미지
              </div>
            ) : (
              <span
                style={{
                  fontSize: 32 * scale,
                  color: "#1C1C1E",
                  lineHeight: 1.4,
                  fontFamily: "system-ui, -apple-system, sans-serif",
                  wordBreak: "keep-all",
                }}
              >
                {text}
              </span>
            )}
          </div>

          {/* 시간 */}
          <span
            style={{
              fontSize: 20 * scale,
              color: "#999",
              whiteSpace: "nowrap",
              fontFamily: "system-ui, -apple-system, sans-serif",
            }}
          >
            {timeStr}
          </span>
        </div>
      </div>
    </div>
  );
};

/**
 * 타이핑 인디케이터 (점 세 개 애니메이션)
 */
export const TypingIndicator: React.FC<{
  sender: string;
  visible: boolean;
  scale?: number;
}> = ({ sender, visible, scale = 1 }) => {
  const frame = useCurrentFrame();

  if (!visible) return null;

  const profileColors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7"];
  const colorIndex =
    sender.split("").reduce((a, c) => a + c.charCodeAt(0), 0) %
    profileColors.length;

  return (
    <div
      style={{
        display: "flex",
        alignItems: "flex-end",
        gap: 8 * scale,
        marginBottom: 12 * scale,
        padding: `0 ${24 * scale}px`,
      }}
    >
      <div
        style={{
          width: 72 * scale,
          height: 72 * scale,
          borderRadius: 24 * scale,
          backgroundColor: profileColors[colorIndex],
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: 28 * scale,
          color: "#FFF",
          fontWeight: 700,
          flexShrink: 0,
        }}
      >
        {sender.charAt(0)}
      </div>
      <div
        style={{
          backgroundColor: "#FFFFFF",
          borderRadius: 16 * scale,
          padding: `${18 * scale}px ${24 * scale}px`,
          display: "flex",
          gap: 6 * scale,
          alignItems: "center",
        }}
      >
        {[0, 1, 2].map((i) => {
          const bounce = Math.sin((frame / 4 + i * 2.5) * 0.8) * 0.5 + 0.5;
          return (
            <div
              key={i}
              style={{
                width: 14 * scale,
                height: 14 * scale,
                borderRadius: "50%",
                backgroundColor: "#999",
                opacity: 0.4 + bounce * 0.6,
                transform: `translateY(${-bounce * 4 * scale}px)`,
              }}
            />
          );
        })}
      </div>
    </div>
  );
};
