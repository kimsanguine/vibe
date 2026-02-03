# Thumbnail Preview Skill (썸네일 프리뷰 스킬)

전체 프리젠테이션을 **한 눈에 조감**할 수 있는 썸네일 그리드를 생성하는 스킬입니다.

---

## 핵심 철학

> "See the forest, not just the trees."
> 나무가 아닌 숲을 보라.

개별 슬라이드만 보면 전체적인 **일관성**, **시각적 리듬**, **스토리 흐름**을 파악하기 어렵습니다.
이 스킬은 모든 슬라이드를 **하나의 이미지**로 조합하여 전체 그림을 볼 수 있게 합니다.

---

## 1. 기능 개요

### 1.1 주요 기능
- 슬라이드 이미지를 그리드 형태로 조합
- 슬라이드 번호 오버레이
- 전체 프리젠테이션 조감도 생성

### 1.2 용도
- Visual QA Agent의 전체 일관성 평가
- 빠른 시각적 검토
- 스토리 흐름 확인
- 문제 슬라이드 식별

---

## 2. 출력 사양

### 2.1 기본 그리드 레이아웃

| 슬라이드 수 | 그리드 | 썸네일 크기 | 출력 크기 |
|------------|--------|------------|----------|
| 1-4 | 2×2 | 480×270 | 960×540 |
| 5-6 | 3×2 | 320×180 | 960×360 |
| 7-9 | 3×3 | 320×180 | 960×540 |
| 10-12 | 4×3 | 240×135 | 960×405 |
| 13-16 | 4×4 | 240×135 | 960×540 |
| 17-20 | 5×4 | 192×108 | 960×432 |
| 21+ | 5×5+ | 192×108 | 가변 |

### 2.2 썸네일 스타일

```css
/* 각 썸네일 스타일 */
.thumbnail {
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  margin: 8px;
}

/* 슬라이드 번호 배지 */
.slide-number {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background: rgba(0,0,0,0.7);
  color: white;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 2px;
}

/* 문제 슬라이드 강조 (옵션) */
.problem-slide {
  border: 2px solid #EF4444;
}
```

---

## 3. 생성 프로세스

### 3.1 입력
```
슬라이드 이미지 파일들:
- slide-1.png
- slide-2.png
- ...
- slide-N.png
```

### 3.2 처리 단계

```
1. 슬라이드 이미지 로드
2. 최적 그리드 레이아웃 계산
3. 썸네일 크기 리사이즈
4. 그리드 캔버스 생성
5. 썸네일 배치
6. 슬라이드 번호 오버레이
7. 출력 이미지 저장
```

### 3.3 Node.js 구현 예시

```javascript
import sharp from 'sharp';
import path from 'path';

async function createThumbnailGrid(slideImages, outputPath, options = {}) {
  const {
    columns = null,  // 자동 계산
    thumbnailWidth = 240,
    gap = 8,
    background = '#F8FAFC',
    showNumbers = true,
    problemSlides = []  // 강조할 슬라이드 번호
  } = options;

  const count = slideImages.length;

  // 최적 열 수 계산
  const cols = columns || Math.ceil(Math.sqrt(count));
  const rows = Math.ceil(count / cols);

  // 썸네일 크기 (16:9 비율 유지)
  const thumbWidth = thumbnailWidth;
  const thumbHeight = Math.round(thumbWidth * 9 / 16);

  // 캔버스 크기
  const canvasWidth = cols * (thumbWidth + gap) + gap;
  const canvasHeight = rows * (thumbHeight + gap) + gap;

  // 배경 캔버스 생성
  const canvas = sharp({
    create: {
      width: canvasWidth,
      height: canvasHeight,
      channels: 4,
      background: background
    }
  });

  // 썸네일 합성 준비
  const composites = [];

  for (let i = 0; i < slideImages.length; i++) {
    const row = Math.floor(i / cols);
    const col = i % cols;
    const x = gap + col * (thumbWidth + gap);
    const y = gap + row * (thumbHeight + gap);

    // 썸네일 리사이즈
    const thumbnail = await sharp(slideImages[i])
      .resize(thumbWidth, thumbHeight, { fit: 'cover' })
      .png()
      .toBuffer();

    composites.push({
      input: thumbnail,
      left: x,
      top: y
    });

    // 슬라이드 번호 배지 (SVG)
    if (showNumbers) {
      const isProblem = problemSlides.includes(i + 1);
      const badgeColor = isProblem ? '#EF4444' : 'rgba(0,0,0,0.7)';
      const badgeSvg = `
        <svg width="24" height="18">
          <rect width="24" height="18" rx="2" fill="${badgeColor}"/>
          <text x="12" y="13" text-anchor="middle"
                font-family="Arial" font-size="10" fill="white">
            ${i + 1}
          </text>
        </svg>
      `;

      composites.push({
        input: Buffer.from(badgeSvg),
        left: x + thumbWidth - 28,
        top: y + thumbHeight - 22
      });
    }
  }

  // 합성 및 저장
  await canvas
    .composite(composites)
    .png()
    .toFile(outputPath);

  return {
    path: outputPath,
    dimensions: { width: canvasWidth, height: canvasHeight },
    grid: { columns: cols, rows: rows },
    thumbnailSize: { width: thumbWidth, height: thumbHeight }
  };
}

export { createThumbnailGrid };
```

### 3.4 Bash 스크립트 (ImageMagick 사용)

