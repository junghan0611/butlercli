# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Context

**Family-Config**는 AI 에이전트 기반 가족 생활 관리 시스템으로, Org-mode, Denote 파일명 규칙, PARA 방법론을 활용합니다.

### 핵심 철학
- **Actionable Intelligence**: 모든 텍스트는 실행 가능한 데이터
- **Denote Naming**: `YYYYMMDDTHHMMSS--한글-제목__family_영역_태그.org` 형식
- **PARA Method**: Projects/Areas/Resources/Archives 구조
- **MCP Integration**: Property 기반 AI 도구 실행

## Directory Structure

```
family-config/
├── finance/           # 재무 관리
├── education/         # 교육 관리
├── childcare/         # 육아 관리
├── travel/            # 여행/휴가 관리
├── events/            # 경조사 관리
├── calendar/          # 통합 일정 관리
├── memory/            # AI 메모리 (PARA)
│   ├── projects/      # 활성 프로젝트
│   ├── areas/         # 지속적 관심사
│   ├── resources/     # 재사용 패턴
│   └── archives/      # 완료 항목
└── scripts/           # 자동화 스크립트
    └── photo_organizer/ # Samsung SmartSwitch 사진 정리 도구
```

각 도메인 디렉토리는 다음 구조를 따릅니다:
- `templates/`: 재사용 가능한 Org-mode 템플릿
- `schemas/`: 데이터 구조 정의
- `README.md`: 영역별 사용 가이드

## File Naming Convention (Denote)

### 형식
```
YYYYMMDDTHHMMSS--한글-제목__family_영역_태그들.org

예시:
20251014T120000--여름휴가-제주도__family_travel_active.org
20251014T120100--월별-예산-2025-10__family_finance_tracking.org
```

### 태그 시스템
- `__active`: 현재 진행 중
- `__urgent`: 긴급
- `__blocked`: 차단됨
- `__template`: 템플릿
- `__done`: 완료됨

### 타임스탬프 생성
```bash
TZ='Asia/Seoul' date '+%Y%m%dT%H%M%S'
```

## Org-mode File Structure

모든 Org 파일은 다음 프론트매터를 포함해야 합니다:
```org
#+title:      제목
#+date:       [YYYY-MM-DD Day HH:MM]
#+filetags:   :family:영역:태그들:
#+identifier: YYYYMMDDTHHMMSS
#+export_file_name: YYYYMMDDTHHMMSS.md
```

### Actionable Item 작성법
```org
* 항목 제목 :AGENT:ACTION:
:PROPERTIES:
:AGENT_ACTION: mcp_tool_name
:INPUT_PARAM1: value1
:STATUS: TODO
:CREATED: [timestamp]
:END:

** Agent Instructions
#+begin_src yaml
action: mcp_tool_name
query: "search query"
output:
  - format: org_table
  - fields: [field1, field2]
#+end_src

** Results
[Agent 실행 후 자동 추가]
```

## Python Development

### Photo Organizer (scripts/photo_organizer/)

Samsung SmartSwitch 백업을 Denote 네이밍으로 정리하는 범용 도구

#### 환경 설정
```bash
cd scripts/photo_organizer
python3 -m venv venv
source venv/bin/activate
pip install pillow python-dateutil exifread
```

#### 실행
```bash
# Dry run 테스트
python family_photo_organizer.py <source> <target> --dry-run --limit 10

# 구조 분석만
python family_photo_organizer.py <source> <target> --analyze-only

# 실제 처리
python family_photo_organizer.py <source> <target>
```

#### 출력 구조
```
target/
├── photos/YYYY/
├── videos/YYYY/
├── screenshots/YYYY/
├── documents/YYYY/
└── logs/
```

## Data Flow

### Template → Actual Data
- **템플릿**: `~/repos/gh/family-config/` (GitHub Public)
- **실제 데이터**: `~/org/family/` (Private Git)
- 템플릿을 복사하여 사용, 실제 데이터는 프라이빗 저장소에서 별도 관리

### AI Agent Workflow
```
1. Property 파싱 (Org-mode)
2. MCP 도구 실행
3. 결과를 Org table/Ledger/iCal로 기록
4. ~/org/family/에 저장
5. 패턴 발견 시 memory/에 저장
6. 템플릿 개선 시 templates/에 반영
```

## Integration with Broader Ecosystem

이 프로젝트는 **시간과정신의방(Time and Mind Room)** 생태계의 일부:
- `claude-config`: 개인 AI 협업 지휘소
- `nixos-config`: 재현 가능한 OS 환경
- `doomemacs-config`: Emacs 환경
- `family-config`: 가족 생활 관리 (이 프로젝트)

모든 프로젝트는 동일한 Denote 규칙, PARA 방법론, AI Agent 친화적 구조를 따릅니다.

## Important Files

- `FAMILY.md`: AI Agent 지침서 (실행 규칙, 자동화 정책)
- `README.md`: 프로젝트 개요 및 시작 가이드
- `INBOX__human.org`: 현재 진행 중인 작업 및 요청사항 (사람이 작성)

## Privacy

### 공개 (이 리포지토리)
- ✅ 템플릿 파일
- ✅ 스키마 정의
- ✅ 문서화
- ✅ 예시 코드

### 비공개 (개인 관리)
- ❌ 실제 가족 데이터 (`~/org/family/`)
- ❌ 금융 정보
- ❌ 개인 식별 정보

## Best Practices

1. **파일 생성 시**: 항상 Denote 네이밍 규칙 준수
2. **템플릿 수정**: 범용성 유지 (특정 가족 정보 제거)
3. **스크립트 개발**: 삼성 사용자가 재사용 가능하도록 범용적으로 작성
4. **문서화**: README.md는 다른 가족도 사용 가능하도록 상세히 작성
5. **Git 커밋**: 프로젝트 스타일 준수 (기존 커밋 히스토리 확인)

**중요**: "Generated with Claude" 또는 "Co-Authored-By" 제외! (깔끔한 커밋 로그 유지)

## 이슈 트래킹: bd (beads)

**중요**: 이 프로젝트는 **bd (beads)** 로 모든 이슈를 관리합니다.

### 필수 명령어

```bash
# 작업 찾기
bd ready --json              # 블로커 없는 작업 가능 이슈
bd list --json               # 전체 이슈 목록
bd show <id>                 # 상세 보기

# 이슈 생성
bd create "제목" -t bug|feature|task -p 0-4 --json

# 작업 시작/완료
bd update <id> --status in_progress --json
bd close <id> --reason "완료" --json
```

### 규칙

- 모든 작업은 bd 이슈로 관리
- 항상 `--json` 플래그 사용
- `.beads/issues.jsonl` 파일은 코드와 함께 커밋


