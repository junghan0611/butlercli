# Synology DS218J NAS 설정 가이드

설정일: 2025-12-27

## 하드웨어 구성

| 항목 | 사양 |
|------|------|
| 모델 | Synology DS218J |
| 디스크 1 | 2TB HDD |
| 디스크 2 | 4TB HDD |
| 스토리지 풀 | SHR (Synology Hybrid RAID) |
| 가용 용량 | ~2TB (이중화 적용) |
| 파일 시스템 | ext4 |

## 폴더 구조

```
NAS Root
├── Photos/              # Synology Photos 기본 폴더
│   └── [사용자별]/      # 휴대폰 자동 백업
│
└── family-photos/       # 정리된 가족 사진 아카이브
    ├── photos/YYYY/     # 연도별 사진
    ├── videos/YYYY/     # 연도별 동영상
    ├── screenshots/YYYY/
    ├── documents/YYYY/
    └── logs/            # 정리 작업 로그
```

## 공유 폴더 설정

### 1. family-photos (정리된 아카이브)

- **경로**: `/volume1/family-photos`
- **용도**: Denote 네이밍으로 정리된 미디어 파일
- **접근 권한**: 관리자 읽기/쓰기
- **휴지통**: 비활성화 (용량 절약)

### 2. Photos (Synology Photos용)

- **경로**: `/volume1/homes/[사용자]/Photos`
- **용도**: 휴대폰 자동 백업 (Synology Photos 앱)
- **접근 권한**: 개인 폴더
- **앱**: Synology Photos 패키지 필요

## 초기 데이터 이관

### 소스 데이터

| 소스 | 경로 | 용량 | 설명 |
|------|------|------|------|
| USB HDD | `/media/goqual/T7 Shield/family-photos` | ~50GB | SmartSwitch + Google Photos 정리 완료 |

### 이관 방법

#### 방법 A: Nautilus SMB 접근 (권장, 실제 사용)

가장 간단하고 확실한 방법:

1. **Nautilus** (파일 관리자) 열기
2. **Ctrl+L** → 주소 입력: `smb://192.168.45.245/family-photos`
3. 사용자/비밀번호 입력
4. USB HDD 폴더에서 NAS 폴더로 **드래그 앤 드롭**

#### 방법 B: USB 직접 연결

1. USB HDD를 DS218J USB 3.0 포트에 연결
2. **File Station** → 외부 장치 확인
3. `family-photos` 폴더 전체를 NAS `family-photos` 공유 폴더로 복사

> **주의**: exFAT 포맷 USB는 **exFAT Access 패키지** (유료, ~$4) 필요

#### 방법 C: 터미널 SMB 마운트 + rsync

```bash
# NAS 마운트
sudo mkdir -p /mnt/nas
sudo mount -t cifs //NAS_IP/family-photos /mnt/nas -o username=admin,vers=3.0

# rsync로 복사 (진행률 표시)
rsync -avh --progress "/media/goqual/T7 Shield/family-photos/" /mnt/nas/

# 완료 후 언마운트
sudo umount /mnt/nas
```

## 시행착오 기록 (Troubleshooting)

### 1. USB 직접 연결 실패
- **문제**: Samsung T7 Shield (exFAT 포맷) NAS에서 인식 안 됨
- **원인**: DS218J는 exFAT 기본 미지원
- **해결**: exFAT Access 패키지 필요 (유료) → 네트워크 복사로 전환

### 2. SSH rsync 인증 실패
```bash
rsync -avh --progress "/media/goqual/T7 Shield/family-photos/" baron@192.168.45.245:/volume1/family-photos/
# → Permission denied, please try again.
```
- **문제**: SSH 비밀번호 인증 시 Permission denied
- **시도**: sshpass 사용 → 동일 오류
- **원인**: 비밀번호 특수문자(`!`) 이스케이프 문제 또는 SSH 설정 문제
- **해결**: SMB 방식으로 전환

