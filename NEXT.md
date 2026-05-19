# NEXT.md

## 현재 상태

설계 문서 완료. 구현 시작 전.
집사봇(`@glg_junghanacs_bot`)이 스킬로 쓰면서 직접 만들어가는 방식으로 진행.

---

## 다음 작업 (우선순위 순)

### 1. 저장 계층 결정

구현 전에 반드시 결정해야 할 것:

- [ ] 파일 기반 (TOML/JSON) vs SQLite
- [ ] private 데이터 위치: `~/org/family/` or separate private repo
- [ ] gogcli Calendar를 primary store로 볼지, local store와 병행할지
- [ ] 에이전트가 호출하는 방식: bash 스크립트? Python typer/click?

**권장 방향**: TOML 파일 로컬 저장 → gogcli Calendar 연동. DB 도입은 그 다음.

### 2. 첫 vertical slice — `butler car wash`

가장 단순하고 이미 실제 사례가 있음 (2026-05-16 셀프세차):

```bash
butler car wash log --date 2026-05-16
butler car wash last          # 마지막 세차 언제?
butler car wash next --days 7 # 7일 후 예정 알림
```

이 세 커맨드만 동작하면 "세차 언제 했지?" 질문에 답할 수 있다.

### 3. CLI 표면 초안 확정

`butler ...` 명령군 5~7개 확정 후 `docs/cli-design.md`에 입력/출력 예시 기록.

후보 도메인: `repair`, `purchase`, `car`, `cleaning`, `schedule`, `followup`, `report`

### 4. gogcli 연동 설계 문서

`docs/gogcli-integration.md`:

- 어떤 gogcli 명령을 어떤 butler 도메인이 호출하는지
- Calendar 이벤트 포맷 (제목 규칙, 메타 필드)
- 조회 패턴: "이번 주 생활 운영 일정" 등

### 5. Telegram 봇 연결 설계 문서

`docs/telegram-integration.md`:

- `workspace-glg/`의 힣봇이 butlercli 스킬을 어떻게 호출하는지
- 메시지 파싱 → 도메인 매핑 예시
- 응답 포맷 (가족이 보는 텔레그램 메시지)

---

## 하지 않을 것

- Google API 직접 구현 — gogcli에 위임
- 대형 DB 스키마 선행 설계 — 실전 사례에서 출발
- 새 폴더/문서 구조 먼저 잡기 — 커맨드 동작 후에 구조가 나온다
