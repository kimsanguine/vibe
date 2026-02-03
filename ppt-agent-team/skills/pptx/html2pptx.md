# HTML to PowerPoint 변환 가이드

HTML 슬라이드를 PowerPoint 프리젠테이션으로 변환하는 상세 가이드입니다.

## 개요

이 워크플로우는 다음 순서로 진행됩니다:

```
HTML 작성 → 브라우저 렌더링 → 스크린샷 캡처 → PptxGenJS로 PPTX 생성
```

## HTML 슬라이드 작성

### 기본 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    body {
      font-family: 'Pretendard', Arial, sans-serif;
    }

    .slide {
      width: 720pt;
      height: 405pt;
      padding: 40pt;
      position: relative;
      overflow: hidden;
    }
  </style>
</head>
<body>
  <div class="slide" id="slide-1">
    <!-- 슬라이드 콘텐츠 -->
  </div>
</body>
</html>
```

### 슬라이드 크기

| 화면 비율 | 너비 | 높이 | 용도 |
|----------|------|------|------|
| 16:9 | 720pt | 405pt | 와이드스크린 (기본) |
| 4:3 | 720pt | 540pt | 표준 모니터 |
| 16:10 | 720pt | 450pt | 맥북 디스플레이 |

## 텍스트 규칙

### 반드시 지켜야 할 규칙

```html
<!-- ✅ 올바른 텍스트 배치 -->
<h1>슬라이드 제목</h1>
<h2>부제목</h2>
<p>본문 텍스트는 p 태그 안에</p>

<ul>
  <li>불릿 포인트 1</li>
  <li>불릿 포인트 2</li>
</ul>

<ol>
  <li>번호 목록 1</li>
  <li>번호 목록 2</li>
</ol>
```

### 피해야 할 패턴

```html
<!-- ❌ 변환 시 무시됨 -->
<div>div 안의 텍스트</div>
<span>span만 사용한 텍스트</span>

<!-- ❌ 수동 불릿 금지 -->
<p>• 이렇게 하지 마세요</p>
<p>- 이것도 안 됨</p>
```

### 텍스트 스타일링

```html
<!-- 인라인 스타일링 -->
<p style="
  font-size: 24pt;
  font-weight: bold;
  color: #E94560;
  text-align: center;
  line-height: 1.5;
">
  스타일이 적용된 텍스트
</p>

<!-- 태그 기반 포맷팅 -->
<p>
  <b>굵은 텍스트</b>,
  <i>기울임 텍스트</i>,
  <u>밑줄 텍스트</u>
</p>

<!-- span으로 부분 스타일링 -->
<p>
  일반 텍스트 <span style="color: #FF6B35; font-weight: bold;">강조</span> 텍스트
</p>
```

## 폰트 사용

### 웹 안전 폰트 (권장)

```css
/* 반드시 PowerPoint에서 렌더링되는 폰트 */
font-family: Arial, sans-serif;
font-family: Helvetica, sans-serif;
font-family: 'Times New Roman', serif;
font-family: Georgia, serif;
font-family: 'Courier New', monospace;
font-family: Verdana, sans-serif;
font-family: 'Trebuchet MS', sans-serif;
font-family: Impact, sans-serif;
```

### 한글 폰트

```css
/* 시스템에 설치된 경우 사용 가능 */
font-family: 'Malgun Gothic', sans-serif;  /* 맑은 고딕 (Windows) */
font-family: 'Apple SD Gothic Neo', sans-serif;  /* 애플 SD 고딕 (macOS) */
font-family: 'Noto Sans KR', sans-serif;  /* 구글 Noto (웹폰트) */
```

## 레이아웃

### 두 열 레이아웃 (권장)

```html
<div class="slide">
  <h1>슬라이드 제목</h1>

  <div style="display: flex; gap: 20pt; margin-top: 30pt;">
    <!-- 왼쪽 열 (40%) -->
    <div style="flex: 0 0 40%;">
      <p>텍스트 콘텐츠</p>
      <ul>
        <li>포인트 1</li>
        <li>포인트 2</li>
      </ul>
    </div>

    <!-- 오른쪽 열 (60%) -->
    <div style="flex: 0 0 60%;">
      <img src="image.png" style="width: 100%;">
    </div>
  </div>
</div>
```

### 그리드 레이아웃

```html
<div style="
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20pt;
">
  <div class="card">항목 1</div>
  <div class="card">항목 2</div>
  <div class="card">항목 3</div>
</div>
```

## 도형 및 박스

### 기본 도형

```html
<!-- 사각형 -->
<div style="
  width: 200pt;
  height: 100pt;
  background-color: #1A1A2E;
  border: 2pt solid #E94560;
">
  <p style="color: white;">박스 안 텍스트</p>
</div>

<!-- 둥근 모서리 -->
<div style="
  border-radius: 10pt;
  background-color: #F5F5F5;
  padding: 20pt;
">
  <p>둥근 카드</p>
</div>

<!-- 원형 -->
<div style="
  width: 100pt;
  height: 100pt;
  border-radius: 50%;
  background-color: #FF6B35;
">
  <p style="text-align: center; line-height: 100pt; color: white;">1</p>
