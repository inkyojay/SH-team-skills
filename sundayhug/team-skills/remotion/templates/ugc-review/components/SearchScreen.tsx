import React from "react";
import {
  AbsoluteFill,
  Video,
  useVideoConfig,
  useCurrentFrame,
  staticFile,
  interpolate,
  spring,
} from "remotion";

/**
 * 네이버/검색 화면 씬 컴포넌트
 *
 * 스크린 녹화 영상 위에 검색어를 오버레이로 표시합니다.
 * 실제 검색 행동을 보여줘 신뢰감을 형성합니다.
 */
export const SearchScreen: React.FC<{
  src: string;
  startFrom?: number;
  searchQuery?: string;
  platform?: "naver" | "google" | "coupang";
  children?: React.ReactNode;
}> = ({ src, startFrom = 0, searchQuery, platform = "naver", children }) => {
  const { fps } = useVideoConfig();
  const frame = useCurrentFrame();

  const badgeScale = spring({
    frame: frame - 10,
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  const platformColors: Record<string, string> = {
    naver: "#03C75A",
    google: "#4285F4",
    coupang: "#E6002D",
  };

  return (
    <AbsoluteFill>
      <Video
        src={staticFile(src)}
        style={{ width: "100%", height: "100%", objectFit: "cover" }}
        startFrom={startFrom * fps}
        muted
      />
      {/* 하단 그라데이션 */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background:
            "linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.6) 100%)",
        }}
      />
      {/* 검색 플랫폼 뱃지 */}
      {searchQuery && (
        <div
          style={{
            position: "absolute",
            top: 100,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            transform: `scale(${Math.max(0, badgeScale)})`,
          }}
        >
          <div
            style={{
              background: platformColors[platform],
              borderRadius: 16,
              padding: "12px 28px",
              boxShadow: "0 4px 16px rgba(0,0,0,0.2)",
            }}
          >
            <span
              style={{
                fontSize: 24,
                fontWeight: 700,
                color: "#fff",
                fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
              }}
            >
              "{searchQuery}" 검색
            </span>
          </div>
        </div>
      )}
      {children}
    </AbsoluteFill>
  );
};
