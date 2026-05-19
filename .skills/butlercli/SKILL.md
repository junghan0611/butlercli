---
name: butlercli
description: "CLI-first home operations agent skill for Butler 힣봇. Manages household life operations via gogcli (Google Workspace). Use for repair requests, purchase tracking, car wash cadence, cleaning routines, schedule management, and family request follow-up. Primary interface for @glg_junghanacs_bot Telegram bot. Triggers: 'butler', 'butlercli', '집사', '세차', '수리', '구입', '청소', '일정 등록', 'home ops', 'car wash', 'repair', 'followup'."
user_invocable: true
---

# butlercli — Home Operations Skill

Agent skill for `~/repos/gh/butlercli`.
주 사용자는 텔레그램 힣봇(`@glg_junghanacs_bot`)이며 다른 봇도 호출 가능하다.

## Architecture

```
Telegram 힣봇 → butlercli (this skill) → gogcli → Google APIs
```

Google Workspace 연동(Calendar, Gmail, Drive, Tasks)은 모두 `gogcli`로 위임.
butlercli는 생활 운영 도메인 로직의 인터페이스 레이어다.

## Domains

| Domain | 역할 |
|--------|------|
| `car` | 세차/정비 주기 기록 및 조회 |
| `repair` | 수리 요청 접수, 연락처, 상태 추적 |
| `purchase` | 구입/비용 비교, 진행 관리 |
| `cleaning` | 청소·세탁 반복 작업 기록 |
| `schedule` | 캘린더 등록 및 후속 추적 (gogcli) |
| `followup` | 미완료 요청 목록 및 상태 갱신 |
| `report` | 주간/월간 생활 운영 현황 |

## CLI Surface (초안)

```bash
butler car wash log --date 2026-05-16
butler car wash last
butler car wash next --days 7
butler repair add --title "정수기 필터 교체"
butler purchase add --title "식기세척기 문의"
butler schedule add --title "세차" --when 2026-05-23T19:00
butler followup list
butler report weekly
```

## Current State

초반 설계 단계 — 구현 시작 전.
집사봇이 스킬로 쓰면서 직접 만들어가는 방식으로 진행 예정.
첫 vertical slice 후보: `butler car wash log` (실제 사례: 2026-05-16 셀프세차).

## Repo

- `~/repos/gh/butlercli/`
- `AGENTS.md`, `NEXT.md` 참조
- Digital garden: https://notes.junghanacs.com/botlog/20260518T094818
