# PPT Agent Team v2.0

Claude의 Sub-agent 기능과 Skill을 활용한 **고품질 프리젠테이션 자동 제작 시스템**입니다.

## 개요

이 프로젝트는 AI 에이전트 팀이 협업하여 PowerPoint 프리젠테이션을 자동으로 생성하고, **이중 품질 평가 시스템**을 통해 완성도를 보장합니다.

```
📊 PPT Agent Team v2.0
├── 🔍 Research Agent      - 다층 리서치
├── 📝 Content Organizer   - 콘텐츠 구성
├── ✅ Slide Evaluator     - 논리적 평가
├── 👁️ Visual QA Agent     - 시각적 검증 ⭐NEW
├── 🎨 Design Skill        - Gemini 스타일 디자인
├── 📦 PPTX Skill          - PPT 생성
├── 🖼️ Canvas-Design Skill - 그래픽 제작
└── 📸 Thumbnail Preview   - 전체 조감 ⭐NEW
```

## 핵심 가치

```
🔍 Research    → 깊이 있는 자료 조사 (다층 리서치)
📝 Structure   → 논리적인 콘텐츠 구성
✅ Evaluate    → 다층적 품질 평가 (논리 + 시각)
🎨 Design      → 세련된 시각 디자인 (Gemini 스타일)
👁️ Visual QA   → 실제 렌더링 기반 검증
📦 Generate    → 완성도 높은 PPTX 생성
```

## 프로젝트 구조

```
ppt-agent-team/
├── agents/                          # 에이전트 정의
│   ├── research_agent.md            # 리서치 에이전트 v2.0
│   ├── content_organizer_agent.md   # 자료 정리 에이전트
│   ├── slide_evaluator_agent.md     # 슬라이드 평가 에이전트
│   └── visual_qa_agent.md           # 시각적 QA 에이전트 ⭐NEW
│
├── skills/                          # 스킬 정의
│   ├── design/
│   │   └── SKILL.md                 # 디자인 스킬 v2.0 (Gemini 스타일)
│   ├── pptx/
│   │   ├── SKILL.md                 # PPTX 스킬
│   │   ├── html2pptx.md             # HTML→PPTX 변환 가이드
│   │   └── ooxml.md                 # OOXML 기술 참조
│   ├── canvas-design/
│   │   └── SKILL.md                 # 캔버스 디자인 스킬
│   └── thumbnail/
│       └── SKILL.md                 # 썸네일 프리뷰 스킬 ⭐NEW
│
├── workflows/
│   └── ppt_workflow.md              # 전체 워크플로우 (5단계)
│
├── output/                          # 출력물
│   └── ai-trends-2026/              # 테스트 프리젠테이션
│       └── v2/
│
├── PRD.md                           # 제품 요구사항 문서
└── README.md                        # 이 파일
```

---

## 에이전트 (Agents)

### 1. Research Agent v2.0 (리서치 에이전트)

**다층 리서치 프레임워크**로 깊이 있는 자료를 조사합니다.

**핵심 기능:**
- 4단계 리서치 (Surface → Context → Depth → Insight)
- 소스 다각화 (학술, 기업, 미디어, 정부)
- 데이터 검증 프로토콜 (교차 검증, 신뢰도 점수)
- 슬라이드별 맞춤 리서치

**사용 도구:** `WebSearch`, `WebFetch`, `Read`

### 2. Content Organizer Agent (자료 정리 에이전트)

수집된 자료를 프리젠테이션에 적합한 형태로 구조화합니다.

**핵심 기능:**
- 스토리라인 설계
- 슬라이드 구성 최적화 (1슬라이드 1메시지)
- 시각화 계획 수립

**협업:** Research Agent와 협력하여 추가 자료 요청

### 3. Slide Evaluator Agent (슬라이드 평가 에이전트)

완성된 구성을 **논리적 관점**에서 평가합니다.

**평가 기준 (100점 만점):**
| 항목 | 배점 |
|------|------|
| 구조적 완성도 | 25점 |
| 메시지 전달력 | 25점 |
| 시각적 일관성 | 25점 |
| 설득력 | 25점 |

