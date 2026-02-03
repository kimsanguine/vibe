# 콘텐츠 마케팅 팀 자동화 시스템

YouTube 자막, 웹문서 본문, 또는 텍스트 콘텐츠를 제공하면 자동으로 멀티 플랫폼 마케팅 콘텐츠가 생성되는 시스템입니다.

## 빠른 시작

### 방법 1: YouTube 자막 첨부

```
"마케팅 콘텐츠 만들어줘"

영상 제목: [제목]
채널: [채널명]

자막:
[YouTube 자막을 복사해서 붙여넣기]
```

### 방법 2: 웹문서 본문 첨부

```
"마케팅 콘텐츠 만들어줘"

제목: [문서 제목]
출처: [URL]

본문:
[웹문서 내용을 복사해서 붙여넣기]
```

### 방법 3: 접근 가능한 URL 제공

```
"https://example.com/article 이 글로 마케팅 콘텐츠 만들어줘"
```

### 방법 4: 핵심 내용 요약 제공

```
"마케팅 콘텐츠 만들어줘"

주제: AI 자동화 도구 리뷰

핵심 포인트:
1. 하루 3시간 절약 가능
2. 초보자도 10분 만에 설정
3. 무료 플랜으로 시작 가능
```

## 시스템 구조

```
.claude/
├── agents/                    # 에이전트 (서브에이전트)
│   ├── planner.md             # 기획 에이전트
│   ├── reviewer.md            # 검수 에이전트
│   ├── newsletter-writer.md   # 뉴스레터 작성
│   ├── blog-writer.md         # 블로그 작성
│   ├── shorts-scriptwriter.md # 쇼츠 대본 작성
│   ├── thread-writer.md       # X 스레드 작성
│   ├── linkedin-writer.md     # 링크드인 작성
│   └── youtube-scriptwriter.md # 유튜브 대본 작성
│
└── skills/                    # 스킬
    ├── nanobanana-visual/     # 비주얼 마케팅
    │   ├── SKILL.md
    │   ├── references/
    │   └── templates/
    │
    └── shorts-video-maker/    # 영상 제작
        ├── SKILL.md
        ├── scripts/
        └── references/
```

## 워크플로우

```
[콘텐츠 입력]
(자막/본문/URL/요약)
    │
    ▼
┌─────────────────────────────────────┐
│ 1. planner (기획 에이전트)           │
│    - 콘텐츠 분석                     │
│    - 핵심 메시지 추출                │
│    - 브리프 작성                     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 2. 병렬 콘텐츠 생성                  │
│                                     │
│   [텍스트 팀]        [비주얼 팀]     │
│   - 뉴스레터         - 카드뉴스     │
│   - 블로그           - 썸네일       │
│   - 쇼츠 대본                       │
│   - 스레드           [영상 팀]      │
│   - 링크드인         - 쇼츠 클립    │
│   - 유튜브 대본                     │
└─────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────┐
│ 3. reviewer (검수 에이전트)          │
│    - 품질 검수                      │
│    - 톤앤매너 확인                   │
│    - 팩트 체크                      │
└─────────────────────────────────────┘
    │
    ▼
[outputs/ 폴더에 최종 결과물]
```

## 입력 방식 상세

### YouTube 자막 가져오는 방법

1. YouTube 영상 페이지에서 `...` 클릭
2. `스크립트 열기` 또는 `Open transcript` 클릭
3. 전체 선택 후 복사

또는 자막 다운로드 사이트 사용:
- downsub.com
- savesubs.com

### 웹문서 본문 가져오는 방법

1. 웹페이지에서 본문 영역 선택
2. 복사하여 붙여넣기

또는 Reader Mode 사용:
- Safari: `Cmd + Shift + R`
- Chrome: 주소창 옆 아이콘

## 에이전트 사용법

### 개별 에이전트 호출

```bash
# 기획 (브리프 작성)
"브리프 작성해줘"

# 뉴스레터
"뉴스레터 작성해줘"

# 블로그
"블로그 글 만들어줘"

# 쇼츠 대본
"쇼츠 대본 작성해줘"

# X 스레드
"스레드 작성해줘"

# 링크드인
"링크드인 포스트 만들어줘"

# 유튜브 대본
"유튜브 대본 작성해줘"

# 검수
"콘텐츠 검수해줘"
```

### 스킬 사용

```bash
# 카드뉴스
"카드뉴스 만들어줘"

# 썸네일
"썸네일 생성해줘"

# 쇼츠 영상
"쇼츠 영상 만들어줘"
```

## 출력 구조

```
outputs/
├── brief.md                # 브리프 (planner)
├── newsletter.md           # 뉴스레터
├── blog.md                 # 블로그
├── linkedin.md             # 링크드인
├── youtube-script.md       # 유튜브 대본
├── threads/
│   └── thread-01~10.md     # X 스레드
├── shorts-scripts/
│   └── shorts-01~03.md     # 쇼츠 대본
├── visuals/
│   ├── card-news/
│   │   └── slide-01~07.png # 카드뉴스
│   └── thumbnail.png       # 썸네일
├── shorts-videos/
│   └── shorts-01~03.mp4    # 쇼츠 영상
└── review-report.md        # 검수 리포트
```

## 필수 요구사항

### 영상 제작 스킬 사용 시

```bash
# Python 패키지
pip install yt-dlp
pip install openai-whisper

# 시스템 패키지
# macOS
brew install ffmpeg

# Ubuntu
apt install ffmpeg
```

### 비주얼 마케팅 스킬 사용 시

```bash
# 환경 변수 설정
export NANOBANANA_API_KEY="your-api-key"
```

## 톤앤매너 가이드

모든 텍스트 콘텐츠는 다음 원칙을 따릅니다:

### 타겟 오디언스
- 1인 창업가 (솔로프리너)
- IT/AI 관심자
- 자동화/생산성 관심자

### 작성 원칙
- 친근하고 실용적인 톤
- "요"체 사용 (예: "~해요")
- 중학생도 이해할 수 있는 쉬운 말

### 금지 표현
- ❌ "혁신적인", "획기적인", "놀라운"
- ❌ "반드시", "매우 중요한"
- ❌ "~의 세계", "~의 여정"
- ✅ 구체적 수치, 실제 사례 사용

## 문제 해결

### YouTube URL에서 자동 추출이 안 될 때
→ 자막을 직접 복사해서 붙여넣기

### 에이전트가 자동으로 호출되지 않을 때
- description에 "USE PROACTIVELY" 또는 "MUST BE USED" 포함 확인
- Claude Code 재시작

### 스킬이 동작하지 않을 때
- 필수 패키지 설치 확인 (yt-dlp, whisper, ffmpeg)
- API 키 설정 확인

### 브리프를 찾을 수 없다고 할 때
- `outputs/brief.md` 파일 존재 확인
- planner 에이전트 먼저 실행

## 커스터마이징

### 에이전트 수정
`.claude/agents/` 폴더의 마크다운 파일을 직접 편집

### 스킬 수정
`.claude/skills/` 폴더의 SKILL.md 및 관련 파일 편집

### 새 에이전트 추가
1. `.claude/agents/` 에 새 마크다운 파일 생성
2. YAML 프론트매터에 name, description, tools, model 설정
3. 시스템 프롬프트 작성
