/**
 * 캠페인 팔레트 12종
 *
 * 각 소구점/캠페인 분위기에 맞는 배경·텍스트·액센트 조합입니다.
 * HTML 프로모션 디자인 시스템에서 파생하여 영상에 최적화했습니다.
 */

export interface CampaignPalette {
  /** 팔레트 이름 */
  name: string;
  /** 주 배경색 */
  bg: string;
  /** 따뜻한 배경색 (순백 대신 사용) */
  bgWarm: string;
  /** 주 텍스트색 */
  text: string;
  /** 보조 텍스트색 */
  textSub: string;
  /** 주 액센트색 */
  accent: string;
  /** 보조 액센트색 */
  accentSub: string;
  /** 오버레이 배경 (반투명) */
  overlay: string;
}

export const PALETTES: Record<string, CampaignPalette> = {
  /** 기본 — 썬데이허그 브랜드 */
  default: {
    name: "썬데이 베이지",
    bg: "#FAF7F4",
    bgWarm: "#F5E6D3",
    text: "#333333",
    textSub: "#8B7355",
    accent: "#8B7355",
    accentSub: "#F2D4C4",
    overlay: "rgba(139,115,85,0.85)",
  },
  /** 봄/자연 — 미스티 그린 */
  spring: {
    name: "스프링 그린",
    bg: "#F5F8F5",
    bgWarm: "#E8F0E8",
    text: "#2D3B2D",
    textSub: "#5A7A5A",
    accent: "#6B8E6B",
    accentSub: "#C5D5C5",
    overlay: "rgba(107,142,107,0.85)",
  },
  /** 여름/시원 — 쿨 블루 */
  summer: {
    name: "쿨 블루",
    bg: "#F5F7FA",
    bgWarm: "#E8EDF5",
    text: "#2B3A4E",
    textSub: "#5B7B9D",
    accent: "#4A7FB5",
    accentSub: "#B8D4E8",
    overlay: "rgba(74,127,181,0.85)",
  },
  /** 가을/따뜻 — 앰버 */
  autumn: {
    name: "오텀 앰버",
    bg: "#FAF5F0",
    bgWarm: "#F0E0CC",
    text: "#3B2E1E",
    textSub: "#8B6B45",
    accent: "#C47830",
    accentSub: "#E8C8A0",
    overlay: "rgba(196,120,48,0.85)",
  },
  /** 겨울/차분 — 슬레이트 */
  winter: {
    name: "윈터 슬레이트",
    bg: "#F0F0F2",
    bgWarm: "#E0E0E5",
    text: "#2B2B35",
    textSub: "#6B6B7B",
    accent: "#5B5B7B",
    accentSub: "#C0C0D5",
    overlay: "rgba(91,91,123,0.85)",
  },
  /** 프리미엄 — 딥 네이비 */
  premium: {
    name: "프리미엄 네이비",
    bg: "#1A1A2E",
    bgWarm: "#16213E",
    text: "#F0E6D3",
    textSub: "#B8A080",
    accent: "#D4A574",
    accentSub: "#2A2A4E",
    overlay: "rgba(26,26,46,0.92)",
  },
  /** 세일/할인 — 세일 레드 */
  sale: {
    name: "세일 레드",
    bg: "#FFF5F3",
    bgWarm: "#FFE8E3",
    text: "#2C1810",
    textSub: "#8B4A3A",
    accent: "#D4534A",
    accentSub: "#FFD0C8",
    overlay: "rgba(212,83,74,0.88)",
  },
  /** 신뢰/안전 — 소프트 블루 */
  trust: {
    name: "트러스트 블루",
    bg: "#F5F8FA",
    bgWarm: "#E8F0F5",
    text: "#1A2B3A",
    textSub: "#4A6A8A",
    accent: "#2E6DA4",
    accentSub: "#C0D8E8",
    overlay: "rgba(46,109,164,0.85)",
  },
  /** 따뜻한 감성 — 로즈 */
  rose: {
    name: "로즈 핑크",
    bg: "#FDF5F5",
    bgWarm: "#F8E8E8",
    text: "#3A2028",
    textSub: "#9B6070",
    accent: "#C87080",
    accentSub: "#F2D0D8",
    overlay: "rgba(200,112,128,0.85)",
  },
  /** 친환경/유기농 — 올리브 */
  organic: {
    name: "오가닉 올리브",
    bg: "#F5F5E8",
    bgWarm: "#E8E8D0",
    text: "#2B2B18",
    textSub: "#6B6B48",
    accent: "#7B8B48",
    accentSub: "#D0D8B0",
    overlay: "rgba(123,139,72,0.85)",
  },
  /** 럭셔리 — 골드 */
  luxury: {
    name: "럭셔리 골드",
    bg: "#FAF5E8",
    bgWarm: "#F0E5C8",
    text: "#2A2010",
    textSub: "#8B7530",
    accent: "#B8952E",
    accentSub: "#E8D898",
    overlay: "rgba(184,149,46,0.88)",
  },
  /** 라벤더 — 부드러운 보라 */
  lavender: {
    name: "라벤더",
    bg: "#F8F5FA",
    bgWarm: "#EDE5F2",
    text: "#2A2035",
    textSub: "#7B6590",
    accent: "#8B6BAE",
    accentSub: "#D8C8E8",
    overlay: "rgba(139,107,174,0.85)",
  },
};

/** 팔레트 키로 팔레트를 가져옵니다. 없으면 default 반환. */
export function getPalette(key?: string): CampaignPalette {
  if (!key) return PALETTES.default;
  return PALETTES[key] ?? PALETTES.default;
}
