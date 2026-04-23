/**
 * 브랜드 공식형 광고 - Config 타입 정의
 *
 * 고정 헤더(로고+제품명+썸네일) + 하단 콘텐츠 순환 구조의
 * 전문적인 브랜드 공식 광고 영상을 구성합니다.
 */

export interface HighlightCaptionConfig {
  /** 자막 텍스트 */
  text: string;
  /** 하이라이트할 키워드 (브랜드 컬러 배경) */
  highlightWords?: string[];
}

export interface BrandHeaderConfig {
  /** 브랜드 로고 이미지 (public/ 기준) */
  logoSrc: string;
  /** 제품명 */
  productName: string;
  /** 제품 썸네일 이미지 (public/ 기준) */
  productImageSrc?: string;
}

export interface ShowcaseSceneConfig {
  /** 비디오 파일명 (public/ 기준) */
  videoSrc: string;
  /** 비디오 시작 지점 (초 단위, 기본 0) */
  videoStartFrom?: number;
  /** 씬 길이 (초 단위) */
  durationSeconds: number;
  /** 씬 유형 */
  type: "intro" | "feature" | "cta";
  /** 하이라이트 자막 */
  caption: HighlightCaptionConfig;
  /** 나레이션 오디오 파일명 */
  narrationSrc?: string;
  /** 나레이션 시작 딜레이 (프레임 단위, 기본 5) */
  narrationDelay?: number;
  /** 자막 등장 딜레이 (프레임 단위, 기본 8) */
  captionDelay?: number;
}

export interface BrandedShowcaseConfig {
  /** 씬 배열 */
  scenes: ShowcaseSceneConfig[];
  /** 브랜드 정보 */
  brand: {
    name: string;
    color: string;
  };
  /** 고정 헤더 설정 */
  header: BrandHeaderConfig;
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
