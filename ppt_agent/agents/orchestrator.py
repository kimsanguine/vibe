"""
Orchestrator Agent
- 전체 워크플로우 조율
- todo.md 패턴으로 진행 상황 관리
- Human-in-the-Loop 인터랙션 관리
"""

from typing import Optional, Callable
from dataclasses import dataclass, field

from ..config import TaskType, AgentConfig
from ..models.slide import Presentation, Slide, SlideContent, SlideType
from .base import BaseAgent, AgentContext, AgentDecision


@dataclass
class TodoItem:
    """진행 상황 추적 (todo.md 패턴)"""
    task: str
    status: str = "pending"  # pending, in_progress, completed, blocked
    agent: str = ""
    result: Optional[str] = None


@dataclass
class HITLRequest:
    """Human-in-the-Loop 요청"""
    question: str
    options: list[str] = field(default_factory=list)
    context: str = ""
    required: bool = True


class OrchestratorAgent(BaseAgent):
    """
    Orchestrator Agent (Claude)

    역할:
    1. 사용자 요청 분석 및 계획 수립
    2. Sub-agent 조율 및 실행
    3. HITL 인터랙션 관리 (최대 3-4회)
    4. 진행 상황 추적 (todo.md 패턴)
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(
            name="Orchestrator",
            task_type=TaskType.ORCHESTRATE,
            config=config
        )
        self.todos: list[TodoItem] = []
        self.hitl_count = 0
        self.max_hitl = 4
        self._hitl_callback: Optional[Callable[[HITLRequest], str]] = None

    @property
    def system_prompt(self) -> str:
        return """당신은 PPT 생성을 총괄하는 Orchestrator Agent입니다.

역할:
1. 사용자 요청을 분석하여 PPT 생성 계획을 수립합니다.
2. 각 단계에서 필요한 정보를 파악하고 Sub-agent에게 전달합니다.
3. 결과물의 품질을 검토하고 필요시 수정을 요청합니다.

원칙:
- Glass Box: 모든 결정에 대한 근거를 명확히 설명합니다.
- 효율성: 불필요한 사용자 인터랙션을 최소화합니다.
- 품질: 각 단계의 결과물을 검증합니다.

응답 형식:
항상 JSON 형식으로 응답하세요."""

    def set_hitl_callback(self, callback: Callable[[HITLRequest], str]):
        """HITL 콜백 설정"""
        self._hitl_callback = callback

    def request_hitl(self, request: HITLRequest) -> Optional[str]:
        """Human-in-the-Loop 요청"""
        if self.hitl_count >= self.max_hitl:
            self.log_decision(
                action="HITL 스킵",
                reasoning=f"최대 HITL 횟수({self.max_hitl})에 도달. 자동 진행.",
                confidence=0.7
            )
            return None

        self.hitl_count += 1
        self.log_decision(
            action=f"HITL #{self.hitl_count}",
            reasoning=f"사용자 확인 필요: {request.question}"
        )

        if self._hitl_callback:
            return self._hitl_callback(request)

        # CLI 기본 인터랙션
        print(f"\n[HITL #{self.hitl_count}] {request.question}")
        if request.context:
            print(f"컨텍스트: {request.context}")
        if request.options:
            for i, opt in enumerate(request.options, 1):
                print(f"  {i}. {opt}")

        response = input("응답: ").strip()
        return response

    def add_todo(self, task: str, agent: str = "") -> TodoItem:
        """할 일 추가"""
        todo = TodoItem(task=task, agent=agent)
        self.todos.append(todo)
        return todo

    def update_todo(self, task: str, status: str, result: Optional[str] = None):
        """할 일 상태 업데이트"""
        for todo in self.todos:
            if todo.task == task:
                todo.status = status
                todo.result = result
                break

    def print_todos(self):
        """진행 상황 출력 (todo.md 스타일)"""
        print("\n## 진행 상황")
        for todo in self.todos:
            status_icon = {
                "pending": "⬜",
                "in_progress": "🔄",
                "completed": "✅",
                "blocked": "❌"
            }.get(todo.status, "⬜")
            print(f"- {status_icon} {todo.task}")
            if todo.result:
                print(f"  → {todo.result[:50]}...")
        print()

    def analyze_request(self, user_input: str) -> AgentContext:
        """사용자 요청 분석"""
        self.log_decision(
            action="요청 분석 시작",
            reasoning="사용자 입력에서 주제, 청중, 톤, 요구사항을 추출합니다."
        )

        prompt = f"""다음 사용자 요청을 분석하여 PPT 생성에 필요한 정보를 추출하세요.

사용자 요청:
{user_input}

다음 JSON 형식으로 응답하세요:
{{
    "topic": "PPT 주제",
    "audience": "대상 청중",
    "tone": "톤 (professional/casual/academic)",
    "requirements": ["요구사항1", "요구사항2"],
    "constraints": ["제약사항1"],
    "slide_count_suggestion": 5,
    "reasoning": "분석 근거"
}}"""

        result = self.generate_json(prompt)

        context = AgentContext(
            topic=result.get("topic", user_input),
            audience=result.get("audience", "일반"),
            tone=result.get("tone", "professional"),
            requirements=result.get("requirements", []),
            constraints=result.get("constraints", [])
        )

        context.data["slide_count_suggestion"] = result.get("slide_count_suggestion", 5)

        self.log_decision(
            action="요청 분석 완료",
            reasoning=result.get("reasoning", "분석 완료")
        )

        return context

    def create_plan(self, context: AgentContext) -> list[TodoItem]:
        """실행 계획 수립"""
        self.log_decision(
            action="실행 계획 수립",
            reasoning="MVP Phase 1: 리서치 → 구조화 → Export"
        )

        # Phase 1 MVP: 간단한 워크플로우
        self.add_todo("사용자 요청 확인 (HITL#1)", "Orchestrator")
        self.add_todo("주제 리서치", "Research Agent")
        self.add_todo("슬라이드 구조 생성", "Orchestrator")
        self.add_todo("PPTX 파일 생성", "Export Skill")

        return self.todos

    def execute(self, context: AgentContext) -> Presentation:
        """전체 워크플로우 실행"""
        self.log_decision(
            action="워크플로우 시작",
            reasoning=f"주제: {context.topic}, 청중: {context.audience}"
        )

        # 1. HITL #1: 요청 확인
        self.update_todo("사용자 요청 확인 (HITL#1)", "in_progress")
        self.print_todos()

        hitl_response = self.request_hitl(HITLRequest(
            question="다음 내용으로 PPT를 생성할까요?",
            context=f"주제: {context.topic}\n청중: {context.audience}\n톤: {context.tone}",
            options=["예, 진행해주세요", "아니요, 수정이 필요합니다"]
        ))

        if hitl_response and "아니" in hitl_response:
            modification = self.request_hitl(HITLRequest(
                question="어떤 부분을 수정할까요?",
                required=True
            ))
            if modification:
                context.requirements.append(modification)

        self.update_todo("사용자 요청 확인 (HITL#1)", "completed")

        # 프레젠테이션 객체 생성
        presentation = Presentation(
            topic=context.topic,
            audience=context.audience,
            tone=context.tone
        )

        return presentation, context
