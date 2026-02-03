# PPT Agent Team - Product Requirements Document (PRD)

## 문서 정보

| 항목 | 내용 |
|------|------|
| 버전 | 2.0 |
| 최종 수정 | 2026-02-03 |
| 상태 | Active Development |

---

## 1. 개요

### 1.1 프로젝트 소개

**PPT Agent Team**은 Claude의 Sub-agent 기능과 Skill을 활용하여 **고품질 PowerPoint 프리젠테이션을 자동 생성**하는 AI 에이전트 팀입니다.

### 1.2 핵심 가치

```
🔍 Research    → 깊이 있는 자료 조사
📝 Structure   → 논리적인 콘텐츠 구성
✅ Evaluate    → 다층적 품질 평가
🎨 Design      → 세련된 시각 디자인
👁️ Visual QA   → 실제 렌더링 기반 검증
📦 Generate    → 완성도 높은 PPTX 생성
```

### 1.3 목표 사용자

- 프리젠테이션 제작이 필요한 비즈니스 전문가
- 시간 효율적인 자료 제작이 필요한 팀
- 디자인 역량이 부족한 콘텐츠 크리에이터

---

## 2. 시스템 아키텍처

### 2.1 전체 구조

```
┌─────────────────────────────────────────────────────────────────┐
│                         PPT Agent Team                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────── Agents ───────────────────┐              │
│  │                                               │              │
│  │  [Research]  →  [Content]  →  [Slide]  →  [Visual QA]       │
│  │   Agent         Organizer     Evaluator     Agent           │
│  │                                                              │
│  └───────────────────────────────────────────────┘              │
│                          ↓                                      │
│  ┌─────────────────── Skills ───────────────────┐              │
│  │                                               │              │
│  │  [Design]  [Canvas]  [PPTX]  [Thumbnail]     │              │
│  │   Skill    Design    Skill    Preview        │              │
│  │                                               │              │
│  └───────────────────────────────────────────────┘              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 컴포넌트 목록

| 유형 | 이름 | 역할 | 버전 |
|------|------|------|------|
| Agent | Research Agent | 웹 리서치, 자료 수집 | v2.0 |
| Agent | Content Organizer | 슬라이드 구성, 스토리라인 | v1.0 |
| Agent | Slide Evaluator | 논리적 구성 평가 | v1.0 |
| Agent | **Visual QA Agent** | 시각적 품질 검증 | v1.0 (NEW) |
| Skill | Design Skill | 디자인 시스템, 가이드 | v2.0 |
| Skill | Canvas-Design Skill | 차트, 그래픽 생성 | v1.0 |
| Skill | PPTX Skill | PPTX 파일 생성 | v1.0 |
| Skill | **Thumbnail Preview** | 썸네일 그리드 생성 | v1.0 (NEW) |

---

## 3. 워크플로우

### 3.1 전체 프로세스 (v2.0)

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
Phase 5: 시각적 검증 (NEW)
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

### 3.2 피드백 루프

#### 논리적 피드백 루프 (Phase 3)
```
Slide Evaluator → Content Organizer → 재구성 → 재평가
```

#### 시각적 피드백 루프 (Phase 5)
```
Visual QA → Design Skill → PPTX 재생성 → 재평가 (최대 3회)
```

---

## 4. 에이전트 상세

### 4.1 Research Agent (리서치 에이전트)

**역할**: 프리젠테이션 주제에 대한 심층 리서치

**핵심 기능**:
- 다층 리서치 프레임워크 (4단계)
- 소스 다각화 전략
- 데이터 검증 프로토콜 (교차 검증)
- 슬라이드별 맞춤 리서치

**출력**: 구조화된 리서치 보고서 (JSON)

### 4.2 Content Organizer Agent (자료 정리 에이전트)

**역할**: 리서치 결과를 슬라이드 구조로 변환

**핵심 기능**:
- 스토리라인 설계
- 슬라이드 유형별 최적화
- 1슬라이드 1메시지 원칙
- Research Agent와 협업

**출력**: 슬라이드 구성안 (JSON)

### 4.3 Slide Evaluator Agent (슬라이드 평가 에이전트)

**역할**: 슬라이드 구성의 논리적 품질 평가

**평가 기준** (100점):
| 항목 | 배점 |
|------|------|
| 구조적 완성도 | 25점 |
| 메시지 전달력 | 25점 |
| 시각적 일관성 | 25점 |
| 설득력 | 25점 |

**통과 기준**: 80점 이상

### 4.4 Visual QA Agent (시각적 품질 검증 에이전트) ⭐ NEW

**역할**: 최종 PPTX의 시각적 품질 검증

**핵심 기능**:
- PPTX → 이미지 변환 (LibreOffice + Poppler)
- Claude Vision 기반 시각 평가
- 구체적 디자인 피드백 생성
- 피드백 루프 관리 (최대 3회)

**평가 기준** (100점):
| 항목 | 배점 |
|------|------|
| 시각적 계층 | 25점 |
| 색상 조화 | 20점 |
| 레이아웃 균형 | 20점 |
| 타이포그래피 | 20점 |
| 전문성/완성도 | 15점 |

**통과 기준**: 80점 이상

---

## 5. 스킬 상세

### 5.1 Design Skill (디자인 스킬)

**역할**: 프리젠테이션 디자인 시스템 제공

**핵심 원칙**:
- Gradient-First Design (그라데이션 우선)
- Circular Form Language (원형 형태 언어)
- Warm Spatial Quality (따뜻한 공간감)

**참조**: Gemini Visual Design, Anthropic Frontend Design Skill

### 5.2 Canvas-Design Skill (캔버스 디자인 스킬)

**역할**: 커스텀 시각 자료 생성

**생성 가능 자산**:
- 차트 (파이, 막대, 라인)
- 인포그래픽
- 아이콘
- 타이포그래피 아트
- 배경/텍스처
- 다이어그램

### 5.3 PPTX Skill (PPTX 스킬)

**역할**: PowerPoint 파일 생성

**워크플로우**: HTML → Playwright → PptxGenJS → PPTX

**의존성**: pptxgenjs, playwright, sharp

### 5.4 Thumbnail Preview Skill ⭐ NEW

**역할**: 전체 프리젠테이션 조감용 썸네일 그리드 생성

**기능**:
- 슬라이드 그리드 조합
- 슬라이드 번호 오버레이
- 문제 슬라이드 강조
- Before/After 비교 (선택)

**의존성**: sharp, ImageMagick (선택)

---

## 6. 기술 스택

### 6.1 런타임
| 환경 | 버전 |
|------|------|
| Node.js | 18+ |
| Python | 3.8+ |

### 6.2 핵심 의존성

**JavaScript**:
```json
{
  "pptxgenjs": "^3.12.0",
  "playwright": "^1.40.0",
  "sharp": "^0.33.0"
}
```

**Python**:
```
markitdown
defusedxml
```

**System**:
```
LibreOffice (headless)
Poppler (pdftoppm)
ImageMagick (선택)
```

---

## 7. 품질 기준

### 7.1 이중 평가 시스템

| 평가 단계 | 평가자 | 관점 | 통과 기준 |
|----------|--------|------|----------|
| Phase 3 | Slide Evaluator | 논리적 구성 | 80점 |
| Phase 5 | Visual QA Agent | 시각적 품질 | 80점 |

### 7.2 피드백 루프 제한

- 논리적 평가: 무제한 (사용자 개입 가능)
- 시각적 평가: 최대 3회 (3회 후 수동 승인)

---

## 8. 출력물

### 8.1 최종 산출물

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

### 8.2 실제 출력물 예시

```
output/
├── ai-trends-2026/          # 예제 1: AI 트렌드 2026
│   ├── AI_Trends_2026.pptx
│   └── v2/
│       ├── AI_Trends_2026_v2.pptx  (220KB)
│       └── research_report.md
│
└── openclaw-analysis/       # 예제 2: OpenClaw 분석 ⭐NEW
    ├── OpenClaw_Analysis.pptx     (220KB, 10슬라이드)
    ├── research_report.md         # 리서치 보고서
    ├── visual_qa_report.md        # Visual QA 88점 PASS
    └── generate-pptx.js           # 생성 스크립트
