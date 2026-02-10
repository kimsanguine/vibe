---
name: nanobanana-visual
description: |
  나노바나나 3.0 프로를 사용해 인스타그램 카드뉴스와 유튜브 썸네일을 생성합니다.
  "카드뉴스 만들어줘", "썸네일 생성해줘", "비주얼 콘텐츠 만들어줘" 요청 시 USE PROACTIVELY.
  planner의 brief.md를 참조하여 브랜드 일관성을 유지합니다.
allowed-tools: Read, Write, Bash
---

# 나노바나나 비주얼 마케팅 스킬

나노바나나 3.0 프로 API를 사용하여 마케팅용 비주얼 콘텐츠를 생성합니다.

## 기능

1. **인스타그램 카드뉴스** (5-7장)
2. **유튜브 썸네일** (1280x720px)

## 워크플로우

### 1단계: 브리프 확인

```
outputs/brief.md 파일을 읽고:
- 비주얼 가이드 섹션 확인
- 카드뉴스 핵심 문구 파악
- 썸네일 메인 텍스트 파악
```

### 2단계: 프롬프트 생성

각 비주얼에 맞는 프롬프트를 생성합니다:
- [카드뉴스 프롬프트 템플릿](templates/card-news-prompt.md) 참조
- [썸네일 프롬프트 템플릿](templates/thumbnail-prompt.md) 참조

### 3단계: API 호출

나노바나나 API를 호출하여 이미지를 생성합니다.

```python
# API 호출 예시 (플레이스홀더)
import requests

API_KEY = os.environ.get('NANOBANANA_API_KEY')
API_URL = 'https://api.nanobanana.com/v3/generate'

def generate_image(prompt, style, size):
    response = requests.post(API_URL,
        headers={'Authorization': f'Bearer {API_KEY}'},
        json={
            'prompt': prompt,
            'style': style,
            'size': size
        }
    )
    return response.json()['image_url']
```

### 4단계: 파일 저장

생성된 이미지를 지정된 위치에 저장합니다:
- 카드뉴스: `outputs/visuals/card-news/slide-01.png` ~ `slide-07.png`
- 썸네일: `outputs/visuals/thumbnail.png`

## 카드뉴스 스펙

자세한 가이드: [references/card-news-guide.md](references/card-news-guide.md)

### 기본 구성 (5-7장)

| 슬라이드 | 내용 | 목적 |
|---------|------|------|
| 1 | 제목 + 후킹 | 스크롤 멈추기 |
| 2-6 | 핵심 포인트 | 정보 전달 |
| 마지막 | CTA | 행동 유도 |

### 디자인 원칙

```
✅ 권장:
- 한 슬라이드 = 한 메시지
- 큰 텍스트, 명확한 계층
- 브랜드 컬러 일관성
- 여백 충분히

❌ 피하기:
- 텍스트 과다
- 복잡한 레이아웃
- 읽기 어려운 폰트
```

## 썸네일 스펙

자세한 가이드: [references/thumbnail-guide.md](references/thumbnail-guide.md)

### 기본 사양

- 크기: 1280 x 720px (16:9)
- 파일 형식: PNG
- 최대 용량: 2MB

### 디자인 원칙

```
✅ 권장:
- 제목 텍스트 크게 (화면의 1/3)
- 눈에 띄는 색상 대비
- 얼굴/사람 이미지 효과적
- 감정을 자극하는 표현

❌ 피하기:
- 작은 텍스트
- 복잡한 배경
- 너무 많은 요소
```

## 스타일 가이드

### 브랜드 컬러

```
Primary: #3B82F6 (Blue)
Secondary: #10B981 (Green)
Accent: #F59E0B (Yellow)
Background: #F3F4F6 (Light Gray)
Text: #1F2937 (Dark Gray)
```

### 폰트 가이드

```
제목: Pretendard Bold
본문: Pretendard Regular
강조: Pretendard SemiBold
```

### 톤앤매너

```
- 깔끔하고 현대적
- 전문적이면서 친근함
- 정보 중심, 과장 없음
```

## 출력 구조

```
outputs/visuals/
├── card-news/
│   ├── slide-01.png  (제목)
│   ├── slide-02.png  (포인트 1)
│   ├── slide-03.png  (포인트 2)
│   ├── slide-04.png  (포인트 3)
│   ├── slide-05.png  (포인트 4)
│   ├── slide-06.png  (포인트 5)
│   └── slide-07.png  (CTA)
└── thumbnail.png
```

## API 설정

### 환경 변수

```bash
export NANOBANANA_API_KEY="your-api-key-here"
```

### 설정 파일 (선택)

`~/.nanobanana/config.json`:
```json
{
  "api_key": "your-api-key",
  "default_style": "modern-minimal",
  "output_format": "png"
}
```

## 참고

- 반드시 `outputs/brief.md`를 먼저 읽고 시작하세요
- API 키가 설정되지 않으면 프롬프트만 생성합니다
- 생성된 이미지는 검수 에이전트(reviewer)가 확인합니다
