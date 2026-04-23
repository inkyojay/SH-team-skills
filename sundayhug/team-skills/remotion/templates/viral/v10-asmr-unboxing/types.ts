/**
 * V10 - ASMR Unboxing
 *
 * 클로즈업 제품 샷 + 느린 줌인으로 만족감을 주는
 * ASMR 스타일 언박싱 템플릿.
 * B급 시리즈의 예외: 프리미엄 감성 (ASMR은 고급스러워야 함).
 */

export interface UnboxLayer {
  /** 미디어 소스 (이미지, public/ 기준) */
  mediaSrc: string;
  /** 레이어 라벨 (선택, 최소한의 텍스트) */
  label?: string;
  /** 이 레이어의 표시 시간 (초) */
  durationSeconds: number;
}

export interface AsmrUnboxingConfig {
  /** 언박싱 레이어 목록 (순서대로 표시) */
  layers: UnboxLayer[];
  /** 제품명 (마지막에 표시) */
  productName: string;
  /** 최종 제품 뷰티샷 이미지 (선택) */
  finalRevealSrc?: string;
  /** 배경 색상 (기본 #0a0a0a) */
  bgColor?: string;
  /** 워밍 오버레이 강도 (0~1, 기본 0.15) */
  warmOverlayIntensity?: number;
  /** 브랜드명 (선택, 좌하단에 작게) */
  brandName?: string;
}
