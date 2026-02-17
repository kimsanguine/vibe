# Canvas-Design Skill (캔버스 디자인 스킬)

슬라이드에 필요한 커스텀 이미지, 그래픽, 타이포그래피를 제작하는 스킬입니다.

## 개요

Canvas API를 활용하여 프리젠테이션에 필요한 고품질 시각 자료를 생성합니다.
프로그래매틱하게 생성되어 일관된 스타일과 완벽한 품질을 보장합니다.

## 핵심 철학

> "90% 시각 디자인, 10% 필수 텍스트"

설명적인 문단이 아닌, 공간 관계, 색상 시스템, 구성을 통해 정보를 전달합니다.

## 생성 가능한 자산 유형

### 1. 인포그래픽

```javascript
// 프로세스 다이어그램
canvas.createProcessDiagram({
  steps: ['리서치', '분석', '디자인', '개발', '출시'],
  style: 'horizontal',
  colors: ['#FF6B35', '#004E89', '#FCBF49']
});

// 통계 인포그래픽
canvas.createStatCard({
  value: '87%',
  label: '성장률',
  trend: 'up',
  color: '#00D4FF'
});
```

### 2. 차트 및 데이터 시각화

```javascript
// 커스텀 파이 차트
canvas.createPieChart({
  data: [30, 25, 20, 15, 10],
  labels: ['A', 'B', 'C', 'D', 'E'],
  style: 'donut',
  palette: 'sunset'
});

// 막대 그래프
canvas.createBarChart({
  data: [120, 98, 156, 87],
  labels: ['Q1', 'Q2', 'Q3', 'Q4'],
  animated: false  // 정적 이미지
});
```

### 3. 아이콘 및 심볼

```javascript
// 커스텀 아이콘 생성
canvas.createIcon({
  type: 'growth',
  size: 128,
  color: '#E94560',
  style: 'filled'
});

// 아이콘 세트
canvas.createIconSet({
  icons: ['user', 'chart', 'settings', 'mail'],
  size: 64,
  palette: 'modern',
  arrangement: 'grid'
});
```

### 4. 타이포그래피 아트

```javascript
// 강조 텍스트 이미지
canvas.createTextArt({
  text: '혁신',
  font: 'Bebas Neue',
  size: 200,
  effects: ['shadow', 'outline'],
  colors: {
    fill: '#1A1A2E',
    shadow: 'rgba(0,0,0,0.3)',
    outline: '#E94560'
  }
});

// 워드 클라우드
canvas.createWordCloud({
  words: [
    { text: 'AI', weight: 100 },
    { text: '혁신', weight: 80 },
    { text: '디지털', weight: 60 }
  ],
  palette: 'tech'
});
```

### 5. 배경 및 텍스처

```javascript
// 그라데이션 배경
canvas.createGradient({
  type: 'radial',
  colors: ['#0A0A0F', '#1A1A2E', '#00D4FF'],
  size: { width: 1920, height: 1080 }
});

// 기하학적 패턴
canvas.createPattern({
  type: 'geometric',
  shapes: ['triangle', 'circle'],
  density: 'sparse',
  colors: ['#FF6B35', '#FCBF49'],
  opacity: 0.1
});

// 노이즈 텍스처
canvas.createTexture({
  type: 'noise',
  intensity: 0.05,
  blend: 'overlay'
});
```

### 6. 다이어그램

```javascript
// 조직도
canvas.createOrgChart({
  data: {
    name: 'CEO',
    children: [
      { name: 'CTO', children: [...] },
      { name: 'CFO', children: [...] }
    ]
  },
  style: 'corporate'
});

// 플로우차트
canvas.createFlowchart({
  nodes: [
    { id: 'start', type: 'terminal', text: '시작' },
    { id: 'process1', type: 'process', text: '데이터 수집' },
    { id: 'decision', type: 'decision', text: '유효?' },
    { id: 'end', type: 'terminal', text: '완료' }
  ],
  connections: [
    { from: 'start', to: 'process1' },
    { from: 'process1', to: 'decision' },
    { from: 'decision', to: 'end', label: 'Yes' }
  ]
});

// 타임라인
canvas.createTimeline({
  events: [
    { year: '2020', title: '설립' },
    { year: '2022', title: '시리즈 A' },
    { year: '2024', title: '글로벌 확장' }
  ],
  style: 'horizontal'
});
```

## 폰트 관리

### 지원 폰트

