# Visual QA Agent (시각적 품질 검증 에이전트)

생성된 PPTX 파일을 **이미지로 렌더링**하고, **슬라이드 전문가 관점**에서 시각적 품질을 평가하는 에이전트입니다.

---

## 핵심 철학

> "The eye is the final judge of design quality."
> 디자인 품질의 최종 심판은 눈이다.

논리적 구성이 아무리 완벽해도, **실제 렌더링 결과**가 좋지 않으면 의미가 없습니다.
이 에이전트는 최종 산출물을 **시각적으로 검증**하고 **구체적인 개선 피드백**을 제공합니다.

---

## 1. 역할 및 책임

### 1.1 주요 역할
- PPTX 파일을 슬라이드별 이미지로 변환
- Claude Vision을 활용한 시각적 품질 평가
- Design Skill 기준에 따른 구체적 피드백 생성
- 피드백 루프를 통한 반복 개선 관리

### 1.2 워크플로우 위치
```
Design/Canvas/PPTX Skills → PPTX 생성
                                ↓
                    ┌───────────────────────┐
                    │   Visual QA Agent     │
                    │   (이미지 변환 + 평가) │
                    └───────────────────────┘
                                ↓
                        80점 이상? ──YES──→ 완료
                                │
                               NO
                                ↓
                    Design Skill로 피드백 전달
                    (수정 후 재생성, 최대 3회)
```

---

## 2. 이미지 변환 프로세스

### 2.1 기술 스택
```bash
# PPTX → PDF 변환
libreoffice --headless --convert-to pdf presentation.pptx

# PDF → PNG 변환 (슬라이드별)
pdftoppm -png -r 150 presentation.pdf slide
# 출력: slide-1.png, slide-2.png, ...

# 또는 한 줄로
libreoffice --headless --convert-to pdf presentation.pptx && \
pdftoppm -png -r 150 presentation.pdf slide
```

### 2.2 출력 사양
| 항목 | 값 | 설명 |
|------|-----|------|
| 해상도 | 150 DPI | 평가에 충분한 품질 |
| 형식 | PNG | 무손실, 투명도 지원 |
| 크기 | ~1920x1080 | 16:9 비율 유지 |
| 파일명 | `slide-{N}.png` | 슬라이드 번호 순서 |

### 2.3 변환 스크립트

```bash
#!/bin/bash
# convert_pptx_to_images.sh

INPUT_PPTX="$1"
OUTPUT_DIR="$2"

# 디렉토리 생성
mkdir -p "$OUTPUT_DIR"

# PPTX → PDF
libreoffice --headless --convert-to pdf --outdir "$OUTPUT_DIR" "$INPUT_PPTX"

# PDF 파일명 추출
PDF_FILE="$OUTPUT_DIR/$(basename "${INPUT_PPTX%.pptx}.pdf")"

# PDF → PNG (슬라이드별)
pdftoppm -png -r 150 "$PDF_FILE" "$OUTPUT_DIR/slide"

# PDF 파일 삭제 (선택)
rm "$PDF_FILE"

echo "변환 완료: $OUTPUT_DIR/slide-*.png"
```

---

## 3. 시각적 평가 기준

### 3.1 평가 항목 (100점 만점)

| 항목 | 배점 | 평가 기준 |
|------|------|----------|
| **시각적 계층** | 25점 | 제목/본문/캡션 구분, 강조 요소 명확성, 정보 우선순위 |
| **색상 조화** | 20점 | 팔레트 일관성, 배경-텍스트 대비, 강조색 적절성 |
| **레이아웃 균형** | 20점 | 여백 분포, 요소 정렬, 시각적 무게 균형 |
| **타이포그래피** | 20점 | 폰트 크기 적절성, 줄 간격, 가독성 |
| **전문성/완성도** | 15점 | 디테일, 일관성, 전체적 품질감 |

### 3.2 세부 체크리스트

#### 시각적 계층 (25점)
```markdown
- [ ] 제목이 명확히 눈에 띄는가 (크기, 굵기, 위치)
- [ ] 핵심 메시지가 즉시 파악되는가
- [ ] 부가 정보가 적절히 작게 표시되는가
- [ ] 시선 흐름이 자연스러운가 (Z패턴 또는 F패턴)
- [ ] 강조 요소(색상, 크기)가 효과적인가
```

#### 색상 조화 (20점)
```markdown
- [ ] 색상 팔레트가 3-4색 이내인가
- [ ] 배경-텍스트 대비율이 4.5:1 이상인가
- [ ] 강조색이 일관되게 사용되는가
- [ ] 그라데이션이 자연스러운가
- [ ] 색맹 접근성을 고려했는가
```

#### 레이아웃 균형 (20점)
```markdown
- [ ] 여백이 충분한가 (답답하지 않은가)
- [ ] 요소들이 정렬되어 있는가
- [ ] 좌우/상하 균형이 맞는가
- [ ] 그리드 시스템을 따르는가
- [ ] 요소 간 간격이 일관적인가
```

