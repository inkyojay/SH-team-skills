import type { SceneConfig } from "../types";

/**
 * TransitionSeries 오버랩을 고려한 절대 시작 프레임 계산
 */
export function calculateSceneStarts(
  scenes: SceneConfig[],
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

/**
 * 전체 Composition 프레임 수 계산
 */
export function calculateTotalFrames(
  scenes: SceneConfig[],
  fps: number,
  transitionDurationFrames: number,
): number {
  const totalSeconds = scenes.reduce((sum, s) => sum + s.durationSeconds, 0);
  const overlapSeconds =
    (transitionDurationFrames * (scenes.length - 1)) / fps;
  return Math.round((totalSeconds - overlapSeconds) * fps);
}
