/**
 * 슬리핑백 릴스 광고 - 타입 정의
 * meta-reels-ad 템플릿 기반 + 릴스 B/C용 확장
 */

export interface SceneConfig {
  /** 비디오 파일명 (public/ 기준) 또는 undefined(이미지 전용 씬) */
  videoSrc?: string;
  /** 비디오 시작 지점 (초 단위, 기본 0) */
  videoStartFrom?: number;
  /** 이미지 파일명 (public/ 기준, 비디오 없을 때 사용) */
  imageSrc?: string;
  /** 씬 길이 (초 단위) */
  durationSeconds: number;
  /** 자막 설정 */
  caption: {
    line1: string;
    line2?: string;
    emoji?: string;
  };
  /** 나레이션 오디오 파일명 */
  narrationSrc?: string;
  /** 나레이션 시작 딜레이 (프레임) */
  narrationDelay?: number;
  /** 자막 등장 딜레이 (프레임, 기본 5) */
  captionDelay?: number;
  /** 브랜드 로고 표시 여부 */
  showBrandLogo?: boolean;
  /** 별점 뱃지 표시 여부 */
  showRatingBadge?: boolean;
  /** 별점 뱃지 등장 딜레이 (프레임) */
  ratingBadgeDelay?: number;
  /** 리뷰 카드 (릴스 B용) */
  reviewCard?: {
    text: string;
    rating?: number;
  };
  /** CTA 엔드카드 표시 여부 */
  showCtaEndCard?: boolean;
  /** CTA 텍스트 */
  ctaText?: string;
  /** 컬러 스와치 표시 여부 */
  showColorSwatches?: boolean;
  /** 배경색 (이미지/그래픽 씬용) */
  backgroundColor?: string;
}

export interface AdConfig {
  scenes: SceneConfig[];
  brand: {
    name: string;
    color: string;
  };
  rating?: {
    score: string;
    reviewCount: string;
  };
  transitionDurationFrames?: number;
  narrationSrc?: string;
  narrationDelay?: number;
  bgmSrc?: string;
  bgmVolume?: number;
}