```javascript
const AVAILABLE_FONTS = {
  // 디스플레이
  display: [
    'Bebas Neue',
    'Playfair Display',
    'Oswald',
    'Montserrat'
  ],
  // 본문
  body: [
    'Source Sans Pro',
    'Lato',
    'Open Sans',
    'Roboto'
  ],
  // 모노스페이스
  mono: [
    'Fira Code',
    'JetBrains Mono',
    'Source Code Pro'
  ],
  // 한글
  korean: [
    'Noto Sans KR',
    'Pretendard',
    'Spoqa Han Sans'
  ]
};
```

### 폰트 로딩

```javascript
// 로컬 폰트 로드
await canvas.loadFont('./canvas-fonts/NotoSansKR-Bold.otf');

// 웹 폰트 로드
await canvas.loadWebFont('Pretendard',
  'https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css'
);
```

## 출력 형식

### PNG 출력
```javascript
// 표준 해상도
canvas.export('output.png', {
  format: 'png',
  quality: 1.0,
  scale: 1
});

// 고해상도 (Retina)
canvas.export('output@2x.png', {
  format: 'png',
  scale: 2
});
```

### PDF 출력
```javascript
canvas.export('output.pdf', {
  format: 'pdf',
  size: 'A4',
  orientation: 'landscape'
});
```

### SVG 출력
```javascript
canvas.export('output.svg', {
  format: 'svg',
  optimized: true
});
```

## 디자인 원칙

### 1. 시각적 계층
```
레벨 1: 가장 큰 요소 (핵심 데이터, 제목)
레벨 2: 중간 요소 (부제목, 주요 정보)
레벨 3: 작은 요소 (세부 정보, 캡션)
레벨 4: 배경 요소 (텍스처, 패턴)
```

### 2. 색상 접근성
```javascript
// 대비 확인
canvas.checkContrast('#FFFFFF', '#1A1A2E');  // 최소 4.5:1 권장

// 색맹 시뮬레이션
canvas.simulateColorBlindness('protanopia');
```

### 3. 일관된 스타일
```javascript
// 글로벌 스타일 설정
canvas.setGlobalStyle({
  cornerRadius: 8,
  shadowOffset: { x: 4, y: 4 },
  shadowBlur: 12,
  shadowColor: 'rgba(0,0,0,0.15)',
  strokeWidth: 2
});
```

## 배치 생성

여러 자산을 한 번에 생성:

```javascript
// 배치 작업 정의
const batch = [
  { type: 'icon', config: {...}, output: 'icon1.png' },
  { type: 'chart', config: {...}, output: 'chart1.png' },
  { type: 'background', config: {...}, output: 'bg1.png' }
];

// 일괄 실행
await canvas.batchCreate(batch, {
  outputDir: './assets/',
  parallel: true
});
```

## 슬라이드 자산 패키지

완성된 프리젠테이션을 위한 자산 세트:

```
assets/
├── backgrounds/
│   ├── title-bg.png
│   ├── content-bg.png
│   └── section-bg.png
├── charts/
│   ├── market-share.png
│   ├── growth-trend.png
│   └── comparison.png
├── icons/
│   ├── icon-set.png
│   └── decorative.png
├── typography/
│   ├── title-art.png
│   └── quote-design.png
└── manifest.json
```

### manifest.json 구조
```json
{
  "assets": [
    {
      "id": "title-bg",
      "path": "backgrounds/title-bg.png",
      "type": "background",
      "dimensions": { "width": 1920, "height": 1080 },
      "forSlides": [1]
    }
  ],
  "palette": {
    "primary": "#1A1A2E",
    "secondary": "#E94560",
    "accent": "#00D4FF"
  },
  "fonts": ["Pretendard", "Bebas Neue"]
}
```

## 품질 기준

### 해상도 가이드
| 용도 | 최소 해상도 | 권장 해상도 |
|-----|-----------|-----------|
| 아이콘 | 64x64 | 128x128 |
| 차트 | 800x600 | 1200x900 |
| 배경 | 1920x1080 | 3840x2160 |

### 파일 크기 최적화
```javascript
canvas.optimize({
  maxFileSize: '500KB',
  colorDepth: 24,
  compression: 'lossy',
  quality: 0.85
});
```

## 출력물

이 스킬로 생성되는 파일:

1. **design-philosophy.md**: 디자인 철학 문서 (4-6 문단)
2. **assets/**: 생성된 모든 시각 자산
3. **manifest.json**: 자산 매니페스트
4. **preview.pdf**: 전체 자산 미리보기
