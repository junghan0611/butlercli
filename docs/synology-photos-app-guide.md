# 가족용 NAS 앱 사용 가이드

**대상**: 가족 구성원 (Android 사용자)
**작성일**: 2025-12-27
**NAS 모델**: Synology DS218J

## 핵심 포인트

- **장소 무관**: 집, 외출, 여행 중 어디서든 접속 가능 (QuickConnect)
- **자동 백업**: 사진 찍으면 자동으로 NAS에 저장
- **무료**: 클라우드 요금 없음, NAS 용량만큼 무제한

---

## 앱 선택 가이드

| 앱 | 용도 | 누가 필요? |
|-----|------|-----------|
| **Synology Photos** | 사진/동영상 자동 백업, 앨범 보기 | **모두 필수** |
| Synology Drive | 문서/파일 동기화 | 파워 유저만 |
| DS File | NAS 파일 탐색기 | 선택 |

> **결론**: 대부분 **Synology Photos 하나면 충분**

---

## 1. 사전 준비 (관리자가 할 일)

NAS에서 다음 설정이 완료되어야 합니다:

### DSM 웹에서 설정

1. **패키지 센터** → "Synology Photos" 설치
2. **제어판** → **사용자** → 사용자 계정 생성
   - 예: `wife` 계정 생성
   - 비밀번호 설정
3. **제어판** → **파일 서비스** → **고급** → QuickConnect 활성화 (외부 접속용)

---

## 2. 앱 설치 (Android)

### Step 1: 앱 다운로드

1. **Google Play 스토어** 열기
2. 검색: `Synology Photos`
3. **Synology Photos** 앱 설치 (개발자: Synology Inc.)

> **주의**: "Synology Photos"와 "DS Photo" 두 가지가 있음
> → **Synology Photos** 설치 (최신 앱)

### Step 2: 앱 실행 및 로그인

1. 앱 열기
2. 로그인 방법 선택:
   - **같은 Wi-Fi**: NAS IP 주소 입력 (예: `192.168.45.245`)
   - **외부 접속**: QuickConnect ID 입력

3. 로그인 정보 입력:
   - **사용자 이름**: 본인 계정 (예: `wife`)
   - **비밀번호**: 설정한 비밀번호

4. **로그인** 버튼 터치

---

## 3. 자동 백업 설정

### Step 1: 백업 메뉴 진입

1. 앱 하단 **메뉴** (≡) 터치
2. **사진 백업** 선택

### Step 2: 백업 활성화

1. **사진 백업 활성화** 터치
2. 옵션 선택:
   - **모든 사진 백업**: 기존 사진 전부 업로드
   - **새 사진만 백업**: 앞으로 찍는 사진만 업로드

3. **백업 대상 폴더** 확인 (기본: `/Photos`)

### Step 3: 백업 조건 설정 (선택)

- **Wi-Fi에서만 백업**: 켜기 권장 (데이터 요금 절약)
- **충전 중에만 백업**: 배터리 걱정되면 켜기
- **중복 파일 건너뛰기**: 켜기 권장

### Step 4: 완료

- 우측 상단 **활성화** 버튼 터치
- 백업이 자동으로 시작됨

---

## 4. 사용 팁

### 사진 보기

- 앱에서 NAS에 저장된 모든 사진 확인 가능
- 타임라인, 앨범별 정리 지원

### 공유 앨범

- 가족 간 특정 앨범 공유 가능
- **앨범** → **공유** 기능 사용

### 저장 공간

- 휴대폰 용량 부족할 때 NAS에만 보관하고 휴대폰에서 삭제 가능
- NAS에 백업된 사진은 안전하게 보관됨

---

## 5. 문제 해결

### 로그인이 안 돼요

1. **같은 Wi-Fi**에 연결되어 있는지 확인
2. NAS IP 주소가 맞는지 확인 (예: `192.168.45.245`)
3. 사용자 이름/비밀번호 확인

### 백업이 멈췄어요

1. 앱을 껐다가 다시 열기
2. **사진 백업** 메뉴에서 상태 확인
3. Wi-Fi 연결 확인

### 외부에서 접속하고 싶어요

1. QuickConnect ID 필요 (관리자에게 문의)
2. 로그인 시 IP 대신 QuickConnect ID 입력

---

## 6. 외부 접속 (QuickConnect)

### QuickConnect란?

집 밖에서도 NAS에 접속할 수 있게 해주는 Synology 무료 서비스.
별도 네트워크 설정 없이 **QuickConnect ID**만 입력하면 접속됨.

### 앱에서 외부 접속 방법

1. 앱 로그인 화면에서 **QuickConnect ID** 입력
2. 사용자 이름/비밀번호 입력
3. 로그인 완료 → 어디서든 사진 보기 가능

### 웹 브라우저로 접속

PC나 다른 기기에서:
```
https://quickconnect.to/[QuickConnect ID]
```

---

## 7. NAS 접속 정보

| 항목 | 값 | 사용 시점 |
|------|-----|----------|
| NAS IP | `192.168.45.245` | 집 Wi-Fi에서 |
| 웹 (집) | `https://192.168.45.245:5001` | 집에서 PC로 |
| QuickConnect ID | `junghanacs` | **외부에서** |
| 웹 (외부) | `https://quickconnect.to/junghanacs` | 외부에서 PC로 |

> **팁**: 앱 설정 시 QuickConnect ID로 로그인하면 집/외부 상관없이 자동 연결됨

---

## 8. 운영 정책

### 데이터 흐름

```
[휴대폰 카메라]
      ↓ (자동 백업)
[NAS: /Photos/사용자별/]     ← 원본 자동 저장
      ↓ (주기적 정리)
[NAS: /family-photos/]       ← 정리된 아카이브
```

### 역할 분담

| 역할 | 담당 | 주기 |
|------|------|------|
| 사진 백업 | 각자 (앱 자동) | 실시간 |
| 사진 정리 | 관리자 | 분기별/연말 |
| 중복 제거 | 관리자 (스크립트) | 필요시 |

### 정리 도구

`family-config/scripts/photo_organizer/` 사용:
- SmartSwitch, Google Photos 등 외부 소스 정리
- Denote 네이밍 규칙 적용

---

## 참고 자료

- [Synology Photos 공식 가이드](https://kb.synology.com/en-us/DSM/tutorial/Quick_Start_Synology_Photos)
- [Android 앱 도움말](https://kb.synology.com/en-ca/DSM/help/SynologyPhotos/Android?version=7)
- [Google Play 스토어](https://play.google.com/store/apps/details?id=com.synology.projectkailash)
