import React from "react";
import { Audio, staticFile } from "remotion";

/**
 * 나레이션 오디오 래퍼 컴포넌트
 *
 * 중요: TransitionSeries 내부에 Audio를 넣으면 씬 전환 시 오디오가 겹칩니다.
 * 반드시 TransitionSeries 바깥에서 Sequence + 절대 프레임으로 배치하세요.
 */
export const Narration: React.FC<{
  src: string;
  volume?: number;
}> = ({ src, volume = 1 }) => {
  return <Audio src={staticFile(src)} volume={volume} />;
};
