"""
Base Agent 클래스
- Glass Box 투명성: 모든 결정에 대한 근거 출력
- 목표 기반 자율성
"""

from abc import ABC, abstractmethod
from typing import Optional, Any
from dataclasses import dataclass, field
from datetime import datetime

from ..config import TaskType, AgentConfig, get_config
from ..llm.router import LLMRouter


@dataclass
class AgentDecision:
    """Agent의 결정 기록 (Glass Box)"""
    action: str
    reasoning: str
    timestamp: datetime = field(default_factory=datetime.now)
    confidence: float = 1.0

    def __str__(self) -> str:
        return f"[결정] {self.action}\n[근거] {self.reasoning}"


@dataclass
class AgentContext:
    """Agent 간 공유되는 컨텍스트"""
    topic: str
    audience: str = ""
    tone: str = "professional"
    requirements: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    decisions: list[AgentDecision] = field(default_factory=list)
    data: dict = field(default_factory=dict)

    def add_decision(self, action: str, reasoning: str, confidence: float = 1.0):
        """결정 기록 추가"""
        decision = AgentDecision(action=action, reasoning=reasoning, confidence=confidence)
        self.decisions.append(decision)
        return decision


class BaseAgent(ABC):
    """
    Agent 베이스 클래스

    핵심 원칙:
    1. Glass Box: 모든 결정에 대한 근거를 출력
    2. 목표 기반: Scaffolding 최소화, 자율적 실행
    3. 컨텍스트 공유: Orchestrator를 통한 정보 전달
    """

    def __init__(
        self,
        name: str,
        task_type: TaskType,
        config: Optional[AgentConfig] = None
    ):
        self.name = name
        self.task_type = task_type
        self.config = config or get_config()
        self.router = LLMRouter(self.config)
        self._decisions: list[AgentDecision] = []

    @property
    @abstractmethod
    def system_prompt(self) -> str:
        """Agent의 시스템 프롬프트"""
        pass

    @abstractmethod
    def execute(self, context: AgentContext) -> Any:
        """Agent 실행"""
        pass

    def log_decision(self, action: str, reasoning: str, confidence: float = 1.0) -> AgentDecision:
        """결정 로깅 (Glass Box)"""
        decision = AgentDecision(action=action, reasoning=reasoning, confidence=confidence)
        self._decisions.append(decision)
        print(f"\n{'='*50}")
        print(f"[{self.name}] {decision}")
        print(f"{'='*50}\n")
        return decision

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """LLM을 통한 텍스트 생성"""
        response = self.router.generate(
            self.task_type,
            prompt,
            system or self.system_prompt
        )
        return response.content

    def generate_json(self, prompt: str, system: Optional[str] = None) -> dict:
        """LLM을 통한 JSON 생성"""
        return self.router.generate_json(
            self.task_type,
            prompt,
            system or self.system_prompt
        )

    def explain_llm_choice(self) -> str:
        """Glass Box: LLM 선택 근거 설명"""
        return self.router.explain_routing(self.task_type)
