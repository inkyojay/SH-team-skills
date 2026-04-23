/**
 * Meta Reels Ad - Config 기반 멀티씬 타입 정의
 *
 * 프로젝트별 AdConfig를 정의하여 MetaReelsAd에 전달합니다.
 */

export interface SceneConfig {
  /** 비디오 파일명 (public/ 기준) */
  videoSrc: string;
  /** 비디오 시작 지점 (초 단위, 기본 0) */
  videoStartFrom?: number;
  /** 씬 길이 (초 단위) */
  durationSeconds: number;
  /** 자막 설정 */
  caption: {
    line1: string;
    line2?: string;
    emoji?: string;
  };
  /** 나레이션 오디오 파일명 (public/ 기준, 없으면 무음) */
  narrationSrc?: string;
  /** 나레이션 시작 딜레이 (프레임 단위, 기본 5) */
  narrationDelay?: number;
  /** 자막 등장 딜레이 (프레임 단위, 기본 5) */
  captionDelay?: number;
  /** 브랜드 로고 표시 여부 (기본 false) */
  showBrandLogo?: boolean;
  /** 별점 뱃지 표시 여부 (기본 false) */
  showRatingBadge?: boolean;
  /** 별점 뱃지 등장 딜레이 (프레임 단위, 기본 40) */
  ratingBadgeDelay?: number;
}

export interface AdConfig {
  /** 씬 배열 */
  scenes: SceneConfig[];
  /** 브랜드 정보 */
  brand: {
    name: string;
    color: string;
  };
  /** 별점/리뷰 정보 (없으면 RatingBadge 미표시) */
  rating?: {
    score: string;
    reviewCount: string;
  };
  /** 씬 전환 트랜지션 길이 (프레임 단위, 기본 8) */
  transitionDurationFrames?: number;
  /** 통합 나레이션 오디오 (전체 영상에 하나의 스토리로 재생, 씬별 narrationSrc보다 우선) */
  narrationSrc?: string;
  /** 통합 나레이션 시작 딜레이 (프레임 단위, 기본 5) */
  narrationDelay?: number;
  /** 배경 음악 오디오 파일명 (public/ 기준) */
  bgmSrc?: string;
  /** 배경 음악 볼륨 (0~1, 기본 0.3) */
  bgmVolume?: number;
}
