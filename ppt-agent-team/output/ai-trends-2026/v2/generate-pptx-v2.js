import PptxGenJS from 'pptxgenjs';

// Create presentation
const pptx = new PptxGenJS();

// Set presentation properties
pptx.author = 'PPT Agent Team';
pptx.title = 'AI Trends 2026';
pptx.subject = 'The New Era of Artificial Intelligence';

// Define layout (16:9)
pptx.defineLayout({ name: 'WIDE', width: 10, height: 5.625 });
pptx.layout = 'WIDE';

// ============================================
// Design System v2 - Gemini Inspired
// ============================================

// Color palette - Modern Clarity with Gradients
const colors = {
  // Base
  surface: 'FFFFFF',
  surfaceElevated: 'F8FAFC',
  surfaceDark: '0F172A',

  // Text
  textPrimary: '0F172A',
  textSecondary: '64748B',
  textLight: 'FFFFFF',
  textMuted: 'A1A1AA',

  // Accent (Gemini-inspired)
  accentIndigo: '6366F1',
  accentViolet: '8B5CF6',
  accentPink: 'EC4899',
  accentCyan: '06B6D4',
  accentEmerald: '10B981',

  // Gradient stops (for reference, applied separately)
  gradientStart: '667eea',
  gradientEnd: '764ba2',
};

// Rounded rectangle helper
function addRoundedCard(slide, x, y, w, h, options = {}) {
  const defaults = {
    fill: { color: colors.surfaceElevated },
    shadow: {
      type: 'outer',
      blur: 8,
      offset: 2,
      angle: 90,
      opacity: 0.15,
      color: '000000'
    },
    line: { color: 'E2E8F0', width: 1 }
  };
  slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x, y, w, h,
    rectRadius: 0.15,
    ...defaults,
    ...options
  });
}

// ============================================
// Slide 1: Title - Hero Statement
// ============================================
let slide1 = pptx.addSlide();

// Gradient background simulation (using two overlapping shapes)
slide1.addShape(pptx.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: colors.surfaceDark }
});

// Decorative gradient circles (Gemini style)
slide1.addShape(pptx.shapes.OVAL, {
  x: -2, y: -1, w: 6, h: 6,
  fill: { color: colors.accentIndigo, transparency: 80 }
});
slide1.addShape(pptx.shapes.OVAL, {
  x: 6, y: 2, w: 5, h: 5,
  fill: { color: colors.accentPink, transparency: 85 }
});

slide1.addText('AI Trends', {
  x: 0.8, y: 1.6, w: 8.4, h: 1,
  fontSize: 72, bold: true, color: colors.textLight,
  fontFace: 'Arial'
});

slide1.addText('2026', {
  x: 0.8, y: 2.5, w: 8.4, h: 0.9,
  fontSize: 72, bold: true, color: colors.accentIndigo,
  fontFace: 'Arial'
});

slide1.addText('The New Era of Artificial Intelligence', {
  x: 0.8, y: 3.6, w: 8.4, h: 0.5,
  fontSize: 24, color: colors.textMuted,
  fontFace: 'Arial'
});

slide1.addText('PPT Agent Team  •  February 2026', {
  x: 0.8, y: 4.8, w: 8.4, h: 0.4,
  fontSize: 14, color: colors.textMuted,
  fontFace: 'Arial'
});

// ============================================
// Slide 2: Executive Summary - 3 Cards
// ============================================
let slide2 = pptx.addSlide();
slide2.background = { color: colors.surface };

