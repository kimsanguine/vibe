---
name: shorts-video-maker
description: |
  YouTube 영상에서 쇼츠 클립 3개를 자동 제작합니다.
  yt-dlp로 영상 다운로드, whisper로 자막 생성, ffmpeg로 클리핑을 수행합니다.
  "쇼츠 만들어줘", "영상 클립 추출해줘", "쇼츠 영상 제작해줘" 요청 시 USE PROACTIVELY.
  shorts-scriptwriter의 대본을 참조하여 클립 구간을 선정합니다.
allowed-tools: Read, Write, Bash
---

# 쇼츠 영상 제작 스킬

YouTube 영상에서 자동으로 쇼츠 클립을 추출하고 제작합니다.

## 기능

1. **영상 다운로드** (yt-dlp)
2. **자막 추출** (whisper)
3. **클립 제작** (ffmpeg - 9:16 크롭 + 자막)

## 필수 요구사항

```bash
# 설치 필요
pip install yt-dlp
pip install openai-whisper
brew install ffmpeg  # macOS
# apt install ffmpeg  # Ubuntu
```

## 워크플로우

### 전체 흐름

```
[YouTube URL]
    │
    ▼
[1. 영상 다운로드] ─── scripts/download_video.py
    │
    ▼
[2. 자막 추출] ─────── scripts/transcribe.py
    │
    ▼
[3. 대본 참조] ─────── outputs/shorts-scripts/
    │
    ▼
[4. 클립 제작] ─────── scripts/cut_shorts.py
    │
    ▼
[outputs/shorts-videos/]
```

### 1단계: 영상 다운로드

```bash
python scripts/download_video.py "YOUTUBE_URL" --output ./temp/
```

자세한 내용: [scripts/download_video.py](scripts/download_video.py)

### 2단계: 자막 추출

```bash
python scripts/transcribe.py ./temp/video.mp4 --output ./temp/transcript.json
```

자세한 내용: [scripts/transcribe.py](scripts/transcribe.py)

### 3단계: 클립 구간 선정

`outputs/shorts-scripts/` 폴더의 대본을 참조하여 클립 구간을 선정합니다:
- `shorts-01.md` → 첫 번째 쇼츠
- `shorts-02.md` → 두 번째 쇼츠
- `shorts-03.md` → 세 번째 쇼츠

자막 타임스탬프와 대본 내용을 매칭하여 최적의 구간을 찾습니다.

### 4단계: 클립 제작

```bash
python scripts/cut_shorts.py \
  --input ./temp/video.mp4 \
  --start "00:01:30" \
  --end "00:02:30" \
  --subtitle "./temp/transcript.srt" \
  --output ./outputs/shorts-videos/shorts-01.mp4
```

자세한 내용: [scripts/cut_shorts.py](scripts/cut_shorts.py)

## 쇼츠 스펙

자세한 가이드: [references/shorts-spec.md](references/shorts-spec.md)

### 기본 사양

| 항목 | 값 |
|------|-----|
| 비율 | 9:16 (세로) |
| 해상도 | 1080 x 1920px |
| 길이 | 15-60초 |
| 형식 | MP4 (H.264) |
| 프레임레이트 | 30fps |

### 자막 설정

```
위치: 하단 중앙
폰트: 굵은 산세리프
크기: 화면 너비의 80%
배경: 반투명 검정 박스
```

## 스크립트 사용법

### download_video.py

```bash
# 기본 사용
python scripts/download_video.py "https://youtube.com/watch?v=xxx"

# 옵션
python scripts/download_video.py "URL" \
  --output ./temp/ \
  --quality best \
  --format mp4
```

### transcribe.py

```bash
# 기본 사용
python scripts/transcribe.py ./temp/video.mp4

# 옵션
python scripts/transcribe.py ./temp/video.mp4 \
  --output ./temp/transcript.json \
  --model base \
  --language ko
```

### cut_shorts.py

```bash
# 기본 사용
python scripts/cut_shorts.py \
  --input ./temp/video.mp4 \
  --start "00:01:30" \
  --end "00:02:30" \
  --output ./outputs/shorts-videos/shorts-01.mp4

# 전체 옵션
python scripts/cut_shorts.py \
  --input ./temp/video.mp4 \
  --start "00:01:30" \
  --end "00:02:30" \
  --subtitle ./temp/transcript.srt \
  --crop center \
  --output ./outputs/shorts-videos/shorts-01.mp4
```

## 출력 구조

```
outputs/shorts-videos/
├── shorts-01.mp4  (첫 번째 쇼츠)
├── shorts-02.mp4  (두 번째 쇼츠)
└── shorts-03.mp4  (세 번째 쇼츠)

temp/  (임시 파일)
├── video.mp4      (원본 영상)
├── transcript.json (자막 데이터)
└── transcript.srt  (SRT 자막 파일)
```

## 클립 구간 선정 가이드

### 좋은 클립의 조건

```
✅ 선정 기준:
- 시작이 후킹으로 시작 (대본 참조)
- 하나의 완결된 메시지
- 60초 이내
- 말이 끊기지 않는 자연스러운 구간
- 화면 전환이 깔끔한 지점

❌ 피해야 할 구간:
- 말이 중간에 끊기는 곳
- 너무 긴 침묵
- 화면이 흔들리는 부분
- 저작권 음악이 큰 부분
```

### 대본-자막 매칭 방법

```python
# 대본의 핵심 키워드로 자막에서 시작점 찾기
keywords = ["첫 번째", "두 번째", "꿀팁"]

# 자막에서 해당 키워드가 나오는 타임스탬프 확인
for segment in transcript:
    if any(kw in segment['text'] for kw in keywords):
        print(f"Found at {segment['start']} - {segment['end']}")
```

## 에러 처리

### 일반적인 문제

```
문제: yt-dlp 다운로드 실패
→ 해결: yt-dlp 업데이트 (pip install -U yt-dlp)

문제: whisper 메모리 부족
→ 해결: 작은 모델 사용 (--model tiny 또는 base)

문제: ffmpeg 코덱 에러
→ 해결: libx264 설치 확인
```

## 참고

- 반드시 `outputs/shorts-scripts/`의 대본을 먼저 확인하세요
- 원본 영상의 저작권을 확인하세요
- 임시 파일은 작업 완료 후 삭제해도 됩니다
- 영상 품질은 원본에 따라 달라집니다