```

### 8.2 메타데이터

```json
{
  "version": "2.0",
  "created_at": "2026-02-03T12:00:00Z",
  "iterations": {
    "content_revisions": 1,
    "design_revisions": 2
  },
  "scores": {
    "slide_evaluator": 85,
    "visual_qa": 82
  }
}
```

---

## 9. 사례 연구: OpenClaw 분석 프리젠테이션

### 9.1 요청 사항

```
"OpenClaw에 대한 분석과 인사이트를 10분 프리젠테이션으로 만들어줘.
 청중은 AI 관심사가 높은 임원들이고, 20년 이상의 AI 프로덕트 리더로서 작성해줘"
```

### 9.2 실행 결과

| 항목 | 결과 |
|------|------|
| 슬라이드 수 | 10장 |
| 파일 크기 | 220KB |
| 발표 시간 | 10분 |
| Visual QA 점수 | **88점 (PASS)** |
| 디자인 시스템 | Dark Sophistication (Gemini Style) |

### 9.3 슬라이드 구성

| # | 제목 | 핵심 내용 |
|---|------|----------|
| 1 | Title | OpenClaw: 오픈소스 AI 에이전트의 부상 |
| 2 | Executive Summary | 4가지 핵심 포인트 (성장, 접근, 위험, 전환) |
| 3 | What is OpenClaw | 정의 + 명칭 변천사 (Clawdbot→Moltbot→OpenClaw) |
| 4 | Core Features | 멀티채널, 시스템 제어, 메모리, 스킬 시스템 |
| 5 | Explosive Growth | 145K+ GitHub Stars, 2개월 역대급 성장 |
| 6 | Moltbook | AI 에이전트 전용 소셜 네트워크 |
| 7 | Security Concerns | 치명적 삼중고, 26% 스킬 취약점 |
| 8 | Competitive Landscape | OpenClaw vs Claude Code 비교 |
| 9 | Enterprise Implications | 기업 도입 시사점, 권장 사항 |
| 10 | Conclusion | AI 에이전트 시대의 시작, Next Step |

### 9.4 Visual QA 상세 결과

| 평가 항목 | 배점 | 획득 점수 |
|----------|------|----------|
| 시각적 계층 | 25 | 23 |
| 색상 조화 | 20 | 18 |
| 레이아웃 균형 | 20 | 17 |
| 타이포그래피 | 20 | 17 |
| 전문성/완성도 | 15 | 13 |
| **총점** | **100** | **88** |

### 9.5 핵심 인사이트 (AI 프로덕트 리더 관점)

1. **OpenClaw = 선행 지표**: AI 에이전트의 가능성과 위험을 동시에 보여줌
2. **보안 vs 자율성**: 엔터프라이즈 도입의 핵심 과제
3. **2026년**: AI 에이전트 폭발의 해, 5년 내 웹 브라우저 수준 보편화 전망
4. **권장 전략**: "관찰하고 학습"하면서 내부 역량 구축

### 9.6 리서치 출처

- [OpenClaw Official](https://openclaw.ai/)
- [GitHub - openclaw/openclaw](https://github.com/openclaw/openclaw)
- [CNBC: From Clawdbot to OpenClaw](https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html)
- [Wikipedia: OpenClaw](https://en.wikipedia.org/wiki/OpenClaw)
- [Fast Company: OpenClaw Security](https://www.fastcompany.com/91485326/openclaw-is-a-major-leap-forward-for-ai-and-a-cybersecurity-nightmare)

---

## 10. 로드맵

### v2.0 (현재)
- ✅ Research Agent v2 (다층 리서치)
- ✅ Design Skill v2 (Gemini 스타일)
- ✅ Visual QA Agent (시각적 검증)
- ✅ Thumbnail Preview Skill
- ✅ OpenClaw 분석 사례 연구

### v2.1 (계획)
- [ ] A/B Design Agent (버전 비교)
- [ ] Style Transfer Skill (참조 기반 스타일)
- [ ] 사용자 피드백 학습

### v3.0 (미래)
- [ ] 실시간 협업 기능
- [ ] 브랜드 가이드라인 자동 준수
- [ ] 다국어 지원

---

## 11. 참고 자료

### 외부 참조
- [Anthropic Skills - Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
- [Anthropic Skills - PPTX](https://github.com/anthropics/skills/tree/main/skills/pptx)
- [Anthropic Skills - Canvas Design](https://github.com/anthropics/skills/tree/main/skills/canvas-design)
- [Google Gemini Visual Design](https://design.google/library/gemini-ai-visual-design)

### 내부 문서
- [README.md](./README.md) - 프로젝트 개요
- [workflows/ppt_workflow.md](./workflows/ppt_workflow.md) - 상세 워크플로우
- [agents/*.md](./agents/) - 에이전트 정의
- [skills/*/SKILL.md](./skills/) - 스킬 정의