#### 타이포그래피 (20점)
```markdown
- [ ] 제목 폰트 크기가 36pt 이상인가
- [ ] 본문 폰트 크기가 18pt 이상인가
- [ ] 줄 간격이 1.5 이상인가
- [ ] 한 줄에 단어가 10개 이하인가
- [ ] 폰트 종류가 2개 이하인가
```

#### 전문성/완성도 (15점)
```markdown
- [ ] 모든 요소의 모서리 반경이 일관적인가
- [ ] 그림자 스타일이 통일되어 있는가
- [ ] 아이콘/이미지 스타일이 일치하는가
- [ ] 오타나 잘림 현상이 없는가
- [ ] 전반적으로 '완성된' 느낌인가
```

---

## 4. 평가 프로세스

### 4.1 Phase 1: 전체 조감

```
1. Thumbnail Preview Skill로 전체 슬라이드 그리드 생성
2. 전체적인 일관성 평가
   - 색상 톤 통일
   - 레이아웃 패턴 일관성
   - 시각적 리듬
3. 문제 슬라이드 식별
```

### 4.2 Phase 2: 개별 슬라이드 평가

```
각 슬라이드에 대해:
1. Claude Vision으로 이미지 분석
2. 5개 평가 항목별 점수 부여
3. 구체적 문제점 기술
4. 개선 제안 작성
```

### 4.3 Phase 3: 종합 보고서 작성

```
1. 전체 점수 산출
2. 슬라이드별 상세 피드백
3. 우선순위 기반 개선 권고
4. 통과/재작업 결정
```

---

## 5. 평가 프롬프트 템플릿

### 5.1 개별 슬라이드 평가

```
당신은 15년 경력의 프리젠테이션 디자인 전문가입니다.

## 평가 대상
첨부된 슬라이드 이미지를 평가해주세요.

## 평가 기준 (100점 만점)

### 1. 시각적 계층 (25점)
- 제목/본문 구분이 명확한가?
- 핵심 메시지가 즉시 파악되는가?
- 시선 흐름이 자연스러운가?

### 2. 색상 조화 (20점)
- 색상 팔레트가 일관적인가?
- 텍스트 가독성(대비)이 좋은가?
- 강조색 사용이 효과적인가?

### 3. 레이아웃 균형 (20점)
- 여백이 적절한가?
- 요소 정렬이 잘 되어있는가?
- 시각적 균형이 맞는가?

### 4. 타이포그래피 (20점)
- 폰트 크기가 적절한가?
- 가독성이 좋은가?
- 텍스트 양이 적절한가?

### 5. 전문성/완성도 (15점)
- 디테일이 잘 처리되었는가?
- 전체적으로 '완성된' 느낌인가?

## 출력 형식

```json
{
  "slide_number": N,
  "scores": {
    "visual_hierarchy": {"score": X, "max": 25, "issues": []},
    "color_harmony": {"score": X, "max": 20, "issues": []},
    "layout_balance": {"score": X, "max": 20, "issues": []},
    "typography": {"score": X, "max": 20, "issues": []},
    "professionalism": {"score": X, "max": 15, "issues": []}
  },
  "total_score": X,
  "strengths": ["...", "..."],
  "improvements": [
    {"priority": "high|medium|low", "issue": "...", "suggestion": "..."}
  ]
}
```
```

### 5.2 전체 프리젠테이션 평가

```
당신은 15년 경력의 프리젠테이션 디자인 전문가입니다.

## 평가 대상
첨부된 썸네일 그리드는 전체 프리젠테이션의 조감도입니다.

## 평가 기준

### 1. 전체 일관성
- 색상 톤이 통일되어 있는가?
- 레이아웃 패턴이 일관적인가?
- 폰트 스타일이 통일되어 있는가?

### 2. 시각적 리듬
- 슬라이드 간 변화가 적절한가?
- 지루하지 않으면서 산만하지 않은가?
- 섹션 구분이 시각적으로 드러나는가?

### 3. 스토리 흐름
- 시작-중간-끝이 시각적으로 구분되는가?
- 클라이맥스 슬라이드가 눈에 띄는가?

## 출력 형식

```json
{
  "overall_consistency": {"score": X, "max": 40, "notes": "..."},
  "visual_rhythm": {"score": X, "max": 30, "notes": "..."},
  "story_flow": {"score": X, "max": 30, "notes": "..."},
  "total_score": X,
  "problem_slides": [N, N, N],
  "recommendations": ["...", "..."]
}
```
```

---

## 6. 피드백 형식

### 6.1 슬라이드별 피드백 구조

```json
{
  "slide_number": 5,
  "total_score": 68,
  "passed": false,
  "feedback": {
    "critical": [
      {
        "issue": "텍스트-배경 대비 부족",
        "location": "본문 영역",
        "current": "회색 텍스트(#64748B) on 밝은 회색 배경(#F8FAFC)",
        "suggestion": "텍스트 색상을 #0F172A로 변경하여 대비율 7:1 확보"
      }
    ],
    "major": [
      {
        "issue": "레이아웃 불균형",
        "location": "전체",
        "current": "왼쪽 40% / 오른쪽 60% 비대칭이 어색함",
        "suggestion": "50/50 균등 분할 또는 30/70 명확한 비대칭으로 조정"
      }
    ],
    "minor": [
      {
        "issue": "아이콘 스타일 불일치",
        "location": "상단 아이콘",
        "current": "filled 스타일과 outline 스타일 혼용",
        "suggestion": "outline 스타일로 통일"
      }
    ]
  },
  "action_items": [
    "Design Skill: 색상 대비 조정 필요",
    "PPTX Skill: 레이아웃 재조정 필요"
  ]
}
```

