# butlercli

CLI-first home operations agent skill.

`butlercli`는 **집사힣봇(Butler 힣봇)의 에이전트 스킬**이자 공개 작업 저장소다.
텔레그램 힣봇(`@glg_junghanacs_bot`)이 주 사용자이고, 다른 봇도 같은 스킬을 쓸 수 있다.

백엔드는 `gogcli`다. 캘린더, Gmail, Drive, Tasks 같은 Google Workspace 제어는
이미 gogcli가 담당하고 있다. butlercli는 그 위에서 **생활 운영 도메인의 인터페이스**로 동작한다.

목적은 단지 생활 잔무 자동화가 아니다.
집사는 가족의 요청을 기억하고, 일정과 맥락을 이어받고,
시간이 지나도 계속 보좌하는 **라이프 에이전트**다.

---

## 아키텍처

```
텔레그램 힣봇  (@glg_junghanacs_bot, openai/gpt-5.4)
      │
      ▼
 butlercli  (agent skill — 생활 운영 인터페이스)
      │
      ▼
  gogcli  (Google Workspace: Calendar / Gmail / Drive / Tasks / Chat)
      │
      ▼
 Google APIs
```

- **텔레그램 봇**: 가족의 요청이 들어오는 인터페이스. 힣봇이 주 사용자.
- **butlercli**: 생활 운영 도메인 로직. 에이전트가 스킬로 호출.
- **gogcli**: Google 쪽 모든 연동. 캘린더 등록, 일정 조회, 메일 전송 등.

집사봇이 직접 만들면서 쓰는 방식으로 발전시킨다.

---

## 담당 도메인

- 수리 요청 접수 및 상태 추적
- 구입/비용 비교 및 진행 관리
- 자동차 세차·정비 주기 기록
- 청소·세탁·건조 같은 반복 생활 작업
- 캘린더 등록과 후속 추적 (gogcli 연동)
- 가족 요청을 **시간축 위의 관리 가능한 사건**으로 바꾸는 일

---

## 작업 원칙

1. **에이전트 스킬 우선** — 명령은 에이전트가 호출하는 단위로 설계한다.
2. **gogcli 연동** — Google 쪽은 gogcli가 담당. 중복 구현하지 않는다.
3. **실전 사건 우선** — 실제 수리/세차/구입 사례에서 명령이 나온다.
4. **공개 저장소 / 사적 데이터 분리** — 운영 원리, 스키마, 샘플만 공개.
5. **작게 세운다** — 기능 하나를 끝까지 세우고 다음으로 간다.

---

## CLI 표면 초안

아직 확정은 아니지만 현재 의도.

```bash
butler inbox add "식기세척기 문의"
butler task create repair --title "정수기 필터 교체"
butler car wash log --date 2026-05-16
butler car wash last
butler schedule add --title "세차" --when 2026-05-23T19:00
butler followup list
butler report weekly
```

도메인 후보:

- `repair`
- `purchase`
- `car`
- `cleaning`
- `schedule`
- `family`
- `report`

---

## 저장 계층 (미결)

결정이 필요한 사항:

- 파일 기반 (TOML/JSON) vs SQLite
- private 데이터 위치: `~/org/family/` 또는 별도 private repo
- gogcli Calendar를 primary store로 볼지, butlercli local store와 병행할지

---

## 디렉토리

```text
butlercli/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── NEXT.md
└── docs/          # 설계 문서 (필요 시 추가)
```

---

## 방향 전환 메모

이 저장소는 `family-config`에서 이름을 바꿨다. 이전 방향:

- 템플릿 중심, family knowledge base 전체 설계, 큰 문서 선행

현재 방향:

- CLI-first, agent skill-first, 실제 운영 루프 먼저

> Butler 힣봇은 단순한 home operations bot이 아니라,
> 가족의 생활 사건과 시간축을 기억하며 장기적으로 보좌하는 life agent다.

---

## 관련 노트

- [butlercli 집사힣봇](https://notes.junghanacs.com/botlog/20260518T094818) — 생활 운영 루프 설계 배경 (digital garden)
