# AGENTS.md

This repository is for **butlercli**, a CLI-first home operations agent skill.

## Identity

`butlercli` is the agent skill and public repo for Butler 힣봇.
It was renamed from `family-config`.

- **Primary user**: 텔레그램 힣봇 (`@glg_junghanacs_bot`, `openai/gpt-5.4`, `workspace-glg/`)
- **Other bots**: 같은 스킬을 다른 봇도 쓸 수 있다
- **Google integration**: `gogcli` — Calendar, Gmail, Drive, Tasks, Chat 연동은 모두 gogcli가 담당

## Architecture

```
Telegram 힣봇
    ↓
butlercli (agent skill)
    ↓
gogcli (Google Workspace backend)
```

butlercli는 생활 운영 도메인 로직의 인터페이스 레이어다.
Google 쪽 실제 제어는 gogcli로 위임한다. 중복 구현하지 않는다.

## What this repo is about

Main domains:
- repairs — 수리 요청 접수, 연락처, 상태 추적
- purchases — 구입/비용 비교, 진행 관리
- car — 세차/정비 주기 기록
- cleaning — 청소·세탁 반복 작업
- schedule — 캘린더 등록 및 후속 추적 (gogcli 연동)
- report — 주간/월간 생활 운영 현황

Goal:
Turn messy household requests into manageable, time-based operational events.

## Working style

- Prefer small vertical slices over large speculative architecture
- Define command surface first (agent calls these as skill)
- gogcli handles Google backend — do not reimplement
- Keep public/private boundary strict (family data stays outside this repo)
- Build by using: 집사봇이 직접 만들면서 쓰는 방식으로 발전

## Read first

1. `README.md`
2. `NEXT.md`
3. relevant implementation files (when they exist)

## Current state

초반 정리 단계 — 설계 문서 완료, 구현 시작 전.
집사봇이 스킬로 쓰면서 직접 만들어가는 방식으로 진행 예정.
