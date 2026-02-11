---
name: generate-subtitle
description: Whisper large-v3로 오디오에서 타임스탬프를 추출하고 SRT 자막을 생성합니다. TTS 오디오의 자막 싱크가 필요할 때, 정확한 단어별 타이밍이 필요할 때 사용하세요.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Generate Subtitle

Whisper large-v3 모델로 오디오 파일에서 단어별 타임스탬프를 추출하고 SRT 자막 파일을 생성합니다.

## Instructions

1. TTS로 생성된 WAV 오디오 파일을 준비합니다.
2. `SubtitleSync.generate_srt()`를 호출합니다.
3. Whisper가 단어별 타임스탬프를 추출합니다.
4. 자동으로 한 줄당 적정 글자 수로 분할된 SRT 파일이 생성됩니다.
5. 출력: `output/subtitles/scene_XX.srt`

## Usage

```python
from src.quote_video.config import Config
from src.quote_video.subtitle_sync import SubtitleSync

# 단일 SRT 생성
config = Config()
sync = SubtitleSync(config)
sync.generate_srt(audio_path="output/audio/scene_01.wav", scene_index=1)

# 한 줄 최대 글자 수 조정
sync.generate_srt(
    audio_path="output/audio/scene_01.wav",
    scene_index=1,
    max_chars_per_line=25,
)

# 여러 오디오 일괄 SRT 생성
from pathlib import Path
audio_paths = [Path(f"output/audio/scene_{i:02d}.wav") for i in range(1, 13)]
srt_paths = sync.generate_srt_batch(audio_paths)

# 타임스탬프만 추출 (디버깅용)
result = sync.transcribe("output/audio/scene_01.wav")
for seg in result["segments"]:
    print(f"{seg['start']:.2f} - {seg['end']:.2f}: {seg['text']}")
```

## Config

| 항목 | 값 | 설명 |
|------|-----|------|
| 모델 | `large-v3` | Whisper 최대 성능 모델, 고정 |
| 언어 | `ko` (한국어) | 한국어 최적화 |
| 단어 타임스탬프 | `True` | 단어별 정밀 싱크 |
| 줄당 최대 글자 | 30자 | 자막 가독성 기본값 |

## Features

1. **단어별 타임스탬프**: Whisper word_timestamps로 정밀한 자막 싱크
2. **자동 줄 분할**: max_chars_per_line 기준으로 자막을 적절히 나눔
3. **SRT 표준 형식**: 모든 영상 편집 도구와 호환
4. **Lazy 모델 로딩**: 첫 호출 시에만 Whisper 모델을 로드 (메모리 최적화)
5. **일괄 처리**: 여러 오디오 파일의 SRT를 한 번에 생성
