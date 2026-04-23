/**
 * V04 - Ugly/Lo-Fi Review 광고
 *
 * 셀카캠 스타일의 볼드 캡션 + 카메라 쉐이크로
 * 의도적으로 "다듬지 않은" 느낌을 내는 B급 감성 리뷰 템플릿.
 */

export interface UglyReviewConfig {
  /** 리뷰 본문 (여러 줄 가능, \n으로 구분) */
  reviewText: string;
  /** 리뷰어 이름 */
  reviewerName: string;
  /** 제품명 (노란/초록 하이라이트) */
  productName: string;
  /** 배경 색상 (기본 #FF6B6B) */
  bgColor?: string;
  /** 배경 그라디언트 끝 색상 (선택) */
  bgGradientEnd?: string;
  /** 별점 (0~5, 선택) */
  rating?: number;
  /** 하이라이트 색상 (기본 #FFFF00) */
  highlightColor?: string;
  /** 카메라 쉐이크 강도 (0~1, 기본 0.5) */
  shakeIntensity?: number;
  /** CTA 텍스트 (선택) */
  ctaText?: string;
}
