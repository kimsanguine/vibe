const PptxGenJS = require('pptxgenjs');

// Create presentation
const pptx = new PptxGenJS();

// Presentation settings
pptx.defineLayout({ name: 'CUSTOM', width: 13.333, height: 7.5 });
pptx.layout = 'CUSTOM';
pptx.title = 'OpenClaw Analysis & Insights';
pptx.author = 'AI Product Leader';
pptx.subject = 'OpenClaw - The Rise of Open-Source AI Agents';

// ============================================
// Design System: Dark Sophistication (Gemini Style)
// ============================================
const colors = {
  // Primary gradient colors
  gradientStart: '1a1a2e',   // Deep navy
  gradientEnd: '16213e',     // Dark blue

  // Accent colors
  accent1: '4ECDC4',         // Teal
  accent2: 'FF6B6B',         // Coral (for warnings)
  accent3: 'FFE66D',         // Yellow (for highlights)
  accent4: '95E1D3',         // Mint

  // Text colors
  textPrimary: 'FFFFFF',
  textSecondary: 'B8C5D6',
  textMuted: '6B7B8C',

  // Background
  bgDark: '0f0f1a',
  bgCard: '1e1e32',

  // Semantic
  success: '4ECDC4',
  warning: 'FFE66D',
  danger: 'FF6B6B'
};

// Font settings
const fonts = {
  title: 'Helvetica Neue',
  body: 'Helvetica Neue',
  mono: 'SF Mono'
};

// Helper function for gradient background
function addGradientBg(slide) {
  slide.background = {
    color: colors.bgDark
  };
  // Add subtle gradient overlay
  slide.addShape('rect', {
    x: 0, y: 0, w: '100%', h: '100%',
    fill: {
      type: 'solid',
      color: colors.bgDark
    }
  });
}

// Helper for accent circle decoration
function addAccentCircle(slide, x, y, size, color, opacity = 0.1) {
  slide.addShape('ellipse', {
    x: x, y: y, w: size, h: size,
    fill: { color: color, transparency: (1 - opacity) * 100 }
  });
}

// ============================================
// Slide 1: Title Slide
// ============================================
let slide1 = pptx.addSlide();
addGradientBg(slide1);

// Decorative circles
addAccentCircle(slide1, 9, -1, 4, colors.accent1, 0.15);
addAccentCircle(slide1, -1, 5, 3, colors.accent4, 0.1);

