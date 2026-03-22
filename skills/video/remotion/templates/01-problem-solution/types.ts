/**
 * 01 문제-해결 소구점 — Config 타입
 *
 * 다크→브라이트 전환으로 문제 제시 후 솔루션을 보여주는 구조입니다.
 * 씬 유형: problem → transition → solution → cta
 */

import type { BaseConfig, BaseSceneConfig } from "../_shared/types/common";

export interface ProblemSceneConfig extends BaseSceneConfig {
  type: "problem";
  /** 비디오/이미지 (public/ 기준) */
  mediaSrc: string;
  videoStartFrom?: number;
  /** 문제 상황 텍스트 (한 줄) */
  problemText: string;
  /** 보조 텍스트 */
  subText?: string;
}

export interface SolutionSceneConfig extends BaseSceneConfig {
  type: "solution";
  /** 비디오/이미지 */
  mediaSrc: string;
  videoStartFrom?: number;
  /** 솔루션 텍스트 */
  solutionText: string;
  /** 보조 텍스트 */
  subText?: string;
  /** 제품명 */
  productName?: string;
}

export interface CtaSceneConfig extends BaseSceneConfig {
  type: "cta";
  /** 배경 비디오/이미지 */
  mediaSrc?: string;
  /** 제품명 */
  productName: string;
  /** CTA 텍스트 */
  ctaText?: string;
}

export type ProblemSolutionScene =
  | ProblemSceneConfig
  | SolutionSceneConfig
  | CtaSceneConfig;

export interface ProblemSolutionConfig extends BaseConfig {
  scenes: ProblemSolutionScene[];
}
