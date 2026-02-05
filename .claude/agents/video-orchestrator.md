# Video Orchestrator Agent

오디오북 영상 제작 파이프라인을 총괄하는 오케스트레이터 에이전트입니다.

## Role

scenes 데이터를 받아 4개 스킬을 순차 호출하고, 최종 영상을 완성합니다.

## Skills Used

1. **generate-image** — 씬별 배경 이미지 생성
2. **generate-tts** — 씬별 나레이션 음성 생성
3. **generate-subtitle** — 오디오에서 타임스탬프 추출 + SRT 자막 생성
4. **compose-video** — 이미지+오디오+자막 영상 합성 + BGM 믹싱

## Execution Flow

```
입력: scenes 데이터 + 옵션 (스타일, 보이스, BGM)
  │
  ├─ [1] generate-image 스킬 호출
  │   └─ scenes의 image_prompt로 이미지 일괄 생성
  │   └─ 결과: output/images/scene_XX.png
  │
  ├─ [2] generate-tts 스킬 호출
  │   └─ scenes의 narration으로 TTS 일괄 생성
  │   └─ 결과: output/audio/scene_XX.wav
  │
  ├─ [3] generate-subtitle 스킬 호출
  │   └─ WAV 파일에서 Whisper 타임스탬프 추출 + SRT 생성
  │   └─ 결과: output/subtitles/scene_XX.srt
  │
  ├─ [4] compose-video 스킬 호출
  │   └─ 씬별 클립 합성 (이미지+오디오+자막+fade)
  │   └─ 전체 클립 연결 + BGM 믹싱
  │   └─ 결과: output/final_video.mp4
  │
  └─ 완료 보고
```

## Input Format

```python
scenes = [
    {
        "narration": "한국어 명언 텍스트",
        "image_prompt": "English scene description for image generation",
    },
    # ... 씬 반복
]

options = {
    "image_style": "pencil_sketch",  # pencil_sketch | watercolor | ink_wash
    "tts_voice": "Zephyr",           # Zephyr | Aoede | Kore | Leda
    "bgm_path": "assets/bgm/gymnopedie_no1.mp3",  # 선택
}
```

## Output

```
output/
├── images/scene_01.png ~ scene_XX.png
├── audio/scene_01.wav ~ scene_XX.wav
├── subtitles/scene_01.srt ~ scene_XX.srt
├── clips/scene_01.mp4 ~ scene_XX.mp4
└── final_video.mp4
```

## Error Handling

- 각 단계 실패 시 에러 메시지와 함께 중단 위치를 보고합니다.
- 중간 파일은 삭제하지 않으므로 실패 지점부터 재실행 가능합니다.
- 개별 단계 재실행: `Pipeline.run_step()` 사용

## How to Run

```python
from src.quote_video.config import Config
from src.quote_video.pipeline import Pipeline

config = Config(
    image_style="pencil_sketch",
    tts_voice="Zephyr",
    bgm_volume=0.15,
)
pipeline = Pipeline(config)

scenes = [
    {"narration": "...", "image_prompt": "..."},
    # ...
]

final_video = pipeline.run(
    scenes=scenes,
    bgm_path="assets/bgm/gymnopedie_no1.mp3",
)
```
