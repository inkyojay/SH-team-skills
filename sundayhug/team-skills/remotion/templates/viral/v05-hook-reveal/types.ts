/**
 * V05 - Scroll-Stop Hook + Reveal 광고
 *
 * 충격적인 대형 텍스트로 스크롤을 멈추게 한 후
 * 하드 컷으로 제품을 공개하는 2단 구성 B급 감성 템플릿.
 */

export interface HookRevealConfig {
  /** 훅 텍스트 (화면의 80% 차지하는 큰 글씨) */
  hookText: string;
  /** 훅 이모지 (선택) */
  hookEmoji?: string;
  /** 훅 배경색 (기본 #000) */
  hookBgColor?: string;
  /** 훅 텍스트 색상 (기본 #FFF) */
  hookTextColor?: string;
  /** 제품명 */
  revealProductName: string;
  /** 제품 이미지/미디어 소스 (선택) */
  revealMediaSrc?: string;
  /** 제품 설명 캡션 */
  revealCaption: string;
  /** CTA 텍스트 */
  ctaText: string;
  /** CTA 색상 (기본 #FF0050) */
  ctaColor?: string;
  /** 리빌 배경색 (기본 #FFF) */
  revealBgColor?: string;
  /** 훅 표시 시간 (초, 기본 1.5) */
  hookDuration?: number;
  /** 글리치/플래시 효과 (기본 true) */
  enableFlash?: boolean;
}
