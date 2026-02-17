# Design Skill (프리젠테이션 디자인 스킬) v2.0

Gemini 스타일과 모던 프론트엔드 디자인 원칙을 결합한 세련된 프리젠테이션 디자인 시스템입니다.

## 핵심 철학

> "Energy flows through gradients, meaning crystallizes in simplicity"
> 에너지는 그라데이션을 통해 흐르고, 의미는 단순함 속에서 결정화된다.

프리젠테이션은 **시각적 에너지**를 전달하는 매체입니다. 정보를 전달하는 것이 아니라, 청중의 감정과 이성을 동시에 움직이는 경험을 설계합니다.

---

## 1. 디자인 원칙

### 1.1 Gradient-First Design (그라데이션 우선)

Gemini 디자인 철학의 핵심: 그라데이션은 **에너지와 방향성**을 전달합니다.

```
그라데이션 규칙:
├── 날카로운 시작점 → 부드러운 확산
├── 방향성으로 시선 유도
├── 감정적 톤 설정 (따뜻함, 차가움, 역동성)
└── 배경보다 '분위기'로 활용
```

**그라데이션 유형:**

| 유형 | 용도 | 예시 |
|------|------|------|
| Linear | 방향성, 진행감 | 타이틀, 섹션 구분 |
| Radial | 집중, 강조 | 데이터 포인트, CTA |
| Conic | 순환, 완성 | 프로세스, 사이클 |
| Mesh | 복잡한 감정 | 배경, 오버레이 |

### 1.2 Circular Form Language (원형 형태 언어)

원은 **단순함, 조화, 편안함**을 전달합니다.

```css
/* 모든 요소에 일관된 둥근 모서리 */
--radius-sm: 8px;    /* 버튼, 태그 */
--radius-md: 16px;   /* 카드, 컨테이너 */
--radius-lg: 24px;   /* 섹션, 모달 */
--radius-full: 50%;  /* 아이콘, 아바타 */
```

### 1.3 Warm Spatial Quality (따뜻한 공간감)

> "Optimistic, delightful, playful, yet sophisticated"
> — Google Design Team

- **넉넉한 여백**: 요소 간 숨 쉴 공간
- **레이어링**: 부드러운 그림자로 깊이감
- **부유하는 요소**: 배경과 분리된 카드

---

## 2. 색상 시스템

### 2.1 Gemini-Inspired Palette

```css
/* Primary Gradient - Google Colors */
--gradient-gemini: linear-gradient(
  135deg,
  #4285F4 0%,    /* Google Blue */
  #9B72CB 25%,   /* Purple */
  #D96570 50%,   /* Red-Pink */
  #F9AB00 75%,  /* Yellow */
  #0F9D58 100%   /* Green */
);

/* Simplified for Presentation */
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--gradient-warm: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--gradient-cool: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
--gradient-sunset: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
--gradient-ocean: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
```

### 2.2 Professional Palettes

#### Palette A: Modern Clarity
```css
--surface: #FFFFFF;
--surface-elevated: #F8FAFC;
--text-primary: #0F172A;
--text-secondary: #64748B;
--accent-primary: #6366F1;    /* Indigo */
--accent-secondary: #EC4899;  /* Pink */
--border: rgba(0, 0, 0, 0.06);
```

#### Palette B: Dark Sophistication
```css
--surface: #0F0F14;
--surface-elevated: #1A1A24;
--text-primary: #FFFFFF;
--text-secondary: #A1A1AA;
--accent-primary: #A78BFA;    /* Violet */
--accent-secondary: #22D3EE;  /* Cyan */
--border: rgba(255, 255, 255, 0.08);
```

#### Palette C: Warm Professional
```css
--surface: #FFFBF5;
--surface-elevated: #FFFFFF;
--text-primary: #1C1917;
--text-secondary: #78716C;
--accent-primary: #EA580C;    /* Orange */
--accent-secondary: #0891B2;  /* Teal */
--border: rgba(0, 0, 0, 0.04);
```

---

## 3. 타이포그래피

### 3.1 폰트 선택 원칙

```
❌ AVOID (절대 사용 금지)
├── Arial, Helvetica (너무 평범)
├── Inter (AI 미학의 클리셰)
├── Space Grotesk (과도하게 사용됨)
└── Roboto (Google 기본값 느낌)

✅ EMBRACE (권장)
├── 개성 있는 디스플레이 폰트
├── 특색 있는 세리프
└── 브랜드 연관 폰트
```

