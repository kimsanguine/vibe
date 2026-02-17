# PPTX Skill (PowerPoint 제작 스킬)

PowerPoint 프리젠테이션(.pptx)을 효과적으로 생성, 편집, 분석하는 스킬입니다.

## 개요

이 스킬은 HTML 기반 워크플로우를 통해 고품질 PowerPoint 파일을 생성하고, OOXML 형식을 직접 조작하여 세밀한 편집을 수행합니다.

## 핵심 워크플로우

### 워크플로우 1: HTML to PPTX (신규 프리젠테이션 생성)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 콘텐츠 구성  │ → │ HTML 슬라이드 │ → │  PPTX 생성   │
│   (JSON)    │    │   생성      │    │ (PptxGenJS) │
└─────────────┘    └─────────────┘    └─────────────┘
```

### 워크플로우 2: 템플릿 기반 생성

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ 템플릿 분석  │ → │  콘텐츠 매핑  │ → │   PPTX 출력  │
│             │    │  및 교체     │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
```

## HTML 슬라이드 작성 규칙

### 기본 구조

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .slide {
      width: 720pt;      /* 16:9 기준 */
      height: 405pt;
      padding: 40pt;
      box-sizing: border-box;
    }
  </style>
</head>
<body>
  <div class="slide">
    <!-- 슬라이드 콘텐츠 -->
  </div>
</body>
</html>
```

### 슬라이드 크기 규격

| 비율 | 너비 | 높이 |
|------|------|------|
| 16:9 (기본) | 720pt | 405pt |
| 4:3 | 720pt | 540pt |
| 16:10 | 720pt | 450pt |

### 텍스트 규칙 (중요!)

```html
<!-- ✅ 올바른 사용 -->
<h1>제목은 h1 태그로</h1>
<p>본문은 반드시 p 태그 안에</p>
<ul>
  <li>리스트는 ul/ol 태그 사용</li>
</ul>

<!-- ❌ 잘못된 사용 (무시됨) -->
<div>이 텍스트는 변환되지 않음</div>
<span>span만 사용하면 안 됨</span>
```

**핵심 규칙**: 모든 텍스트는 반드시 `<p>`, `<h1>`-`<h6>`, `<ul>`, `<ol>` 태그 안에 있어야 합니다.

### 웹 안전 폰트 목록

PowerPoint에서 정상적으로 렌더링되는 폰트:

```
Arial, Helvetica, Times New Roman, Georgia,
Courier New, Verdana, Trebuchet MS, Impact,
Comic Sans MS, Palatino Linotype
```

### 스타일링

#### 텍스트 포맷팅
```html
<p><b>굵게</b>, <i>기울임</i>, <u>밑줄</u></p>
<p style="color: #ff6b35; font-size: 24pt;">스타일 적용</p>
```

#### 도형 스타일 (div에만 적용)
```html
<div style="
  background-color: #1a1a2e;
  border: 2pt solid #e94560;
  border-radius: 10pt;
  box-shadow: 5pt 5pt 10pt rgba(0,0,0,0.3);
">
  <p>도형 안의 텍스트</p>
</div>
```

#### 금지 사항
```css
/* ❌ CSS 그라데이션 사용 금지 */
background: linear-gradient(...);  /* 변환 안 됨 */
background: radial-gradient(...);  /* 변환 안 됨 */
```

그라데이션이 필요한 경우 PNG 이미지로 미리 렌더링합니다.

## PptxGenJS 통합

### 차트 생성

```javascript
// 색상 지정 시 # 접두사 제거 필수!
slide.addChart(pptx.charts.BAR, chartData, {
  x: 1, y: 1, w: 8, h: 4,
  chartColors: ['FF6B35', '004E89', 'FCBF49'],  // ✅ # 없이
  // chartColors: ['#FF6B35', '#004E89'],       // ❌ 파일 손상
});
```

### 지원 차트 유형

| 차트 타입 | 코드 |
|----------|------|
| 막대 차트 | `pptx.charts.BAR` |
| 라인 차트 | `pptx.charts.LINE` |
| 파이 차트 | `pptx.charts.PIE` |
| 도넛 차트 | `pptx.charts.DOUGHNUT` |
| 산점도 | `pptx.charts.SCATTER` |
| 영역 차트 | `pptx.charts.AREA` |

### 이미지 추가

```javascript
slide.addImage({
  path: './images/chart.png',
  x: 1, y: 1, w: 6, h: 4
});

