/**
 * 02 감성 소구점 — Config 타입
 *
 * Ken Burns 풀블리드, 슬로우 페이드, 감성적 인용구로 분위기를 전달합니다.
 */

import type { BaseConfig, BaseSceneConfig } from "../_shared/types/common";

export interface EmotionalSceneConfig extends BaseSceneConfig {
  type: "mood" | "quote" | "product" | "cta";
}

export interface MoodSceneConfig extends BaseSceneConfig {
  type: "mood";
  /** 풀블리드 이미지/비디오 */
  mediaSrc: string;
  videoStartFrom?: number;
  /** Ken Burns 방향 (기본: "zoom-in") */
  kenBurnsDirection?: "zoom-in" | "zoom-out" | "pan-left" | "pan-right";
  /** 오버레이 텍스트 (짧은 감성 카피) */
  overlayText?: string;
}

export interface QuoteSceneConfig extends BaseSceneConfig {
  type: "quote";
  /** 배경 이미지/비디오 */
  mediaSrc?: string;
  /** 인용구 텍스트 */
  quoteText: string;
  /** 인용구 출처 (예: "30대 워킹맘") */
  attribution?: string;
  /** 배경색 (mediaSrc 없을 때 사용) */
  backgroundColor?: string;
}

export interface EmotionalProductSceneConfig extends BaseSceneConfig {
  type: "product";
  /** 제품 이미지/비디오 */
  mediaSrc: string;
  videoStartFrom?: number;
  /** 제품 감성 카피 */
  caption: string;
  subCaption?: string;
}

export interface EmotionalCtaSceneConfig extends BaseSceneConfig {
  type: "cta";
  productName: string;
  ctaText?: string;
  mediaSrc?: string;
}

export type EmotionalScene =
  | MoodSceneConfig
  | QuoteSceneConfig
  | EmotionalProductSceneConfig
  | EmotionalCtaSceneConfig;

export interface EmotionalConfig extends BaseConfig {
  scenes: EmotionalScene[];
}
