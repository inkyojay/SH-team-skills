/**
 * 04 사회적 증거 소구점 — Config 타입
 *
 * 숫자 카운트업, 별점 애니메이션, 인증 뱃지로 신뢰를 구축합니다.
 */

import type { BaseConfig, BaseSceneConfig } from "../_shared/types/common";

export interface StatItem {
  /** 숫자 값 */
  value: number;
  /** 접미사 (예: "+", "만", "%") */
  suffix?: string;
  /** 접두사 (예: "★", "₩") */
  prefix?: string;
  /** 라벨 (예: "누적 판매", "만족도") */
  label: string;
  /** 소수점 자릿수 */
  decimals?: number;
}

export interface BadgeItem {
  /** 뱃지 텍스트 (예: "네이버 1위", "KC인증") */
  text: string;
  /** 아이콘 이미지 (public/ 기준, 선택) */
  iconSrc?: string;
}

export interface ReviewItem {
  /** 리뷰 텍스트 */
  text: string;
  /** 작성자명 */
  author?: string;
  /** 별점 (0~5) */
  rating?: number;
}

export interface StatsSceneConfig extends BaseSceneConfig {
  type: "stats";
  /** 배경 미디어 */
  mediaSrc?: string;
  /** 통계 항목들 */
  stats: StatItem[];
}

export interface RatingSceneConfig extends BaseSceneConfig {
  type: "rating";
  /** 배경 미디어 */
  mediaSrc?: string;
  /** 별점 */
  score: number;
  /** 리뷰 수 텍스트 (예: "3,842개 리뷰") */
  reviewCountText: string;
  /** 대표 리뷰 */
  featuredReview?: ReviewItem;
}

export interface BadgeSceneConfig extends BaseSceneConfig {
  type: "badges";
  /** 배경 미디어 */
  mediaSrc?: string;
  /** 인증 뱃지들 */
  badges: BadgeItem[];
  /** 헤드라인 (예: "검증된 품질") */
  headline?: string;
}

export interface ReviewCarouselSceneConfig extends BaseSceneConfig {
  type: "reviews";
  /** 배경 미디어 */
  mediaSrc?: string;
  /** 리뷰 목록 */
  reviews: ReviewItem[];
}

export interface SPCtaSceneConfig extends BaseSceneConfig {
  type: "cta";
  productName: string;
  ctaText?: string;
  mediaSrc?: string;
}

export type SocialProofScene =
  | StatsSceneConfig
  | RatingSceneConfig
  | BadgeSceneConfig
  | ReviewCarouselSceneConfig
  | SPCtaSceneConfig;

export interface SocialProofConfig extends BaseConfig {
  scenes: SocialProofScene[];
}
