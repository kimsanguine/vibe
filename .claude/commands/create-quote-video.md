# /create-quote-video

명언 오디오북 영상을 자동으로 생성합니다.

## Usage

```
/create-quote-video <테마 또는 인물> [옵션]
```

### Examples

```
/create-quote-video 쇼펜하우어
/create-quote-video 스토아 철학 --voice Leda --style watercolor
/create-quote-video 니체 --count 8 --bgm assets/bgm/gymnopedie_no1.mp3
/create-quote-video 위로의 말 --voice Aoede --style ink_wash --bgm-volume 0.2
```

## Options

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--count` | 12 | 명언 개수 |
| `--voice` | Zephyr | TTS 보이스 (Zephyr, Aoede, Kore, Leda) |
| `--style` | pencil_sketch | 이미지 스타일 (pencil_sketch, watercolor, ink_wash) |
| `--bgm` | (없음) | BGM 파일 경로 |
| `--bgm-volume` | 0.15 | BGM 볼륨 (0.0~1.0) |
| `--tone` | contemplative | 분위기 프리셋 (contemplative, hopeful, melancholic, stoic) |

## Pipeline Flow

```
┌─────────────────────────────────────────────────────┐
│  /create-quote-video 쇼펜하우어 --voice Zephyr      │
└──────────────┬──────────────────────────────────────┘
               ▼
┌──────────────────────────────┐
│  1. quote-writer 에이전트     │
│     → 명언 선별               │
│     → 이미지 프롬프트 작성     │
│     → scenes 데이터 구성       │
└──────────────┬───────────────┘
               ▼
┌──────────────────────────────┐
│  2. video-orchestrator       │
│     에이전트                  │
│                              │
│  ┌────────────────────────┐  │
│  │ generate-image 스킬     │  │
│  │ → Gemini 3 Pro          │  │
│  │ → output/images/        │  │
│  └───────────┬────────────┘  │
│              ▼               │
│  ┌────────────────────────┐  │
│  │ generate-tts 스킬       │  │
│  │ → Gemini TTS            │  │
│  │ → output/audio/         │  │
│  └───────────┬────────────┘  │
│              ▼               │
│  ┌────────────────────────┐  │
│  │ generate-subtitle 스킬  │  │
│  │ → Whisper large-v3      │  │
│  │ → output/subtitles/     │  │
│  └───────────┬────────────┘  │
│              ▼               │
│  ┌────────────────────────┐  │
│  │ compose-video 스킬      │  │
│  │ → FFmpeg                │  │
│  │ → output/clips/         │  │
│  │ → output/final_video.mp4│  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

## Execution Steps

이 커맨드를 실행하면 다음 순서로 진행됩니다:

### Step 1: 콘텐츠 기획 (quote-writer)
- 주어진 테마/인물에 맞는 명언을 선별합니다.
- 각 명언에 맞는 영어 이미지 프롬프트를 작성합니다.
- `scenes` 리스트를 구성합니다.

### Step 2: 이미지 생성 (generate-image)
```python
from src.quote_video.image_generator import ImageGenerator
gen = ImageGenerator(config)
image_paths = gen.generate_batch(scenes, style=style)
# → output/images/scene_01.png ~ scene_12.png
```

### Step 3: TTS 나레이션 생성 (generate-tts)
```python
from src.quote_video.tts_generator import TTSGenerator
tts = TTSGenerator(config)
audio_paths = tts.generate_batch(scenes, voice=voice)
# → output/audio/scene_01.wav ~ scene_12.wav
```

### Step 4: 자막 생성 (generate-subtitle)
```python
from src.quote_video.subtitle_sync import SubtitleSync
sync = SubtitleSync(config)
srt_paths = sync.generate_srt_batch(audio_paths)
# → output/subtitles/scene_01.srt ~ scene_12.srt
```

### Step 5: 영상 합성 + BGM (compose-video)
```python
from src.quote_video.video_composer import VideoComposer
composer = VideoComposer(config)
clip_paths = composer.compose_batch(image_paths, audio_paths, srt_paths)
final = composer.concatenate(clip_paths, bgm_path=bgm_path)
# → output/final_video.mp4
```

## Output Structure

```
output/
├── images/
│   ├── scene_01.png
│   ├── scene_02.png
│   └── ...
├── audio/
│   ├── scene_01.wav
│   ├── scene_02.wav
│   └── ...
├── subtitles/
│   ├── scene_01.srt
│   ├── scene_02.srt
│   └── ...
├── clips/
│   ├── scene_01.mp4
│   ├── scene_02.mp4
│   └── ...
└── final_video.mp4          ← 최종 결과물
```

## Quick Start

가장 빠른 시작:

```
/create-quote-video 쇼펜하우어
```

이것만으로 12개 명언 영상이 자동 생성됩니다:
- 이미지: 연필 스케치 스타일
- 보이스: Zephyr (밝은 여성 톤)
- 자막: 손글씨체
- BGM: 없음

커스텀 예시:

```
/create-quote-video 마르쿠스 아우렐리우스 \
  --count 10 \
  --voice Leda \
  --style ink_wash \
  --tone stoic \
  --bgm assets/bgm/gymnopedie_no1.mp3 \
  --bgm-volume 0.12
```
