# PPT Agent Team

Claude의 Sub-agent 기능과 Skill을 활용한 프리젠테이션 자동 제작 시스템입니다.

## 개요

이 프로젝트는 AI 에이전트 팀이 협업하여 고품질 PowerPoint 프리젠테이션을 자동으로 생성합니다.

```
📊 PPT Agent Team
├── 🔍 Research Agent      - 자료 조사
├── 📝 Content Organizer   - 콘텐츠 구성
├── ✅ Slide Evaluator     - 품질 평가
├── 🎨 Design Skill        - 시각 디자인
├── 📦 PPTX Skill          - PPT 생성
└── 🖼️ Canvas-Design Skill - 그래픽 제작
```

## 프로젝트 구조

```
ppt-agent-team/
├── agents/                          # 에이전트 정의
│   ├── research_agent.md            # 리서치 에이전트
│   ├── content_organizer_agent.md   # 자료 정리 에이전트
│   └── slide_evaluator_agent.md     # 슬라이드 평가 에이전트
│
├── skills/                          # 스킬 정의
│   ├── design/
│   │   └── SKILL.md                 # 디자인 스킬
│   ├── pptx/
│   │   ├── SKILL.md                 # PPTX 스킬
│   │   ├── html2pptx.md             # HTML→PPTX 변환 가이드
│   │   └── ooxml.md                 # OOXML 기술 참조
│   └── canvas-design/
│       └── SKILL.md                 # 캔버스 디자인 스킬
│
├── workflows/
│   └── ppt_workflow.md              # 전체 워크플로우
│
└── README.md                        # 이 파일
```

## 에이전트 (Agents)

### 1. Research Agent (리서치 에이전트)

웹에서 프리젠테이션에 필요한 모든 자료를 조사합니다.

**핵심 기능:**
- 주제 관련 최신 정보 검색
- 통계 및 데이터 수집
- 신뢰도 검증 및 출처 정리

**사용 도구:** `WebSearch`, `WebFetch`, `Read`

### 2. Content Organizer Agent (자료 정리 에이전트)

수집된 자료를 프리젠테이션에 적합한 형태로 구조화합니다.

**핵심 기능:**
- 스토리라인 설계
- 슬라이드 구성 최적화
- 시각화 계획 수립

**협업:** Research Agent와 협력하여 추가 자료 요청

### 3. Slide Evaluator Agent (슬라이드 평가 에이전트)

완성된 구성을 평가하고 개선점을 제안합니다.

**평가 기준 (100점 만점):**
| 항목 | 배점 |
|------|------|
| 구조적 완성도 | 25점 |
| 메시지 전달력 | 25점 |
| 시각적 일관성 | 25점 |
| 설득력 | 25점 |

**통과 기준:** 80점 이상

## 스킬 (Skills)

### 1. Design Skill (디자인 스킬)

프론트엔드 디자인 원칙 기반의 프리젠테이션 디자인입니다.

**제공 기능:**
- 대담한 시각적 방향 설정
- 색상 팔레트 가이드 (17종)
- 폰트 페어링 추천
- 레이아웃 패턴

**참조:** [Anthropic Skills - Frontend Design](https://github.com/anthropics/skills/tree/main/skills/frontend-design)

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
- 다이어그램 (조직도, 플로우차트, 타임라인)

**출력 형식:** PNG, PDF, SVG

**참조:** [Anthropic Skills - Canvas Design](https://github.com/anthropics/skills/tree/main/skills/canvas-design)

## 워크플로우

### 전체 프로세스

```
1. 사용자 요청
       ↓
2. Research Agent: 자료 조사
       ↓
3. Content Organizer: 슬라이드 구성
       ↓
4. Slide Evaluator: 평가 및 승인
       ↓ (80점 이상 통과)
5. Design Skill: 디자인 가이드 생성
       ↓
6. Canvas-Design: 시각 자료 생성
       ↓
7. PPTX Skill: 최종 파일 생성
       ↓
8. 완성된 PPTX 출력
```

### 평가 실패 시 반복

평가 점수가 80점 미만인 경우:
1. Slide Evaluator가 구체적 피드백 제공
2. Content Organizer가 수정 작업
3. 재평가 수행
4. 3회 실패 시 사용자에게 보고

## 사용 예시

### 기본 요청

```
"AI 트렌드에 대한 15분 프리젠테이션을 만들어줘.
 청중은 기업 임원들이고, 투자 결정에 참고할 내용으로 구성해줘."
```

### 출력물

1. `presentation.pptx` - 최종 PowerPoint 파일
2. `assets/` - 사용된 시각 자료
3. `speaker_notes.md` - 발표자 노트
4. `sources.md` - 참고 자료 목록

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
    "LibreOffice",
    "Poppler"
  ]
}
```

### 권장 환경

- Node.js 18+
- Python 3.8+
- Claude API 접근

## 참고 자료

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [PptxGenJS Documentation](https://gitbrent.github.io/PptxGenJS/)
- [Office Open XML Reference](https://docs.microsoft.com/en-us/office/open-xml/open-xml-sdk)

## 라이선스

이 프로젝트는 Anthropic Skills의 라이선스를 따릅니다.
