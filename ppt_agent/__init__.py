"""
PPT Agent - Multi-LLM PPT Generation System
Claude (논리적 태스크) + Gemini (시각적 태스크) 분리 구조
"""

__version__ = "0.1.0"

from .main import PPTAgent
from .config import get_config, AgentConfig
