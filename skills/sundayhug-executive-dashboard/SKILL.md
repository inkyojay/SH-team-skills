---
name: executive-dashboard
description: SAS Dashboard MCP의 읽기 전용 데이터를 바탕으로 대표이사용 SundayHug 경영 대시보드를 만든다.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# 대표이사 경영 대시보드

Use this when:
- 대표이사/CEO가 일간 또는 주간 사업 요약을 원할 때
- SAS Dashboard의 실시간 데이터를 경영자용으로 압축해야 할 때
- raw 데이터 나열 없이 즉시 의사결정 포인트를 찾아야 할 때

## Prerequisites
- 현재 프로젝트/세션에서 `sas_dashboard` MCP 서버를 사용할 수 있어야 한다.
- 읽기 전용 접근만 사용한다.
- 우선 사용 도구:
  - `sas_ping`
  - `sas_whoami`
  - `analytics_sales_summary`
  - `analytics_order_status`
  - `inventory_low_stock_alerts`
  - `finance_cashflow_get`

## Workflow
1. 필요하면 `sas_ping`으로 MCP 연결 상태를 확인한다.
2. `sas_whoami`로 tenant/workspace와 현재 권한을 확인한다.
3. `analytics_sales_summary`로 매출 추세를 읽는다.
4. `analytics_order_status`로 주문 병목 상태를 읽는다.
5. `inventory_low_stock_alerts`로 재고 위험을 읽는다.
6. `finance_cashflow_get`으로 현금흐름 상태를 읽는다.
7. 결과를 대표이사용 브리프로 압축한다. 핵심은 숫자 나열이 아니라 리스크, 변화, 결정 포인트다.

## Output format
다음 구조로 한국어로 답한다:
1. 한줄 요약
2. 매출 요약
3. 주문 상태 요약
4. 재고 위험
5. 현금흐름
6. 오늘 의사결정 포인트 3개 이내

## Rules
- 사용자가 요청하지 않으면 raw JSON이나 긴 row dump를 출력하지 않는다.
- 숫자 나열보다 해석과 우선순위를 우선한다.
- 모든 지표보다 예외, 리스크, 변화에 집중한다.
- write 가능한 도구는 호출하지 않는다.
- 특정 지표를 못 읽었으면 추측하지 말고 무엇이 비어 있었는지 명시한다.

## Good trigger phrases
- 오늘 경영 브리프 줘
- 이번주 실적 요약해줘
- 대표이사 대시보드 보여줘
- 지금 위험한 숫자 뭐야

## Notes
- 사용자가 더 자세히 보고 싶어 하면 필요한 섹션만 drill-down 한다.
- 분석가 스타일보다 경영자 스타일의 짧고 명확한 언어를 선호한다.
