# Family Photo Organizer - Samsung SmartSwitch Processor

## 개요
삼성 SmartSwitch 백업에서 가족 사진/동영상을 Denote 네이밍 규칙으로 정리하는 범용 도구입니다.

## 특징
- **범용성**: 모든 삼성 SmartSwitch 백업 지원
- **Denote 네이밍**: `YYYYMMDDTHHMMSS--original-name__tags.ext`
- **중복 제거**: MD5 해시 기반 정확한 중복 감지
- **메타데이터 보존**: EXIF, GPS 정보 유지
- **자동 분류**: 사진/동영상/스크린샷/문서 자동 분류

## SmartSwitch 백업 구조

```
SM-XXXXX_deviceid/
├── 1757590576343/           # Unix timestamp (백업 시점)
│   ├── PHOTO/               # 갤러리 사진/동영상
│   │   └── DCIM/
│   │       ├── Camera/      # 카메라로 촬영한 사진/동영상
│   │       ├── Screenshots/ # 스크린샷
│   │       ├── Restored/    # 복원된 미디어
│   │       └── 서류/        # 문서 사진
│   ├── MESSAGE/            # 메시지 첨부 파일
│   ├── GALLERYLOCATION/    # 위치 정보
│   └── PHOTO_ORIGIN/       # 원본 데이터
└── backup_media.db         # 미디어 데이터베이스
```

## 설치

### NixOS/Nix 사용자 (권장)

```bash
# nix-shell 진입 (모든 의존성 자동 설치)
nix-shell
```

### 일반 Python 환경

```bash
# Python 가상환경 생성
python3 -m venv venv
source venv/bin/activate

# 필요 패키지 설치
pip install pillow python-dateutil exifread
```

## 사용법

### 1. 기본 사용

```bash
# SmartSwitch 백업을 정리
python family_photo_organizer.py \
    ~/sync/family-photos-work/smartswitch-backup/SM-S921N_xxx \
    ~/sync/family-photos
```

### 2. 테스트 실행 (Dry Run)

```bash
# 실제로 파일을 이동하지 않고 테스트
python family_photo_organizer.py \
    ~/sync/family-photos-work/smartswitch-backup/SM-S921N_xxx \
    ~/sync/family-photos \
    --dry-run \
    --limit 10
```

### 3. 구조 분석만

```bash
# SmartSwitch 구조만 분석
python family_photo_organizer.py \
    ~/sync/family-photos-work/smartswitch-backup/SM-S921N_xxx \
    ~/sync/family-photos \
    --analyze-only
```

## 출력 구조

```
~/sync/family-photos/
├── photos/           # 일반 사진
│   ├── 2019/
│   ├── 2020/
│   └── 2021/
├── videos/          # 동영상
│   └── YYYY/
├── screenshots/     # 스크린샷
│   └── YYYY/
├── documents/       # 문서 사진
│   └── YYYY/
└── logs/           # 처리 로그
    ├── duplicate_cache.json
    └── organize_YYYYMMDD_HHMMSS.log
```

## 파일명 규칙

### Denote 네이밍
```
20251019T143025--IMG-1234__photo.jpg
└──────┬──────┘  └───┬───┘ └─┬─┘ └┬┘
   timestamp    original   tags  ext

태그 종류:
- __photo: 일반 사진
- __video: 동영상
- __screenshot: 스크린샷
- __document: 문서
- __restored: 복원된 파일
- __message: 메시지 첨부
- __baron: 특정 폴더 (예: 아이 이름)
```

## 중복 처리

1. **크기 비교**: 파일 크기가 다르면 다른 파일
2. **MD5 해시**: 크기가 같으면 해시 비교
3. **캐싱**: 해시 결과를 캐시해서 성능 향상

## 메타데이터 추출

우선순위:
1. EXIF DateTimeOriginal
2. 파일명의 날짜 패턴 (YYYYMMDD_HHMMSS)
3. Unix timestamp (파일명)
4. 파일 수정 시간

## 성능

- 100KB 이상 파일만 처리 (썸네일 제외)
- 병렬 처리 미지원 (순차 처리)
- 3,800개 파일 기준 약 10-15분 소요

## 로그

모든 처리 과정은 `logs/` 폴더에 기록됩니다:
- `organize_YYYYMMDD_HHMMSS.log`: 처리 로그
- `report_YYYYMMDD_HHMMSS.txt`: 최종 보고서
- `duplicate_cache.json`: 중복 검사 캐시

## 라이선스

MIT License - 자유롭게 사용 가능

## 기여

이 도구는 삼성 사용자들을 위한 범용 도구입니다.
개선사항이나 버그를 발견하시면 이슈를 등록해주세요.

## 작성자

- Junghan Kim (junghanacs@gmail.com)
- Family-Config Project
- 2025-10-19