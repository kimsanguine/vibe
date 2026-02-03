"""
PPT Agent 설정 및 환경변수 관리
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class LLMProvider(Enum):
    """LLM 제공자"""
    CLAUDE = "claude"
    GEMINI = "gemini"
    MOCK = "mock"


class TaskType(Enum):
    """태스크 유형 - LLM 라우팅에 사용"""
    ORCHESTRATE = "orchestrate"
    RESEARCH = "research"
    STRUCTURE = "structure"
    LOGIC_EVAL = "logic_eval"
    EXPORT = "export"
    DESIGN = "design"
    ASSET = "asset"
    VISUAL_EVAL = "visual_eval"


@dataclass
class LLMConfig:
    """LLM 설정"""
    provider: LLMProvider
    model: str
    api_key: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7


@dataclass
class ClaudeConfig(LLMConfig):
    """Claude 설정"""
    provider: LLMProvider = LLMProvider.CLAUDE
    model: str = "claude-sonnet-4-20250514"
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY"))


@dataclass
class GeminiConfig(LLMConfig):
    """Gemini 설정 (Phase 2)"""
    provider: LLMProvider = LLMProvider.GEMINI
    model: str = "gemini-2.0-flash-exp"
    api_key: Optional[str] = field(default_factory=lambda: os.getenv("GOOGLE_API_KEY"))


@dataclass
class AgentConfig:
    """Agent 전체 설정"""
    claude: ClaudeConfig = field(default_factory=ClaudeConfig)
    gemini: GeminiConfig = field(default_factory=GeminiConfig)
    max_hitl_interactions: int = 4
    output_dir: str = "./output"
    language: str = "ko"  # 한국어 기본
    mock_mode: bool = field(default_factory=lambda: os.getenv("PPT_AGENT_MOCK", "").lower() == "true")


# LLM 라우팅 맵
LLM_ROUTING = {
    TaskType.ORCHESTRATE: LLMProvider.CLAUDE,
    TaskType.RESEARCH: LLMProvider.CLAUDE,
    TaskType.STRUCTURE: LLMProvider.CLAUDE,
    TaskType.LOGIC_EVAL: LLMProvider.CLAUDE,
    TaskType.EXPORT: LLMProvider.CLAUDE,
    TaskType.DESIGN: LLMProvider.GEMINI,
    TaskType.ASSET: LLMProvider.GEMINI,
    TaskType.VISUAL_EVAL: LLMProvider.GEMINI,
}


def get_config() -> AgentConfig:
    """설정 인스턴스 반환"""
    return AgentConfig()