```bash
#!/bin/bash
# create_thumbnail_grid.sh

INPUT_DIR="$1"
OUTPUT_FILE="$2"
COLS="${3:-4}"  # 기본 4열

# 썸네일 크기
THUMB_WIDTH=240
THUMB_HEIGHT=135

# 임시 디렉토리
TEMP_DIR=$(mktemp -d)

# 각 슬라이드를 썸네일로 변환
for img in "$INPUT_DIR"/slide-*.png; do
  filename=$(basename "$img")
  convert "$img" -resize ${THUMB_WIDTH}x${THUMB_HEIGHT} \
    -gravity SouthEast \
    -stroke none -fill 'rgba(0,0,0,0.7)' \
    -draw "roundrectangle 0,0 24,18 2,2" \
    "$TEMP_DIR/$filename"
done

# 그리드로 조합
montage "$TEMP_DIR"/slide-*.png \
  -tile ${COLS}x \
  -geometry ${THUMB_WIDTH}x${THUMB_HEIGHT}+8+8 \
  -background '#F8FAFC' \
  "$OUTPUT_FILE"

# 정리
rm -rf "$TEMP_DIR"

echo "썸네일 그리드 생성 완료: $OUTPUT_FILE"
```

---

## 4. 출력 형식

### 4.1 기본 출력

```
thumbnail_grid.png
├── 해상도: 960×540+ (그리드 크기에 따라 가변)
├── 형식: PNG
├── 배경: #F8FAFC (밝은 회색)
└── 각 썸네일에 번호 배지 포함
```

### 4.2 문제 슬라이드 강조 모드

Visual QA Agent가 문제 슬라이드를 식별한 경우:

```
thumbnail_grid_annotated.png
├── 문제 슬라이드: 빨간 테두리 (#EF4444)
├── 정상 슬라이드: 기본 스타일
└── 번호 배지: 문제 슬라이드는 빨간색
```

---

## 5. Visual QA Agent와의 통합

### 5.1 워크플로우

```
PPTX 생성 완료
    ↓
이미지 변환 (slide-1.png ~ slide-N.png)
    ↓
┌─────────────────────────────────┐
│  Thumbnail Preview Skill       │
│  → thumbnail_grid.png 생성     │
└─────────────────────────────────┘
    ↓
Visual QA Agent
├── 1. 전체 그리드로 일관성 평가
└── 2. 개별 슬라이드 상세 평가
```

### 5.2 데이터 전달

```json
{
  "thumbnail_grid": {
    "path": "output/thumbnail_grid.png",
    "dimensions": {"width": 960, "height": 540},
    "slide_count": 10,
    "grid": {"columns": 4, "rows": 3}
  },
  "slide_images": [
    "output/slide-1.png",
    "output/slide-2.png",
    // ...
  ]
}
```

---

## 6. 추가 기능

### 6.1 비교 그리드 (Before/After)

두 버전의 프리젠테이션을 나란히 비교:

```
┌─────────────────┬─────────────────┐
│   Version 1     │   Version 2     │
├─────────────────┼─────────────────┤
│  [1] [2] [3]    │  [1] [2] [3]    │
│  [4] [5] [6]    │  [4] [5] [6]    │
│  [7] [8] [9]    │  [7] [8] [9]    │
└─────────────────┴─────────────────┘
```

### 6.2 섹션 구분 그리드

프리젠테이션 섹션별로 그룹화:

```
┌─ 도입부 ────────────────────────┐
│  [1: 타이틀] [2: 어젠다]        │
└─────────────────────────────────┘
┌─ 본론 ──────────────────────────┐
│  [3] [4] [5] [6] [7]            │
└─────────────────────────────────┘
┌─ 결론 ──────────────────────────┐
│  [8: 요약] [9: Thank You]       │
└─────────────────────────────────┘
```

### 6.3 히트맵 오버레이

평가 점수 기반 색상 코딩:

```
점수 범위 → 색상
90-100: 초록 (#10B981)
80-89:  연두 (#84CC16)
70-79:  노랑 (#FBBF24)
60-69:  주황 (#F97316)
0-59:   빨강 (#EF4444)
```

---

## 7. 의존성

```json
{
  "node": {
    "sharp": "^0.33.0"
  },
  "system": [
    "ImageMagick (선택)",
    "LibreOffice (PPTX→이미지용)"
  ]
}
```

---

## 8. 출력물

이 스킬로 생성되는 파일:

1. **thumbnail_grid.png** - 기본 썸네일 그리드
2. **thumbnail_grid_annotated.png** - 문제 슬라이드 강조 버전 (선택)
3. **comparison_grid.png** - Before/After 비교 (선택)
4. **heatmap_grid.png** - 점수 기반 히트맵 (선택)

---

## 9. 사용 예시

### 9.1 기본 사용

```bash
# Node.js
node create-thumbnail.js ./slides/ ./output/thumbnail_grid.png

# Bash (ImageMagick)
./create_thumbnail_grid.sh ./slides/ ./output/thumbnail_grid.png 4
```

### 9.2 문제 슬라이드 강조

```javascript
await createThumbnailGrid(slideImages, 'thumbnail_grid.png', {
  problemSlides: [3, 7, 9],  // Visual QA에서 식별된 문제 슬라이드
  showNumbers: true
});
```

### 9.3 비교 그리드

```javascript
await createComparisonGrid(
  v1SlideImages,
  v2SlideImages,
  'comparison_grid.png'
);
```
