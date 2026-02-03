"""
LLM 클라이언트 구현
- ClaudeClient: Anthropic Claude API
- GeminiClient: Google Gemini API (Phase 2)
"""

import json
from abc import ABC, abstractmethod
from typing import Optional, Any
from dataclasses import dataclass

from ..config import LLMConfig, ClaudeConfig, GeminiConfig


@dataclass
class LLMResponse:
    """LLM 응답"""
    content: str
    model: str
    usage: Optional[dict] = None
    raw_response: Optional[Any] = None


class BaseLLMClient(ABC):
    """LLM 클라이언트 베이스 클래스"""

    def __init__(self, config: LLMConfig):
        self.config = config
        self._client = None

    @abstractmethod
    def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        """텍스트 생성"""
        pass

    @abstractmethod
    def generate_json(self, prompt: str, system: Optional[str] = None) -> dict:
        """JSON 형식으로 생성"""
        pass


class ClaudeClient(BaseLLMClient):
    """Claude API 클라이언트"""

    def __init__(self, config: Optional[ClaudeConfig] = None):
        super().__init__(config or ClaudeConfig())
        self._init_client()

    def _init_client(self):
        """Anthropic 클라이언트 초기화"""
        try:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.config.api_key)
        except ImportError:
            raise ImportError("anthropic 패키지가 필요합니다: pip install anthropic")

    def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        """텍스트 생성"""
        messages = [{"role": "user", "content": prompt}]

        kwargs = {
            "model": self.config.model,
            "max_tokens": self.config.max_tokens,
            "messages": messages,
        }

        if system:
            kwargs["system"] = system

        response = self._client.messages.create(**kwargs)

        return LLMResponse(
            content=response.content[0].text,
            model=response.model,
            usage={
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            },
            raw_response=response
        )

    def generate_json(self, prompt: str, system: Optional[str] = None) -> dict:
        """JSON 형식으로 생성"""
        json_system = (system or "") + "\n\nIMPORTANT: 반드시 유효한 JSON만 출력하세요. 다른 텍스트 없이 JSON만 출력하세요."

        response = self.generate(prompt, json_system)
        content = response.content.strip()

        # JSON 블록 추출
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 실패: {e}\n응답: {content}")


class GeminiClient(BaseLLMClient):
    """Gemini API 클라이언트 (Phase 2)"""

    def __init__(self, config: Optional[GeminiConfig] = None):
        super().__init__(config or GeminiConfig())
        self._init_client()

    def _init_client(self):
        """Google Generative AI 클라이언트 초기화"""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.config.api_key)
            self._client = genai.GenerativeModel(self.config.model)
        except ImportError:
            raise ImportError("google-generativeai 패키지가 필요합니다: pip install google-generativeai")

    def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        """텍스트 생성"""
        full_prompt = f"{system}\n\n{prompt}" if system else prompt

        response = self._client.generate_content(full_prompt)

        return LLMResponse(
            content=response.text,
            model=self.config.model,
            raw_response=response
        )

    def generate_json(self, prompt: str, system: Optional[str] = None) -> dict:
        """JSON 형식으로 생성"""
        json_system = (system or "") + "\n\nIMPORTANT: 반드시 유효한 JSON만 출력하세요."

        response = self.generate(prompt, json_system)
        content = response.content.strip()

        if "```json" in content:
            content = content.split("```json")[1].split("```")[0].strip()
        elif "```" in content:
            content = content.split("```")[1].split("```")[0].strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 파싱 실패: {e}\n응답: {content}")

    def generate_image(self, prompt: str) -> bytes:
        """이미지 생성 (Phase 2)"""
        # Gemini 2.0 Flash의 이미지 생성 기능 활용
        raise NotImplementedError("Phase 2에서 구현 예정")


