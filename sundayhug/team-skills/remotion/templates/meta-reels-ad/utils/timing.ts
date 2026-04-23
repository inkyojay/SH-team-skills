import type { SceneConfig } from "../types";

/**
 * TransitionSeries의 오버랩을 고려하여 각 씬의 절대 시작 프레임을 계산합니다.
 *
 * TransitionSeries에서 씬 간 전환이 겹치므로,
 * 실제 시작 프레임 = 이전 씬들의 누적 길이 - 누적 트랜지션 오버랩
 *
 * @param scenes - 씬 설정 배열
 * @param fps - 초당 프레임 수
 * @param transitionDuration - 트랜지션 길이 (프레임 단위)
 * @returns 각 씬의 절대 시작 프레임 배열
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
