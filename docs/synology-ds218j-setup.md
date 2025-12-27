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

#### 방법 A: USB 직접 연결 (권장)

1. USB HDD를 DS218J USB 3.0 포트에 연결
2. **File Station** → 외부 장치 확인
3. `family-photos` 폴더 전체를 NAS `family-photos` 공유 폴더로 복사

#### 방법 B: 네트워크 복사 (Linux)

```bash
# NAS 마운트
sudo mkdir -p /mnt/nas
sudo mount -t cifs //NAS_IP/family-photos /mnt/nas -o username=admin,vers=3.0

# rsync로 복사 (진행률 표시)
rsync -avh --progress "/media/goqual/T7 Shield/family-photos/" /mnt/nas/

# 완료 후 언마운트
sudo umount /mnt/nas
```

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

## 참고 링크

- [Synology DS218J 사양](https://www.synology.com/ko-kr/products/DS218j)
- [Synology Photos 가이드](https://kb.synology.com/ko-kr/DSM/help/SynologyPhotos)
