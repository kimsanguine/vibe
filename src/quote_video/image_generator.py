"""Gemini 3 Pro 이미지 생성 모듈."""

import base64
import json
from pathlib import Path

from google import genai
from google.genai import types

from .config import Config, IMAGE_STYLES, OUTPUT_IMAGES


class ImageGenerator:
    """Gemini 3 Pro를 사용해 스타일별 일러스트 이미지를 생성한다."""

    def __init__(self, config: Config | None = None):
        self.config = config or Config()
        self.client = genai.Client(api_key=self.config.gemini_api_key)

    def generate(
        self,
        prompt: str,
        output_path: str | Path | None = None,
        style: str | None = None,
        scene_index: int = 1,
    ) -> Path:
        """이미지를 생성하고 파일로 저장한다.

        Args:
            prompt: 씬 설명 (영어 권장).
            output_path: 저장 경로. None이면 output/images/scene_{index}.png.
            style: 이미지 스타일 키. None이면 config 기본값 사용.
            scene_index: 씬 번호 (파일명에 사용).

        Returns:
            저장된 이미지 파일 경로.
        """
        # 스타일 결정
        use_style = style or self.config.image_style
        if use_style not in IMAGE_STYLES:
            raise ValueError(
                f"Unknown style '{use_style}'. "
                f"Available: {list(IMAGE_STYLES.keys())}"
            )

        # 프롬프트 합성
        style_info = IMAGE_STYLES[use_style]
        full_prompt = f"{style_info['prompt_prefix']} {prompt}"

        # 출력 경로
        if output_path is None:
            OUTPUT_IMAGES.mkdir(parents=True, exist_ok=True)
            output_path = OUTPUT_IMAGES / f"scene_{scene_index:02d}.png"
        else:
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

        # Gemini 이미지 생성 요청
        response = self.client.models.generate_content(
            model=self.config.image_model,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["image"],
            ),
        )

        # 응답에서 이미지 추출 및 저장
        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                output_path.write_bytes(image_data)
                print(f"[ImageGenerator] Saved: {output_path} (style: {use_style})")
                return output_path

        raise RuntimeError("Gemini 응답에 이미지 데이터가 없습니다.")

    def generate_batch(
        self,
        scenes: list[dict],
        style: str | None = None,
    ) -> list[Path]:
        """여러 씬의 이미지를 일괄 생성한다.

        Args:
            scenes: [{"image_prompt": "...", ...}, ...] 형식의 씬 목록.
            style: 이미지 스타일 키. None이면 config 기본값 사용.

        Returns:
            생성된 이미지 경로 목록.
        """
        paths = []
        for i, scene in enumerate(scenes, start=1):
            prompt = scene.get("image_prompt", "")
            if not prompt:
                raise ValueError(f"Scene {i}: 'image_prompt' is required.")
            path = self.generate(
                prompt=prompt,
                scene_index=i,
                style=style,
            )
            paths.append(path)
        return paths
