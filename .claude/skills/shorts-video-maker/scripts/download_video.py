#!/usr/bin/env python3
"""
YouTube 영상 다운로드 스크립트
yt-dlp를 사용하여 YouTube 영상을 다운로드합니다.

사용법:
    python download_video.py "https://youtube.com/watch?v=xxx"
    python download_video.py "URL" --output ./temp/ --quality best
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def check_ytdlp_installed():
    """yt-dlp 설치 여부 확인"""
    try:
        subprocess.run(
            ["yt-dlp", "--version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def download_video(url: str, output_dir: str = "./temp", quality: str = "best",
                   video_format: str = "mp4") -> str:
    """
    YouTube 영상을 다운로드합니다.

    Args:
        url: YouTube 영상 URL
        output_dir: 출력 디렉토리
        quality: 영상 품질 (best, worst, 720p, 1080p 등)
        video_format: 출력 형식 (mp4, webm 등)

    Returns:
        다운로드된 파일 경로
    """
    # yt-dlp 설치 확인
    if not check_ytdlp_installed():
        print("Error: yt-dlp가 설치되어 있지 않습니다.")
        print("설치: pip install yt-dlp")
        sys.exit(1)

    # 출력 디렉토리 생성
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 출력 파일 템플릿
    output_template = str(output_path / "video.%(ext)s")

    # 품질 설정
    if quality == "best":
        format_spec = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    elif quality == "worst":
        format_spec = "worstvideo+worstaudio/worst"
    elif quality in ["720p", "1080p", "1440p", "2160p"]:
        height = quality[:-1]
        format_spec = f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={height}][ext=mp4]/best"
    else:
        format_spec = "best"

    # yt-dlp 명령어 구성
    cmd = [
        "yt-dlp",
        "-f", format_spec,
        "--merge-output-format", video_format,
        "-o", output_template,
        "--no-playlist",  # 플레이리스트 제외
        "--no-warnings",
        url
    ]

    print(f"다운로드 시작: {url}")
    print(f"출력 디렉토리: {output_dir}")
    print(f"품질: {quality}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        # 다운로드된 파일 찾기
        downloaded_file = None
        for ext in [video_format, "mkv", "webm", "mp4"]:
            potential_file = output_path / f"video.{ext}"
            if potential_file.exists():
                downloaded_file = str(potential_file)
                break

        if downloaded_file:
            print(f"다운로드 완료: {downloaded_file}")
            return downloaded_file
        else:
            print("Error: 다운로드된 파일을 찾을 수 없습니다.")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Error: 다운로드 실패")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def get_video_info(url: str) -> dict:
    """
    영상 정보를 가져옵니다.

    Args:
        url: YouTube 영상 URL

    Returns:
        영상 정보 딕셔너리
    """
    cmd = [
        "yt-dlp",
        "--dump-json",
        "--no-playlist",
        url
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        import json
        info = json.loads(result.stdout)

        return {
            "title": info.get("title", "Unknown"),
            "duration": info.get("duration", 0),
            "uploader": info.get("uploader", "Unknown"),
            "view_count": info.get("view_count", 0),
            "description": info.get("description", ""),
        }

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Warning: 영상 정보를 가져올 수 없습니다: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="YouTube 영상을 다운로드합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python download_video.py "https://youtube.com/watch?v=xxx"
  python download_video.py "URL" --output ./temp/ --quality 720p
  python download_video.py "URL" --info  # 영상 정보만 확인
        """
    )

    parser.add_argument(
        "url",
        help="YouTube 영상 URL"
    )

    parser.add_argument(
        "--output", "-o",
        default="./temp",
        help="출력 디렉토리 (기본값: ./temp)"
    )

    parser.add_argument(
        "--quality", "-q",
        default="best",
        choices=["best", "worst", "720p", "1080p", "1440p", "2160p"],
        help="영상 품질 (기본값: best)"
    )

    parser.add_argument(
        "--format", "-f",
        default="mp4",
        choices=["mp4", "webm", "mkv"],
        help="출력 형식 (기본값: mp4)"
    )

    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="영상 정보만 출력하고 다운로드하지 않음"
    )

    args = parser.parse_args()

    # 영상 정보 출력
    if args.info:
        info = get_video_info(args.url)
        if info:
            print("\n=== 영상 정보 ===")
            print(f"제목: {info.get('title')}")
            print(f"길이: {info.get('duration')}초")
            print(f"업로더: {info.get('uploader')}")
            print(f"조회수: {info.get('view_count'):,}")
        return

    # 다운로드 실행
    downloaded_file = download_video(
        url=args.url,
        output_dir=args.output,
        quality=args.quality,
        video_format=args.format
    )

    print(f"\n완료! 파일: {downloaded_file}")


if __name__ == "__main__":
    main()
