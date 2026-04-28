# 카카오 메시지 발송 전 검증 체크리스트

> 빌드 후 카카오 비즈채널 콘솔에 업로드하기 전 반드시 확인할 6개 체크 항목입니다. `kakao_validator.py`가 1~5번을 자동 검증, 6번은 사용자가 직접 확인.

---

## 1. ✅ 사이즈 정확성

| 타입 | 정확 매칭 필수 사이즈 |
|---|---|
| 02-wide-image | 800 × 600 |
| 03-wide-list (헤더) | 800 × 400 |
| 03-wide-list (리스트) | 800 × 800 |
| 04-carousel-feed | 800 × 600 (또는 800 × 400, 모두 통일) |
| 05-carousel-commerce | 800 × 800 |
| 06-commerce | 800 × 600 |
| 07-alimtalk-image | 800 × 400 |

자동 검증: `kakao_validator.validate_size(png_path, expected)`

---

## 2. ✅ 캐러셀 카드 비율 일관성

캐러셀(04, 05)은 **모든 카드가 같은 사이즈**여야 카카오에서 캐러셀로 작동.

자동 검증:
```python
kakao_validator.validate_carousel_uniformity([
    "card01_800x800.png",
    "card02_800x800.png",
    "card03_800x800.png",
])
# → True (모두 800×800)
```

실패 사례:
- 인트로 카드만 800×600, 후속은 800×800 → 캐러셀 미작동, 단일 카드만 보임
- 카드 수 1개 또는 8개 이상 → 캐러셀 미작동 (2~7장 한도)

---

## 3. ✅ 용량 한도

| 타입 | 한도 | 초과 시 |
|---|---|---|
| 알림톡 (07, 08) | **500KB** | **즉시 발송 거부** |
| 친구톡 (01~06) | 2MB | 카카오가 자동 압축 시도, 화질 손실 |
| 비즈보드 (BB) | 300KB | 등록 거부 |

자동 검증 + 자동 압축:
```python
kakao_validator.compress_to_target("notification.png", target_kb=500)
# Pillow quality 95→85→75→65 단계적 하향, 한도 내 진입 시 중단
# 65에서도 초과 시 사용자에게 원본 이미지 리사이즈 요청
```

---

## 4. ✅ 알림톡 카피 검열

알림톡(07, 08)에 광고/할인 키워드 포함 시 자동 차단.

자동 검증:
```python
banned = kakao_validator.validate_copy_for_notification("지금 50% 할인 이벤트")
# → ['할인', '%', '이벤트']  (키워드 검출됨 → 빌드 실패)
```

상세 키워드 리스트는 [kakao-copy-rules.md](./kakao-copy-rules.md) 참조.

---

## 5. ✅ 이미지 해상도 (선명도)

원본 이미지가 200dpi 미만이면 800px 캔버스에 늘어나면서 깨짐.

권장:
- 친구톡 와이드/이미지형: 원본 ≥ 1600×1200 (2배 supersampling)
- 캐러셀 커머스: 원본 ≥ 1600×1600
- 알림톡: 원본 ≥ 1600×800

자동 검증:
```python
kakao_validator.validate_source_resolution(image_path, min_width=1600)
# → False면 경고만 (차단 X — 사용자 판단)
```

---

## 6. ⚠️ 수동 확인 (자동화 불가)

### A. 카피 의미 검증
- 오타/맞춤법 (`kakao_validator`는 키워드만 검사, 자연어 검증 X)
- 가격/할인율 정확성 (DB 값 vs 입력값)
- CTA URL 작동 여부

### B. 이미지 적합성
- 모델 초상권 (계약 만료 모델 사용 시 법적 문제)
- 경쟁사 로고/제품 노출
- 원본 저작권 (프리뷰엔 OK여도 발송엔 부적합한 이미지)

### C. 발송 정책
- 친구톡 야간 발송 금지 (21시 ~ 익일 8시)
- 알림톡 발송 사유의 정당성 (실제 주문/거래/회원 활동 기반)
- 채널 친구 수 vs 발송량 (전체 발송 시 비용 확인)

---

## 검증 자동화 — 빌드 시점

```bash
python3 scripts/kakao_factory.py build path/to/config.py --strict
```

`--strict` 플래그 시 1~5번 자동 검증 실행, 어느 하나라도 실패 시 빌드 중단.

`--warn-only` 플래그 시 검증 실패해도 진행 (검토용 빌드).
