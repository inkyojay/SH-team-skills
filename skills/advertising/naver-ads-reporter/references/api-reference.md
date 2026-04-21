# 네이버 검색광고 API 레퍼런스

**공식 문서**: https://naver.github.io/searchad-apidoc/

---

## 기본 정보

| 항목 | 값 |
|---|---|
| Base URL | `https://api.searchad.naver.com` |
| 인증 | HMAC-SHA256 서명 (hex digest) |
| Content-Type | `application/json; charset=UTF-8` |

## 인증 헤더

모든 요청에 필수:

| 헤더 | 값 |
|---|---|
| `X-Timestamp` | Unix 밀리초 (`str(int(time.time() * 1000))`) |
| `X-API-KEY` | 액세스라이선스 |
| `X-Customer` | 광고주 번호 (CUSTOMER_ID) |
| `X-Signature` | HMAC-SHA256 hex digest |

### 서명 생성
```python
message = f"{timestamp}.{method}.{path}"
signature = hmac.new(
    secret_key.encode("utf-8"),
    message.encode("utf-8"),
    hashlib.sha256
).hexdigest()
```

**주의**: `path`는 query string 미포함, 순수 경로만.
예: `/stat-reports` (O), `/stat-reports?statDt=2026-04-20` (X)

---

## 엔드포인트 (이 스킬에서 사용)

### 1. 캠페인/광고그룹/키워드 마스터

| Method | Path | 설명 |
|---|---|---|
| GET | `/ncc/campaigns` | 전체 캠페인 목록 |
| GET | `/ncc/campaigns/{id}` | 단일 캠페인 상세 |
| GET | `/ncc/adgroups?nccCampaignId={id}` | 광고그룹 목록 |
| GET | `/ncc/keywords?nccAdgroupId={id}` | 키워드 목록 |
| GET | `/ncc/ads?nccAdgroupId={id}` | 소재 목록 |

### 2. 대용량 보고서 (핵심)

| Method | Path | 설명 |
|---|---|---|
| POST | `/stat-reports` | 보고서 발급 요청 |
| GET | `/stat-reports/{id}` | 상태 조회 |
| GET | `/stat-reports` | 내 보고서 목록 |
| DELETE | `/stat-reports/{id}` | 보고서 삭제 |

**POST body**:
```json
{ "reportTp": "AD", "statDt": "2026-04-20" }
```

**Response**:
```json
{
  "reportJobId": 12345,
  "status": "REGIST",
  "reportTp": "AD",
  "statDt": "2026-04-20T00:00:00.000Z",
  "registTm": "2026-04-21T03:45:12.000Z"
}
```

**상태 전이**: `REGIST` → `RUNNING` → `BUILT` (완료) / `FAILED` / `EXPIRED`

**BUILT 응답에 `downloadUrl` 포함** — 이 URL로 TSV 다운로드.

### 3. 실시간 통계 (보조)

| Method | Path | 설명 |
|---|---|---|
| GET | `/stats` | 당일 누적 (제한적) |

지연 있음, 대용량 리포트 대비 부정확. 긴급 모니터링용.

---

## Rate Limit

- 시간당 호출 수 제한 존재 (정확한 수치는 공식 문서 참조)
- 초과 시 HTTP 429 반환
- **대응**: exponential backoff (본 스킬 기본 내장)
  - 429 수령 시 20s → 40s → 80s 대기
  - 3회 실패 시 예외 발생

## 데이터 제공 범위

- 최대 과거 365일
- 당일 데이터는 약 2~3시간 지연 반영
- 쇼핑검색광고 브랜드형은 2021-03-31 이후만

---

## 주요 에러 코드

| HTTP | 의미 | 대응 |
|---|---|---|
| 400 `invalid.signature` | 서명 오류 | timestamp 단위(ms), path 정확성, secret key 재확인 |
| 401 `unauthorized` | 인증 실패 | API_KEY/CUSTOMER_ID 재확인 |
| 403 `forbidden` | 권한 없음 | 해당 리소스 소유 여부 확인 |
| 404 | 리소스 없음 | ID 철자 확인 |
| 429 `rate.limit.exceeded` | 호출 초과 | 대기 후 재시도 |
| 500~503 | 서버 오류 | 재시도 |

---

## 보안 주의

- `SECRET_KEY`는 **절대 로그/응답/URL에 노출되면 안 됨**
- 클라이언트 사이드 (웹 브라우저) 호출 금지 — 반드시 서버에서만
- 키 유출 의심 시 즉시 searchad.naver.com에서 재발급

---

## 참고 링크

- 공식 API 문서: https://naver.github.io/searchad-apidoc/
- 공식 샘플 코드 (Python): https://github.com/naver/searchad-apidoc
- 관리 콘솔: https://searchad.naver.com/my-screen
- API 사용 신청/확인: 광고시스템 > 도구 > API 사용 관리
