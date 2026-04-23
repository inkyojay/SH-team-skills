/**
 * V08 - Order vs Reality (주문 vs 현실)
 *
 * "What I ordered" vs "What I got" 밈 스타일 비교 템플릿.
 * isMatch 여부에 따라 긍정(신뢰) 또는 부정(코미디) 연출.
 */

export interface OrderVsRealityConfig {
  /** "주문한 것" 이미지 (public/ 기준) */
  orderImageSrc: string;
  /** "받은 것" 이미지 (public/ 기준, 미지정 시 orderImageSrc 재사용) */
  realityImageSrc?: string;
  /** 제품명 */
  productName: string;
  /** 기대=현실 여부 (true: 긍정/신뢰, false: 코미디/실망) */
  isMatch: boolean;
  /** 추가 캡션 (선택) */
  caption?: string;
  /** 주문 라벨 (기본: "주문한 것") */
  orderLabel?: string;
  /** 현실 라벨 (기본: "받은 것") */
  realityLabel?: string;
}