// Base64 이미지
slide.addImage({
  data: 'data:image/png;base64,...',
  x: 1, y: 1, w: 4, h: 3
});
```

### 테이블 생성

```javascript
slide.addTable([
  [{ text: '항목', options: { bold: true }}, '값'],
  ['데이터 1', '100'],
  ['데이터 2', '200'],
], {
  x: 1, y: 2, w: 8,
  border: { pt: 1, color: '000000' },
  fill: 'F5F5F5'
});
```

## 색상 팔레트 (html2pptx 내장)

### 사전 정의된 팔레트

```javascript
const PALETTES = {
  modern: ['1a1a2e', '16213e', 'e94560', 'f5f5f5'],
  ocean: ['0077b6', '00b4d8', '90e0ef', 'caf0f8'],
  sunset: ['ff6b35', 'ff8c42', 'ffd166', 'fcf8e8'],
  forest: ['2d5a27', '5a8a4c', '8fbc8f', 'c5e1a5'],
  midnight: ['0a0a0f', '1a1a2e', '00d4ff', '7b2cbf'],
  // ... 총 17개 팔레트
};
```

## OOXML 직접 편집

### 파일 구조

```
presentation.pptx (unzipped)
├── [Content_Types].xml
├── _rels/
├── docProps/
│   ├── app.xml
│   └── core.xml
└── ppt/
    ├── presentation.xml
    ├── slides/
    │   ├── slide1.xml
    │   └── slide2.xml
    ├── slideLayouts/
    ├── slideMasters/
    ├── theme/
    └── media/
```

### 언팩/리팩 명령어

```bash
# 언팩
python ooxml/scripts/unpack.py presentation.pptx ./output_dir

# 리팩
python ooxml/scripts/pack.py ./output_dir new_presentation.pptx

# 검증
python ooxml/scripts/validate.py presentation.pptx
```

### 슬라이드 XML 기본 구조

```xml
<?xml version="1.0" encoding="UTF-8"?>
<p:sld xmlns:p="...">
  <p:cSld>
    <p:spTree>
      <!-- 텍스트 상자 -->
      <p:sp>
        <p:txBody>
          <a:p>
            <a:r>
              <a:t>텍스트 내용</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
</p:sld>
```

## 유틸리티 스크립트

### 썸네일 생성
```bash
python scripts/thumbnail.py presentation.pptx
# 결과: presentation_thumb.png
```

### 슬라이드 이미지 변환
```bash
# LibreOffice를 통한 PDF 변환 후 이미지화
libreoffice --headless --convert-to pdf presentation.pptx
pdftoppm presentation.pdf slide -png
```

### 텍스트 추출
```bash
python -m markitdown presentation.pptx > content.md
```

## 의존성

```json
{
  "dependencies": {
    "pptxgenjs": "^3.12.0",
    "playwright": "^1.40.0",
    "sharp": "^0.33.0"
  },
  "system": [
    "LibreOffice",
    "Poppler (pdftoppm)",
    "Python 3.8+",
    "defusedxml"
  ]
}
```

## 품질 체크리스트

### 생성 전
- [ ] 콘텐츠 구조 JSON 검증
- [ ] 이미지 파일 존재 확인
- [ ] 폰트 사용 가능 여부 확인

### 생성 중
- [ ] 텍스트가 올바른 태그 안에 있는지
- [ ] 색상 코드에 # 없는지 (PptxGenJS)
- [ ] CSS 그라데이션 사용하지 않았는지

### 생성 후
- [ ] PowerPoint에서 정상 열림
- [ ] 모든 슬라이드 렌더링 확인
- [ ] 텍스트 인코딩 정상
- [ ] 이미지 표시 정상
- [ ] 차트 데이터 정확성

## 출력물

이 스킬로 생성되는 파일:

1. **presentation.pptx**: 최종 PowerPoint 파일
2. **slides.html**: 중간 HTML 파일 (디버깅용)
3. **thumbnails/**: 슬라이드 미리보기 이미지
