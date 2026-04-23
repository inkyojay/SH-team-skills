/**
 * 12 라이프스타일/루틴 소구점 — Config 타입
 *
 * 스텝 번호 팝인, 타임라인 연결선, 프로그레스 닷으로
 * 일상 루틴 속 제품 사용을 보여줍니다.
 */

import type { BaseConfig, BaseSceneConfig } from "../_shared/types/common";

export interface RoutineStep {
  /** 스텝 번호 (1, 2, 3...) */
  stepNumber: number;
  /** 스텝 제목 (예: "목욕 후 보습") */
  title: string;
  /** 설명 텍스트 */
  description?: string;
  /** 시간대 텍스트 (예: "PM 8:00") */
  timeLabel?: string;
  /** 비디오/이미지 */
  mediaSrc: string;
  videoStartFrom?: number;
}

export interface IntroSceneConfig extends BaseSceneConfig {
  type: "intro";
  /** 배경 미디어 */
  mediaSrc: string;
  /** 인트로 텍스트 */
  title: string;
  subTitle?: string;
}

export interface StepSceneConfig extends BaseSceneConfig {
  type: "step";
  /** 루틴 스텝 정보 */
  step: RoutineStep;
  /** 전체 스텝 수 (프로그레스 닷 표시용) */
  totalSteps: number;
}

export interface SummarySceneConfig extends BaseSceneConfig {
  type: "summary";
  /** 배경 미디어 */
  mediaSrc?: string;
  /** 요약 텍스트 */
  summaryText: string;
  /** 제품명 */
  productName?: string;
}

export interface RoutineCtaSceneConfig extends BaseSceneConfig {
  type: "cta";
  productName: string;
  ctaText?: string;
  mediaSrc?: string;
}

export type LifestyleScene =
  | IntroSceneConfig
  | StepSceneConfig
  | SummarySceneConfig
  | RoutineCtaSceneConfig;

export interface LifestyleRoutineConfig extends BaseConfig {
  scenes: LifestyleScene[];
}
