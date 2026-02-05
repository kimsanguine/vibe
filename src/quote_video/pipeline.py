"""전체 파이프라인 조율 모듈."""

from pathlib import Path

from .config import Config, ImageStyle, TTSVoice
from .image_generator import ImageGenerator
from .tts_generator import TTSGenerator
from .subtitle_sync import SubtitleSync
from .video_composer import VideoComposer


class Pipeline:
    """오디오북 영상 생성 파이프라인.

    scenes 데이터를 받아 이미지 → TTS → 자막 → 영상 합성 → 연결의
    전체 과정을 자동으로 수행한다.
    """

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.image_gen = ImageGenerator(self.config)
        self.tts_gen = TTSGenerator(self.config)
        self.subtitle_sync = SubtitleSync(self.config)
        self.video_composer = VideoComposer(self.config)

    def run(
        self,
        scenes: list[dict],
        bgm_path: str | Path | None = None,
        output_path: str | Path | None = None,
        image_style: ImageStyle | None = None,
        tts_voice: TTSVoice | None = None,
    ) -> Path:
        """전체 파이프라인을 실행한다.

        Args:
            scenes: 씬 데이터 목록.
                각 씬: {"narration": "한국어 텍스트", "image_prompt": "영어 설명"}
            bgm_path: BGM 파일 경로 (선택).
            output_path: 최종 영상 저장 경로 (선택).
            image_style: 이미지 스타일 오버라이드 (선택).
            tts_voice: TTS 보이스 오버라이드 (선택).

        Returns:
            최종 영상 MP4 파일 경로.
        """
        self.config.ensure_dirs()

        total = len(scenes)
        print(f"[Pipeline] Starting: {total} scenes")
        print(f"[Pipeline] Image style: {image_style or self.config.image_style}")
        print(f"[Pipeline] TTS voice: {tts_voice or self.config.tts_voice}")

        # ── Step 1: 이미지 생성 ───────────────────────────────
        print(f"\n{'='*50}")
        print("[Pipeline] Step 1/5: Generating images...")
        print(f"{'='*50}")
        image_paths = self.image_gen.generate_batch(scenes, style=image_style)

        # ── Step 2: TTS 생성 ──────────────────────────────────
        print(f"\n{'='*50}")
        print("[Pipeline] Step 2/5: Generating TTS narrations...")
        print(f"{'='*50}")
        audio_paths = self.tts_gen.generate_batch(scenes, voice=tts_voice)

        # ── Step 3: 타임스탬프 추출 + SRT 생성 ─────────────────
        print(f"\n{'='*50}")
        print("[Pipeline] Step 3/5: Extracting timestamps & generating subtitles...")
        print(f"{'='*50}")
        srt_paths = self.subtitle_sync.generate_srt_batch(audio_paths)

        # ── Step 4: 씬별 영상 합성 ────────────────────────────
        print(f"\n{'='*50}")
        print("[Pipeline] Step 4/5: Composing scene videos...")
        print(f"{'='*50}")
        clip_paths = self.video_composer.compose_batch(
            image_paths, audio_paths, srt_paths
        )

        # ── Step 5: 전체 연결 + BGM 믹싱 ──────────────────────
        print(f"\n{'='*50}")
        print("[Pipeline] Step 5/5: Concatenating clips & mixing BGM...")
        print(f"{'='*50}")
        final_path = self.video_composer.concatenate(
            clip_paths,
            output_path=output_path,
            bgm_path=bgm_path,
        )

        print(f"\n{'='*50}")
        print(f"[Pipeline] Done! Final video: {final_path}")
        print(f"{'='*50}")
        return final_path

    def run_step(
        self,
        step: str,
        scenes: list[dict] | None = None,
        audio_paths: list[Path] | None = None,
        image_paths: list[Path] | None = None,
        srt_paths: list[Path] | None = None,
        clip_paths: list[Path] | None = None,
        bgm_path: str | Path | None = None,
        **kwargs,
    ):
        """개별 단계만 실행한다 (디버깅/테스트용).

        Args:
            step: 실행할 단계 ("image", "tts", "subtitle", "compose", "concat").
            나머지: 각 단계에 필요한 입력 데이터.

        Returns:
            해당 단계의 출력 결과.
        """
        self.config.ensure_dirs()

        if step == "image":
            if scenes is None:
                raise ValueError("scenes is required for 'image' step.")
            return self.image_gen.generate_batch(scenes, **kwargs)

        elif step == "tts":
            if scenes is None:
                raise ValueError("scenes is required for 'tts' step.")
            return self.tts_gen.generate_batch(scenes, **kwargs)

        elif step == "subtitle":
            if audio_paths is None:
                raise ValueError("audio_paths is required for 'subtitle' step.")
            return self.subtitle_sync.generate_srt_batch(audio_paths)

        elif step == "compose":
            if not all([image_paths, audio_paths, srt_paths]):
                raise ValueError(
                    "image_paths, audio_paths, srt_paths are all required "
                    "for 'compose' step."
                )
            return self.video_composer.compose_batch(
                image_paths, audio_paths, srt_paths
            )

        elif step == "concat":
            if clip_paths is None:
                raise ValueError("clip_paths is required for 'concat' step.")
            return self.video_composer.concatenate(
                clip_paths, bgm_path=bgm_path
            )

        else:
            raise ValueError(
                f"Unknown step '{step}'. "
                f"Available: image, tts, subtitle, compose, concat"
            )
