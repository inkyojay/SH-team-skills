/**
 * V07 - Countdown Listicle
 *
 * "Top 3 이유" 스타일 역순 카운트다운 템플릿.
 * 각 항목이 드라마틱하게 등장하며 #1은 특별 처리.
 */

export interface CountdownItem {
  /** 카운트다운 번호 (3, 2, 1 등) */
  number: number;
  /** 항목 설명 텍스트 */
  text: string;
  /** 배경 이미지/미디어 (선택) */
  mediaSrc?: string;
}

export interface CountdownConfig {
  /** 영상 제목 (예: "이걸 안 쓰는 3가지 이유") */
  title: string;
  /** 카운트다운 항목 목록 (number 내림차순 권장) */
  items: CountdownItem[];
  /** CTA 텍스트 (마지막에 표시, 선택) */
  ctaText?: string;
  /** 배경 색상 (기본 #0d0d0d) */
  bgColor?: string;
  /** 번호 색상 (기본 그라디언트) */
  numberColor?: string;
  /** 각 항목 표시 시간 (초, 기본 4) */
  itemDurationSeconds?: number;
}