### 3.2 추천 폰트 페어링

#### Pairing 1: Elegant Authority
```
Display: Fraunces (Variable, Serif)
Body: Plus Jakarta Sans
특징: 권위 있으면서도 친근함
```

#### Pairing 2: Modern Edge
```
Display: Syne (Sans-serif, Bold)
Body: Satoshi
특징: 현대적이고 날카로움
```

#### Pairing 3: Refined Classic
```
Display: Libre Baskerville
Body: DM Sans
특징: 클래식하지만 세련됨
```

#### Pairing 4: Tech Forward (한글 지원)
```
Display: Pretendard (Black)
Body: Pretendard (Regular)
특징: 한글 완벽 지원, 현대적
```

### 3.3 Type Scale

```
--text-hero: clamp(48px, 8vw, 96px);     /* 히어로 타이틀 */
--text-display: clamp(36px, 5vw, 64px);  /* 슬라이드 제목 */
--text-heading: clamp(24px, 3vw, 36px);  /* 섹션 제목 */
--text-body: clamp(18px, 2vw, 24px);     /* 본문 */
--text-caption: clamp(12px, 1.5vw, 16px); /* 캡션 */
```

---

## 4. 레이아웃 시스템

### 4.1 Grid System

```
16:9 Slide (1920x1080)
├── Margin: 80px (좌우), 60px (상하)
├── Gutter: 32px
├── Columns: 12
└── Safe Zone: 1760 x 960
```

### 4.2 레이아웃 패턴

#### Pattern A: Hero Statement
```
┌────────────────────────────────────┐
│                                    │
│     ╔════════════════════════╗     │
│     ║   ONE POWERFUL         ║     │
│     ║   STATEMENT HERE       ║     │
│     ╚════════════════════════╝     │
│                                    │
│              ○ ○ ○                 │
└────────────────────────────────────┘
중앙 집중, 최대 임팩트
```

#### Pattern B: Asymmetric Split (60/40)
```
┌────────────────────────────────────┐
│ ┌─────────────────┐  ┌──────────┐  │
│ │                 │  │ ▪ Point  │  │
│ │   BIG VISUAL    │  │ ▪ Point  │  │
│ │   OR METRIC     │  │ ▪ Point  │  │
│ │                 │  │          │  │
│ └─────────────────┘  └──────────┘  │
└────────────────────────────────────┘
시각 자료 강조 + 핵심 포인트
```

#### Pattern C: Card Grid
```
┌────────────────────────────────────┐
│  Title                             │
│  ┌────────┐ ┌────────┐ ┌────────┐  │
│  │ ╭────╮ │ │ ╭────╮ │ │ ╭────╮ │  │
│  │ │ 01 │ │ │ │ 02 │ │ │ │ 03 │ │  │
│  │ ╰────╯ │ │ ╰────╯ │ │ ╰────╯ │  │
│  │  Text  │ │  Text  │ │  Text  │  │
│  └────────┘ └────────┘ └────────┘  │
└────────────────────────────────────┘
둥근 카드, 부유하는 느낌
```

#### Pattern D: Data Focus
```
┌────────────────────────────────────┐
│  Context Label                     │
│  ┌─────────────────────────────┐   │
│  │         ╭───────╮           │   │
│  │         │ 87%   │           │   │
│  │         ╰───────╯           │   │
│  │    ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬       │   │
│  └─────────────────────────────┘   │
│  Source: Citation                  │
└────────────────────────────────────┘
데이터가 주인공
```

---

## 5. 시각적 요소

### 5.1 그림자 시스템

```css
/* Layered Shadow - 부드러운 깊이감 */
--shadow-sm:
  0 1px 2px rgba(0,0,0,0.04),
  0 2px 4px rgba(0,0,0,0.04);

--shadow-md:
  0 4px 6px rgba(0,0,0,0.04),
  0 10px 15px rgba(0,0,0,0.06);

--shadow-lg:
  0 10px 25px rgba(0,0,0,0.06),
  0 20px 48px rgba(0,0,0,0.08);

/* Colored Glow - 그라데이션과 어울리는 글로우 */
--glow-primary: 0 0 40px rgba(99, 102, 241, 0.3);
--glow-accent: 0 0 40px rgba(236, 72, 153, 0.3);
```

