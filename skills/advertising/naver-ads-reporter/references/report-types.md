# 대용량 보고서(StatReport) 타입별 가이드

네이버 검색광고 API는 **일자 단위**로 리포트를 발급합니다.
즉, 7일치 데이터가 필요하면 7번 발급해야 합니다.

---

## 리포트 타입 개요

| reportTp | 집계 단위 | 주요 지표 | 용도 |
|---|---|---|---|
| **AD** | 캠페인/광고그룹/소재 | 노출·클릭·비용·평균순위 | 기본 성과 조회 |
| **AD_DETAIL** | + 디바이스(PC/모바일) | 위와 동일 | 디바이스별 분석 |
| **AD_CONVERSION** | + 전환 유형 | 전환수·전환금액 | ROAS/CPA 분석 |
| **KEYWORD** | 키워드 단위 | 노출·클릭·비용·평균순위 | 키워드 효율 |
| **SHOPPING_PRODUCT** | NV_MID(상품) | 노출·클릭·비용 | 쇼핑검색광고 상품 성과 |
| **SHOPPING_PRODUCT_CONVERSION** | NV_MID + 전환 유형 | 전환·전환금액 | 상품별 ROAS |
| **SHOPPINGBRANDPRODUCT** | NV_MID(브랜드형) | 위와 동일 | 쇼핑검색광고 브랜드형 |

---

## 각 리포트 TSV 예상 컬럼

TSV 파일은 **헤더가 없을 수 있음**. 다음 순서로 파싱합니다.
(실제 첫 실행 시 실제 컬럼과 diff 필요 — POC 단계에서 확정)

### AD
```
date | customer_id | campaign_id | adgroup_id | keyword_id |
ad_id | business_channel_id | media | pc_mobile_type |
impressions | clicks | cost | avg_rank
```

### AD_CONVERSION
```
date | customer_id | campaign_id | adgroup_id | keyword_id |
ad_id | business_channel_id | media | pc_mobile_type |
conv_type | conversions | conversion_value
```
→ AD와 JOIN해야 ROAS 계산 가능.

### KEYWORD
```
date | customer_id | campaign_id | adgroup_id | keyword_id |
impressions | clicks | cost | avg_rank
```

### SHOPPING_PRODUCT
```
date | customer_id | campaign_id | adgroup_id |
product_id_nv_mid | product_name |
media | pc_mobile_type |
impressions | clicks | cost
```

---

## 전환 지표 합치기

AD(또는 KEYWORD) 리포트와 `_CONVERSION` 리포트는 **분리되어** 있습니다.
ROAS/CPA 계산하려면 같은 날짜+엔티티 ID로 JOIN 필요.

```python
# 의사 코드
merged = df_ad.merge(
    df_conv.groupby(['date', 'campaign_id', 'adgroup_id', 'keyword_id', 'ad_id'])
           .agg({'conversions': 'sum', 'conversion_value': 'sum'})
           .reset_index(),
    on=['date', 'campaign_id', 'adgroup_id', 'keyword_id', 'ad_id'],
    how='left'
)
merged['conversions'] = merged['conversions'].fillna(0)
merged['conversion_value'] = merged['conversion_value'].fillna(0)
```

**편의상 본 스킬 v1은 AD 리포트에 전환 컬럼을 직접 조회하는 간이 방식 사용.**
필요 시 CONVERSION 별도 호출하여 merge하는 기능 추가 예정 (v2).

---

## 전환 유형 코드 (conv_type)

| 코드 | 설명 |
|---|---|
| `1` | 직접 전환 (광고 클릭 후 당일 전환) |
| `2` | 간접 전환 (광고 클릭 후 7일 이내 재방문 전환) |
| (기타) | 맞춤 전환 등 |

**직접+간접 합산**하여 리포트에 노출하는 것이 일반적.

---

## PC/Mobile 구분 (pc_mobile_type)

| 코드 | 설명 |
|---|---|
| `1` | PC |
| `2` | 모바일 |

---

## Media 코드 (media)

네이버 통합검색, 쇼핑, 모바일 메인 등 매체 구분.
**썬데이허그 v1에서는 media 차원 집계는 생략** — 전체 집계 기준.
필요 시 v2에서 추가.

---

## 실제 사용 패턴 (본 스킬)

1. 전체 성과 리포트: `AD` 1개 + `AD_CONVERSION` 1개 (merge)
2. 쇼핑검색광고 상품 분석: `SHOPPING_PRODUCT` + `SHOPPING_PRODUCT_CONVERSION`
3. 키워드 효율 분석: `KEYWORD`
4. 디바이스 분석 (요청 시): `AD_DETAIL`

**v1은 단순화를 위해 `AD` 하나로 시작** → 전환 컬럼이 AD 리포트에 포함되는지 실제 검증 후 CONVERSION merge 여부 결정.
