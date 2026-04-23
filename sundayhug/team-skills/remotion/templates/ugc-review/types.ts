/**
 * UGC 리뷰형 광고 - Config 타입 정의
 *
 * 셀카 훅 → 검색 화면 → 제품 시연 → 기능 소개 → CTA 흐름의
 * 캐주얼 UGC 스타일 광고 영상을 구성합니다.
 */

export interface UgcCaptionConfig {
  /** 자막 텍스트 */
  text: string;
  /** 강조할 키워드 (노랑색 하이라이트) */
  highlightWords?: string[];
}

export interface UgcSceneConfig {
  /** 비디오 파일명 (public/ 기준) */
  videoSrc: string;
  /** 비디오 시작 지점 (초 단위, 기본 0) */
  videoStartFrom?: number;
  /** 씬 길이 (초 단위) */
  durationSeconds: number;
  /** 씬 유형 */
  type: "selfie-hook" | "search-screen" | "demo-clip" | "feature" | "cta";
  /** 자막 설정 */
  caption: UgcCaptionConfig;
  /** 나레이션 오디오 파일명 (public/ 기준, 없으면 무음) */
  narrationSrc?: string;
  /** 나레이션 시작 딜레이 (프레임 단위, 기본 5) */
  narrationDelay?: number;
  /** 자막 등장 딜레이 (프레임 단위, 기본 5) */
  captionDelay?: number;
}

export interface SearchScreenOverlay {
  /** 검색 플랫폼 */
  platform: "naver" | "google" | "coupang";
  /** 검색어 텍스트 */
  searchQuery: string;
}

export interface UgcReviewConfig {
  /** 씬 배열 */
  scenes: UgcSceneConfig[];
  /** 브랜드 정보 */
  brand: {
    name: string;
    color: string;
  };
  /** 검색 화면 오버레이 설정 (search-screen 타입 씬에 적용) */
  searchOverlay?: SearchScreenOverlay;
  /** 강조 키워드 색상 (기본 #FFE53B) */
  highlightColor?: string;
  /** 씬 전환 트랜지션 길이 (프레임 단위, 기본 4) - UGC는 빠른 컷 */
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
