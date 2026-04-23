/**
 * 비교 추천형 광고 - Config 타입 정의
 *
 * 문제 제시 → 제품 비교 → 솔루션 시연 → 차별화 → CTA 흐름의
 * 정보 전달형 비교 광고 영상을 구성합니다.
 */

export interface PillCaptionConfig {
  /** 자막 텍스트 */
  text: string;
  /** 필 배경색 (기본: 반투명 검정) */
  backgroundColor?: string;
  /** 텍스트 색상 (기본: 흰색) */
  textColor?: string;
}

export interface ProductItem {
  /** 제품명 */
  name: string;
  /** 제품 이미지 파일명 (public/ 기준) */
  imageSrc: string;
  /** 한 줄 설명 */
  description?: string;
  /** 이 제품이 추천 제품인지 (하이라이트 표시) */
  isRecommended?: boolean;
}

export interface ComparisonSceneConfig {
  /** 비디오 파일명 (public/ 기준) */
  videoSrc: string;
  /** 비디오 시작 지점 (초 단위, 기본 0) */
  videoStartFrom?: number;
  /** 씬 길이 (초 단위) */
  durationSeconds: number;
  /** 씬 유형 */
  type: "problem" | "comparison" | "solution" | "differentiator" | "cta";
  /** 필 스타일 자막 */
  caption: PillCaptionConfig;
  /** 비교 그리드에 표시할 제품들 (comparison 타입일 때) */
  products?: ProductItem[];
  /** 상단 질문 텍스트 (comparison 타입일 때) */
  questionText?: string;
  /** 나레이션 오디오 파일명 */
  narrationSrc?: string;
  /** 나레이션 시작 딜레이 (프레임 단위, 기본 5) */
  narrationDelay?: number;
  /** 자막 등장 딜레이 (프레임 단위, 기본 8) */
  captionDelay?: number;
}

export interface ComparisonConfig {
  /** 씬 배열 */
  scenes: ComparisonSceneConfig[];
  /** 브랜드 정보 */
  brand: {
    name: string;
    color: string;
  };
  /** 씬 전환 트랜지션 길이 (프레임 단위, 기본 10) */
  transitionDurationFrames?: number;
}
