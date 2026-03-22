/**
 * V02 - KakaoTalk Chat 대화형 광고
 *
 * 카카오톡 채팅 인터페이스를 재현하여
 * 대화 형태로 제품/서비스를 소개하는 B급 감성 템플릿.
 */

export interface ChatMessage {
  /** 발신자 이름 */
  sender: string;
  /** 메시지 텍스트 */
  text: string;
  /** 내 메시지 여부 (오른쪽 정렬) */
  isMe: boolean;
  /** 이전 메시지 후 대기 시간 (초, 기본 1) */
  delay?: number;
  /** 이미지 URL (제품 이미지 등) */
  imageSrc?: string;
  /** 이모티콘/이모지 (텍스트 대신 큰 이모지) */
  emoji?: string;
}

export interface KakaoChatConfig {
  /** 채팅 메시지 목록 */
  messages: ChatMessage[];
  /** 채팅방 제목 */
  chatTitle: string;
  /** 참여자 수 (헤더 표시, 기본 2) */
  participantCount?: number;
  /** 마지막 제품 공개 메시지 */
  productReveal?: {
    productName: string;
    productImage?: string;
    linkText?: string;
  };
  /** 타이핑 인디케이터 표시 시간 (초, 기본 0.8) */
  typingDuration?: number;
}
