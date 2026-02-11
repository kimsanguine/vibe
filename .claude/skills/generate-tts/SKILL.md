---
name: generate-tts
description: Gemini TTS로 여성 보이스 나레이션을 생성합니다. 명언 텍스트를 음성으로 변환할 때, 오디오북 나레이션이 필요할 때 사용하세요.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Generate TTS

Gemini 2.5 Pro TTS 모델을 사용해 한국어 텍스트를 자연스러운 여성 보이스로 변환합니다.

## Instructions

1. 나레이션 텍스트(한국어)를 준비합니다.
2. 보이스를 선택합니다 (기본: Zephyr).
3. `TTSGenerator.generate()` 또는 `generate_batch()`를 호출합니다.
4. 생성된 오디오는 `output/audio/scene_XX.wav`에 저장됩니다.

## Usage

```python
from src.quote_video.config import Config
from src.quote_video.tts_generator import TTSGenerator

# 단일 TTS 생성 (기본 Zephyr 보이스)
config = Config(tts_voice="Zephyr")
tts = TTSGenerator(config)
tts.generate(text="고통 없이 얻어진 것은 쉽게 사라진다.", scene_index=1)

# 보이스 변경
tts.generate(text="삶이 있는 한 희망은 있다.", scene_index=2, voice="Aoede")

# 여러 씬 일괄 생성
scenes = [
    {"narration": "고통 없이 얻어진 것은 쉽게 사라진다.", "image_prompt": "..."},
    {"narration": "삶이 있는 한 희망은 있다.", "image_prompt": "..."},
]
paths = tts.generate_batch(scenes, voice="Leda")

# 사용 가능한 보이스 목록 확인
print(TTSGenerator.list_voices())
```

## Config

| 항목 | 값 | 설명 |
|------|-----|------|
| 모델 | `gemini-2.5-pro-preview-tts` | 고정, 변경 불가 |
| 기본 보이스 | `Zephyr` | 런타임에 변경 가능 |
| 샘플레이트 | 24000Hz | WAV 출력 |
| 비트 | 16-bit mono | WAV 형식 |

## Voices

| 보이스 | 특징 | 추천 용도 |
|--------|------|-----------|
| **Zephyr** (기본) | 밝고 생동감 있는 여성 톤 | 에너지 있는 명언, 동기부여 |
| **Aoede** | 따뜻하고 부드러운 여성 톤 | 수면/명상 콘텐츠 |
| **Kore** | 맑고 또렷한 여성 톤 | 교육/강의 스타일 내레이션 |
| **Leda** | 차분하고 우아한 여성 톤 | 철학적/문학적 콘텐츠 |

## Features

1. **보이스 선택**: 4종 여성 보이스 중 런타임 선택 가능
2. **일괄 생성**: scenes 리스트로 전체 나레이션 순차 생성
3. **WAV 출력**: 24000Hz, 16-bit, mono WAV 파일로 저장
4. **보이스 조회**: `list_voices()`로 사용 가능한 보이스 확인
