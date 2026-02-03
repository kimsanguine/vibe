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
