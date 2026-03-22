/**
 * 썬데이허그 브랜드 상수
 *
 * 영상 템플릿 전체에서 일관된 브랜드 표현을 위한 상수 모음입니다.
 */

export const BRAND = {
  name: "SUNDAY HUG",
  color: "#8B7355",
  bgWarm: "#FAF7F4",
  beige: "#F5E6D3",
  cream: "#FAFAF7",
  softGray: "#E8E4DE",
  saleRed: "#D4534A",
  softPink: "#F2D4C4",
  mistyGreen: "#C5D5C5",
} as const;

export const BRAND_TEXT = {
  deep: "#8B7355",
  dark: "#333333",
  mid: "#666666",
  light: "#999999",
} as const;

/** 폰트 패밀리 */
export const FONT = {
  body: "'Noto Sans KR', 'Pretendard', system-ui, -apple-system, sans-serif",
  display: "'Cormorant Garamond', Georgia, serif",
  english: "'DM Sans', 'Pretendard', system-ui, sans-serif",
} as const;

/** 애니메이션 가이드라인 */
export const MOTION = {
  /** 표준 spring: 부드럽고 자연스러운 등장 */
  spring: { damping: 16, stiffness: 150 },
  /** 약한 spring: 매우 부드러운 등장 */
  springGentle: { damping: 18, stiffness: 120 },
  /** 강한 spring: 빠르고 명확한 등장 */
  springSnappy: { damping: 14, stiffness: 180 },
  /** 전환 길이 (프레임) */
  transitionFrames: 12,
  /** Ken Burns 스케일 범위 */
  kenBurns: { from: 1.0, to: 1.08 },
} as const;
