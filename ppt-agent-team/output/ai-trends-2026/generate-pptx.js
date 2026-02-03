import PptxGenJS from 'pptxgenjs';

// Create presentation
const pptx = new PptxGenJS();

// Set presentation properties
pptx.author = 'PPT Agent Team';
pptx.title = 'AI Trends 2026';
pptx.subject = 'The New Era of Artificial Intelligence';
pptx.company = 'PPT Agent Team';

// Define layout (16:9)
pptx.defineLayout({ name: 'WIDE', width: 10, height: 5.625 });
pptx.layout = 'WIDE';

// Color palette - Tech Futuristic (without # prefix!)
const colors = {
  primary: '0a0a0f',
  secondary: '1a1a2e',
  accentCyan: '00d4ff',
  accentPurple: '7b2cbf',
  textWhite: 'ffffff',
  textGray: 'b0b0b0'
};

// ============================================
// Slide 1: Title
// ============================================
let slide1 = pptx.addSlide();
slide1.background = { color: colors.primary };

slide1.addText('AI Trends 2026', {
  x: 0, y: 1.8, w: '100%', h: 1.2,
  fontSize: 60, bold: true, color: colors.accentCyan,
  align: 'center'
});

slide1.addText('The New Era of Artificial Intelligence', {
  x: 0, y: 3.0, w: '100%', h: 0.6,
  fontSize: 24, color: colors.textWhite,
  align: 'center'
});

slide1.addText('PPT Agent Team | February 2026', {
  x: 0, y: 4.5, w: '100%', h: 0.4,
  fontSize: 14, color: colors.textGray,
  align: 'center'
});

// ============================================
// Slide 2: Agenda
// ============================================
let slide2 = pptx.addSlide();
slide2.background = { color: colors.primary };

slide2.addText('Agenda', {
  x: 0.5, y: 0.4, w: 9, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide2.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

const agendaItems = [
  'AI Market Overview',
  '5 Key Trends for 2026',
  'Key Takeaways'
];

agendaItems.forEach((item, idx) => {
  slide2.addText(`${idx + 1}. ${item}`, {
    x: 0.8, y: 1.5 + (idx * 0.8), w: 8, h: 0.6,
    fontSize: 24, color: colors.textWhite,
    bullet: false
  });
});

// ============================================
// Slide 3: Market Size
// ============================================
let slide3 = pptx.addSlide();
slide3.background = { color: colors.primary };

slide3.addText('AI Market Size', {
  x: 0.5, y: 0.4, w: 9, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide3.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

const marketData = [
  { value: '$294B', label: '2025 Market Size' },
  { value: '$375B', label: '2026 Projected' },
  { value: '$3.5T', label: '2034 Forecast' },
  { value: '30%+', label: 'Annual CAGR' }
];

marketData.forEach((data, idx) => {
  const xPos = 0.5 + (idx * 2.4);

  slide3.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: xPos, y: 1.5, w: 2.2, h: 1.8,
    fill: { color: colors.secondary },
    line: { color: colors.accentPurple, width: 2, dashType: 'solid' }
  });

  slide3.addText(data.value, {
    x: xPos, y: 1.7, w: 2.2, h: 0.8,
    fontSize: 28, bold: true, color: colors.accentCyan,
    align: 'center'
  });

  slide3.addText(data.label, {
    x: xPos, y: 2.5, w: 2.2, h: 0.5,
    fontSize: 11, color: colors.textGray,
    align: 'center'
  });
});

slide3.addText('Source: Fortune Business Insights, Statista, Grand View Research', {
  x: 0.5, y: 5.0, w: 9, h: 0.3,
  fontSize: 10, color: colors.textGray
});

// ============================================
// Slide 4: Trend 1 - Agentic AI
// ============================================
let slide4 = pptx.addSlide();
slide4.background = { color: colors.primary };

slide4.addText('01', {
  x: 7.5, y: 0.3, w: 2, h: 1.5,
  fontSize: 80, color: '1a2a3a', bold: true, align: 'right'
});

slide4.addText('Trend 1: Agentic AI', {
  x: 0.5, y: 0.4, w: 7, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide4.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

// Highlight box
slide4.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.4, w: 9, h: 0.7,
  fill: { color: colors.secondary }
});

slide4.addText([
  { text: '40%', options: { bold: true, color: colors.accentCyan } },
  { text: ' of enterprise apps will use AI agents by 2026', options: { color: colors.textWhite } }
], {
  x: 0.7, y: 1.5, w: 8.6, h: 0.5, fontSize: 20
});

const agenticPoints = [
  'Autonomous systems for Finance, HR, Customer Support',
  'Minimal human intervention in decision-making',
  'Intelligent supply chain orchestration',
  'Data interpretation and system access'
];

agenticPoints.forEach((point, idx) => {
  slide4.addText(`• ${point}`, {
    x: 0.5, y: 2.3 + (idx * 0.55), w: 9, h: 0.5,
    fontSize: 18, color: colors.textWhite
  });
});

slide4.addText('Source: Gartner Predictions 2026', {
  x: 0.5, y: 5.0, w: 9, h: 0.3,
  fontSize: 10, color: colors.accentPurple
});

// ============================================
// Slide 5: Trend 2 - On-Device AI
// ============================================
let slide5 = pptx.addSlide();
slide5.background = { color: colors.primary };

slide5.addText('02', {
  x: 7.5, y: 0.3, w: 2, h: 1.5,
  fontSize: 80, color: '1a2a3a', bold: true, align: 'right'
});

slide5.addText('Trend 2: On-Device AI', {
  x: 0.5, y: 0.4, w: 7, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide5.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

// Left column
slide5.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.4, w: 4.3, h: 0.6,
  fill: { color: colors.secondary }
});
slide5.addText([
  { text: 'Edge Intelligence', options: { bold: true, color: colors.accentCyan } },
  { text: ' goes mainstream', options: { color: colors.textWhite } }
], { x: 0.7, y: 1.5, w: 4, h: 0.4, fontSize: 16 });

const leftPoints = ['Mobile AI experiences', 'IoT applications', 'Privacy-critical systems'];
leftPoints.forEach((point, idx) => {
  slide5.addText(`• ${point}`, {
    x: 0.5, y: 2.2 + (idx * 0.5), w: 4.3, h: 0.4,
    fontSize: 16, color: colors.textWhite
  });
});

// Right column
slide5.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 5.2, y: 1.4, w: 4.3, h: 0.6,
  fill: { color: colors.secondary }
});
slide5.addText([
  { text: 'No Cloud', options: { bold: true, color: colors.accentCyan } },
  { text: ' dependency', options: { color: colors.textWhite } }
], { x: 5.4, y: 1.5, w: 4, h: 0.4, fontSize: 16 });

