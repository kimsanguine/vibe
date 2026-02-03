#!/usr/bin/env python3
"""
영상에서 오디오를 추출하는 스크립트
ffmpeg를 사용하여 영상 파일에서 오디오를 추출합니다.

사용법:
    python extract_audio.py ./temp/video.mp4
    python extract_audio.py ./temp/video.mp4 --output ./temp/audio.wav
"""

import argparse
import os
import sys
import subprocess
from pathlib import Path


def check_ffmpeg_installed():
    """ffmpeg 설치 여부 확인"""
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def extract_audio(input_file: str, output_file: str = None,
                  audio_format: str = "wav", sample_rate: int = 16000) -> str:
    """
    영상에서 오디오를 추출합니다.

    Args:
        input_file: 입력 영상 파일 경로
        output_file: 출력 오디오 파일 경로 (None이면 자동 생성)
        audio_format: 오디오 형식 (wav, mp3, m4a)
        sample_rate: 샘플레이트 (Hz)

    Returns:
        추출된 오디오 파일 경로
    """
    # ffmpeg 설치 확인
    if not check_ffmpeg_installed():
        print("Error: ffmpeg가 설치되어 있지 않습니다.")
        print("설치:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: apt install ffmpeg")
        print("  Windows: https://ffmpeg.org/download.html")
        sys.exit(1)

    # 입력 파일 확인
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: 입력 파일을 찾을 수 없습니다: {input_file}")
        sys.exit(1)

    # 출력 파일 경로 설정
    if output_file is None:
        output_file = str(input_path.parent / f"audio.{audio_format}")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 코덱 설정
    codec_map = {
        "wav": "pcm_s16le",
        "mp3": "libmp3lame",
        "m4a": "aac",
        "flac": "flac"
    }
    codec = codec_map.get(audio_format, "pcm_s16le")

    # ffmpeg 명령어 구성
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vn",  # 비디오 제외
        "-acodec", codec,
        "-ar", str(sample_rate),  # 샘플레이트
        "-ac", "1",  # 모노 (Whisper 권장)
        "-y",  # 덮어쓰기
        output_file
    ]

    print(f"오디오 추출 시작: {input_file}")
    print(f"출력 파일: {output_file}")
    print(f"형식: {audio_format}, 샘플레이트: {sample_rate}Hz")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        if output_path.exists():
            file_size = output_path.stat().st_size / (1024 * 1024)  # MB
            print(f"오디오 추출 완료: {output_file}")
            print(f"파일 크기: {file_size:.2f} MB")
            return str(output_path)
        else:
            print("Error: 오디오 파일이 생성되지 않았습니다.")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Error: 오디오 추출 실패")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def get_audio_info(file_path: str) -> dict:
    """
    오디오 파일 정보를 가져옵니다.

    Args:
        file_path: 오디오 파일 경로

    Returns:
        오디오 정보 딕셔너리
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        file_path
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

        audio_stream = None
        for stream in info.get("streams", []):
            if stream.get("codec_type") == "audio":
                audio_stream = stream
                break

        if audio_stream:
            return {
                "codec": audio_stream.get("codec_name", "Unknown"),
                "sample_rate": audio_stream.get("sample_rate", "Unknown"),
                "channels": audio_stream.get("channels", "Unknown"),
                "duration": float(info.get("format", {}).get("duration", 0)),
            }

        return {}

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Warning: 오디오 정보를 가져올 수 없습니다: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="영상에서 오디오를 추출합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python extract_audio.py ./temp/video.mp4
  python extract_audio.py ./temp/video.mp4 --output ./temp/audio.wav
  python extract_audio.py ./temp/video.mp4 --format mp3 --rate 44100
        """
    )

    parser.add_argument(
        "input",
        help="입력 영상 파일 경로"
    )

    parser.add_argument(
        "--output", "-o",
        default=None,
        help="출력 오디오 파일 경로 (기본값: 입력파일과 같은 위치에 audio.wav)"
    )

    parser.add_argument(
        "--format", "-f",
        default="wav",
        choices=["wav", "mp3", "m4a", "flac"],
        help="오디오 형식 (기본값: wav)"
    )

    parser.add_argument(
        "--rate", "-r",
        type=int,
        default=16000,
        help="샘플레이트 Hz (기본값: 16000, Whisper 권장)"
    )

    parser.add_argument(
        "--info", "-i",
        action="store_true",
        help="입력 파일의 오디오 정보만 출력"
    )

    args = parser.parse_args()

    # 오디오 정보 출력
    if args.info:
        info = get_audio_info(args.input)
        if info:
            print("\n=== 오디오 정보 ===")
            print(f"코덱: {info.get('codec')}")
            print(f"샘플레이트: {info.get('sample_rate')} Hz")
            print(f"채널: {info.get('channels')}")
            print(f"길이: {info.get('duration'):.2f}초")
        return

    # 오디오 추출 실행
    output_file = extract_audio(
        input_file=args.input,
        output_file=args.output,
        audio_format=args.format,
        sample_rate=args.rate
    )

    print(f"\n완료! 파일: {output_file}")


if __name__ == "__main__":
    main()
