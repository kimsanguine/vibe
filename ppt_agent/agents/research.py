"""
Research Agent
- 웹 검색 및 정보 수집
- 출처와 신뢰도 기록
- Glass Box: 검색 전략 및 결과 평가 근거 출력
"""

from typing import Optional
from datetime import datetime

from ..config import TaskType, AgentConfig
from ..models.slide import ResearchResult, ConfidenceLevel
from .base import BaseAgent, AgentContext


class ResearchAgent(BaseAgent):
    """
    Research Agent (Claude)

    역할:
    1. 주제에 대한 핵심 정보 수집
    2. 출처와 신뢰도 기록
    3. PPT에 적합한 핵심 포인트 추출
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(
            name="Research Agent",
            task_type=TaskType.RESEARCH,
            config=config
        )

    @property
    def system_prompt(self) -> str:
        return """당신은 PPT 작성을 위한 리서치 전문 Agent입니다.

역할:
1. 주어진 주제에 대해 신뢰할 수 있는 정보를 수집합니다.
2. 각 정보의 출처와 신뢰도를 명시합니다.
3. PPT 슬라이드에 적합한 핵심 포인트를 추출합니다.

원칙:
- 정확성: 검증된 정보만 제공합니다.
- 출처 명시: 모든 정보에 출처를 기록합니다.
- 간결성: PPT에 적합한 핵심 내용 위주로 정리합니다.
- Glass Box: 검색 전략과 정보 선별 근거를 설명합니다.

응답 형식:
항상 JSON 형식으로 응답하세요."""

    def research(self, topic: str, context: AgentContext) -> list[ResearchResult]:
        """주제 리서치 수행"""
        self.log_decision(
            action="리서치 시작",
            reasoning=f"주제 '{topic}'에 대해 {context.audience} 대상 정보 수집"
        )

        prompt = f"""다음 주제에 대해 PPT 작성에 필요한 핵심 정보를 리서치하세요.

주제: {topic}
대상 청중: {context.audience}
톤: {context.tone}
요구사항: {', '.join(context.requirements) if context.requirements else '없음'}

다음 JSON 형식으로 5개의 핵심 정보를 제공하세요:
{{
    "research_strategy": "검색 전략 설명",
    "results": [
        {{
            "topic": "세부 주제",
            "content": "핵심 내용 (2-3문장)",
            "source": "정보 출처",
            "confidence": "high/medium/low",
            "reasoning": "이 정보를 선택한 이유"
        }}
    ],
    "summary": "전체 리서치 요약",
    "key_insights": ["핵심 인사이트 1", "핵심 인사이트 2", "핵심 인사이트 3"]
}}"""

        result = self.generate_json(prompt)

        self.log_decision(
            action="리서치 전략",
            reasoning=result.get("research_strategy", "일반적인 검색 전략 적용")
        )

        research_results = []
        for item in result.get("results", []):
            confidence_map = {
                "high": ConfidenceLevel.HIGH,
                "medium": ConfidenceLevel.MEDIUM,
                "low": ConfidenceLevel.LOW
            }

            research_result = ResearchResult(
                topic=item.get("topic", ""),
                content=item.get("content", ""),
                source=item.get("source", "일반 지식"),
                confidence=confidence_map.get(item.get("confidence", "medium"), ConfidenceLevel.MEDIUM),
                reasoning=item.get("reasoning", "")
            )
            research_results.append(research_result)

        # 컨텍스트에 리서치 결과 저장
        context.data["research_results"] = research_results
        context.data["key_insights"] = result.get("key_insights", [])
        context.data["research_summary"] = result.get("summary", "")

        self.log_decision(
            action="리서치 완료",
            reasoning=f"{len(research_results)}개 정보 수집 완료. 요약: {result.get('summary', '')[:100]}..."
        )

        return research_results

    def evaluate_results(self, results: list[ResearchResult]) -> dict:
        """리서치 결과 품질 평가"""
        self.log_decision(
            action="결과 품질 평가",
            reasoning="수집된 정보의 신뢰도와 커버리지 평가"
        )

        high_confidence = sum(1 for r in results if r.confidence == ConfidenceLevel.HIGH)
        medium_confidence = sum(1 for r in results if r.confidence == ConfidenceLevel.MEDIUM)
        low_confidence = sum(1 for r in results if r.confidence == ConfidenceLevel.LOW)

        total = len(results)
        score = (high_confidence * 1.0 + medium_confidence * 0.7 + low_confidence * 0.4) / total if total > 0 else 0

        evaluation = {
            "total_results": total,
            "high_confidence": high_confidence,
            "medium_confidence": medium_confidence,
            "low_confidence": low_confidence,
            "quality_score": round(score, 2),
            "pass": score >= 0.7
        }

        self.log_decision(
            action="평가 완료",
            reasoning=f"품질 점수: {evaluation['quality_score']} ({'통과' if evaluation['pass'] else '재검토 필요'})"
        )

        return evaluation

    def execute(self, context: AgentContext) -> list[ResearchResult]:
        """리서치 실행"""
        results = self.research(context.topic, context)
        evaluation = self.evaluate_results(results)

        context.add_decision(
            action="리서치 Agent 실행 완료",
            reasoning=f"품질 점수 {evaluation['quality_score']}, {len(results)}개 정보 수집"
        )

        return results
