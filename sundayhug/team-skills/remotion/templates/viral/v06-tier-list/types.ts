/**
 * V06 - Tier List / Ranking
 *
 * S/A/B/C/F 티어 그리드에 제품/항목을 배치하는
 * B급 감성 랭킹 템플릿. 브랜드 제품은 항상 S티어.
 */

export type Tier = "S" | "A" | "B" | "C" | "F";

export interface TierItem {
  /** 항목 이름 */
  name: string;
  /** 항목 이미지 (public/ 기준, 선택) */
  imageSrc?: string;
  /** 배치될 티어 */
  tier: Tier;
  /** 등장 딜레이 (초 단위, 기본 0) */
  delay?: number;
}

export interface TierListConfig {
  /** 영상 제목 */
  title: string;
  /** 티어에 배치할 항목 목록 */
  items: TierItem[];
  /** 브랜드 하이라이트 항목 이름 (S티어에서 글로우 효과) */
  brandHighlight?: string;
  /** 배경 색상 (기본 #1a1a2e) */
  bgColor?: string;
  /** CTA 텍스트 (마지막에 표시, 선택) */
  ctaText?: string;
}

export const TIER_COLORS: Record<Tier, string> = {
  S: "#FFD700",
  A: "#4CAF50",
  B: "#2196F3",
  C: "#FF9800",
  F: "#F44336",
};