### 3. SMB 마운트 권한 문제
```bash
sudo mount -t cifs //192.168.45.245/family-photos /mnt/nas -o username=baron,vers=3.0
# rsync 시 Permission denied (mkdir, mkstemp 실패)
```
- **문제**: 마운트는 되지만 파일/폴더 생성 권한 없음
- **시도**: `uid`, `gid`, `file_mode`, `dir_mode` 옵션 추가 → mount 자체 실패
- **원인**: 시놀로지 SMB 권한 설정과 Linux 마운트 옵션 충돌
- **해결**: Nautilus GUI로 SMB 접근 (자동 권한 처리)

### 4. 최종 해결책
**Nautilus SMB 접근**이 가장 안정적:
- GUI에서 인증 처리 자동화
- 권한 문제 없이 드래그 앤 드롭 복사
- 진행률 표시 지원

## 운영 정책

### 백업 흐름

```
[휴대폰] → Synology Photos 앱 → Photos/ (자동)
                                    ↓
                              (필요시 정리)
                                    ↓
                            family-photos/ (수동/스크립트)
```

### 정리 주기

- **일상**: Synology Photos로 자동 백업
- **분기별 또는 연말**: `Photos/` → `family-photos/` 정리 작업

### 정리 스크립트

`scripts/photo_organizer/` 도구 사용:

```bash
# NAS에서 SSH 또는 로컬에서 마운트 후 실행
python google_photos_organizer.py /path/to/Photos /path/to/family-photos --dry-run
```

## 추가 설정 (선택)

### Synology Photos 활성화

1. **패키지 센터** → "Synology Photos" 설치
2. 사용자별 Photos 폴더 자동 생성
3. 모바일 앱 설치 → 자동 백업 설정

### SMB 접근 (Linux/Mac)

```bash
# fstab 영구 마운트 (옵션)
//NAS_IP/family-photos /mnt/nas-photos cifs credentials=/home/user/.nas-creds,vers=3.0 0 0
```

### 자동 백업 (외부 디스크)

- **Hyper Backup** 패키지로 USB HDD 정기 백업 설정 가능

## 디스크 확장 (향후)

### 현재 → 확장 시나리오

| 상태 | 디스크 구성 | 가용 용량 |
|------|------------|----------|
| **현재** | 2TB + 4TB (SHR) | ~2TB |
| **확장 후** | 4TB + 4TB (SHR) | ~4TB |

### 마이그레이션 절차

1. **새 4TB 디스크 구매**

2. **2TB 디스크 교체**
   - DSM 웹 → **스토리지 관리자**
   - 2TB 디스크 **비활성화**
   - NAS 전원 종료 (아래 참조)
   - 2TB 빼고 → 새 4TB 삽입
   - NAS 전원 켜기

3. **자동 복구**
   - DSM에서 새 디스크 인식
   - **스토리지 관리자** → **복구** 클릭
   - 데이터 재구축 (수 시간~하루 소요)
   - 완료 후 용량 자동 확장 (~4TB)

### 주의사항

- **복구 중 전원 끄지 말 것** (데이터 손실 위험)
- 복구 중에도 NAS 사용 가능 (느려짐)
- 복구 완료 전까지 이중화 없음 → **중요 데이터 백업 권장**
- DS218J는 **핫스왑 미지원** → 전원 끄고 교체

---

## 전원 관리

### 안전하게 끄는 방법

#### 방법 1: DSM 웹 (권장)
1. DSM 웹 접속
2. 우측 상단 **사람 아이콘** 클릭
3. **종료** 선택
4. 확인 후 안전하게 종료

#### 방법 2: 물리 버튼
1. 전면 **전원 버튼** 4초 누르기
2. 비프음 후 안전 종료 시작

#### 방법 3: SSH
```bash
sudo poweroff
```

> **경고**: 전원 케이블 그냥 뽑으면 **데이터 손상** 위험!

### 전원 켜기
- 전면 **전원 버튼** 짧게 누르기
- 부팅 완료까지 1~2분 소요

---

## 참고 링크

- [Synology DS218J 사양](https://www.synology.com/ko-kr/products/DS218j)
- [Synology Photos 가이드](https://kb.synology.com/ko-kr/DSM/help/SynologyPhotos)
