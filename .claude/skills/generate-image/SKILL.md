---
name: generate-image
description: Gemini 3 Pro로 스타일별 일러스트 이미지를 생성합니다. 명언 영상의 배경 이미지가 필요할 때, 철학적/예술적 씬 이미지를 만들 때 사용하세요.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Generate Image

Gemini 3 Pro 이미지 생성 모델을 사용해 오디오북 영상의 배경 일러스트를 생성합니다.

## Instructions

1. `image_prompt` (영어)를 준비합니다 — 씬의 시각적 묘사를 담아야 합니다.
2. 이미지 스타일을 선택합니다 (기본: pencil_sketch).
3. `ImageGenerator.generate()` 또는 `generate_batch()`를 호출합니다.
4. 생성된 이미지는 `output/images/scene_XX.png`에 저장됩니다.

## Usage

```python
from src.quote_video.config import Config
from src.quote_video.image_generator import ImageGenerator

# 단일 이미지 생성
config = Config(image_style="pencil_sketch")
gen = ImageGenerator(config)
gen.generate(prompt="A lone philosopher sitting under a willow tree", scene_index=1)

# 스타일 변경해서 생성
gen.generate(prompt="Moonlit ocean waves", scene_index=2, style="watercolor")

# 여러 씬 일괄 생성
scenes = [
    {"image_prompt": "A lone philosopher sitting under a willow tree", "narration": "..."},
    {"image_prompt": "Moonlit ocean waves crashing on rocks", "narration": "..."},
]
paths = gen.generate_batch(scenes, style="ink_wash")
```

## Config

| 항목 | 값 | 설명 |
|------|-----|------|
| 모델 | `gemini-3-pro-image-preview` | 고정, 변경 불가 |
| 해상도 | 1920x1080 | 영상 기본 해상도 |
| API 키 | `GEMINI_API_KEY` 환경변수 | 필수 |

## Styles

| 키 | 이름 | 설명 |
|-----|------|------|
| `pencil_sketch` | 연필 스케치 | 빈티지 크림색 종이, 볼드 잉크 아웃라인, 미니멀 |
| `watercolor` | 수채화 일러스트 | 파스텔 워시, 부드러운 번짐, 몽환적 분위기 |
| `ink_wash` | 수묵화 | 동양화 먹 기법, 여백의 미, 명상적 무드 |

## Features

1. **스타일 선택**: pencil_sketch, watercolor, ink_wash 3종 중 선택
2. **일괄 생성**: scenes 리스트를 넘기면 전체 이미지를 순차 생성
3. **경로 자동 관리**: output/images/scene_XX.png 자동 저장
4. **커스텀 경로**: output_path 파라미터로 저장 경로 지정 가능
