/**
 * V09 - Text Bomb / 배민 Style
 *
 * 화면의 80%를 차지하는 위트있는 텍스트 한 줄.
 * 솔리드 배경 + 미니멀 구성의 안티디자인 감성.
 * 의도적으로 파워포인트 슬라이드처럼 보이게 연출.
 */

export type FontStyle = "bold" | "retro" | "handwritten" | "impact";

export type BackgroundPattern = "none" | "dots" | "lines" | "grid";

export interface TextBombConfig {
  /** 메인 텍스트 (화면의 80% 차지) */
  mainText: string;
  /** 서브 텍스트 (선택, 0.5초 후 등장) */
  subText?: string;
  /** 브랜드명 (우하단 작게) */
  brandName: string;
  /** 배경 색상 */
  bgColor: string;
  /** 텍스트 색상 (기본 bgColor 대비 자동) */
  textColor?: string;
  /** 폰트 스타일 (기본 bold) */
  fontStyle?: FontStyle;
  /** 배경 패턴 (기본 none) */
  backgroundPattern?: BackgroundPattern;
}