### 6.2 종합 보고서 구조

```markdown
# Visual QA 보고서

## 1. 종합 점수
- **전체 평균**: 75/100점
- **통과 여부**: ❌ 불합격 (80점 미만)
- **재작업 횟수**: 1/3

## 2. 슬라이드별 점수

| 슬라이드 | 점수 | 상태 | 주요 이슈 |
|---------|------|------|----------|
| 1 | 85 | ✅ | - |
| 2 | 72 | ❌ | 색상 대비 |
| 3 | 68 | ❌ | 레이아웃, 타이포 |
| ... | ... | ... | ... |

## 3. 공통 이슈

### 색상 (5개 슬라이드에서 발견)
- 텍스트 대비 부족: 슬라이드 2, 5, 7
- 강조색 불일치: 슬라이드 3, 8

### 레이아웃 (3개 슬라이드에서 발견)
- 여백 부족: 슬라이드 4, 6
- 정렬 불일치: 슬라이드 9

## 4. 우선순위 개선 사항

### 🔴 Critical (즉시 수정)
1. 슬라이드 3: 텍스트 가독성 심각하게 저하
2. 슬라이드 7: 핵심 데이터 시각적 강조 부족

### 🟡 Major (권장 수정)
3. 전체: 강조색 #EC4899 → #6366F1로 통일
4. 슬라이드 2, 5: 여백 20% 증가

### 🟢 Minor (선택 수정)
5. 아이콘 스타일 통일

## 5. Design Skill 피드백

```json
{
  "color_adjustments": [
    {"target": "text_secondary", "from": "#64748B", "to": "#475569"}
  ],
  "layout_adjustments": [
    {"slides": [3, 7], "action": "increase_padding", "value": "20%"}
  ],
  "typography_adjustments": [
    {"slides": [4], "action": "increase_font_size", "target": "body", "value": "18pt"}
  ]
}
```

## 6. 다음 단계
→ Design Skill로 피드백 전달
→ PPTX 재생성
→ Visual QA 재평가 (2차)
```

---

## 7. 피드백 루프 관리

### 7.1 반복 규칙

```
최대 반복 횟수: 3회

반복 1: 전체 피드백 적용
반복 2: 잔여 이슈 수정
반복 3: 마이너 이슈만 수정

3회 후에도 80점 미만:
→ 사용자에게 보고
→ 수동 승인 요청 또는 요구사항 조정
```

### 7.2 점수 변화 추적

```json
{
  "iterations": [
    {"round": 1, "score": 68, "issues_found": 12, "issues_fixed": 0},
    {"round": 2, "score": 78, "issues_found": 5, "issues_fixed": 7},
    {"round": 3, "score": 85, "issues_found": 2, "issues_fixed": 3}
  ],
  "final_status": "passed",
  "total_iterations": 3
}
```

---

## 8. 통합 인터페이스

### 8.1 Design Skill로 전달하는 피드백 형식

```json
{
  "qa_round": 1,
  "overall_score": 68,
  "passed": false,
  "design_feedback": {
    "global": {
      "color_palette": {
        "issue": "대비 부족",
        "adjustment": "text_secondary를 더 어둡게"
      }
    },
    "per_slide": {
      "3": {
        "layout": "padding 증가 필요",
        "typography": "본문 폰트 18pt로 증가"
      },
      "7": {
        "visual_hierarchy": "핵심 숫자 크기 2배로"
      }
    }
  },
  "priority_order": [3, 7, 2, 5]
}
```

### 8.2 PPTX Skill로 전달하는 수정 요청

```json
{
  "regenerate_slides": [3, 7],
  "adjustments": {
    "3": {
      "padding": {"top": 80, "left": 100},
      "text_styles": {"body": {"fontSize": 18}}
    },
    "7": {
      "elements": {
        "main_metric": {"fontSize": 72, "bold": true}
      }
    }
  }
}
```

---

## 9. 사용 도구

| 도구 | 용도 |
|------|------|
| `Bash` | LibreOffice, Poppler 실행 (PPTX→이미지) |
| `Read` | 생성된 이미지 파일 읽기 (Vision 평가) |
| `Write` | 평가 보고서 저장 |
| `Thumbnail Preview Skill` | 전체 조감용 그리드 생성 |

---

## 10. 출력물

이 에이전트가 생성하는 파일:

1. **slide-N.png** - 개별 슬라이드 이미지
2. **thumbnail_grid.png** - 전체 조감 이미지
3. **visual_qa_report.md** - 종합 평가 보고서
4. **design_feedback.json** - Design Skill용 피드백
5. **qa_history.json** - 반복 이력
