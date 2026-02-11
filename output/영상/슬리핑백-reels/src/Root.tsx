import React from "react";
import { Composition, Folder } from "remotion";

import { ReelsA } from "./compositions/ReelsA";
import { ReelsB } from "./compositions/ReelsB";
import { ReelsC } from "./compositions/ReelsC";

/**
 * 썬데이허그 꿀잠 슬리핑백 실키 밤부 - 인스타그램 릴스 광고 3종
 *
 * 규격: 1080x1920 (9:16), 30fps
 * 세이프존: 상단 108px, 하단 320px, 좌 60px, 우 120px
 */

const FPS = 30;
const WIDTH = 1080;
const HEIGHT = 1920;

// ─── 릴스별 트랜지션 설정 ───
// 릴스 A: 7씬, 6 transitions × 8f = 48f overlap
const REELS_A_SCENE_TOTAL = 3.3 + 3.3 + 4.2 + 6.4 + 6.2 + 4.2 + 4.0; // 31.6s
const REELS_A_OVERLAP = (8 * 6) / FPS; // 1.6s
const REELS_A_FRAMES = Math.round((REELS_A_SCENE_TOTAL - REELS_A_OVERLAP) * FPS); // ~900f = 30s

// 릴스 B: 7씬, 6 transitions × 6f = 36f overlap
const REELS_B_SCENE_TOTAL = 3.2 + 4.2 + 4.2 + 4.2 + 4.2 + 3.0 + 3.2; // 26.2s
const REELS_B_OVERLAP = (6 * 6) / FPS; // 1.2s
const REELS_B_FRAMES = Math.round((REELS_B_SCENE_TOTAL - REELS_B_OVERLAP) * FPS); // ~750f = 25s

// 릴스 C: 5씬, 4 transitions × 12f = 48f overlap
const REELS_C_SCENE_TOTAL = 3.4 + 4.4 + 4.4 + 5.4 + 4.0; // 21.6s
const REELS_C_OVERLAP = (12 * 4) / FPS; // 1.6s
const REELS_C_FRAMES = Math.round((REELS_C_SCENE_TOTAL - REELS_C_OVERLAP) * FPS); // ~600f = 20s

export const RemotionRoot: React.FC = () => {
  return (
    <Folder name="SleepingBag-Reels">
      {/* ─── 릴스 A: Problem-Solution (30초) ─── */}
      <Composition
        id="ReelsA"
        component={ReelsA}
        durationInFrames={REELS_A_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />

      {/* ─── 릴스 B: UGC 리뷰 컴필레이션 (25초) ─── */}
      <Composition
        id="ReelsB"
        component={ReelsB}
        durationInFrames={REELS_B_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />

      {/* ─── 릴스 C: 소재감 감성 ASMR (20초) ─── */}
      <Composition
        id="ReelsC"
        component={ReelsC}
        durationInFrames={REELS_C_FRAMES}
        fps={FPS}
        width={WIDTH}
        height={HEIGHT}
      />
    </Folder>
  );
};
