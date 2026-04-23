/**
 * 리뷰 배너형 광고 - Config 타입 정의
 *
 * 정적 컴포지트 레이아웃으로 리뷰 카드 + 제품 배너를 조합합니다.
 * 짧은 피드 광고(5~10초)에 최적화되어 있습니다.
 */

export interface ReviewCardConfig {
  /** 별점 (1~5) */
  rating: number;
  /** 리뷰 텍스트 */
  reviewText: string;
  /** 리뷰어 이름 (선택) */
  reviewerName?: string;
}

export interface ProductBannerConfig {
  /** 제품 이미지 파일명 (public/ 기준) */
  imageSrc: string;
  /** 제품명 */
  productName: string;
  /** 가격 텍스트 (예: "39,000원") */
  priceText?: string;
  /** CTA 텍스트 (예: "자세히 보기") */
  ctaText?: string;
}

export interface ReviewBannerConfig {
  /** 배경 이미지 또는 비디오 파일명 (public/ 기준) */
  backgroundSrc: string;
  /** 배경이 비디오인지 여부 (기본 false = 이미지) */
  isBackgroundVideo?: boolean;
  /** 비디오 시작 지점 (초 단위, 기본 0) */
  backgroundStartFrom?: number;
  /** 전체 영상 길이 (초 단위, 기본 6) */
  durationSeconds?: number;
  /** 브랜드 정보 */
  brand: {
    name: string;
    color: string;
  };
  /** 리뷰 카드 설정 */
  review: ReviewCardConfig;
  /** 제품 배너 설정 */
  product: ProductBannerConfig;
  /** 리뷰 카드 등장 딜레이 (프레임 단위, 기본 15) */
  reviewDelay?: number;
  /** 제품 배너 등장 딜레이 (프레임 단위, 기본 30) */
  bannerDelay?: number;
}
