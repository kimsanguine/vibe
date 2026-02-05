"""Gemini TTS 나레이션 생성 모듈."""

import wave
from pathlib import Path

from google import genai
from google.genai import types

from .config import Config, TTS_VOICES, TTSVoice, OUTPUT_AUDIO


class TTSGenerator:
    """Gemini TTS를 사용해 나레이션 오디오를 생성한다."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.client = genai.Client(api_key=self.config.gemini_api_key)

    def generate(
        self,
        text: str,
        output_path: str | Path | None = None,
        voice: TTSVoice | None = None,
        scene_index: int = 1,
    ) -> Path:
        """텍스트를 음성으로 변환하고 WAV 파일로 저장한다.

        Args:
            text: 나레이션 텍스트 (한국어).
            output_path: 저장 경로. None이면 output/audio/scene_{index}.wav.
            voice: TTS 보이스. None이면 config 기본값(Zephyr) 사용.
            scene_index: 씬 번호 (파일명에 사용).

        Returns:
            저장된 WAV 파일 경로.
        """
        use_voice = voice or self.config.tts_voice

        if use_voice not in TTS_VOICES:
            raise ValueError(
                f"Unknown voice '{use_voice}'. "
                f"Available: {list(TTS_VOICES.keys())}"
            )

        # 출력 경로
        if output_path is None:
            OUTPUT_AUDIO.mkdir(parents=True, exist_ok=True)
            output_path = OUTPUT_AUDIO / f"scene_{scene_index:02d}.wav"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Gemini TTS 요청
        response = self.client.models.generate_content(
            model=self.config.tts_model,
            contents=text,
            config=types.GenerateContentConfig(
                response_modalities=["audio"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=use_voice,
                        )
                    )
                ),
            ),
        )

        # 응답에서 오디오 추출
        audio_data = None
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                audio_data = part.inline_data.data
                break

        if audio_data is None:
            raise RuntimeError("Gemini 응답에 오디오 데이터가 없습니다.")

        # WAV 파일 저장
        self._save_wav(audio_data, output_path)
        print(f"[TTSGenerator] Saved: {output_path} (voice: {use_voice})")
        return output_path

    def generate_batch(
        self,
        scenes: list[dict],
        voice: TTSVoice | None = None,
    ) -> list[Path]:
        """여러 씬의 나레이션을 일괄 생성한다.

        Args:
            scenes: [{"narration": "...", ...}, ...] 형식의 씬 목록.
            voice: TTS 보이스. None이면 config 기본값 사용.

        Returns:
            생성된 WAV 파일 경로 목록.
        """
        paths = []
        for i, scene in enumerate(scenes, start=1):
            text = scene.get("narration", "")
            if not text:
                raise ValueError(f"Scene {i}: 'narration' is required.")
            path = self.generate(
                text=text,
                voice=voice,
                scene_index=i,
            )
            paths.append(path)
        return paths

    def _save_wav(self, pcm_data: bytes, output_path: Path) -> None:
        """PCM 데이터를 WAV 파일로 저장한다."""
        with wave.open(str(output_path), "wb") as wf:
            wf.setnchannels(self.config.tts_channels)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.config.tts_sample_rate)
            wf.writeframes(pcm_data)

    @staticmethod
    def list_voices() -> dict[str, str]:
        """사용 가능한 보이스 목록을 반환한다."""
        return dict(TTS_VOICES)