slide2.addText('Executive Summary', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.7,
  fontSize: 36, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

// Underline accent
slide2.addShape(pptx.shapes.RECTANGLE, {
  x: 0.8, y: 1.05, w: 1.5, h: 0.06,
  fill: { color: colors.accentIndigo }
});

const summaryCards = [
  { value: '$375B', label: 'AI 시장 규모 2026', color: colors.accentIndigo },
  { value: '88%', label: '기업 AI 채택률', color: colors.accentViolet },
  { value: '50%+', label: 'VC 투자 중 AI 비중', color: colors.accentPink }
];

summaryCards.forEach((card, idx) => {
  const xPos = 0.8 + (idx * 3.0);

  addRoundedCard(slide2, xPos, 1.5, 2.7, 2.2);

  slide2.addText(card.value, {
    x: xPos, y: 1.9, w: 2.7, h: 0.8,
    fontSize: 42, bold: true, color: card.color,
    align: 'center', fontFace: 'Arial'
  });

  slide2.addText(card.label, {
    x: xPos, y: 2.8, w: 2.7, h: 0.6,
    fontSize: 14, color: colors.textSecondary,
    align: 'center', fontFace: 'Arial'
  });
});

slide2.addText('Sources: McKinsey, Fortune Business Insights, Silicon Valley Bank', {
  x: 0.8, y: 4.9, w: 8.4, h: 0.3,
  fontSize: 10, color: colors.textMuted,
  fontFace: 'Arial'
});

// ============================================
// Slide 3: Market Size - Data Focus
// ============================================
let slide3 = pptx.addSlide();
slide3.background = { color: colors.surface };

slide3.addText('AI Market Size', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.7,
  fontSize: 36, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

slide3.addShape(pptx.shapes.RECTANGLE, {
  x: 0.8, y: 1.05, w: 1.5, h: 0.06,
  fill: { color: colors.accentIndigo }
});

// Market data cards
const marketData = [
  { year: '2025', value: '$294B', growth: 'Current' },
  { year: '2026', value: '$375B', growth: '+27.6%' },
  { year: '2030', value: '$1.68T', growth: 'CAGR 36.9%' },
  { year: '2034', value: '$3.5T', growth: '10x Growth' }
];

marketData.forEach((data, idx) => {
  const xPos = 0.6 + (idx * 2.35);

  addRoundedCard(slide3, xPos, 1.4, 2.15, 2.5);

  slide3.addText(data.year, {
    x: xPos, y: 1.6, w: 2.15, h: 0.4,
    fontSize: 16, color: colors.textSecondary,
    align: 'center', fontFace: 'Arial'
  });

  slide3.addText(data.value, {
    x: xPos, y: 2.0, w: 2.15, h: 0.7,
    fontSize: 36, bold: true, color: colors.accentIndigo,
    align: 'center', fontFace: 'Arial'
  });

  slide3.addText(data.growth, {
    x: xPos, y: 2.8, w: 2.15, h: 0.4,
    fontSize: 12, color: colors.accentEmerald,
    align: 'center', fontFace: 'Arial'
  });
});

// Growth arrow
slide3.addText('→', {
  x: 4.5, y: 4.1, w: 1, h: 0.5,
  fontSize: 24, color: colors.textMuted,
  align: 'center'
});

slide3.addText('10x Growth Expected Over Next Decade', {
  x: 0.8, y: 4.0, w: 8.4, h: 0.4,
  fontSize: 16, color: colors.textSecondary,
  align: 'center', fontFace: 'Arial'
});

slide3.addText('Source: Fortune Business Insights, Statista, Grand View Research', {
  x: 0.8, y: 4.9, w: 8.4, h: 0.3,
  fontSize: 10, color: colors.textMuted,
  fontFace: 'Arial'
});

// ============================================
// Slide 4: Agentic AI - Asymmetric Split
// ============================================
let slide4 = pptx.addSlide();
slide4.background = { color: colors.surface };

slide4.addText('01', {
  x: 8.5, y: 0.3, w: 1.2, h: 1,
  fontSize: 60, color: 'F1F5F9', bold: true,
  fontFace: 'Arial'
});

slide4.addText('Agentic AI', {
  x: 0.8, y: 0.4, w: 7, h: 0.7,
  fontSize: 36, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

slide4.addText('자율적 AI 에이전트의 부상', {
  x: 0.8, y: 1.0, w: 7, h: 0.4,
  fontSize: 16, color: colors.textSecondary,
  fontFace: 'Arial'
});

// Left: Key metrics
addRoundedCard(slide4, 0.8, 1.6, 4.2, 2.8, {
  fill: { color: colors.surfaceDark }
});

slide4.addText('40%', {
  x: 0.8, y: 1.9, w: 4.2, h: 0.8,
  fontSize: 56, bold: true, color: colors.accentIndigo,
  align: 'center', fontFace: 'Arial'
});

slide4.addText('기업 앱에 AI 에이전트 포함 예측', {
  x: 0.8, y: 2.7, w: 4.2, h: 0.4,
  fontSize: 14, color: colors.textLight,
  align: 'center', fontFace: 'Arial'
});

slide4.addText('Gartner 2026 Prediction', {
  x: 0.8, y: 3.2, w: 4.2, h: 0.3,
  fontSize: 11, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

// Mini stats
const miniStats = [
  { value: '35%', label: '이미 채택' },
  { value: '39%', label: '10+ 에이전트' },
  { value: '2x', label: '생산성 향상' }
];

miniStats.forEach((stat, idx) => {
  const xPos = 0.9 + (idx * 1.35);
  slide4.addText(stat.value, {
    x: xPos, y: 3.6, w: 1.2, h: 0.35,
    fontSize: 18, bold: true, color: colors.accentPink,
    align: 'center', fontFace: 'Arial'
  });
  slide4.addText(stat.label, {
    x: xPos, y: 3.95, w: 1.2, h: 0.3,
    fontSize: 9, color: colors.textMuted,
    align: 'center', fontFace: 'Arial'
  });
});

// Right: Key points
const agenticPoints = [
  '재무, HR, 고객지원에 자율 시스템 적용',
  '최소 인간 개입으로 의사결정 수행',
  '공급망 전체 지능형 조율',
  '76% 임원이 "동료"로 인식'
];

agenticPoints.forEach((point, idx) => {
  slide4.addText(`• ${point}`, {
    x: 5.2, y: 1.7 + (idx * 0.55), w: 4.3, h: 0.5,
    fontSize: 14, color: colors.textPrimary,
    fontFace: 'Arial'
  });
});

slide4.addText('Source: Gartner, McKinsey, MIT/BCG Survey', {
  x: 0.8, y: 4.9, w: 8.4, h: 0.3,
  fontSize: 10, color: colors.textMuted,
  fontFace: 'Arial'
});

// ============================================
// Slide 5: Agentic AI Case Studies
// ============================================
let slide5 = pptx.addSlide();
slide5.background = { color: colors.surface };

slide5.addText('Agentic AI 성공 사례', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.7,
  fontSize: 32, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

slide5.addShape(pptx.shapes.RECTANGLE, {
  x: 0.8, y: 1.0, w: 1.5, h: 0.06,
  fill: { color: colors.accentIndigo }
});

const caseStudies = [
  { company: 'AtlantiCare', sector: '의료', metric: '-42%', desc: '문서화 시간', detail: '일 66분 절약' },
  { company: 'Bradesco', sector: '금융', metric: '+17%', desc: '직원 역량 확보', detail: '리드타임 22%↓' },
  { company: 'AMD', sector: 'HR', metric: '-80%', desc: '문의 해결 시간', detail: '90일 내 만족도 70%' },
  { company: 'Banking KYC', sector: '규정준수', metric: '200-2000%', desc: '생산성 향상', detail: 'McKinsey 보고' }
];

caseStudies.forEach((cs, idx) => {
  const row = Math.floor(idx / 2);
  const col = idx % 2;
  const xPos = 0.8 + (col * 4.5);
  const yPos = 1.3 + (row * 1.65);

  addRoundedCard(slide5, xPos, yPos, 4.2, 1.5);

  slide5.addText(cs.company, {
    x: xPos + 0.2, y: yPos + 0.15, w: 2.5, h: 0.35,
    fontSize: 14, bold: true, color: colors.textPrimary,
    fontFace: 'Arial'
  });

  slide5.addText(cs.sector, {
    x: xPos + 2.8, y: yPos + 0.15, w: 1.2, h: 0.35,
    fontSize: 11, color: colors.textMuted,
    align: 'right', fontFace: 'Arial'
  });

  slide5.addText(cs.metric, {
    x: xPos + 0.2, y: yPos + 0.5, w: 1.8, h: 0.5,
    fontSize: 28, bold: true, color: colors.accentEmerald,
    fontFace: 'Arial'
  });

  slide5.addText(cs.desc, {
    x: xPos + 2.0, y: yPos + 0.55, w: 2.0, h: 0.4,
    fontSize: 12, color: colors.textSecondary,
    fontFace: 'Arial'
  });

  slide5.addText(cs.detail, {
    x: xPos + 0.2, y: yPos + 1.05, w: 3.8, h: 0.3,
    fontSize: 10, color: colors.textMuted,
    fontFace: 'Arial'
  });
});

slide5.addText('Source: Deloitte Insights, Google Cloud, MIT Sloan', {
  x: 0.8, y: 4.9, w: 8.4, h: 0.3,
  fontSize: 10, color: colors.textMuted,
  fontFace: 'Arial'
});

// ============================================
// Slide 6: Edge AI & On-Device AI
// ============================================
let slide6 = pptx.addSlide();
slide6.background = { color: colors.surface };

slide6.addText('02', {
  x: 8.5, y: 0.3, w: 1.2, h: 1,
  fontSize: 60, color: 'F1F5F9', bold: true,
  fontFace: 'Arial'
});

slide6.addText('Edge AI & On-Device AI', {
  x: 0.8, y: 0.4, w: 7, h: 0.7,
  fontSize: 36, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

slide6.addText('클라우드 없이 기기에서 직접 AI 실행', {
  x: 0.8, y: 1.0, w: 7, h: 0.4,
  fontSize: 16, color: colors.textSecondary,
  fontFace: 'Arial'
});

// Left column - Market Data
addRoundedCard(slide6, 0.8, 1.5, 4.2, 2.7);

slide6.addText('Edge AI Market', {
  x: 0.8, y: 1.65, w: 4.2, h: 0.35,
  fontSize: 14, bold: true, color: colors.textSecondary,
  align: 'center', fontFace: 'Arial'
});

slide6.addText('$143B', {
  x: 0.8, y: 2.0, w: 4.2, h: 0.7,
  fontSize: 48, bold: true, color: colors.accentCyan,
  align: 'center', fontFace: 'Arial'
});

slide6.addText('2034년 전망 (CAGR 21%)', {
  x: 0.8, y: 2.7, w: 4.2, h: 0.35,
  fontSize: 12, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

slide6.addText('On-Device AI: $75.5B (2033, CAGR 27.8%)', {
  x: 0.8, y: 3.2, w: 4.2, h: 0.35,
  fontSize: 11, color: colors.textSecondary,
  align: 'center', fontFace: 'Arial'
});

// Stats row
slide6.addText('97%', {
  x: 1.0, y: 3.6, w: 1.3, h: 0.35,
  fontSize: 20, bold: true, color: colors.accentViolet,
  align: 'center', fontFace: 'Arial'
});
slide6.addText('CIO 로드맵', {
  x: 1.0, y: 3.95, w: 1.3, h: 0.25,
  fontSize: 9, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

slide6.addText('90%', {
  x: 2.3, y: 3.6, w: 1.3, h: 0.35,
  fontSize: 20, bold: true, color: colors.accentViolet,
  align: 'center', fontFace: 'Arial'
});
slide6.addText('예산 증가', {
  x: 2.3, y: 3.95, w: 1.3, h: 0.25,
  fontSize: 9, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

slide6.addText('46%', {
  x: 3.6, y: 3.6, w: 1.3, h: 0.35,
  fontSize: 20, bold: true, color: colors.accentViolet,
  align: 'center', fontFace: 'Arial'
});
slide6.addText('스마트폰 점유', {
  x: 3.6, y: 3.95, w: 1.3, h: 0.25,
  fontSize: 9, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

// Right column - Drivers
const edgeDrivers = [
  { icon: '⚡', text: '실시간 데이터 처리 수요' },
  { icon: '🔒', text: '프라이버시 보호 요구' },
  { icon: '📱', text: 'IoT 기기 150억+ 대 보급' },
  { icon: '🌐', text: '저지연 의사결정 필요' }
];

slide6.addText('성장 동인', {
  x: 5.2, y: 1.5, w: 4.3, h: 0.4,
  fontSize: 14, bold: true, color: colors.textSecondary,
  fontFace: 'Arial'
});

edgeDrivers.forEach((driver, idx) => {
  addRoundedCard(slide6, 5.2, 1.95 + (idx * 0.65), 4.3, 0.55);
  slide6.addText(`${driver.icon}  ${driver.text}`, {
    x: 5.4, y: 2.0 + (idx * 0.65), w: 4.0, h: 0.45,
    fontSize: 13, color: colors.textPrimary,
    fontFace: 'Arial'
  });
});

slide6.addText('Source: Precedence Research, Grand View Research', {
  x: 0.8, y: 4.9, w: 8.4, h: 0.3,
  fontSize: 10, color: colors.textMuted,
  fontFace: 'Arial'
});

// ============================================
// Slide 7: AI Adoption - Data Focus
// ============================================
let slide7 = pptx.addSlide();
slide7.background = { color: colors.surface };

slide7.addText('03', {
  x: 8.5, y: 0.3, w: 1.2, h: 1,
  fontSize: 60, color: 'F1F5F9', bold: true,
  fontFace: 'Arial'
});

slide7.addText('AI 채택 현황', {
  x: 0.8, y: 0.4, w: 7, h: 0.7,
  fontSize: 36, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

slide7.addText('실험에서 운영 핵심으로', {
  x: 0.8, y: 1.0, w: 7, h: 0.4,
  fontSize: 16, color: colors.textSecondary,
  fontFace: 'Arial'
});

// Main stat
addRoundedCard(slide7, 0.8, 1.5, 3.0, 2.0, {
  fill: { color: colors.surfaceDark }
});

slide7.addText('88%', {
  x: 0.8, y: 1.8, w: 3.0, h: 0.8,
  fontSize: 56, bold: true, color: colors.accentIndigo,
  align: 'center', fontFace: 'Arial'
});

slide7.addText('기업 AI 채택률', {
  x: 0.8, y: 2.6, w: 3.0, h: 0.4,
  fontSize: 14, color: colors.textLight,
  align: 'center', fontFace: 'Arial'
});

slide7.addText('McKinsey 2025', {
  x: 0.8, y: 3.0, w: 3.0, h: 0.3,
  fontSize: 10, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

// Secondary stats
const adoptionStats = [
  { value: '78%', label: 'Gen AI 채택', source: 'McKinsey' },
  { value: '80%+', label: 'Fortune 500\nChatGPT 사용', source: 'Industry' },
  { value: '20-40%', label: '생산성 향상', source: 'McKinsey' }
];

adoptionStats.forEach((stat, idx) => {
  const xPos = 4.0 + (idx * 2.0);
  addRoundedCard(slide7, xPos, 1.5, 1.85, 2.0);

  slide7.addText(stat.value, {
    x: xPos, y: 1.75, w: 1.85, h: 0.55,
    fontSize: 28, bold: true, color: colors.accentViolet,
    align: 'center', fontFace: 'Arial'
  });

  slide7.addText(stat.label, {
    x: xPos, y: 2.35, w: 1.85, h: 0.6,
    fontSize: 11, color: colors.textSecondary,
    align: 'center', fontFace: 'Arial'
  });

  slide7.addText(stat.source, {
    x: xPos, y: 3.0, w: 1.85, h: 0.3,
    fontSize: 9, color: colors.textMuted,
    align: 'center', fontFace: 'Arial'
  });
});

// Warning box
addRoundedCard(slide7, 0.8, 3.7, 8.7, 0.9, {
  fill: { color: 'FEF3C7' },
  line: { color: 'F59E0B', width: 1 }
});

slide7.addText('⚠️  단 1% 기업만 AI 성숙도 "성숙" 단계  •  57% 데이터가 "AI-ready" 아님  •  CEO 만족도 30% 미만', {
  x: 1.0, y: 3.85, w: 8.3, h: 0.6,
  fontSize: 12, color: '92400E',
  fontFace: 'Arial'
});

// ============================================
// Slide 8: AI Company Competition
// ============================================
let slide8 = pptx.addSlide();
slide8.background = { color: colors.surface };

slide8.addText('04', {
  x: 8.5, y: 0.3, w: 1.2, h: 1,
  fontSize: 60, color: 'F1F5F9', bold: true,
  fontFace: 'Arial'
});

slide8.addText('AI 기업 경쟁 구도', {
  x: 0.8, y: 0.4, w: 7, h: 0.7,
  fontSize: 36, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

slide8.addText('독점에서 다자 경쟁 체제로', {
  x: 0.8, y: 1.0, w: 7, h: 0.4,
  fontSize: 16, color: colors.textSecondary,
  fontFace: 'Arial'
});

// Company cards
const companies = [
  { name: 'NVIDIA', value: '$4.5T', desc: 'AI 컴퓨팅 80%+ 점유', color: colors.accentEmerald },
  { name: 'OpenAI', value: '$500B+', desc: '2026 IPO 목표, 매출 5x', color: colors.accentIndigo },
  { name: 'Anthropic', value: '$350B', desc: '매출 $1B→$26B (26x)', color: colors.accentViolet },
  { name: 'Google', value: 'Gemini 3', desc: 'LLMArena Top 10 중 4개', color: colors.accentCyan }
];

companies.forEach((company, idx) => {
  const row = Math.floor(idx / 2);
  const col = idx % 2;
  const xPos = 0.8 + (col * 4.5);
  const yPos = 1.4 + (row * 1.55);

  addRoundedCard(slide8, xPos, yPos, 4.2, 1.4);

  // Color accent bar
  slide8.addShape(pptx.shapes.RECTANGLE, {
    x: xPos, y: yPos, w: 0.08, h: 1.4,
    fill: { color: company.color }
  });

  slide8.addText(company.name, {
    x: xPos + 0.2, y: yPos + 0.15, w: 2.5, h: 0.4,
    fontSize: 16, bold: true, color: colors.textPrimary,
    fontFace: 'Arial'
  });

  slide8.addText(company.value, {
    x: xPos + 0.2, y: yPos + 0.55, w: 2.5, h: 0.45,
    fontSize: 24, bold: true, color: company.color,
    fontFace: 'Arial'
  });

  slide8.addText(company.desc, {
    x: xPos + 0.2, y: yPos + 1.0, w: 3.8, h: 0.3,
    fontSize: 11, color: colors.textSecondary,
    fontFace: 'Arial'
  });
});

slide8.addText('💡 "3-4개 기업 경쟁 체제로 전환 중" - Foundation Capital', {
  x: 0.8, y: 4.5, w: 8.7, h: 0.35,
  fontSize: 12, color: colors.textSecondary,
  fontFace: 'Arial'
});

// ============================================
// Slide 9: Key Takeaways
// ============================================
let slide9 = pptx.addSlide();
slide9.background = { color: colors.surface };

slide9.addText('Key Takeaways', {
  x: 0.8, y: 0.4, w: 8.4, h: 0.7,
  fontSize: 36, bold: true, color: colors.textPrimary,
  fontFace: 'Arial'
});

slide9.addShape(pptx.shapes.RECTANGLE, {
  x: 0.8, y: 1.0, w: 1.5, h: 0.06,
  fill: { color: colors.accentIndigo }
});

const takeaways = [
  { num: '01', title: 'Agentic AI', desc: '40% 기업 앱 채택, 생산성 2x', color: colors.accentIndigo },
  { num: '02', title: 'Edge AI', desc: '$143B 시장, CAGR 21%', color: colors.accentCyan },
  { num: '03', title: 'AI 채택 급증', desc: '88% 기업 채택, 주류화', color: colors.accentViolet },
  { num: '04', title: '경쟁 심화', desc: 'OpenAI→다자 경쟁 체제', color: colors.accentPink },
  { num: '05', title: '투자 집중', desc: 'VC의 50%+가 AI에 투자', color: colors.accentEmerald }
];

takeaways.forEach((item, idx) => {
  const row = Math.floor(idx / 3);
  const col = idx % 3;
  const xPos = 0.6 + (col * 3.1);
  const yPos = 1.3 + (row * 1.6);
  const width = idx < 3 ? 2.9 : (idx === 3 ? 4.4 : 4.4);
  const actualX = idx === 3 ? 0.6 : (idx === 4 ? 5.2 : xPos);

  addRoundedCard(slide9, actualX, yPos, idx < 3 ? 2.9 : 4.3, 1.45);

  slide9.addText(item.num, {
    x: actualX + 0.15, y: yPos + 0.15, w: 0.5, h: 0.4,
    fontSize: 14, bold: true, color: item.color,
    fontFace: 'Arial'
  });

  slide9.addText(item.title, {
    x: actualX + 0.15, y: yPos + 0.5, w: idx < 3 ? 2.6 : 4.0, h: 0.4,
    fontSize: 16, bold: true, color: colors.textPrimary,
    fontFace: 'Arial'
  });

  slide9.addText(item.desc, {
    x: actualX + 0.15, y: yPos + 0.9, w: idx < 3 ? 2.6 : 4.0, h: 0.4,
    fontSize: 12, color: colors.textSecondary,
    fontFace: 'Arial'
  });
});

// ============================================
// Slide 10: Thank You
// ============================================
let slide10 = pptx.addSlide();

// Dark gradient background
slide10.addShape(pptx.shapes.RECTANGLE, {
  x: 0, y: 0, w: 10, h: 5.625,
  fill: { color: colors.surfaceDark }
});

// Decorative gradient circles
slide10.addShape(pptx.shapes.OVAL, {
  x: 6, y: -1, w: 5, h: 5,
  fill: { color: colors.accentViolet, transparency: 85 }
});
slide10.addShape(pptx.shapes.OVAL, {
  x: -1, y: 3, w: 4, h: 4,
  fill: { color: colors.accentCyan, transparency: 90 }
});

slide10.addText('Thank You', {
  x: 0, y: 1.8, w: 10, h: 1,
  fontSize: 54, bold: true, color: colors.textLight,
  align: 'center', fontFace: 'Arial'
});

slide10.addText('AI Trends 2026', {
  x: 0, y: 2.9, w: 10, h: 0.5,
  fontSize: 20, color: colors.accentIndigo,
  align: 'center', fontFace: 'Arial'
});

slide10.addText('Created by PPT Agent Team', {
  x: 0, y: 3.5, w: 10, h: 0.4,
  fontSize: 14, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

slide10.addText('Sources: McKinsey, Gartner, MIT Sloan, Deloitte, Fortune Business Insights', {
  x: 0, y: 4.6, w: 10, h: 0.4,
  fontSize: 11, color: colors.textMuted,
  align: 'center', fontFace: 'Arial'
});

// Save the presentation
const outputPath = './AI_Trends_2026_v2.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(fileName => {
    console.log(`✅ Presentation created: ${fileName}`);
  })
  .catch(err => {
    console.error('❌ Error creating presentation:', err);
  });
