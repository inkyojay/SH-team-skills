/**
 * V01 - iPhone Notes App 타이핑 광고
 *
 * Apple Notes 앱 UI를 재현하여 타이핑 애니메이션으로
 * 제품/브랜드 메시지를 전달하는 B급 감성 템플릿.
 */

export interface NotesLine {
  /** 타이핑할 텍스트 */
  text: string;
  /** 이전 줄 완성 후 대기 시간 (초, 기본 0.3) */
  delay?: number;
  /** 의도적 오타를 남길 인덱스 (선택) */
  typoAt?: number;
  /** 볼드 처리 여부 */
  bold?: boolean;
}

export interface NotesAppConfig {
  /** 타이핑할 줄 목록 */
  lines: NotesLine[];
  /** 브랜드명 (노트 상단 표시) */
  brandName?: string;
  /** 제품명 (하이라이트 처리) */
  productName?: string;
  /** CTA 텍스트 (마지막에 표시) */
  ctaText?: string;
  /** 글자당 타이핑 속도 (초, 기본 0.06) */
  charSpeed?: number;
  /** CTA 배경색 (기본 #007AFF) */
  ctaColor?: string;
}
