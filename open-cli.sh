#!/bin/bash
#
# open-cli.sh - 파일, 폴더, URL을 실제로 여는 CLI 도구
# 클립보드 복사 대신 시스템 기본 프로그램으로 엽니다.
#

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    echo "사용법: open-cli <파일|폴더|URL>"
    echo ""
    echo "예시:"
    echo "  open-cli ./README.md          # 파일 열기"
    echo "  open-cli /home/user/project   # 폴더 열기"
    echo "  open-cli https://example.com  # URL 열기"
    exit 1
}

# 인자 확인
if [ $# -eq 0 ]; then
    usage
fi

TARGET="$1"

# 운영체제 감지 및 열기 명령 실행
open_target() {
    local target="$1"

    case "$(uname -s)" in
        Linux*)
            if command -v xdg-open &> /dev/null; then
                xdg-open "$target" 2>/dev/null &
                echo -e "${GREEN}열기 완료:${NC} $target"
            elif command -v gnome-open &> /dev/null; then
                gnome-open "$target" 2>/dev/null &
                echo -e "${GREEN}열기 완료:${NC} $target"
            elif command -v kde-open &> /dev/null; then
                kde-open "$target" 2>/dev/null &
                echo -e "${GREEN}열기 완료:${NC} $target"
            else
                echo -e "${RED}오류:${NC} 열기 명령을 찾을 수 없습니다. xdg-utils를 설치하세요."
                echo "  sudo apt install xdg-utils"
                exit 1
            fi
            ;;
        Darwin*)
            open "$target"
            echo -e "${GREEN}열기 완료:${NC} $target"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            start "" "$target"
            echo -e "${GREEN}열기 완료:${NC} $target"
            ;;
        *)
            echo -e "${RED}오류:${NC} 지원되지 않는 운영체제입니다."
            exit 1
            ;;
    esac
}

# URL인지 확인
is_url() {
    local target="$1"
    [[ "$target" =~ ^https?:// ]] || [[ "$target" =~ ^file:// ]]
}

# 메인 로직
if is_url "$TARGET"; then
    echo -e "${YELLOW}URL 열기:${NC} $TARGET"
    open_target "$TARGET"
elif [ -e "$TARGET" ]; then
    # 상대 경로를 절대 경로로 변환
    ABSOLUTE_PATH="$(cd "$(dirname "$TARGET")" && pwd)/$(basename "$TARGET")"

    if [ -d "$TARGET" ]; then
        echo -e "${YELLOW}폴더 열기:${NC} $ABSOLUTE_PATH"
    else
        echo -e "${YELLOW}파일 열기:${NC} $ABSOLUTE_PATH"
    fi
    open_target "$ABSOLUTE_PATH"
else
    echo -e "${RED}오류:${NC} '$TARGET' 파일 또는 폴더를 찾을 수 없습니다."
    exit 1
fi
