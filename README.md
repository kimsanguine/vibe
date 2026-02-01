# Vibe

## Installation

### OpenClaw

To install OpenClaw, run the following command:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

## CLI 열기 도구

CLI에서 "열기" 기능이 클립보드 복사만 되는 문제를 해결하는 도구입니다.

### 사용법

```bash
# 스크립트를 PATH에 추가하거나 직접 실행
./open-cli.sh <파일|폴더|URL>

# 예시
./open-cli.sh ./README.md          # 파일 열기
./open-cli.sh /home/user/project   # 폴더 열기
./open-cli.sh https://example.com  # URL 열기
```

### 전역 설치

```bash
# 시스템 전역에서 사용하려면
sudo cp open-cli.sh /usr/local/bin/open-cli
# 또는 심볼릭 링크 생성
sudo ln -s $(pwd)/open-cli.sh /usr/local/bin/open-cli
```

### 지원 운영체제

- **Linux**: xdg-open, gnome-open, kde-open 사용
- **macOS**: open 명령어 사용
- **Windows**: start 명령어 사용 (Git Bash/MSYS)
