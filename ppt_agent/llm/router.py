"""
LLM Router - 태스크 유형에 따라 적절한 LLM 선택
"""

from typing import Optional

from ..config import TaskType, LLMProvider, LLM_ROUTING, AgentConfig, get_config
from .clients import BaseLLMClient, ClaudeClient, GeminiClient, MockClient, LLMResponse


class LLMRouter:
    """
    태스크 유형에 따라 적절한 LLM을 라우팅

    라우팅 로직:
    - Mock 모드: 모든 태스크 → MockClient
    - 논리적 태스크 (orchestrate, research, structure, logic_eval, export) → Claude
    - 시각적 태스크 (design, asset, visual_eval) → Gemini
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or get_config()
        self._clients: dict[LLMProvider, BaseLLMClient] = {}
        self._mock_client: Optional[MockClient] = None

    def _get_client(self, provider: LLMProvider) -> BaseLLMClient:
        """LLM 클라이언트 가져오기 (lazy initialization)"""
        # Mock 모드면 항상 MockClient 반환
        if self.config.mock_mode:
            if self._mock_client is None:
                self._mock_client = MockClient()
            return self._mock_client

        if provider not in self._clients:
            if provider == LLMProvider.CLAUDE:
                self._clients[provider] = ClaudeClient(self.config.claude)
            elif provider == LLMProvider.GEMINI:
                self._clients[provider] = GeminiClient(self.config.gemini)
            elif provider == LLMProvider.MOCK:
                self._clients[provider] = MockClient()
            else:
                raise ValueError(f"알 수 없는 LLM 제공자: {provider}")
        return self._clients[provider]

    def route(self, task_type: TaskType) -> LLMProvider:
        """태스크 유형에 따라 LLM 제공자 결정"""
        if self.config.mock_mode:
            return LLMProvider.MOCK
        return LLM_ROUTING.get(task_type, LLMProvider.CLAUDE)

    def get_client_for_task(self, task_type: TaskType) -> BaseLLMClient:
        """태스크에 적합한 LLM 클라이언트 반환"""
        provider = self.route(task_type)
        return self._get_client(provider)

    def generate(
        self,
        task_type: TaskType,
        prompt: str,
        system: Optional[str] = None
    ) -> LLMResponse:
        """태스크 유형에 맞는 LLM으로 생성"""
        client = self.get_client_for_task(task_type)
        return client.generate(prompt, system)

    def generate_json(
        self,
        task_type: TaskType,
        prompt: str,
        system: Optional[str] = None
    ) -> dict:
        """태스크 유형에 맞는 LLM으로 JSON 생성"""
        client = self.get_client_for_task(task_type)
        return client.generate_json(prompt, system)

    def explain_routing(self, task_type: TaskType) -> str:
        """Glass Box: 라우팅 결정 근거 설명"""
        provider = self.route(task_type)
        reasons = {
            LLMProvider.CLAUDE: "Claude는 논리적 추론, 긴 문서 처리, 구조화에 강점이 있습니다.",
            LLMProvider.GEMINI: "Gemini는 시각적 이해와 이미지 생성에 강점이 있습니다.",
            LLMProvider.MOCK: "[Mock 모드] API 없이 테스트용 더미 데이터를 사용합니다."
        }
        return f"[라우팅] {task_type.value} → {provider.value}: {reasons.get(provider, '')}"
