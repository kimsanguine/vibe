---
name: compose-video
description: FFmpeg로 이미지+오디오+자막을 영상으로 합성하고 BGM을 믹싱합니다. 씬별 영상 클립을 만들 때, 최종 영상을 완성할 때 사용하세요.
allowed-tools:
  - Bash
  - Read
  - Write
---

# Compose Video

FFmpeg를 사용해 이미지, 오디오, 자막을 하나의 영상 클립으로 합성하고, 여러 클립을 연결하며 BGM을 믹싱합니다.

## Instructions

1. 이미지, 오디오(WAV), 자막(SRT) 파일을 준비합니다.
2. `VideoComposer.compose_scene()`으로 씬별 클립을 생성합니다.
3. `VideoComposer.concatenate()`로 클립을 연결하고 BGM을 추가합니다.
4. 최종 출력: `output/final_video.mp4`

## Usage

```python
from src.quote_video.config import Config
from src.quote_video.video_composer import VideoComposer

config = Config()
composer = VideoComposer(config)

# 단일 씬 합성
composer.compose_scene(
    image_path="output/images/scene_01.png",
    audio_path="output/audio/scene_01.wav",
    srt_path="output/subtitles/scene_01.srt",
    scene_index=1,
)

# 여러 씬 일괄 합성
from pathlib import Path
image_paths = [Path(f"output/images/scene_{i:02d}.png") for i in range(1, 13)]
audio_paths = [Path(f"output/audio/scene_{i:02d}.wav") for i in range(1, 13)]
srt_paths = [Path(f"output/subtitles/scene_{i:02d}.srt") for i in range(1, 13)]

clip_paths = composer.compose_batch(image_paths, audio_paths, srt_paths)

# 최종 연결 + BGM 믹싱
final = composer.concatenate(
    clip_paths,
    bgm_path="assets/bgm/gymnopedie_no1.mp3",
)
```

## Config

| 항목 | 값 | 설명 |
|------|-----|------|
| 해상도 | 1920x1080 | Full HD |
| FPS | 30 | 프레임레이트 |
| Fade 효과 | 0.5초 | in/out 모두 적용 |
| BGM 볼륨 | 15% (0.15) | 나레이션 대비 배경 볼륨 |
| 코덱 | H.264 (libx264) + AAC | 범용 호환 |
| CRF | 23 | 화질/용량 밸런스 |
| 자막 폰트 | KOTRA_SONGEULSSI | 손글씨체, 하단 배치 |
| 자막 위치 | 하단 중앙, MarginV=60 | 가독성 확보 |

## Features

1. **씬별 합성**: 이미지+오디오+자막 → MP4 클립 (fade-in/out 효과 포함)
2. **일괄 합성**: compose_batch()로 전체 씬을 한 번에 처리
3. **클립 연결**: 여러 클립을 하나의 영상으로 concat
4. **BGM 믹싱**: BGM 파일을 루프 재생하며 지정 볼륨으로 나레이션과 믹싱
5. **자막 스타일링**: 커스텀 폰트, 외곽선, 하단 배치 자동 적용
6. **종횡비 보정**: 이미지를 영상 해상도에 맞게 scale + pad 처리
