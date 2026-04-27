---
name: ops-morning-check
description: SAS Dashboard MCP 데이터를 바탕으로 운영팀장의 아침 점검을 수행한다. 주문 병목, 저재고 위험, SKU drill-down, 채널 상태를 본다.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# 운영팀장 아침 점검

Use this when:
- 운영팀장 / Operations Lead가 하루 시작 전에 운영 상태를 점검할 때
- 주문 backlog, 품절 위험, 채널 이상징후를 빠르게 찾아야 할 때
- 실행 전에 짧은 운영 액션리스트가 필요할 때

## Prerequisites
- 현재 프로젝트/세션에서 `sas_dashboard` MCP 서버를 사용할 수 있어야 한다.
- 초기 워크플로는 읽기 전용으로 유지한다.
- 우선 사용 도구:
  - `sas_ping`
  - `sas_whoami`
  - `analytics_order_status`
  - `orders_list`
  - `inventory_low_stock_alerts`
  - `inventory_get_by_sku`
  - `channels_stats`

## Workflow
1. `sas_whoami`로 workspace/role을 확인한다.
2. `analytics_order_status`로 전체 주문 상태 분포를 확인한다.
3. `orders_list`로 최근 주문 또는 backlog 주문을 본다.
4. `inventory_low_stock_alerts`로 저재고/안전재고 하회 항목을 본다.
5. 예외 SKU가 있으면 `inventory_get_by_sku`로 상세 drill-down 한다.
6. `channels_stats`로 채널 상태/동기화 맥락을 본다.
7. 결과를 짧은 운영 체크리스트와 즉시 액션으로 정리한다.

## Output format
다음 구조로 한국어로 답한다:
1. 오늘 주문 현황
2. 품절/안전재고 위험
3. 채널 이상 여부
4. 바로 처리할 액션 3개
5. 사람 확인 필요한 항목

## Rules
- 첫 점검은 읽기 전용으로 유지한다.
- 주문 상태 변경, 재고 조정, 동기화 실행을 자동으로 하지 않는다.
- SKU drill-down은 예외 항목이나 고위험 항목에만 사용한다.
- 가능하면 구체적인 숫자를 포함한다.
- 데이터가 불완전하면 확인 필요라고 표시한다.

## Good trigger phrases
- 오늘 주문 상태 체크해줘
- 재고 위험 뭐 있어?
- 출고 막히는 거 있나?
- 오늘 운영팀 체크리스트 줘

## Notes
- 이 스킬은 쓰기 자동화 스킬이 아니라 아침 점검 스킬이다.
- 긴 진단 리포트보다 짧은 액션리스트를 우선한다.
