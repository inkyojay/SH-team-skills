/**
 * 공용 타입 정의
 *
 * 모든 소구점별 템플릿이 공유하는 기본 타입입니다.
 */

export type VideoFormat = "reels" | "feed-square" | "feed-vertical";

export interface FormatSpec {
  width: number;
  height: number;
  /** 세이프존 (% 단위) - 텍스트/CTA 배치 금지 영역 */
  safeZone?: {
    top?: number;
    bottom?: number;
  };
}

export const FORMAT_SPECS: Record<VideoFormat, FormatSpec> = {
  reels: {
    width: 1080,
    height: 1920,
    safeZone: { top: 14, bottom: 35 },
  },
  "feed-square": {
    width: 1080,
    height: 1080,
  },
  "feed-vertical": {
    width: 1080,
    height: 1350,
  },
};

export interface BrandInfo {
  name: string;
  color: string;
  /** 로고 이미지 (public/ 기준) */
  logoSrc?: string;
}

export interface BaseConfig {
  brand: BrandInfo;
  /** 캠페인 팔레트 키 (palettes.ts 참조) */
  palette?: string;
  /** 영상 포맷 (기본: reels) */
  format?: VideoFormat;
  /** 씬 전환 길이 (프레임, 기본 10) */
  transitionDurationFrames?: number;
  /** 통합 나레이션 오디오 */
  narrationSrc?: string;
  /** 배경 음악 */
  bgmSrc?: string;
  /** BGM 볼륨 (0~1, 기본 0.3) */
  bgmVolume?: number;
}

export interface BaseSceneConfig {
  /** 씬 길이 (초) */
  durationSeconds: number;
  /** 나레이션 오디오 */
  narrationSrc?: string;
  /** 나레이션 딜레이 (프레임, 기본 5) */
  narrationDelay?: number;
}