const rightPoints = ['Efficient model design', 'Hardware acceleration', 'Real-time processing'];
rightPoints.forEach((point, idx) => {
  slide5.addText(`• ${point}`, {
    x: 5.2, y: 2.2 + (idx * 0.5), w: 4.3, h: 0.4,
    fontSize: 16, color: colors.textWhite
  });
});

// ============================================
// Slide 6: Trend 3 - AI as Partner
// ============================================
let slide6 = pptx.addSlide();
slide6.background = { color: colors.primary };

slide6.addText('03', {
  x: 7.5, y: 0.3, w: 2, h: 1.5,
  fontSize: 80, color: '1a2a3a', bold: true, align: 'right'
});

slide6.addText('Trend 3: AI as Partner', {
  x: 0.5, y: 0.4, w: 7, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide6.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

slide6.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.4, w: 9, h: 0.7,
  fill: { color: colors.secondary }
});

slide6.addText([
  { text: 'AI evolves from ', options: { color: colors.textWhite } },
  { text: 'instrument', options: { bold: true, color: colors.accentCyan } },
  { text: ' to ', options: { color: colors.textWhite } },
  { text: 'collaborative partner', options: { bold: true, color: colors.accentCyan } }
], { x: 0.7, y: 1.55, w: 8.6, h: 0.5, fontSize: 20 });

const partnerPoints = [
  'Amplifies human expertise',
  'Collaborates in creation and problem-solving',
  'Transforms how we work',
  'Beyond answering questions'
];

partnerPoints.forEach((point, idx) => {
  slide6.addText(`• ${point}`, {
    x: 0.5, y: 2.3 + (idx * 0.55), w: 9, h: 0.5,
    fontSize: 18, color: colors.textWhite
  });
});

slide6.addText('Source: Microsoft AI Research', {
  x: 0.5, y: 5.0, w: 9, h: 0.3,
  fontSize: 10, color: colors.accentPurple
});

// ============================================
// Slide 7: Trend 4 - Quantum Computing
// ============================================
let slide7 = pptx.addSlide();
slide7.background = { color: colors.primary };

slide7.addText('04', {
  x: 7.5, y: 0.3, w: 2, h: 1.5,
  fontSize: 80, color: '1a2a3a', bold: true, align: 'right'
});

slide7.addText('Trend 4: Quantum Leap', {
  x: 0.5, y: 0.4, w: 7, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide7.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

slide7.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.4, w: 9, h: 0.7,
  fill: { color: colors.secondary }
});

slide7.addText([
  { text: 'IBM: Quantum computers will ', options: { color: colors.textWhite } },
  { text: 'outperform', options: { bold: true, color: colors.accentCyan } },
  { text: ' classical computers in 2026', options: { color: colors.textWhite } }
], { x: 0.7, y: 1.55, w: 8.6, h: 0.5, fontSize: 18 });

slide7.addText('Breakthrough Areas:', {
  x: 0.5, y: 2.2, w: 9, h: 0.5,
  fontSize: 22, bold: true, color: colors.textWhite
});

const quantumPoints = ['Drug development', 'Materials science', 'Financial optimization', 'Complex simulations'];
quantumPoints.forEach((point, idx) => {
  slide7.addText(`• ${point}`, {
    x: 0.5, y: 2.7 + (idx * 0.5), w: 9, h: 0.45,
    fontSize: 18, color: colors.textWhite
  });
});

