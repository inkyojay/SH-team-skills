import React from "react";
import {
  AbsoluteFill,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import type { FakeNotificationConfig } from "./types";
import { IOSNotification } from "./components/IOSNotification";

/**
 * V03 - Fake Notification Overlay 광고
 *
 * iOS 알림 배너가 위에서 슬라이드 다운되는 B급 감성 템플릿.
 * 배경 콘텐츠 위에 알림이 겹쳐 표시되어 시선을 강탈합니다.
 *
 * @example
 * ```tsx
 * <Composition
 *   id="FakeNotification"
 *   component={FakeNotification}
 *   durationInFrames={30 * 15}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{
 *     config: {
 *       notifications: [
 *         {
 *           appName: "쿠팡",
 *           title: "품절 임박!",
 *           body: "선데이허그 스와들스트랩 재입고 알림",
 *           delay: 1,
 *           appIcon: "🛒",
 *         },
 *         {
 *           appName: "인스타그램",
 *           title: "육아맘후기 님이 태그했습니다",
 *           body: "이거 진짜 신세계... 아기가 바로 잠듦",
 *           delay: 3,
 *           appIcon: "📸",
 *         },
 *       ],
 *       productContent: {
 *         text: "선데이허그",
 *         subText: "스와들스트랩",
 *         emoji: "👶",
 *       },
 *     },
 *   }}
 * />
 * ```
 */
export const FakeNotification: React.FC<{
  config: FakeNotificationConfig;
}> = ({ config }) => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  const scale = Math.min(width / 1080, height / 1920);

  // 알림 타이밍 계산
  const notificationTimings = React.useMemo(() => {
    let currentFrame = 0;
    return config.notifications.map((notif) => {
      const delay = (notif.delay ?? 2) * fps;
      const appearFrame = currentFrame + delay;
      const stayDuration = (notif.stayDuration ?? 2) * fps;
      currentFrame = appearFrame + stayDuration * 0.5; // 다음 알림은 이전 것이 살짝 남아있을 때
      return { appearFrame, stayDurationFrames: stayDuration };
    });
  }, [config.notifications, fps]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: config.backgroundColor ?? "#1C1C1E",
      }}
    >
      {/* Background Content */}
      <AbsoluteFill
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          gap: 24 * scale,
        }}
      >
        {config.productContent ? (
          <>
            {config.productContent.emoji && (
              <span style={{ fontSize: 120 * scale }}>
                {config.productContent.emoji}
              </span>
            )}
            <div
              style={{
                fontSize: 64 * scale,
                fontWeight: 800,
                color: "#FFF",
                fontFamily: "system-ui, -apple-system, sans-serif",
                textAlign: "center",
              }}
            >
              {config.productContent.text}
            </div>
            {config.productContent.subText && (
              <div
                style={{
                  fontSize: 40 * scale,
                  fontWeight: 400,
                  color: "rgba(255,255,255,0.6)",
                  fontFamily: "system-ui, -apple-system, sans-serif",
                  textAlign: "center",
                }}
              >
                {config.productContent.subText}
              </div>
            )}
          </>
        ) : (
          <div
            style={{
              width: "100%",
              height: "100%",
              backgroundColor: "#2C2C2E",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 32 * scale,
              color: "#666",
              fontFamily: "system-ui, sans-serif",
            }}
          >
            배경 콘텐츠 영역
          </div>
        )}
      </AbsoluteFill>

      {/* iOS Status Bar */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          height: 54 * scale,
          display: "flex",
          alignItems: "flex-end",
          justifyContent: "center",
          paddingBottom: 4 * scale,
          zIndex: 50,
        }}
      >
        <span
          style={{
            fontSize: 28 * scale,
            fontWeight: 600,
            color: "#FFF",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          9:41
        </span>
      </div>

      {/* Notifications */}
      {config.notifications.map((notif, i) => (
        <IOSNotification
          key={i}
          appName={notif.appName}
          title={notif.title}
          body={notif.body}
          appIcon={notif.appIcon}
          appearFrame={notificationTimings[i].appearFrame}
          stayDurationFrames={notificationTimings[i].stayDurationFrames}
          index={i}
          scale={scale}
        />
      ))}
    </AbsoluteFill>
  );
};
