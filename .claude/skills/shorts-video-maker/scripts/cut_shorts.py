#!/usr/bin/env python3
"""
쇼츠 클립 제작 스크립트
ffmpeg를 사용하여 영상에서 쇼츠 클립을 추출하고 9:16 비율로 변환합니다.

사용법:
    python cut_shorts.py --input ./temp/video.mp4 --start 00:01:30 --end 00:02:30
    python cut_shorts.py --input video.mp4 --start 90 --end 150 --subtitle transcript.srt
"""

import argparse
import os
import sys
import subprocess
import json
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


def parse_timestamp(timestamp: str) -> float:
    """
    타임스탬프를 초 단위로 변환합니다.

    Args:
        timestamp: 타임스탬프 문자열 (HH:MM:SS, MM:SS, 또는 초)

    Returns:
        초 단위 float
    """
    # 이미 숫자인 경우
    try:
        return float(timestamp)
    except ValueError:
        pass

    # HH:MM:SS 또는 MM:SS 형식
    parts = timestamp.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = map(float, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:
        minutes, seconds = map(float, parts)
        return minutes * 60 + seconds
    else:
        raise ValueError(f"Invalid timestamp format: {timestamp}")


def format_timestamp(seconds: float) -> str:
    """초를 HH:MM:SS 형식으로 변환"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"


def get_video_info(input_file: str) -> dict:
    """
    영상 정보를 가져옵니다.

    Args:
        input_file: 입력 영상 파일 경로

    Returns:
        영상 정보 딕셔너리
    """
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        input_file
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        info = json.loads(result.stdout)

        video_stream = None
        for stream in info.get("streams", []):
            if stream.get("codec_type") == "video":
                video_stream = stream
                break

        if video_stream:
            return {
                "width": int(video_stream.get("width", 1920)),
                "height": int(video_stream.get("height", 1080)),
                "duration": float(info.get("format", {}).get("duration", 0)),
                "fps": eval(video_stream.get("r_frame_rate", "30/1")),
            }

        return {"width": 1920, "height": 1080, "duration": 0, "fps": 30}

    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Warning: 영상 정보를 가져올 수 없습니다: {e}")
        return {"width": 1920, "height": 1080, "duration": 0, "fps": 30}


def cut_shorts(input_file: str, start: str, end: str, output_file: str,
               subtitle_file: str = None, crop_position: str = "center") -> str:
    """
    쇼츠 클립을 제작합니다.

    Args:
        input_file: 입력 영상 파일 경로
        start: 시작 시간 (HH:MM:SS 또는 초)
        end: 종료 시간 (HH:MM:SS 또는 초)
        output_file: 출력 파일 경로
        subtitle_file: SRT 자막 파일 경로 (선택)
        crop_position: 크롭 위치 (center, left, right)

    Returns:
        출력 파일 경로
    """
    # ffmpeg 설치 확인
    if not check_ffmpeg_installed():
        print("Error: ffmpeg가 설치되어 있지 않습니다.")
        print("설치:")
        print("  macOS: brew install ffmpeg")
        print("  Ubuntu: apt install ffmpeg")
        sys.exit(1)

    # 입력 파일 확인
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: 입력 파일을 찾을 수 없습니다: {input_file}")
        sys.exit(1)

    # 출력 디렉토리 생성
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 시간 파싱
    start_seconds = parse_timestamp(start)
    end_seconds = parse_timestamp(end)
    duration = end_seconds - start_seconds

    if duration <= 0:
        print(f"Error: 종료 시간이 시작 시간보다 앞입니다.")
        sys.exit(1)

    if duration > 60:
        print(f"Warning: 클립 길이가 60초를 초과합니다 ({duration:.1f}초). 쇼츠 제한을 확인하세요.")

    # 영상 정보 가져오기
    video_info = get_video_info(input_file)
    src_width = video_info["width"]
    src_height = video_info["height"]

    # 9:16 크롭 계산
    target_ratio = 9 / 16
    src_ratio = src_width / src_height

    if src_ratio > target_ratio:
        # 영상이 더 넓음 -> 좌우 크롭
        new_width = int(src_height * target_ratio)
        new_height = src_height

        if crop_position == "left":
            x_offset = 0
        elif crop_position == "right":
            x_offset = src_width - new_width
        else:  # center
            x_offset = (src_width - new_width) // 2

        y_offset = 0
    else:
        # 영상이 더 높거나 같음 -> 상하 크롭
        new_width = src_width
        new_height = int(src_width / target_ratio)
        x_offset = 0
        y_offset = (src_height - new_height) // 2

    print(f"클립 제작 시작")
    print(f"입력: {input_file}")
    print(f"구간: {format_timestamp(start_seconds)} - {format_timestamp(end_seconds)} ({duration:.1f}초)")
    print(f"크롭: {src_width}x{src_height} -> {new_width}x{new_height} (9:16)")

    # 필터 체인 구성
    filters = []

    # 크롭 필터
    filters.append(f"crop={new_width}:{new_height}:{x_offset}:{y_offset}")

    # 1080x1920으로 스케일
    filters.append("scale=1080:1920:flags=lanczos")

    # 자막 필터 (있는 경우)
    if subtitle_file and Path(subtitle_file).exists():
        # 자막 시작 시간 조정
        subtitle_filter = f"subtitles={subtitle_file}:force_style='FontSize=24,FontName=Arial,Bold=1,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Shadow=1,Alignment=2,MarginV=50'"
        filters.append(subtitle_filter)
        print(f"자막: {subtitle_file}")

    filter_chain = ",".join(filters)

    # ffmpeg 명령어 구성
    cmd = [
        "ffmpeg",
        "-ss", str(start_seconds),  # 시작 시간 (입력 전에 배치하여 빠른 탐색)
        "-i", input_file,
        "-t", str(duration),  # 길이
        "-vf", filter_chain,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-c:a", "aac",
        "-b:a", "128k",
        "-ar", "44100",
        "-movflags", "+faststart",
        "-y",  # 덮어쓰기
        output_file
    ]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        if output_path.exists():
            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"클립 생성 완료: {output_file}")
            print(f"파일 크기: {file_size:.2f} MB")
            return str(output_path)
        else:
            print("Error: 클립 파일이 생성되지 않았습니다.")
            sys.exit(1)

    except subprocess.CalledProcessError as e:
        print(f"Error: 클립 생성 실패")
        print(f"stderr: {e.stderr}")
        sys.exit(1)


def batch_cut(input_file: str, clips: list, output_dir: str,
              subtitle_file: str = None) -> list:
    """
    여러 클립을 일괄 생성합니다.

    Args:
        input_file: 입력 영상 파일
        clips: 클립 정보 리스트 [{"start": "00:01:00", "end": "00:02:00", "name": "shorts-01"}]
        output_dir: 출력 디렉토리
        subtitle_file: 자막 파일 (선택)

    Returns:
        생성된 파일 경로 리스트
    """
    results = []

    for i, clip in enumerate(clips, 1):
        output_file = Path(output_dir) / f"{clip.get('name', f'shorts-{i:02d}')}.mp4"

        print(f"\n=== 클립 {i}/{len(clips)} ===")

        result = cut_shorts(
            input_file=input_file,
            start=clip["start"],
            end=clip["end"],
            output_file=str(output_file),
            subtitle_file=subtitle_file,
            crop_position=clip.get("crop", "center")
        )

        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(
        description="쇼츠 클립을 제작합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  # 단일 클립
  python cut_shorts.py --input video.mp4 --start 00:01:30 --end 00:02:30 --output shorts-01.mp4

  # 자막 포함
  python cut_shorts.py --input video.mp4 --start 90 --end 150 --subtitle transcript.srt

  # 일괄 처리 (JSON 파일)
  python cut_shorts.py --input video.mp4 --batch clips.json --output-dir ./shorts/

clips.json 형식:
  [
    {"start": "00:01:00", "end": "00:02:00", "name": "shorts-01"},
    {"start": "00:05:30", "end": "00:06:30", "name": "shorts-02"}
  ]
        """
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="입력 영상 파일 경로"
    )

    parser.add_argument(
        "--start", "-s",
        help="시작 시간 (HH:MM:SS 또는 초)"
    )

    parser.add_argument(
        "--end", "-e",
        help="종료 시간 (HH:MM:SS 또는 초)"
    )

    parser.add_argument(
        "--output", "-o",
        default="./outputs/shorts-videos/shorts-01.mp4",
        help="출력 파일 경로"
    )

    parser.add_argument(
        "--subtitle",
        default=None,
        help="SRT 자막 파일 경로 (하드코딩)"
    )

    parser.add_argument(
        "--crop", "-c",
        default="center",
        choices=["center", "left", "right"],
        help="9:16 크롭 위치 (기본값: center)"
    )

    parser.add_argument(
        "--batch", "-b",
        default=None,
        help="일괄 처리용 JSON 파일"
    )

    parser.add_argument(
        "--output-dir",
        default="./outputs/shorts-videos/",
        help="일괄 처리 시 출력 디렉토리"
    )

    parser.add_argument(
        "--info",
        action="store_true",
        help="입력 영상 정보만 출력"
    )

    args = parser.parse_args()

    # 영상 정보 출력
    if args.info:
        info = get_video_info(args.input)
        print("\n=== 영상 정보 ===")
        print(f"해상도: {info.get('width')}x{info.get('height')}")
        print(f"길이: {info.get('duration'):.2f}초")
        print(f"FPS: {info.get('fps')}")
        return

    # 일괄 처리
    if args.batch:
        with open(args.batch, "r", encoding="utf-8") as f:
            clips = json.load(f)

        results = batch_cut(
            input_file=args.input,
            clips=clips,
            output_dir=args.output_dir,
            subtitle_file=args.subtitle
        )

        print(f"\n=== 완료 ===")
        print(f"생성된 클립: {len(results)}개")
        for r in results:
            print(f"  - {r}")
        return

    # 단일 클립
    if not args.start or not args.end:
        print("Error: --start와 --end를 지정해야 합니다.")
        print("       또는 --batch로 일괄 처리할 수 있습니다.")
        sys.exit(1)

    output_file = cut_shorts(
        input_file=args.input,
        start=args.start,
        end=args.end,
        output_file=args.output,
        subtitle_file=args.subtitle,
        crop_position=args.crop
    )

    print(f"\n완료! 파일: {output_file}")


if __name__ == "__main__":
    main()
