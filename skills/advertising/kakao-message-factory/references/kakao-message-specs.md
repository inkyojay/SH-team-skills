# 카카오톡 비즈니스 메시지 스펙 (공식 가이드 기반)

> 본 문서는 카카오 비즈니스/카카오 i 비즈메시지 공식 가이드를 기반으로 정리한 메시지 디자인 스펙입니다. 스킬은 이 스펙을 검증 기준으로 사용합니다.

---

## 메시지 8타입 사이즈 표

| # | 타입 | 카카오 코드 | 캔버스 사이즈 | 비율 | 용량 한도 | 본문 한도 | 버튼 | 비고 |
|---|---|---|---|---|---|---|---|---|
| 01 | 이미지형 (친구톡) | FI | 가로 ≥500px | 2:1 ~ 3:4 | ≤2MB | 400자 | 1 | 가로 비율 강제 |
| 02 | 와이드 이미지형 (친구톡) | FW | **800×600** | 4:3 | ≤2MB | 76자 | 1 | 가장 일반적인 광고 |
| 03 | 와이드 리스트형 (친구톡) | FL | 800×400 (헤더) + 800×800 (리스트) | — | ≤2MB | — | 리스트당 1 | 리스트 3~4개 |
| 04 | 캐러셀 피드형 (친구톡) | FC | 800×600/카드 (또는 800×400) | 4:3 또는 2:1 | ≤2MB/카드 | 76자/카드 | 카드당 ≤2 | 카드 2~6, **모두 같은 비율** |
| 05 | 캐러셀 커머스형 (친구톡) | FA | 800×800/카드 | 1:1 | ≤2MB/카드 | 상품명 20자 | 카드당 1~2 | 인트로+상품 ≤7장 |
| 06 | 커머스형 (친구톡) | FC2 | 800×600 | 4:3 | ≤2MB | — | 1~2 | 단일 제품 + 가격 |
| 07 | 알림톡 이미지형 | AI | **800×400** | **2:1 강제** | **≤500KB** | 1,000자 | ≤2 | **광고/할인 카피 절대 금지** |
| 08 | 아이템리스트 알림톡 | AL | 가변 | — | ≤500KB | 700자 | ≤2 | 아이템 ≤10개 |

### 추가 참고 — 비즈보드 (카톡 채팅 탭 상단 광고)
- 사이즈: **1029×258px** (구 222px → 258px로 변경됨)
- 포맷: PNG-24/32 (투명 배경 필수)
- 용량: ≤300KB
- 배경 #f3f3f3 유사색 사용 금지

### 추가 참고 — 모먼트 디스플레이 광고 (2025.06 기준)
- 1:1 (≥500×500)
- 2:1 (≥1200×600)

---

## 비율/사이즈 검증 규칙

| 검증 | 적용 타입 | 실패 시 결과 |
|---|---|---|
| 캔버스 정확 매칭 | 02, 03, 05, 06, 07 | 카카오 비즈채널 발송 거부 |
| 비율만 강제 (사이즈 가변) | 01, 04 | 비율 어긋나면 자동 크롭됨 |
| 카드 간 비율 일관성 | 04, 05 (캐러셀) | 캐러셀 미작동 (모든 카드 같은 사이즈여야 함) |
| 용량 한도 | 전체 | 알림톡 500KB 초과 시 즉시 발송 거부, 친구톡은 자동 압축 시도 |

---

## 카피 글자수 한도 (실측)

| 타입 | 본문 | 제목 | CTA 버튼 |
|---|---|---|---|
| 친구톡 와이드 이미지 (02) | 76자 | — | 14자 |
| 친구톡 캐러셀 커머스 상품명 (05) | 20자 | — | 14자 |
| 친구톡 캐러셀 피드 (04) | 76자/카드 | — | 14자/버튼 |
| 알림톡 (07, 08) | 1,000자 (07) / 700자 (08) | — | 14자 |
| 강조표기형 알림톡 강조문구 | 50자 (취소선 포함) | — | — |

**캐러셀 커머스 가격 표시**: 정가/할인가 모두 숫자만 (예: "29900"), 통화 기호는 템플릿이 자동 추가.

---

## 디자인 제약

1. **JS/애니메이션 완전 금지** — HTML → 이미지 변환 용도 (정적 캡처)
2. **`object-fit: cover` 필수** — 모든 이미지는 비율 맞춤 자동 크롭
3. **알림톡 광고 카피 금지** — `kakao_validator.BANNED_WORDS_NOTIFICATION` 키워드 검출 시 빌드 차단
4. **다크 팔레트 (midnight-luxe)** — `data-palette="midnight-luxe"` 시 자동 다크 오버라이드 적용

---

## 출처 (공식)

- 카카오 비즈니스 가이드 - 알림톡 콘텐츠: https://kakaobusiness.gitbook.io/main/ad/infotalk/content-guide
- 카카오 비즈니스 가이드 - 비즈보드 제작: https://kakaobusiness.gitbook.io/main/ad/moment/performance/talkboard/content-guide
- 카카오 비즈니스 가이드 - 채널 메시지: https://kakaobusiness.gitbook.io/main/channel/run/message
- 카카오 비즈니스 가이드 - 디스플레이 광고: https://kakaobusiness.gitbook.io/main/ad/moment/performance/displayad
- 카카오 i 비즈메시지 공통 가이드: https://docs.kakaoi.ai/kakao_i_connect_message/bizmessage/common_guide/
- 카카오 고객센터 - 와이드 이미지형 권장 사이즈: https://cs.kakao.com/helps_html/1073188049

## 출처 (3rd-party 보조)

- NHN Cloud 친구톡 콘솔 가이드: https://docs.nhncloud.com/ko/Notification/KakaoTalk%20Bizmessage/ko/friendtalk-console-guide/
- Infobip KakaoTalk Message Types: https://www.infobip.com/docs/kakaotalk/message-types
- 인포뱅크 친구톡 API: https://infobank-guide.gitbook.io/kkorest-api/api-reference/send/friendtalk
- ifdo - 친구톡 신규 유형: https://ifdo.co.kr/blog/572
- bizgo 친구톡 가이드: https://blog.bizgo.io/howto/friends-talk/
