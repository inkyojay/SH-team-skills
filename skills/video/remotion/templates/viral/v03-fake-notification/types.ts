/**
 * V03 - Fake Notification Overlay 광고
 *
 * iOS 알림 배너가 화면 위에서 내려오는 형태의
 * 시선 집중형 B급 감성 템플릿.
 */

export interface NotificationItem {
  /** 앱 이름 */
  appName: string;
  /** 알림 제목 (볼드) */
  title: string;
  /** 알림 본문 */
  body: string;
  /** 이전 알림 후 대기 시간 (초, 기본 2) */
  delay?: number;
  /** 표시 유지 시간 (초, 기본 2) */
  stayDuration?: number;
  /** 앱 아이콘 이모지 (기본 📱) */
  appIcon?: string;
}

export interface FakeNotificationConfig {
  /** 알림 목록 */
  notifications: NotificationItem[];
  /** 배경 이미지/영상 소스 (선택) */
  backgroundSrc?: string;
  /** 배경 색상 (backgroundSrc 없을 때, 기본 #1C1C1E) */
  backgroundColor?: string;
  /** 제품/콘텐츠 영역 설정 */
  productContent?: {
    text: string;
    subText?: string;
    emoji?: string;
  };
}
