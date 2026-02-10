#!/usr/bin/env python3
"""
음성을 텍스트로 변환하는 스크립트
OpenAI Whisper를 사용하여 오디오/비디오 파일에서 자막을 생성합니다.

사용법:
    python transcribe.py ./temp/video.mp4
    python transcribe.py ./temp/audio.wav --output ./temp/transcript.json --model base
"""

import argparse
import os
import sys
import json
from pathlib import Path


def check_whisper_installed():
    """Whisper 설치 여부 확인"""
    try:
        import whisper
        return True
    except ImportError:
        return False


def transcribe_audio(input_file: str, output_file: str = None,
                     model_name: str = "base", language: str = "ko") -> dict:
    """
    오디오/비디오 파일을 텍스트로 변환합니다.

    Args:
        input_file: 입력 파일 경로 (오디오 또는 비디오)
        output_file: 출력 JSON 파일 경로 (None이면 자동 생성)
        model_name: Whisper 모델 (tiny, base, small, medium, large)
        language: 언어 코드 (ko, en, ja 등)

    Returns:
        전사 결과 딕셔너리
    """
    # Whisper 설치 확인
    if not check_whisper_installed():
        print("Error: openai-whisper가 설치되어 있지 않습니다.")
        print("설치: pip install openai-whisper")
        sys.exit(1)

    import whisper

    # 입력 파일 확인
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: 입력 파일을 찾을 수 없습니다: {input_file}")
        sys.exit(1)

    # 출력 파일 경로 설정
    if output_file is None:
        output_file = str(input_path.parent / "transcript.json")

    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"전사 시작: {input_file}")
    print(f"모델: {model_name}")
    print(f"언어: {language}")
    print("모델 로딩 중... (첫 실행 시 다운로드가 필요합니다)")

    # 모델 로드
    model = whisper.load_model(model_name)

    print("전사 중... (파일 길이에 따라 시간이 걸릴 수 있습니다)")

    # 전사 실행
    result = model.transcribe(
        input_file,
        language=language,
        verbose=False,
        word_timestamps=True  # 단어별 타임스탬프
    )

    # 결과 구조화
    transcript_data = {
        "text": result["text"],
        "language": result.get("language", language),
        "segments": []
    }

    for segment in result["segments"]:
        transcript_data["segments"].append({
            "id": segment["id"],
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip(),
        })

    # JSON 저장
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(transcript_data, f, ensure_ascii=False, indent=2)

    print(f"전사 완료: {output_file}")
    print(f"총 세그먼트 수: {len(transcript_data['segments'])}")

    # SRT 파일도 생성
    srt_file = str(output_path.parent / "transcript.srt")
    generate_srt(transcript_data["segments"], srt_file)
    print(f"SRT 파일 생성: {srt_file}")

    return transcript_data


def generate_srt(segments: list, output_file: str):
    """
    세그먼트 데이터로 SRT 자막 파일을 생성합니다.

    Args:
        segments: 세그먼트 리스트
        output_file: 출력 SRT 파일 경로
    """
    def format_timestamp(seconds: float) -> str:
        """초를 SRT 타임스탬프 형식으로 변환"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    srt_content = []
    for i, segment in enumerate(segments, 1):
        start = format_timestamp(segment["start"])
        end = format_timestamp(segment["end"])
        text = segment["text"]

        srt_content.append(f"{i}")
        srt_content.append(f"{start} --> {end}")
        srt_content.append(text)
        srt_content.append("")  # 빈 줄

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(srt_content))


def find_segment_by_text(transcript_data: dict, search_text: str) -> list:
    """
    텍스트로 세그먼트를 검색합니다.

    Args:
        transcript_data: 전사 데이터
        search_text: 검색할 텍스트

    Returns:
        매칭된 세그먼트 리스트
    """
    results = []
    for segment in transcript_data.get("segments", []):
        if search_text.lower() in segment["text"].lower():
            results.append(segment)
    return results


def main():
    parser = argparse.ArgumentParser(
        description="오디오/비디오 파일을 텍스트로 변환합니다.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  python transcribe.py ./temp/video.mp4
  python transcribe.py ./temp/audio.wav --output ./temp/transcript.json
  python transcribe.py ./temp/video.mp4 --model small --language ko

모델 크기:
  tiny   - 가장 빠름, 정확도 낮음 (~1GB VRAM)
  base   - 빠름, 적당한 정확도 (~1GB VRAM)
  small  - 중간 속도, 좋은 정확도 (~2GB VRAM)
  medium - 느림, 높은 정확도 (~5GB VRAM)
  large  - 가장 느림, 최고 정확도 (~10GB VRAM)
        """
    )

    parser.add_argument(
        "input",
        help="입력 오디오/비디오 파일 경로"
    )

    parser.add_argument(
        "--output", "-o",
        default=None,
        help="출력 JSON 파일 경로 (기본값: 입력파일과 같은 위치에 transcript.json)"
    )

    parser.add_argument(
        "--model", "-m",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper 모델 (기본값: base)"
    )

    parser.add_argument(
        "--language", "-l",
        default="ko",
        help="언어 코드 (기본값: ko, 한국어)"
    )

    parser.add_argument(
        "--search", "-s",
        default=None,
        help="기존 transcript.json에서 텍스트 검색"
    )

    args = parser.parse_args()

    # 텍스트 검색 모드
    if args.search:
        input_path = Path(args.input)
        if input_path.suffix == ".json":
            with open(args.input, "r", encoding="utf-8") as f:
                transcript_data = json.load(f)

            results = find_segment_by_text(transcript_data, args.search)

            if results:
                print(f"\n'{args.search}' 검색 결과:")
                for seg in results:
                    print(f"  [{seg['start']:.2f}s - {seg['end']:.2f}s] {seg['text']}")
            else:
                print(f"'{args.search}'를 찾을 수 없습니다.")
        else:
            print("Error: 검색 모드에서는 JSON 파일을 입력해야 합니다.")
        return

    # 전사 실행
    transcript_data = transcribe_audio(
        input_file=args.input,
        output_file=args.output,
        model_name=args.model,
        language=args.language
    )

    # 요약 출력
    print(f"\n=== 전사 요약 ===")
    print(f"전체 텍스트 길이: {len(transcript_data['text'])}자")
    print(f"세그먼트 수: {len(transcript_data['segments'])}")

    if transcript_data['segments']:
        total_duration = transcript_data['segments'][-1]['end']
        print(f"총 길이: {total_duration:.2f}초 ({total_duration/60:.1f}분)")


if __name__ == "__main__":
    main()