// ============================================
// Slide 8: Trend 5 - Global AI Race
// ============================================
let slide8 = pptx.addSlide();
slide8.background = { color: colors.primary };

slide8.addText('05', {
  x: 7.5, y: 0.3, w: 2, h: 1.5,
  fontSize: 80, color: '1a2a3a', bold: true, align: 'right'
});

slide8.addText('Trend 5: Global AI Race', {
  x: 0.5, y: 0.4, w: 7, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide8.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

// Left column
slide8.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.5, y: 1.4, w: 4.3, h: 0.6,
  fill: { color: colors.secondary }
});
slide8.addText([
  { text: 'China', options: { bold: true, color: colors.accentCyan } },
  { text: ' Open Source Rise', options: { color: colors.textWhite } }
], { x: 0.7, y: 1.5, w: 4, h: 0.4, fontSize: 16 });

slide8.addText('• Open source AI adoption', {
  x: 0.5, y: 2.2, w: 4.3, h: 0.4, fontSize: 16, color: colors.textWhite
});
slide8.addText('• Global AI community goodwill', {
  x: 0.5, y: 2.6, w: 4.3, h: 0.4, fontSize: 16, color: colors.textWhite
});

// Right column
slide8.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 5.2, y: 1.4, w: 4.3, h: 0.6,
  fill: { color: colors.secondary }
});
slide8.addText([
  { text: 'Tech Gap: ', options: { color: colors.textWhite } },
  { text: 'Months → Weeks', options: { bold: true, color: colors.accentCyan } }
], { x: 5.4, y: 1.5, w: 4, h: 0.4, fontSize: 16 });

slide8.addText('• Silicon Valley adopting Chinese models', {
  x: 5.2, y: 2.2, w: 4.3, h: 0.4, fontSize: 16, color: colors.textWhite
});
slide8.addText('• Rapid innovation cycle', {
  x: 5.2, y: 2.6, w: 4.3, h: 0.4, fontSize: 16, color: colors.textWhite
});

// ============================================
// Slide 9: Key Takeaways
// ============================================
let slide9 = pptx.addSlide();
slide9.background = { color: colors.primary };

slide9.addText('Key Takeaways', {
  x: 0.5, y: 0.4, w: 9, h: 0.8,
  fontSize: 36, bold: true, color: colors.accentCyan
});

slide9.addShape(pptx.shapes.RECTANGLE, {
  x: 0.5, y: 1.1, w: 9, h: 0.05,
  fill: { color: colors.accentPurple }
});

const takeaways = [
  { value: '30%+', label: 'Annual AI Market Growth' },
  { value: 'Agentic AI', label: 'Drives Enterprise Innovation' },
  { value: 'On-Device', label: 'Enhanced Privacy' },
  { value: 'Global Race', label: 'Intensifying Competition' }
];

takeaways.forEach((item, idx) => {
  const row = Math.floor(idx / 2);
  const col = idx % 2;
  const xPos = 0.5 + (col * 4.7);
  const yPos = 1.4 + (row * 1.8);

  slide9.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
    x: xPos, y: yPos, w: 4.3, h: 1.5,
    fill: { color: colors.secondary },
    line: { color: colors.accentPurple, width: 1 }
  });

  slide9.addText(item.value, {
    x: xPos, y: yPos + 0.3, w: 4.3, h: 0.6,
    fontSize: 24, bold: true, color: colors.accentCyan, align: 'center'
  });

  slide9.addText(item.label, {
    x: xPos, y: yPos + 0.9, w: 4.3, h: 0.4,
    fontSize: 14, color: colors.textGray, align: 'center'
  });
});

// ============================================
// Slide 10: Thank You
// ============================================
let slide10 = pptx.addSlide();
slide10.background = { color: colors.secondary };

slide10.addText('Thank You', {
  x: 0, y: 1.8, w: '100%', h: 1,
  fontSize: 54, bold: true, color: colors.accentCyan, align: 'center'
});

slide10.addText('AI Trends 2026 Presentation', {
  x: 0, y: 3.0, w: '100%', h: 0.5,
  fontSize: 20, color: colors.textWhite, align: 'center'
});

slide10.addText('Created by PPT Agent Team', {
  x: 0, y: 3.5, w: '100%', h: 0.5,
  fontSize: 16, color: colors.textGray, align: 'center'
});

slide10.addText('Sources: Microsoft, MIT Tech Review, IBM, Gartner, Statista', {
  x: 0, y: 4.5, w: '100%', h: 0.4,
  fontSize: 12, color: colors.textGray, align: 'center'
});

// Save the presentation
const outputPath = './AI_Trends_2026.pptx';
pptx.writeFile({ fileName: outputPath })
  .then(fileName => {
    console.log(`Presentation created: ${fileName}`);
  })
  .catch(err => {
    console.error('Error creating presentation:', err);
  });