**통과 기준:** 80점 이상

### 4. Visual QA Agent (시각적 QA 에이전트) ⭐NEW

PPTX를 **실제 이미지로 렌더링**하고 시각적 품질을 검증합니다.

**핵심 기능:**
- PPTX → 이미지 변환 (LibreOffice + Poppler)
- Claude Vision 기반 시각 평가
- 구체적 디자인 피드백 생성
- 피드백 루프 관리 (최대 3회)

**평가 기준 (100점 만점):**
| 항목 | 배점 |
|------|------|
| 시각적 계층 | 25점 |
| 색상 조화 | 20점 |
| 레이아웃 균형 | 20점 |
| 타이포그래피 | 20점 |
| 전문성/완성도 | 15점 |

**통과 기준:** 80점 이상

---

## 스킬 (Skills)

### 1. Design Skill v2.0 (디자인 스킬)

**Gemini 스타일**의 세련된 프리젠테이션 디자인 시스템입니다.

**핵심 원칙:**
- **Gradient-First Design**: 그라데이션으로 에너지 전달
- **Circular Form Language**: 원형으로 조화와 편안함
- **Warm Spatial Quality**: 넉넉한 여백, 부유하는 요소

**제공 기능:**
- 색상 팔레트 (Modern Clarity, Dark Sophistication, Warm Professional)
- 폰트 페어링 (Fraunces+Plus Jakarta, Syne+Satoshi, Pretendard)
- 레이아웃 패턴 (Hero, Asymmetric, Card Grid, Data Focus)

