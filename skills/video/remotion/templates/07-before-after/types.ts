/**
 * 07 비포/애프터 소구점 — Config 타입
 *
 * clipPath wipe로 전/후 상태를 극적으로 비교합니다.
 * 채도 0.3→1.0 전환으로 변화를 강조합니다.
 */

import type { BaseConfig, BaseSceneConfig } from "../_shared/types/common";

export interface BeforeAfterPair {
  /** Before 이미지/비디오 */
  beforeSrc: string;
  /** After 이미지/비디오 */
  afterSrc: string;
  /** Before 라벨 (기본: "BEFORE") */
  beforeLabel?: string;
  /** After 라벨 (기본: "AFTER") */
  afterLabel?: string;
  /** 캡션 텍스트 */
  caption?: string;
}

export interface BeforeAfterSceneConfig extends BaseSceneConfig {
  type: "compare" | "intro" | "cta";
}

export interface CompareSceneConfig extends BaseSceneConfig {
  type: "compare";
  /** 비교 쌍 */
  pair: BeforeAfterPair;
  /** wipe 방향 (기본: "horizontal") */
  wipeDirection?: "horizontal" | "vertical";
}

export interface IntroSceneConfig extends BaseSceneConfig {
  type: "intro";
  /** 배경 미디어 */
  mediaSrc: string;
  /** 인트로 텍스트 */
  text: string;
  subText?: string;
}

export interface BACtaSceneConfig extends BaseSceneConfig {
  type: "cta";
  productName: string;
  ctaText?: string;
  mediaSrc?: string;
}

export type BeforeAfterScene =
  | CompareSceneConfig
  | IntroSceneConfig
  | BACtaSceneConfig;

export interface BeforeAfterConfig extends BaseConfig {
  scenes: BeforeAfterScene[];
}
