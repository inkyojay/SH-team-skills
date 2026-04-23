import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
} from "remotion";
import type { KakaoChatConfig } from "./types";
import { ChatBubble, TypingIndicator } from "./components/ChatBubble";

/**
 * V02 - KakaoTalk Chat 대화형 광고
 *
 * 카카오톡 채팅 UI를 재현한 B급 감성 템플릿.
 * 메시지가 하나씩 등장하며 타이핑 인디케이터가 선행.
 * 마지막에 제품 공개 메시지를 넣을 수 있습니다.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="KakaoChat"
 *   component={KakaoChat}
 *   durationInFrames={30 * 20}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       chatTitle: "육아 고민 상담",
 *       messages: [
 *         { sender: "엄마A", text: "아기 잠투정 너무 심해ㅠ", isMe: false, delay: 0 },
 *         { sender: "나", text: "우리도 그랬는데", isMe: true, delay: 1 },
 *         { sender: "나", text: "스와들스트랩 쓰고 해결됨!", isMe: true, delay: 0.8 },
 *         { sender: "엄마A", text: "뭐야 그게??", isMe: false, delay: 0.5 },
 *       ],
 *     },
 *   }}
 * />
 * ```
 */
export const KakaoChat: React.FC<{ config: KakaoChatConfig }> = ({
  config,
}) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const typingDuration = (config.typingDuration ?? 0.8) * fps;
  const scale = Math.min(width / 1080, height / 1920);

  // 메시지 등장 타이밍 계산
  const messageTimings = React.useMemo(() => {
    let currentFrame = fps * 0.5; // 0.5초 후 시작
    return config.messages.map((msg) => {
      const delay = (msg.delay ?? 1) * fps;
      const typingStart = currentFrame + delay;
      const appearFrame = typingStart + typingDuration;
      currentFrame = appearFrame;
      return { typingStart, appearFrame };
    });
  }, [config.messages, fps, typingDuration]);

  // 현재 타이핑 중인 메시지 찾기
  const typingIndex = messageTimings.findIndex(
    (t) => frame >= t.typingStart && frame < t.appearFrame
  );
  const typingSender =
    typingIndex >= 0 && !config.messages[typingIndex].isMe
      ? config.messages[typingIndex].sender
      : null;

  // 제품 공개 타이밍
  const lastMsgEnd =
    messageTimings.length > 0
      ? messageTimings[messageTimings.length - 1].appearFrame
      : 0;
  const revealFrame = lastMsgEnd + fps * 1;

  return (
    <AbsoluteFill style={{ backgroundColor: "#B2C7D9" }}>
      {/* Status Bar */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 88 * scale,
          backgroundColor: "#3C3C3C",
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "center",
          paddingBottom: 8 * scale,
          fontSize: 28 * scale,
          fontWeight: 600,
          fontFamily: "system-ui, -apple-system, sans-serif",
          color: "#FFF",
          zIndex: 10,
        }}
      >
        <span>오후 3:42</span>
      </div>

      {/* Chat Header */}
      <div
        style={{
          position: "absolute",
          top: 88 * scale,
          left: 0,
          right: 0,
          height: 100 * scale,
          backgroundColor: "#3C3C3C",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: 8 * scale,
          zIndex: 10,
        }}
      >
        <span
          style={{
            position: "absolute",
            left: 24 * scale,
            fontSize: 36 * scale,
            color: "#FFF",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          ←
        </span>
        <span
          style={{
            fontSize: 34 * scale,
            fontWeight: 700,
            color: "#FFF",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {config.chatTitle}
        </span>
        <span
          style={{
            fontSize: 26 * scale,
            color: "#AAA",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {config.participantCount ?? 2}
        </span>
        <span
          style={{
            position: "absolute",
            right: 24 * scale,
            fontSize: 32 * scale,
            color: "#FFF",
          }}
        >
          ☰
        </span>
      </div>

      {/* Chat Messages Area */}
      <div
        style={{
          position: "absolute",
          top: (88 + 100) * scale,
          left: 0,
          right: 0,
          bottom: 120 * scale,
          display: "flex",
          flexDirection: "column",
          justifyContent: "flex-end",
          paddingBottom: 20 * scale,
          overflow: "hidden",
        }}
      >
        {/* Date Separator */}
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            marginBottom: 20 * scale,
          }}
        >
          <span
            style={{
              backgroundColor: "rgba(0,0,0,0.15)",
              borderRadius: 20 * scale,
              padding: `${6 * scale}px ${20 * scale}px`,
              fontSize: 22 * scale,
              color: "#FFF",
              fontFamily: "system-ui, -apple-system, sans-serif",
            }}
          >
            2024년 3월 15일 금요일
          </span>
        </div>

        {/* Messages */}
        {config.messages.map((msg, i) => (
          <ChatBubble
            key={i}
            sender={msg.sender}
            text={msg.text}
            isMe={msg.isMe}
            appearFrame={messageTimings[i].appearFrame}
            emoji={msg.emoji}
            imageSrc={msg.imageSrc}
            scale={scale}
          />
        ))}

        {/* Typing Indicator */}
        {typingSender && (
          <TypingIndicator sender={typingSender} visible scale={scale} />
        )}

        {/* Product Reveal */}
        {config.productReveal && frame >= revealFrame && (
          <div
            style={{
              margin: `${12 * scale}px ${24 * scale}px`,
              backgroundColor: "#FFF",
              borderRadius: 16 * scale,
              padding: `${20 * scale}px`,
              opacity: interpolate(
                frame - revealFrame,
                [0, 8],
                [0, 1],
                { extrapolateRight: "clamp" }
              ),
              transform: `scale(${interpolate(
                frame - revealFrame,
                [0, 8],
                [0.95, 1],
                { extrapolateRight: "clamp" }
              )})`,
            }}
          >
            <div
              style={{
                width: "100%",
                height: 300 * scale,
                backgroundColor: "#F5F5F5",
                borderRadius: 12 * scale,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginBottom: 16 * scale,
                fontSize: 60 * scale,
              }}
            >
              📦
            </div>
            <div
              style={{
                fontSize: 32 * scale,
                fontWeight: 700,
                color: "#1C1C1E",
                fontFamily: "system-ui, -apple-system, sans-serif",
                marginBottom: 8 * scale,
              }}
            >
              {config.productReveal.productName}
            </div>
            {config.productReveal.linkText && (
              <div
                style={{
                  fontSize: 26 * scale,
                  color: "#007AFF",
                  fontFamily: "system-ui, -apple-system, sans-serif",
                }}
              >
                🔗 {config.productReveal.linkText}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Input Bar */}
      <div
        style={{
          position: "absolute",
          bottom: 0,
          left: 0,
          right: 0,
          height: 120 * scale,
          backgroundColor: "#F7F7F7",
          display: "flex",
          alignItems: "center",
          padding: `0 ${20 * scale}px`,
          gap: 12 * scale,
          borderTop: "1px solid #E0E0E0",
        }}
      >
        <span style={{ fontSize: 36 * scale }}>+</span>
        <div
          style={{
            flex: 1,
            height: 72 * scale,
            backgroundColor: "#FFF",
            borderRadius: 36 * scale,
            border: "1px solid #DDD",
            display: "flex",
            alignItems: "center",
            paddingLeft: 20 * scale,
            fontSize: 28 * scale,
            color: "#999",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          메시지 입력
        </div>
        <span style={{ fontSize: 36 * scale }}>😊</span>
        <span style={{ fontSize: 36 * scale }}>#</span>
      </div>
    </AbsoluteFill>
  );
};