**참조:** [Google Gemini Visual Design](https://design.google/library/gemini-ai-visual-design)

### 2. PPTX Skill (PPTX 스킬)

PowerPoint 파일을 효과적으로 생성합니다.

**핵심 워크플로우:**
1. HTML 슬라이드 작성
2. Playwright로 렌더링
3. PptxGenJS로 PPTX 변환

**기술 문서:**
- `html2pptx.md`: HTML→PPTX 변환 가이드
- `ooxml.md`: XML 레벨 편집 참조

**참조:** [Anthropic Skills - PPTX](https://github.com/anthropics/skills/tree/main/skills/pptx)

### 3. Canvas-Design Skill (캔버스 디자인 스킬)

커스텀 시각 자료를 프로그래매틱하게 생성합니다.

**생성 가능 자산:**
- 차트 및 데이터 시각화
- 인포그래픽
- 아이콘 및 심볼
- 타이포그래피 아트
- 배경 및 텍스처
- 다이어그램

**출력 형식:** PNG, PDF, SVG

**참조:** [Anthropic Skills - Canvas Design](https://github.com/anthropics/skills/tree/main/skills/canvas-design)

### 4. Thumbnail Preview Skill (썸네일 프리뷰 스킬) ⭐NEW

전체 프리젠테이션을 **한 눈에 조감**할 수 있는 썸네일 그리드를 생성합니다.

**핵심 기능:**
- 슬라이드 이미지를 그리드 형태로 조합
- 슬라이드 번호 오버레이
- 문제 슬라이드 강조 (빨간 테두리)
- Before/After 비교 그리드

**의존성:** sharp, ImageMagick (선택)

---

## 워크플로우

### 전체 프로세스 (5단계)

```
Phase 1: 리서치
┌─────────────────────────────────────────────┐
│  Research Agent                             │
│  ├─ 다층 리서치 (Surface→Context→Depth→Insight)
│  ├─ 소스 다각화 (학술, 기업, 미디어)         │
│  └─ 데이터 검증 (교차 검증, 신뢰도 점수)     │
└─────────────────────┬───────────────────────┘
                      ↓
Phase 2: 콘텐츠 구성
┌─────────────────────────────────────────────┐
│  Content Organizer Agent                    │
│  ├─ 스토리라인 설계                         │
│  ├─ 슬라이드 구조화 (1슬라이드 1메시지)     │
│  └─ Research Agent와 협업 (추가 자료 요청)  │
└─────────────────────┬───────────────────────┘
                      ↓
Phase 3: 논리적 평가
┌─────────────────────────────────────────────┐
│  Slide Evaluator Agent                      │
│  ├─ 4개 항목 평가 (100점 만점)              │
│  ├─ 80점 이상: Phase 4로 진행               │
│  └─ 80점 미만: Content Organizer로 피드백   │
└─────────────────────┬───────────────────────┘
                      ↓
Phase 4: 디자인 & 생성
┌─────────────────────────────────────────────┐
│  Design Skill → Canvas-Design → PPTX Skill  │
│  ├─ 디자인 시스템 적용                      │
│  ├─ 시각 자료 생성                          │
│  └─ PPTX 파일 생성                          │
└─────────────────────┬───────────────────────┘
                      ↓
Phase 5: 시각적 검증 ⭐NEW
┌─────────────────────────────────────────────┐
│  Visual QA Agent + Thumbnail Preview        │
│  ├─ PPTX → 이미지 변환                      │
│  ├─ 썸네일 그리드 생성 (전체 조감)          │
│  ├─ Claude Vision 기반 시각 평가            │
│  ├─ 80점 이상: 완료                         │
│  └─ 80점 미만: Design Skill로 피드백 (최대 3회)
└─────────────────────┬───────────────────────┘
                      ↓
                   완료 ✓
```

### 이중 피드백 루프

#### 논리적 피드백 루프 (Phase 3)
```
Slide Evaluator → Content Organizer → 재구성 → 재평가
```

#### 시각적 피드백 루프 (Phase 5)
```
Visual QA → Design Skill → PPTX 재생성 → 재평가 (최대 3회)
```

---

## 사용 예시

### 기본 요청

```
"AI 트렌드에 대한 15분 프리젠테이션을 만들어줘.
 청중은 기업 임원들이고, 투자 결정에 참고할 내용으로 구성해줘."
```

### 출력물

```
output/
├── presentation.pptx        # 최종 프리젠테이션
├── slides/
│   ├── slide-1.png          # 슬라이드 이미지
│   ├── slide-2.png
│   └── ...
├── thumbnail_grid.png       # 전체 조감 이미지
├── assets/                  # 사용된 시각 자료
├── research_report.md       # 리서치 보고서
├── visual_qa_report.md      # 시각적 평가 보고서
├── speaker_notes.md         # 발표자 노트
└── sources.md               # 참고 자료
```

---

## 기술 스택

### 의존성

```json
{
  "javascript": {
    "pptxgenjs": "^3.12.0",
    "playwright": "^1.40.0",
    "sharp": "^0.33.0"
  },
  "python": {
    "markitdown": "latest",
    "defusedxml": "latest"
  },
  "system": [
    "LibreOffice (headless)",
    "Poppler (pdftoppm)",
    "ImageMagick (선택)"
  ]
}
```

### 권장 환경

- Node.js 18+
- Python 3.8+
- Claude API 접근

---

## 문서

- **[PRD.md](./PRD.md)** - 제품 요구사항 문서
- **[workflows/ppt_workflow.md](./workflows/ppt_workflow.md)** - 상세 워크플로우
- **[agents/](./agents/)** - 에이전트 정의
- **[skills/](./skills/)** - 스킬 정의

## 참고 자료

### 외부 참조
- [Google Gemini Visual Design](https://design.google/library/gemini-ai-visual-design)
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [PptxGenJS Documentation](https://gitbrent.github.io/PptxGenJS/)
- [Office Open XML Reference](https://docs.microsoft.com/en-us/office/open-xml/open-xml-sdk)

---

## 버전 히스토리

| 버전 | 날짜 | 주요 변경 |
|------|------|----------|
| v2.0 | 2026-02-03 | Visual QA Agent, Thumbnail Preview, Design v2.0, Research v2.0 |
| v1.0 | 2026-02-03 | 초기 버전 |

## 라이선스

이 프로젝트는 Anthropic Skills의 라이선스를 따릅니다.