</div>
```

### 그림자 효과

```html
<div style="
  box-shadow: 5pt 5pt 15pt rgba(0, 0, 0, 0.2);
  padding: 20pt;
  background: white;
">
  <p>그림자가 있는 카드</p>
</div>
```

### 테두리 스타일

```html
<!-- 전체 테두리 -->
<div style="border: 2pt solid #004E89;">

<!-- 부분 테두리 -->
<div style="border-left: 4pt solid #E94560;">

<!-- 점선 테두리 -->
<div style="border: 2pt dashed #FCBF49;">
```

## 금지 사항

### CSS 그라데이션 (변환 불가)

```css
/* ❌ 사용 금지 */
background: linear-gradient(to right, #FF6B35, #FCBF49);
background: radial-gradient(circle, #00D4FF, #7B2CBF);
```

**대안**: Sharp 라이브러리로 그라데이션 PNG 생성 후 배경 이미지로 사용

```html
<!-- ✅ 대안 -->
<div style="background-image: url('gradient.png'); background-size: cover;">
```

### 복잡한 CSS 기능

```css
/* ❌ 변환 시 문제 발생 가능 */
filter: blur(5px);
backdrop-filter: blur(10px);
mix-blend-mode: multiply;
transform: rotate(15deg);
```

## 이미지 처리

### 이미지 삽입

```html
<!-- 기본 이미지 -->
<img src="./images/chart.png" style="width: 400pt; height: auto;">

<!-- 배경 이미지 -->
<div style="
  background-image: url('./images/bg.png');
  background-size: cover;
  background-position: center;
  width: 100%;
  height: 100%;
">
```

### 이미지 권장 사양

| 용도 | 포맷 | 최소 해상도 |
|------|------|-----------|
| 사진 | JPG | 1200x800 |
| 아이콘/그래픽 | PNG | 128x128 |
| 로고 | PNG/SVG | 300x300 |
| 배경 | PNG/JPG | 1920x1080 |

## 색상 팔레트

### 내장 팔레트

```javascript
const PALETTES = {
  // 비즈니스
  corporate: ['1a1a2e', '16213e', '0f3460', 'e94560'],
  professional: ['2d3436', '636e72', 'b2bec3', 'dfe6e9'],

  // 대담한
  bold: ['ff6b35', '004e89', 'fcbf49', '1a1a2e'],
  vibrant: ['e63946', 'f1faee', 'a8dadc', '457b9d'],

  // 자연
  nature: ['2d5a27', '5a8a4c', '8fbc8f', 'c5e1a5'],
  ocean: ['0077b6', '00b4d8', '90e0ef', 'caf0f8'],

  // 테크
  tech: ['0a0a0f', '1a1a2e', '00d4ff', '7b2cbf'],
  dark: ['121212', '1e1e1e', '2d2d2d', 'ffffff'],

  // 따뜻한
  sunset: ['ff6b35', 'ff8c42', 'ffd166', 'fcf8e8'],
  autumn: ['d4a373', 'ccd5ae', 'e9edc9', 'fefae0'],

  // 럭셔리
  luxury: ['2d2d2d', 'a68a64', 'ffffff', 'f8f6f0'],
  gold: ['1a1a1a', 'd4af37', 'f5f5f5', 'ffffff'],

  // 모던
  modern: ['1a1a2e', '16213e', 'e94560', 'f5f5f5'],
  minimal: ['ffffff', 'f5f5f5', '333333', '000000']
};
```

## 변환 프로세스

### 1. Playwright로 캡처

```javascript
const { chromium } = require('playwright');

async function captureSlides(htmlPath) {
  const browser = await chromium.launch();
  const page = await browser.newPage();

  await page.goto(`file://${htmlPath}`);

  // 각 슬라이드 캡처
  const slides = await page.$$('.slide');
  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({
      path: `slide-${i + 1}.png`,
      type: 'png'
    });
  }

  await browser.close();
}
```

### 2. PptxGenJS로 변환

```javascript
const PptxGenJS = require('pptxgenjs');

async function createPptx(images) {
  const pptx = new PptxGenJS();
  pptx.defineLayout({ name: 'WIDE', width: 10, height: 5.625 });
  pptx.layout = 'WIDE';

  for (const imagePath of images) {
    const slide = pptx.addSlide();
    slide.addImage({
      path: imagePath,
      x: 0, y: 0,
      w: '100%', h: '100%'
    });
  }

  await pptx.writeFile({ fileName: 'presentation.pptx' });
}
```

## 체크리스트

### 작성 전
- [ ] 슬라이드 크기 결정 (16:9/4:3/16:10)
- [ ] 색상 팔레트 선택
- [ ] 폰트 선택 (웹 안전 폰트)
- [ ] 이미지 자산 준비

### 작성 중
- [ ] 텍스트가 올바른 태그 안에 있는지 확인
- [ ] CSS 그라데이션 사용하지 않음
- [ ] 이미지 경로 유효
- [ ] 폰트가 사용 가능한지 확인

### 변환 후
- [ ] PowerPoint에서 정상 열림
- [ ] 모든 텍스트 표시됨
- [ ] 이미지 품질 양호
- [ ] 레이아웃 깨지지 않음
