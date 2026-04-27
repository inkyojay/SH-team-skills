---
name: daily-ops-brief
description: SAS Dashboard MCP 데이터를 바탕으로 전략실장용 일일 운영 브리프를 만든다. 병목, 채널 상태, 재고 경고, 결재 대기를 중심으로 본다.
version: 1.0.0
author: Hermes Agent
license: MIT
---

# 전략실장 일일 운영 브리프

Use this when:
- 전략실장 / Chief of Staff가 아침 또는 저녁 운영 브리프를 원할 때
- 라우팅 우선순위와 에스컬레이션 후보를 빨리 파악해야 할 때
- 전사 운영 상태를 짧고 실행 가능하게 요약해야 할 때

## Prerequisites
- 현재 프로젝트/세션에서 `sas_dashboard` MCP 서버를 사용할 수 있어야 한다.
- 읽기 전용 접근만 사용한다.
- 우선 사용 도구:
  - `sas_ping`
  - `sas_whoami`
  - `analytics_order_status`
  - `analytics_order_overview`
  - `inventory_low_stock_alerts`
  - `channels_stats`
  - `tasks_pending_approvals`

## Workflow
1. `sas_whoami`로 현재 workspace와 권한을 확인한다.
2. `analytics_order_status`로 주문 상태 병목을 확인한다.
3. `analytics_order_overview`로 채널별 추이와 주문 흐름을 본다.
4. `inventory_low_stock_alerts`로 저재고/품절 위험을 본다.
5. `channels_stats`로 채널/시스템 상태를 확인한다.
6. `tasks_pending_approvals`로 결재 대기 건을 확인한다.
7. 결과를 팀별 전달사항과 CEO 에스컬레이션 후보 중심으로 재구성한다.

## Output format
다음 구조로 한국어로 답한다:
1. 오늘 운영상태 한줄 요약
2. 긴급 이슈
3. 팀별 전달사항
4. CEO 에스컬레이션 필요 항목
5. 오늘 체크 KPI

## Rules
- 병목, 지연, 액션 중심으로 정리한다.
- 운영 이슈와 CEO 에스컬레이션 이슈를 분리한다.
- 사용자가 요청하지 않으면 raw table dump를 피한다.
- 승인 처리나 상태 변경 같은 write 액션은 자동 실행하지 않는다.
- 긴급 이슈가 없으면 정상 또는 특이사항 없음이라고 명시한다.

## Good trigger phrases
- 오늘 운영 브리프 줘
- 병목 뭐 있어?
- 오늘 누구한테 어떤 이슈 넘겨야 해?
- 결재 대기 뭐 있지?

## Notes
- 이 스킬은 실행 스킬이 아니라 조율/에스컬레이션 스킬이다.
- 누가 무엇을 왜 알아야 하는지 보이도록 액션 중심 문장으로 정리한다.
