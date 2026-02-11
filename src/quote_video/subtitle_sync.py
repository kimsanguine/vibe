"""Whisper 타임스탬프 추출 + SRT 자막 생성 모듈."""

from datetime import timedelta
from pathlib import Path

from .config import Config, OUTPUT_SUBTITLES


class SubtitleSync:
    """Whisper large-v3로 오디오에서 타임스탬프를 추출하고 SRT 자막을 생성한다."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self._model = None

    @property
    def model(self):
        """Whisper 모델을 lazy-load 한다."""
        if self._model is None:
            import whisper
            print(f"[SubtitleSync] Loading Whisper {self.config.whisper_model}...")
            self._model = whisper.load_model(self.config.whisper_model)
        return self._model

    def transcribe(self, audio_path: str | Path) -> dict:
        """오디오 파일에서 타임스탬프가 포함된 전사 결과를 반환한다.

        Args:
            audio_path: WAV 오디오 파일 경로.

        Returns:
            Whisper 전사 결과 dict (segments 포함).
        """
        result = self.model.transcribe(
            str(audio_path),
            language=self.config.whisper_language,
            word_timestamps=True,
        )
        return result

    def generate_srt(
        self,
        audio_path: str | Path,
        output_path: str | Path | None = None,
        scene_index: int = 1,
        max_chars_per_line: int = 30,
    ) -> Path:
        """오디오 파일에서 SRT 자막 파일을 생성한다.

        Args:
            audio_path: WAV 오디오 파일 경로.
            output_path: SRT 저장 경로. None이면 output/subtitles/scene_{index}.srt.
            scene_index: 씬 번호 (파일명에 사용).
            max_chars_per_line: 자막 한 줄 최대 글자 수.

        Returns:
            저장된 SRT 파일 경로.
        """
        # 출력 경로
        if output_path is None:
            OUTPUT_SUBTITLES.mkdir(parents=True, exist_ok=True)
            output_path = OUTPUT_SUBTITLES / f"scene_{scene_index:02d}.srt"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Whisper 전사
        result = self.transcribe(audio_path)

        # SRT 생성
        srt_content = self._build_srt(result["segments"], max_chars_per_line)
        output_path.write_text(srt_content, encoding="utf-8")
        print(f"[SubtitleSync] Saved: {output_path}")
        return output_path

    def generate_srt_batch(
        self,
        audio_paths: list[Path],
    ) -> list[Path]:
        """여러 오디오 파일에서 SRT 자막을 일괄 생성한다.

        Args:
            audio_paths: WAV 파일 경로 목록.

        Returns:
            생성된 SRT 파일 경로 목록.
        """
        srt_paths = []
        for i, audio_path in enumerate(audio_paths, start=1):
            srt_path = self.generate_srt(audio_path=audio_path, scene_index=i)
            srt_paths.append(srt_path)
        return srt_paths

    def _build_srt(self, segments: list[dict], max_chars: int) -> str:
        """Whisper segments를 SRT 형식 문자열로 변환한다."""
        srt_entries = []
        index = 1

        for segment in segments:
            # 단어 단위 타임스탬프가 있으면 활용
            words = segment.get("words", [])
            if words:
                entries = self._words_to_srt_entries(words, max_chars, index)
                srt_entries.extend(entries)
                index += len(entries)
            else:
                # 세그먼트 단위 자막
                start = self._format_time(segment["start"])
                end = self._format_time(segment["end"])
                text = segment["text"].strip()
                srt_entries.append(f"{index}\n{start} --> {end}\n{text}\n")
                index += 1

        return "\n".join(srt_entries)

    def _words_to_srt_entries(
        self, words: list[dict], max_chars: int, start_index: int
    ) -> list[str]:
        """단어 목록을 max_chars 기준으로 묶어 SRT 엔트리로 변환한다."""
        entries = []
        current_words = []
        current_text = ""
        index = start_index

        for word_info in words:
            word = word_info.get("word", word_info.get("text", "")).strip()
            if not word:
                continue

            test_text = f"{current_text} {word}".strip() if current_text else word

            if len(test_text) > max_chars and current_words:
                # 현재 묶음 완성
                start = self._format_time(current_words[0]["start"])
                end = self._format_time(current_words[-1]["end"])
                entries.append(f"{index}\n{start} --> {end}\n{current_text}\n")
                index += 1
                current_words = [word_info]
                current_text = word
            else:
                current_words.append(word_info)
                current_text = test_text

        # 마지막 묶음
        if current_words:
            start = self._format_time(current_words[0]["start"])
            end = self._format_time(current_words[-1]["end"])
            entries.append(f"{index}\n{start} --> {end}\n{current_text}\n")

        return entries

    @staticmethod
    def _format_time(seconds: float) -> str:
        """초를 SRT 시간 형식(HH:MM:SS,mmm)으로 변환한다."""
        td = timedelta(seconds=seconds)
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