### 5.2 아이콘 스타일

```
권장 스타일:
├── Phosphor Icons (Duotone)
├── Lucide Icons (Stroke)
├── Heroicons (Outline)
└── Custom geometric shapes

아이콘 크기:
├── Inline: 20-24px
├── Card: 32-48px
├── Hero: 64-96px
└── Decorative: 128px+
```

### 5.3 이미지 처리

```css
/* 이미지 오버레이 */
.image-overlay {
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(0,0,0,0.7) 100%
  );
}

/* 이미지 마스킹 */
.image-masked {
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
}

/* 소프트 블러 배경 */
.image-bg-blur {
  filter: blur(60px);
  opacity: 0.6;
}
```

---

## 6. 슬라이드 타입별 템플릿

### 6.1 타이틀 슬라이드

```
배경: Gradient mesh 또는 단색 + 글로우
제목: Hero 사이즈, 중앙 또는 좌하단
부제: Secondary 색상, 30% 작게
로고/날짜: 모서리에 작게
```

### 6.2 어젠다 슬라이드

```
배경: 밝은 단색
제목: 좌상단
항목: 번호 + 텍스트, 수직 배열
강조: 그라데이션 번호 또는 아이콘
```

### 6.3 데이터 슬라이드

```
배경: 밝은 단색
숫자: 초대형, 그라데이션 또는 액센트
라벨: 숫자 아래, 설명적
출처: 하단, 작게
```

### 6.4 비교 슬라이드

```
배경: 두 영역으로 분할 (색상 대비)
왼쪽: Before / 문제 / A안
오른쪽: After / 해결 / B안
중앙: 구분선 또는 VS
```

### 6.5 인용구 슬라이드

```
배경: 단색 또는 그라데이션
인용구: 중앙, 대형 따옴표
출처: 하단 우측, 작게
```

### 6.6 Thank You 슬라이드

```
배경: Gradient (Brand colors)
제목: "Thank You" 또는 CTA
연락처: 하단 중앙
로고: 중앙 또는 하단
```

---

## 7. 애니메이션

### 7.1 권장 전환

```css
/* Fade + Rise */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Staggered Reveal */
.item:nth-child(1) { animation-delay: 0ms; }
.item:nth-child(2) { animation-delay: 100ms; }
.item:nth-child(3) { animation-delay: 200ms; }

/* Timing */
--ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
--duration-fast: 200ms;
--duration-normal: 400ms;
--duration-slow: 600ms;
```

### 7.2 마이크로 인터랙션

```
버튼 호버: Scale 1.02 + Shadow 증가
카드 호버: Y -4px + Shadow 증가
링크 호버: 밑줄 애니메이션
숫자: 카운트업 애니메이션
```

---

## 8. 디자인 QA 체크리스트

```markdown
## 시각적 일관성
- [ ] 색상 팔레트 3-4색 이내
- [ ] 폰트 2종 이내
- [ ] 일관된 모서리 반경
- [ ] 일관된 그림자 사용
- [ ] 일관된 여백 시스템

## 가독성
- [ ] 최소 대비율 4.5:1
- [ ] 본문 18px 이상
- [ ] 줄 간격 1.5 이상
- [ ] 한 슬라이드 50단어 이하

## 전문성
- [ ] 그라데이션 자연스러움
- [ ] 정렬 완벽함
- [ ] 요소 간 관계 명확
- [ ] 불필요한 장식 없음

## 브랜드
- [ ] 로고 배치 일관성
- [ ] 톤앤매너 통일
- [ ] 청중에 적합한 스타일
```

---

## 9. 출력물

이 스킬로 생성되는 파일:

1. **design-system.json** - 색상, 폰트, 스페이싱 토큰
2. **slide-templates.html** - 슬라이드 타입별 HTML 템플릿
3. **style-guide.md** - 디자인 결정 근거 문서

---

## 참고 자료

- [Google Gemini Visual Design](https://design.google/library/gemini-ai-visual-design)
- [Anthropic Frontend Design Skill](https://github.com/anthropics/skills/tree/main/skills/frontend-design)
