/**
 * 씬 타이밍 유틸리티 (공용)
 *
 * TransitionSeries 오버랩을 고려한 절대 프레임 계산입니다.
 * 기존 meta-reels-ad/utils/timing.ts에서 범용화.
 */

export interface TimingScene {
  durationSeconds: number;
}

/**
 * TransitionSeries의 오버랩을 고려하여 각 씬의 절대 시작 프레임을 계산합니다.
 */
export function calculateSceneStarts(
  scenes: TimingScene[],
  fps: number,
  transitionDuration: number,
): number[] {
  const starts: number[] = [];
  let currentFrame = 0;

  for (let i = 0; i < scenes.length; i++) {
    starts.push(currentFrame);
    const sceneDurationFrames = Math.round(scenes[i].durationSeconds * fps);
    currentFrame += sceneDurationFrames - transitionDuration;
  }

  return starts;
}

/** 초를 프레임으로 변환 */
export function secondsToFrames(seconds: number, fps: number): number {
  return Math.round(seconds * fps);
}

/** 총 영상 길이(프레임)를 씬 배열에서 계산 */
export function calculateTotalFrames(
  scenes: TimingScene[],
  fps: number,
  transitionDuration: number,
): number {
  const totalSceneFrames = scenes.reduce(
    (sum, s) => sum + Math.round(s.durationSeconds * fps),
    0,
  );
  const totalTransitionOverlap =
    Math.max(0, scenes.length - 1) * transitionDuration;
  return totalSceneFrames - totalTransitionOverlap;
}
