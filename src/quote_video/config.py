"""공통 설정 모듈 - API 키, 모델명, 경로, 스타일 프롬프트."""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


# ── 프로젝트 경로 ──────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ASSETS_DIR = PROJECT_ROOT / "assets"
OUTPUT_DIR = PROJECT_ROOT / "output"

FONT_PATH = ASSETS_DIR / "font" / "KOTRA_SONGEULSSI.ttf"
BGM_DIR = ASSETS_DIR / "bgm"

OUTPUT_IMAGES = OUTPUT_DIR / "images"
OUTPUT_AUDIO = OUTPUT_DIR / "audio"
OUTPUT_SUBTITLES = OUTPUT_DIR / "subtitles"
OUTPUT_CLIPS = OUTPUT_DIR / "clips"


# ── TTS 보이스 ─────────────────────────────────────────────────
TTSVoice = Literal["Zephyr", "Aoede", "Kore", "Leda"]

TTS_VOICES: dict[str, str] = {
    "Zephyr": "밝고 생동감 있는 여성 톤",
    "Aoede": "따뜻하고 부드러운 여성 톤",
    "Kore": "맑고 또렷한 여성 톤",
    "Leda": "차분하고 우아한 여성 톤",
}

# ── 이미지 스타일 ──────────────────────────────────────────────
ImageStyle = Literal["pencil_sketch", "watercolor", "ink_wash"]

IMAGE_STYLES: dict[str, dict[str, str]] = {
    "pencil_sketch": {
        "name": "연필 스케치",
        "prompt_prefix": (
            "Pencil sketch on vintage cream-colored paper. "
            "Bold black ink outlines, minimal shading, clean composition. "
            "Notion-style minimalist illustration. "
            "No color, only graphite pencil strokes on aged paper texture."
        ),
    },
    "watercolor": {
        "name": "수채화 일러스트",
        "prompt_prefix": (
            "Delicate watercolor illustration on textured white paper. "
            "Soft pastel washes with gentle color bleeding at edges. "
            "Dreamy, ethereal atmosphere with muted tones. "
            "Loose brushwork, organic shapes, subtle gradients."
        ),
    },
    "ink_wash": {
        "name": "수묵화",
        "prompt_prefix": (
            "Traditional East Asian ink wash painting (수묵화/水墨画). "
            "Black sumi ink on rice paper with elegant brushstrokes. "
            "Varying ink density from deep black to pale gray washes. "
            "Zen minimalism, negative space, contemplative mood."
        ),
    },
}


# ── 설정 데이터클래스 ──────────────────────────────────────────
@dataclass
class Config:
    """파이프라인 전체 설정."""

    # API
    gemini_api_key: str = field(
        default_factory=lambda: os.environ.get("GEMINI_API_KEY", "")
    )

    # 이미지 생성
    image_model: str = "gemini-3-pro-image-preview"
    image_style: ImageStyle = "pencil_sketch"
    image_width: int = 1920
    image_height: int = 1080

    # TTS
    tts_model: str = "gemini-2.5-pro-preview-tts"
    tts_voice: TTSVoice = "Zephyr"
    tts_sample_rate: int = 24000
    tts_channels: int = 1  # mono

    # Whisper
    whisper_model: str = "large-v3"
    whisper_language: str = "ko"

    # 영상 합성
    video_fps: int = 30
    video_width: int = 1920
    video_height: int = 1080
    fade_duration: float = 0.5  # 초
    bgm_volume: float = 0.15  # 15%

    # 경로
    output_dir: Path = OUTPUT_DIR
    font_path: Path = FONT_PATH
    bgm_dir: Path = BGM_DIR

    def get_style_prompt(self, custom_prompt: str = "") -> str:
        """현재 이미지 스타일의 프롬프트 프리픽스 + 커스텀 프롬프트를 합쳐 반환."""
        style = IMAGE_STYLES[self.image_style]
        parts = [style["prompt_prefix"]]
        if custom_prompt:
            parts.append(custom_prompt)
        return " ".join(parts)

    def ensure_dirs(self) -> None:
        """출력 디렉토리들이 존재하도록 생성."""
        for d in [OUTPUT_IMAGES, OUTPUT_AUDIO, OUTPUT_SUBTITLES, OUTPUT_CLIPS]:
            d.mkdir(parents=True, exist_ok=True)