// Main title
slide1.addText('OpenClaw', {
  x: 0.8, y: 2.2, w: 11.7, h: 1.2,
  fontSize: 64,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

// Subtitle
slide1.addText('오픈소스 AI 에이전트의 부상과 전략적 시사점', {
  x: 0.8, y: 3.4, w: 11.7, h: 0.6,
  fontSize: 24,
  fontFace: fonts.body,
  color: colors.textSecondary
});

// Accent line
slide1.addShape('rect', {
  x: 0.8, y: 4.2, w: 2, h: 0.06,
  fill: { color: colors.accent1 }
});

// Meta info
slide1.addText('AI Product Leader Perspective | 10분 프리젠테이션', {
  x: 0.8, y: 6.5, w: 6, h: 0.4,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textMuted
});

slide1.addText('2026.02', {
  x: 10.5, y: 6.5, w: 2, h: 0.4,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textMuted,
  align: 'right'
});

// ============================================
// Slide 2: Executive Summary
// ============================================
let slide2 = pptx.addSlide();
addGradientBg(slide2);
addAccentCircle(slide2, 10, 4, 5, colors.accent1, 0.08);

slide2.addText('Executive Summary', {
  x: 0.8, y: 0.5, w: 10, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

const summaryPoints = [
  { icon: '🦞', title: 'OpenClaw', desc: '2개월 만에 GitHub 145K 스타, 역사상 가장 빠른 성장' },
  { icon: '🔓', title: 'Full Access', desc: '파일, 메시지, 브라우저, 시스템 전체 접근하는 자율 AI 에이전트' },
  { icon: '⚠️', title: 'Security Risk', desc: '26% 스킬에 취약점, 엔터프라이즈 도입은 시기상조' },
  { icon: '🚀', title: 'Paradigm Shift', desc: 'AI 에이전트 시대의 시작, 5년 내 웹 브라우저만큼 보편화 전망' }
];

summaryPoints.forEach((point, idx) => {
  const yPos = 1.6 + (idx * 1.35);

  // Icon background
  slide2.addShape('ellipse', {
    x: 0.8, y: yPos, w: 0.8, h: 0.8,
    fill: { color: colors.bgCard }
  });

  // Icon
  slide2.addText(point.icon, {
    x: 0.8, y: yPos + 0.1, w: 0.8, h: 0.6,
    fontSize: 24,
    align: 'center'
  });

  // Title
  slide2.addText(point.title, {
    x: 1.9, y: yPos, w: 4, h: 0.5,
    fontSize: 20,
    fontFace: fonts.title,
    color: colors.accent1,
    bold: true
  });

  // Description
  slide2.addText(point.desc, {
    x: 1.9, y: yPos + 0.45, w: 10, h: 0.5,
    fontSize: 16,
    fontFace: fonts.body,
    color: colors.textSecondary
  });
});

// ============================================
// Slide 3: What is OpenClaw?
// ============================================
let slide3 = pptx.addSlide();
addGradientBg(slide3);

slide3.addText('OpenClaw란?', {
  x: 0.8, y: 0.5, w: 10, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

// Definition card
slide3.addShape('roundRect', {
  x: 0.8, y: 1.5, w: 5.5, h: 2.5,
  fill: { color: colors.bgCard },
  rectRadius: 0.2
});

slide3.addText('오픈소스 자율형\nAI 개인 비서', {
  x: 1.1, y: 1.7, w: 5, h: 1,
  fontSize: 22,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

slide3.addText('사용자 기기에서 로컬로 실행되며\n메시징 플랫폼과 통합되는\n진정한 "나만의 AI"', {
  x: 1.1, y: 2.7, w: 5, h: 1.2,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textSecondary,
  lineSpacingMultiple: 1.3
});

// Timeline
slide3.addText('명칭 변천사', {
  x: 6.8, y: 1.5, w: 5, h: 0.5,
  fontSize: 16,
  fontFace: fonts.title,
  color: colors.textMuted
});

const timeline = [
  { date: '2025.11', name: 'Clawdbot', note: '최초 출시' },
  { date: '2025.12', name: 'Moltbot', note: 'Anthropic 상표권 요청' },
  { date: '2026.01', name: 'OpenClaw', note: '현재 명칭' }
];

timeline.forEach((item, idx) => {
  const yPos = 2.2 + (idx * 0.9);

  slide3.addText(item.date, {
    x: 6.8, y: yPos, w: 1.5, h: 0.4,
    fontSize: 12,
    fontFace: fonts.mono,
    color: colors.accent1
  });

  slide3.addText(item.name, {
    x: 8.5, y: yPos, w: 2, h: 0.4,
    fontSize: 16,
    fontFace: fonts.title,
    color: colors.textPrimary,
    bold: true
  });

  slide3.addText(item.note, {
    x: 10.5, y: yPos, w: 2, h: 0.4,
    fontSize: 12,
    fontFace: fonts.body,
    color: colors.textMuted
  });
});

// Creator info
slide3.addShape('roundRect', {
  x: 0.8, y: 4.5, w: 11.7, h: 1.2,
  fill: { color: colors.bgCard },
  rectRadius: 0.15
});

slide3.addText('개발자: Peter Steinberger (오스트리아)', {
  x: 1.1, y: 4.7, w: 5, h: 0.4,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textSecondary
});

slide3.addText('라이선스: MIT (완전 오픈소스)', {
  x: 6.8, y: 4.7, w: 5, h: 0.4,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textSecondary
});

slide3.addText('아키텍처: Gateway 중앙 제어 + WebSocket 기반', {
  x: 1.1, y: 5.2, w: 10, h: 0.4,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textSecondary
});

// ============================================
// Slide 4: Core Features
// ============================================
let slide4 = pptx.addSlide();
addGradientBg(slide4);
addAccentCircle(slide4, -2, -2, 6, colors.accent4, 0.06);

slide4.addText('핵심 기능', {
  x: 0.8, y: 0.5, w: 10, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

const features = [
  {
    title: '멀티채널 통합',
    items: ['WhatsApp, Telegram, Slack', 'Discord, Signal, iMessage', 'Teams, Matrix, WebChat'],
    color: colors.accent1
  },
  {
    title: '시스템 제어',
    items: ['브라우저 자동화', '파일 읽기/쓰기', '셸 명령어 실행', 'Cron 예약 작업'],
    color: colors.accent3
  },
  {
    title: '지속적 메모리',
    items: ['로컬 장기 기억 저장', '선호도, 프로젝트 기억', '시간이 지날수록 개인화'],
    color: colors.accent4
  },
  {
    title: '스킬 시스템',
    items: ['100+ 사전 구성 스킬', '커뮤니티 스킬 수백 개', 'AI가 자율적 스킬 생성'],
    color: colors.accent2
  }
];

features.forEach((feature, idx) => {
  const col = idx % 2;
  const row = Math.floor(idx / 2);
  const xPos = 0.8 + (col * 6.3);
  const yPos = 1.5 + (row * 2.7);

  // Feature card
  slide4.addShape('roundRect', {
    x: xPos, y: yPos, w: 5.8, h: 2.4,
    fill: { color: colors.bgCard },
    rectRadius: 0.15
  });

  // Color accent bar
  slide4.addShape('rect', {
    x: xPos, y: yPos, w: 0.08, h: 2.4,
    fill: { color: feature.color }
  });

  // Title
  slide4.addText(feature.title, {
    x: xPos + 0.3, y: yPos + 0.2, w: 5, h: 0.5,
    fontSize: 18,
    fontFace: fonts.title,
    color: feature.color,
    bold: true
  });

  // Items
  feature.items.forEach((item, itemIdx) => {
    slide4.addText('• ' + item, {
      x: xPos + 0.3, y: yPos + 0.8 + (itemIdx * 0.4), w: 5, h: 0.4,
      fontSize: 13,
      fontFace: fonts.body,
      color: colors.textSecondary
    });
  });
});

// ============================================
// Slide 5: Explosive Growth
// ============================================
let slide5 = pptx.addSlide();
addGradientBg(slide5);

slide5.addText('폭발적 성장', {
  x: 0.8, y: 0.5, w: 10, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

// Big numbers
const metrics = [
  { value: '145K+', label: 'GitHub Stars', subtext: '2개월 만에 달성' },
  { value: '20K+', label: 'Forks', subtext: '활발한 커뮤니티' },
  { value: '#1', label: 'Growth Rate', subtext: 'GitHub 역사상' }
];

metrics.forEach((metric, idx) => {
  const xPos = 0.8 + (idx * 4.2);

  slide5.addShape('roundRect', {
    x: xPos, y: 1.5, w: 3.8, h: 2.5,
    fill: { color: colors.bgCard },
    rectRadius: 0.2
  });

  slide5.addText(metric.value, {
    x: xPos, y: 1.7, w: 3.8, h: 1,
    fontSize: 48,
    fontFace: fonts.title,
    color: colors.accent1,
    bold: true,
    align: 'center'
  });

  slide5.addText(metric.label, {
    x: xPos, y: 2.7, w: 3.8, h: 0.5,
    fontSize: 16,
    fontFace: fonts.body,
    color: colors.textPrimary,
    align: 'center'
  });

  slide5.addText(metric.subtext, {
    x: xPos, y: 3.2, w: 3.8, h: 0.4,
    fontSize: 12,
    fontFace: fonts.body,
    color: colors.textMuted,
    align: 'center'
  });
});

// Global adoption
slide5.addText('글로벌 확산', {
  x: 0.8, y: 4.3, w: 10, h: 0.5,
  fontSize: 18,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

const adoptionPoints = [
  '실리콘밸리 → 베이징: 알리바바, 텐센트, 바이트댄스 등 주요 AI 기업 채택',
  '다수 VC가 OpenClaw 기반 스타트업에 투자 진행 중',
  '"5년 내 웹 브라우저만큼 보편화될 것" - 투자자 전망'
];

adoptionPoints.forEach((point, idx) => {
  slide5.addText('→ ' + point, {
    x: 0.8, y: 4.9 + (idx * 0.5), w: 12, h: 0.5,
    fontSize: 14,
    fontFace: fonts.body,
    color: colors.textSecondary
  });
});

// ============================================
// Slide 6: Moltbook - AI Social Network
// ============================================
let slide6 = pptx.addSlide();
addGradientBg(slide6);
addAccentCircle(slide6, 9, 3, 5, colors.accent3, 0.08);

slide6.addText('Moltbook: AI 에이전트 소셜 네트워크', {
  x: 0.8, y: 0.5, w: 12, h: 0.8,
  fontSize: 32,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

// Concept card
slide6.addShape('roundRect', {
  x: 0.8, y: 1.5, w: 6, h: 3,
  fill: { color: colors.bgCard },
  rectRadius: 0.2
});

slide6.addText('🤖 → 🤖', {
  x: 0.8, y: 1.7, w: 6, h: 0.8,
  fontSize: 36,
  align: 'center'
});

slide6.addText('AI가 AI와 대화하는 소셜 네트워크', {
  x: 1.1, y: 2.6, w: 5.5, h: 0.5,
  fontSize: 18,
  fontFace: fonts.title,
  color: colors.accent3,
  bold: true,
  align: 'center'
});

slide6.addText('• 2026년 1월 출시\n• 자율 에이전트 간 상호작용\n• 인간은 관찰만 가능, 직접 참여 불가\n• 에이전트의 사회적 행동 연구 가능', {
  x: 1.1, y: 3.2, w: 5.5, h: 1.2,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textSecondary,
  lineSpacingMultiple: 1.4
});

// IBM Quote
slide6.addShape('roundRect', {
  x: 7.2, y: 1.5, w: 5.3, h: 3,
  fill: { color: colors.bgCard },
  rectRadius: 0.2
});

slide6.addText('IBM 연구진 시사점', {
  x: 7.5, y: 1.7, w: 4.7, h: 0.5,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.accent1
});

slide6.addText('"Moltbook 내 에이전트 행동 관찰은 엔터프라이즈 에이전트 테스트를 위한 통제된 샌드박스, 리스크 시나리오 분석, 대규모 워크플로우 최적화에 영감을 줄 수 있다"', {
  x: 7.5, y: 2.3, w: 4.7, h: 2,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textSecondary,
  italic: true,
  lineSpacingMultiple: 1.4
});

// Implications
slide6.addText('프로덕트 리더를 위한 시사점', {
  x: 0.8, y: 4.8, w: 12, h: 0.5,
  fontSize: 16,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

slide6.addText('에이전트 행동 패턴 분석 → 안전한 엔터프라이즈 에이전트 설계에 활용 가능', {
  x: 0.8, y: 5.4, w: 12, h: 0.4,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textSecondary
});

// ============================================
// Slide 7: Security Concerns
// ============================================
let slide7 = pptx.addSlide();
addGradientBg(slide7);

slide7.addText('보안 위험: 치명적 삼중고', {
  x: 0.8, y: 0.5, w: 10, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.accent2,
  bold: true
});

// Warning banner
slide7.addShape('roundRect', {
  x: 0.8, y: 1.4, w: 11.7, h: 0.8,
  fill: { color: '3d1f1f' },
  rectRadius: 0.1
});

slide7.addText('⚠️  Palo Alto Networks: "Lethal Trifecta of Risks"', {
  x: 1.1, y: 1.5, w: 11, h: 0.6,
  fontSize: 16,
  fontFace: fonts.body,
  color: colors.accent2,
  bold: true
});

// Three risks
const risks = [
  { num: '1', title: '민감 데이터 접근', desc: '파일, 이메일, 메시지 전체', icon: '📁' },
  { num: '2', title: '신뢰할 수 없는 콘텐츠 노출', desc: '외부 입력에 취약', icon: '🌐' },
  { num: '3', title: '광범위한 능력', desc: '시스템 전체 제어', icon: '⚡' }
];

risks.forEach((risk, idx) => {
  const xPos = 0.8 + (idx * 4.2);

  slide7.addShape('roundRect', {
    x: xPos, y: 2.5, w: 3.8, h: 1.8,
    fill: { color: colors.bgCard },
    rectRadius: 0.15
  });

  slide7.addText(risk.icon, {
    x: xPos, y: 2.6, w: 3.8, h: 0.6,
    fontSize: 28,
    align: 'center'
  });

  slide7.addText(risk.title, {
    x: xPos + 0.2, y: 3.3, w: 3.4, h: 0.5,
    fontSize: 14,
    fontFace: fonts.title,
    color: colors.accent2,
    bold: true,
    align: 'center'
  });

  slide7.addText(risk.desc, {
    x: xPos + 0.2, y: 3.8, w: 3.4, h: 0.4,
    fontSize: 12,
    fontFace: fonts.body,
    color: colors.textMuted,
    align: 'center'
  });
});

// Statistics
slide7.addShape('roundRect', {
  x: 0.8, y: 4.6, w: 5.5, h: 1.5,
  fill: { color: colors.bgCard },
  rectRadius: 0.15
});

slide7.addText('26%', {
  x: 0.8, y: 4.7, w: 2, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.accent2,
  bold: true,
  align: 'center'
});

slide7.addText('Cisco 분석: 31,000개 스킬 중\n취약점 포함 비율', {
  x: 2.8, y: 4.9, w: 3.3, h: 0.8,
  fontSize: 13,
  fontFace: fonts.body,
  color: colors.textSecondary
});

slide7.addText('2026.01 가짜 Moltbot 악성코드로\n시스템 해킹 사례 발생', {
  x: 1.0, y: 5.6, w: 5, h: 0.5,
  fontSize: 12,
  fontFace: fonts.body,
  color: colors.textMuted
});

// Expert quote
slide7.addShape('roundRect', {
  x: 6.8, y: 4.6, w: 5.7, h: 1.5,
  fill: { color: colors.bgCard },
  rectRadius: 0.15
});

slide7.addText('"직원이 OpenClaw를 설치하면 자신과 동일한 권한의 그림자 사용자를 생성하는 것이지만, 소셜 엔지니어링을 감지할 판단력은 없다"', {
  x: 7.0, y: 4.8, w: 5.3, h: 1.2,
  fontSize: 12,
  fontFace: fonts.body,
  color: colors.textSecondary,
  italic: true,
  lineSpacingMultiple: 1.3
});

// ============================================
// Slide 8: Competitive Landscape
// ============================================
let slide8 = pptx.addSlide();
addGradientBg(slide8);

slide8.addText('경쟁 환경: OpenClaw vs Claude Code', {
  x: 0.8, y: 0.5, w: 12, h: 0.8,
  fontSize: 32,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

// Comparison table header
slide8.addShape('roundRect', {
  x: 0.8, y: 1.4, w: 11.7, h: 0.7,
  fill: { color: colors.bgCard },
  rectRadius: 0.1
});

const tableHeaders = ['구분', 'OpenClaw', 'Claude Code'];
const colWidths = [2.5, 4.6, 4.6];
let xOffset = 0.8;

tableHeaders.forEach((header, idx) => {
  slide8.addText(header, {
    x: xOffset, y: 1.5, w: colWidths[idx], h: 0.5,
    fontSize: 14,
    fontFace: fonts.title,
    color: colors.accent1,
    bold: true,
    align: 'center'
  });
  xOffset += colWidths[idx];
});

// Table rows
const comparisonData = [
  ['영역', '메시징 앱, 일상 자동화', '터미널, 코딩 작업'],
  ['인터페이스', 'WhatsApp, Slack 등', 'CLI / IDE'],
  ['주요 용도', '이메일, 캘린더, 리서치', '코드, 테스트, Git'],
  ['가격', 'API 비용 (변동, 고가)', '$20-200/월'],
  ['보안', '높은 위험 ⚠️', '상대적 안전 ✓']
];

comparisonData.forEach((row, rowIdx) => {
  const yPos = 2.2 + (rowIdx * 0.7);
  xOffset = 0.8;

  row.forEach((cell, colIdx) => {
    const isWarning = cell.includes('⚠️');
    const isSafe = cell.includes('✓');

    slide8.addText(cell, {
      x: xOffset, y: yPos, w: colWidths[colIdx], h: 0.6,
      fontSize: 13,
      fontFace: fonts.body,
      color: isWarning ? colors.accent2 : (isSafe ? colors.accent1 : (colIdx === 0 ? colors.textMuted : colors.textSecondary)),
      align: 'center',
      bold: colIdx === 0
    });
    xOffset += colWidths[colIdx];
  });
});

// Key insight
slide8.addShape('roundRect', {
  x: 0.8, y: 5.6, w: 11.7, h: 1.2,
  fill: { color: colors.bgCard },
  rectRadius: 0.15
});

slide8.addText('💡 핵심 인사이트', {
  x: 1.1, y: 5.75, w: 3, h: 0.4,
  fontSize: 14,
  fontFace: fonts.title,
  color: colors.accent3,
  bold: true
});

slide8.addText('"두 도구는 근본적으로 다른 목적. 하나는 코딩을 위한 터미널에, 다른 하나는 그 외 모든 것을 위한 메시징 앱에 존재한다"', {
  x: 1.1, y: 6.15, w: 11, h: 0.5,
  fontSize: 13,
  fontFace: fonts.body,
  color: colors.textSecondary,
  italic: true
});

// ============================================
// Slide 9: Enterprise Implications
// ============================================
let slide9 = pptx.addSlide();
addGradientBg(slide9);
addAccentCircle(slide9, 10, -1, 4, colors.accent1, 0.1);

slide9.addText('엔터프라이즈 시사점', {
  x: 0.8, y: 0.5, w: 10, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

// Two columns: Now vs Enterprise
slide9.addText('🚀 OpenClaw (현재)', {
  x: 0.8, y: 1.4, w: 5.5, h: 0.5,
  fontSize: 18,
  fontFace: fonts.title,
  color: colors.accent2,
  bold: true
});

slide9.addText('🏢 Enterprise (지향점)', {
  x: 7, y: 1.4, w: 5.5, h: 0.5,
  fontSize: 18,
  fontFace: fonts.title,
  color: colors.accent1,
  bold: true
});

const approaches = [
  { now: '빠름', enterprise: '느림 (통제된)' },
  { now: '낮은 통제', enterprise: '높은 통제' },
  { now: '감사 없음', enterprise: '감사 필수' },
  { now: '자유로운 승인', enterprise: '정책 기반' }
];

approaches.forEach((item, idx) => {
  const yPos = 2.0 + (idx * 0.7);

  slide9.addShape('roundRect', {
    x: 0.8, y: yPos, w: 5.5, h: 0.6,
    fill: { color: '3d2020' },
    rectRadius: 0.1
  });

  slide9.addText(item.now, {
    x: 0.8, y: yPos + 0.1, w: 5.5, h: 0.4,
    fontSize: 14,
    fontFace: fonts.body,
    color: colors.textSecondary,
    align: 'center'
  });

  slide9.addShape('roundRect', {
    x: 7, y: yPos, w: 5.5, h: 0.6,
    fill: { color: '1a3d3d' },
    rectRadius: 0.1
  });

  slide9.addText(item.enterprise, {
    x: 7, y: yPos + 0.1, w: 5.5, h: 0.4,
    fontSize: 14,
    fontFace: fonts.body,
    color: colors.textSecondary,
    align: 'center'
  });
});

// Recommendations
slide9.addText('프로덕트 리더 권장 사항', {
  x: 0.8, y: 5, w: 12, h: 0.5,
  fontSize: 18,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

const recommendations = [
  '단기: 기업 차원 OpenClaw 사용 정책 수립 (금지 또는 엄격 규제)',
  '중기: 통제된 샌드박스 환경에서 에이전트 테스트 및 학습',
  '장기: 보안-기능 균형 잡힌 엔터프라이즈 에이전트 솔루션 개발/도입'
];

recommendations.forEach((rec, idx) => {
  slide9.addText((idx + 1) + '. ' + rec, {
    x: 0.8, y: 5.5 + (idx * 0.5), w: 12, h: 0.5,
    fontSize: 13,
    fontFace: fonts.body,
    color: colors.textSecondary
  });
});

// ============================================
// Slide 10: Conclusion & Call to Action
// ============================================
let slide10 = pptx.addSlide();
addGradientBg(slide10);
addAccentCircle(slide10, -2, 2, 6, colors.accent1, 0.08);
addAccentCircle(slide10, 10, 5, 4, colors.accent4, 0.06);

slide10.addText('결론: AI 에이전트 시대의 시작', {
  x: 0.8, y: 0.5, w: 12, h: 0.8,
  fontSize: 36,
  fontFace: fonts.title,
  color: colors.textPrimary,
  bold: true
});

// Key takeaways
const takeaways = [
  { emoji: '🦞', text: 'OpenClaw는 AI 에이전트의 가능성과 위험을 동시에 보여주는 "선행 지표"' },
  { emoji: '⚡', text: '2026년은 AI 에이전트 폭발의 해 - 선제적 대응 전략 필수' },
  { emoji: '🔐', text: '보안과 자율성의 균형이 엔터프라이즈 AI 에이전트 성공의 핵심' },
  { emoji: '🎯', text: '지금은 "관찰하고 학습"하면서 내부 역량 구축할 시점' }
];

takeaways.forEach((item, idx) => {
  const yPos = 1.5 + (idx * 1.1);

  slide10.addShape('roundRect', {
    x: 0.8, y: yPos, w: 11.7, h: 0.9,
    fill: { color: colors.bgCard },
    rectRadius: 0.15
  });

  slide10.addText(item.emoji, {
    x: 1.0, y: yPos + 0.15, w: 0.8, h: 0.6,
    fontSize: 24
  });

  slide10.addText(item.text, {
    x: 2, y: yPos + 0.2, w: 10, h: 0.6,
    fontSize: 16,
    fontFace: fonts.body,
    color: colors.textSecondary
  });
});

// Call to action
slide10.addShape('roundRect', {
  x: 0.8, y: 5.6, w: 11.7, h: 1.2,
  fill: { color: '1a2d3d' },
  rectRadius: 0.15
});

slide10.addText('Next Step: 우리 조직의 AI 에이전트 전략 논의 시작', {
  x: 0.8, y: 5.85, w: 11.7, h: 0.7,
  fontSize: 20,
  fontFace: fonts.title,
  color: colors.accent1,
  bold: true,
  align: 'center'
});

// Footer
slide10.addText('Q&A', {
  x: 0.8, y: 6.9, w: 2, h: 0.4,
  fontSize: 14,
  fontFace: fonts.body,
  color: colors.textMuted
});

slide10.addText('Sources: OpenClaw.ai, GitHub, CNBC, Palo Alto Networks, Cisco, IBM', {
  x: 4, y: 6.9, w: 8.5, h: 0.4,
  fontSize: 10,
  fontFace: fonts.body,
  color: colors.textMuted,
  align: 'right'
});

// ============================================
// Save the presentation
// ============================================
pptx.writeFile({ fileName: '/home/user/vibe/ppt-agent-team/output/openclaw-analysis/OpenClaw_Analysis.pptx' })
  .then(fileName => {
    console.log(`Created: ${fileName}`);
  })
  .catch(err => {
    console.error(err);
  });