class MockClient(BaseLLMClient):
    """Mock 클라이언트 - API 없이 테스트용"""

    def __init__(self, config: Optional[LLMConfig] = None):
        super().__init__(config or LLMConfig(provider=None, model="mock"))

    def generate(self, prompt: str, system: Optional[str] = None) -> LLMResponse:
        """Mock 텍스트 생성"""
        return LLMResponse(
            content="Mock response for testing",
            model="mock"
        )

    def generate_json(self, prompt: str, system: Optional[str] = None) -> dict:
        """Mock JSON 생성 - 프롬프트 내용에 따라 적절한 응답 반환"""

        # 슬라이드 구조 (먼저 체크 - "리서치 결과"가 포함될 수 있음)
        if "PPT" in prompt and "슬라이드" in prompt:
            return {
                "storyline": "[Mock] AI 트렌드 → 핵심 기술 → 적용 사례 → 시사점",
                "slides": [
                    {
                        "slide_type": "title",
                        "title": "AI 기술 트렌드 2024",
                        "body": ["미래를 이끄는 인공지능의 진화"],
                        "key_message": "2024년 AI 핵심 트렌드 소개",
                        "notes": "인사 및 발표 개요 소개",
                        "reasoning": "청중 주목 집중"
                    },
                    {
                        "slide_type": "content",
                        "title": "생성형 AI의 확산",
                        "body": [
                            "ChatGPT, Claude 등 LLM 기반 서비스 폭발적 성장",
                            "기업 업무 자동화 및 생산성 향상",
                            "창작, 코딩, 분석 등 다양한 영역 활용"
                        ],
                        "key_message": "생성형 AI가 산업 전반을 변화시키고 있음",
                        "notes": "실제 사용 사례 언급",
                        "reasoning": "가장 영향력 있는 트렌드"
                    },
                    {
                        "slide_type": "content",
                        "title": "멀티모달 AI의 진화",
                        "body": [
                            "텍스트 + 이미지 + 음성 통합 처리",
                            "GPT-4V, Gemini 등 멀티모달 모델 등장",
                            "더 자연스러운 인간-AI 인터랙션"
                        ],
                        "key_message": "AI가 인간처럼 다양한 감각을 통합",
                        "notes": "데모 영상 활용 가능",
                        "reasoning": "차세대 AI 방향성"
                    },
                    {
                        "slide_type": "content",
                        "title": "AI 에이전트 시대",
                        "body": [
                            "자율적으로 작업을 수행하는 AI 시스템",
                            "복잡한 워크플로우 자동화",
                            "인간과 협업하는 AI 파트너"
                        ],
                        "key_message": "AI가 단순 도구에서 자율 에이전트로 진화",
                        "notes": "에이전트 활용 시나리오 설명",
                        "reasoning": "신규 패러다임 소개"
                    },
                    {
                        "slide_type": "conclusion",
                        "title": "핵심 시사점",
                        "body": [
                            "생성형 AI 활용 전략 수립 필요",
                            "멀티모달 역량 확보 검토",
                            "AI 규제 동향 모니터링"
                        ],
                        "key_message": "AI 트렌드에 대응하는 전략적 준비 필요",
                        "notes": "Q&A 유도",
                        "reasoning": "실행 가능한 인사이트 제공"
                    }
                ],
                "structure_reasoning": "[Mock] 기승전결 구조로 논리적 흐름 구성"
            }

        # 요청 분석
        if "요청을 분석" in prompt or "분석하여" in prompt:
            return {
                "topic": "AI 기술 트렌드 2024",
                "audience": "IT 전문가",
                "tone": "professional",
                "requirements": ["최신 트렌드 포함", "실용적 인사이트"],
                "constraints": [],
                "slide_count_suggestion": 5,
                "reasoning": "[Mock] 주제 분석 완료"
            }

        # 리서치
        if "리서치" in prompt or "핵심 정보" in prompt:
            return {
                "research_strategy": "[Mock] AI 트렌드 검색 전략",
                "results": [
                    {
                        "topic": "생성형 AI",
                        "content": "ChatGPT, Claude 등 LLM 기반 생성형 AI가 산업 전반에 확산",
                        "source": "Industry Report 2024",
                        "confidence": "high",
                        "reasoning": "주요 기술 트렌드"
                    },
                    {
                        "topic": "멀티모달 AI",
                        "content": "텍스트, 이미지, 음성을 통합 처리하는 멀티모달 모델 발전",
                        "source": "Tech Analysis",
                        "confidence": "high",
                        "reasoning": "차세대 AI 방향"
                    },
                    {
                        "topic": "AI 에이전트",
                        "content": "자율적으로 작업을 수행하는 AI 에이전트 시스템 등장",
                        "source": "Research Paper",
                        "confidence": "medium",
                        "reasoning": "신규 패러다임"
                    },
                    {
                        "topic": "엣지 AI",
                        "content": "온디바이스 AI로 프라이버시와 속도 개선",
                        "source": "Hardware Trends",
                        "confidence": "high",
                        "reasoning": "하드웨어 트렌드"
                    },
                    {
                        "topic": "AI 규제",
                        "content": "EU AI Act 등 글로벌 AI 규제 프레임워크 도입",
                        "source": "Policy Review",
                        "confidence": "high",
                        "reasoning": "정책 동향"
                    }
                ],
                "summary": "[Mock] 2024년 AI 핵심 트렌드 5가지 분석 완료",
                "key_insights": ["생성형 AI 확산", "멀티모달 통합", "AI 에이전트 부상"]
            }

        # 디자인 시스템
        if "design" in prompt.lower() or "디자인" in prompt or "color" in prompt.lower():
            return {
                "options": [
                    {
                        "name": "Tech Blue",
                        "description": "전문적이고 신뢰감 있는 테크 스타일",
                        "primary_color": "#1E40AF",
                        "secondary_color": "#3B82F6",
                        "accent_color": "#F59E0B",
                        "background_color": "#FFFFFF",
                        "text_color": "#1F2937",
                        "font_title": "맑은 고딕",
                        "font_body": "맑은 고딕",
                        "font_size_title": 44,
                        "font_size_body": 18,
                        "style_keywords": ["professional", "tech", "modern"],
                        "reasoning": "IT 전문가 대상으로 신뢰감 있는 블루 계열"
                    },
                    {
                        "name": "Innovation Purple",
                        "description": "혁신적이고 미래지향적인 스타일",
                        "primary_color": "#7C3AED",
                        "secondary_color": "#A78BFA",
                        "accent_color": "#06B6D4",
                        "background_color": "#FAFAFA",
                        "text_color": "#1E293B",
                        "font_title": "나눔스퀘어",
                        "font_body": "나눔고딕",
                        "font_size_title": 44,
                        "font_size_body": 18,
                        "style_keywords": ["innovative", "future", "creative"],
                        "reasoning": "AI 주제에 맞는 혁신적 느낌"
                    },
                    {
                        "name": "Clean Minimal",
                        "description": "깔끔하고 미니멀한 스타일",
                        "primary_color": "#0F172A",
                        "secondary_color": "#475569",
                        "accent_color": "#10B981",
                        "background_color": "#FFFFFF",
                        "text_color": "#0F172A",
                        "font_title": "맑은 고딕",
                        "font_body": "맑은 고딕",
                        "font_size_title": 44,
                        "font_size_body": 18,
                        "style_keywords": ["minimal", "clean", "elegant"],
                        "reasoning": "콘텐츠에 집중하는 미니멀 디자인"
                    }
                ],
                "recommendation": 0,
                "recommendation_reason": "[Mock] IT 전문가 대상 발표에 Tech Blue 추천"
            }

        # 기본 응답
        return {"status": "ok", "message": "[Mock] 기본 응답"}
