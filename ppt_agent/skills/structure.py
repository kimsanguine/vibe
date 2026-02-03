"""
Structure Skill
- 슬라이드 구조 생성
- 한국형 PPT 템플릿 지원
- 스토리라인 및 핵심 메시지 정의
"""

from typing import Optional

from ..config import TaskType, AgentConfig, get_config
from ..llm.router import LLMRouter
from ..models.slide import (
    Presentation, Slide, SlideContent, SlideType, ResearchResult
)
from ..agents.base import AgentContext


class StructureSkill:
    """
    Structure Skill (Claude)

    역할:
    1. 리서치 결과를 바탕으로 슬라이드 구조 생성
    2. 각 슬라이드의 핵심 메시지 정의
    3. 한국형 PPT 구조 (기-승-전-결) 지원
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or get_config()
        self.router = LLMRouter(self.config)
        self.task_type = TaskType.STRUCTURE

    @property
    def system_prompt(self) -> str:
        return """당신은 PPT 구조화 전문가입니다.

역할:
1. 리서치 결과를 효과적인 슬라이드 구조로 변환합니다.
2. 각 슬라이드의 핵심 메시지를 명확히 정의합니다.
3. 청중에게 설득력 있는 스토리라인을 구성합니다.

한국형 PPT 구조:
- 기(起): 도입 - 주제 소개, 청중 관심 유발
- 승(承): 전개 - 핵심 내용 전달
- 전(轉): 전환 - 인사이트, 시사점
- 결(結): 마무리 - 요약, Call to Action

원칙:
- 슬라이드당 핵심 메시지 1개
- 글머리 기호 3-5개
- 명확하고 간결한 제목

응답 형식:
항상 JSON 형식으로 응답하세요."""

    def generate_structure(
        self,
        presentation: Presentation,
        research_results: list[ResearchResult],
        context: AgentContext
    ) -> list[Slide]:
        """슬라이드 구조 생성"""

        research_summary = "\n".join([
            f"- {r.topic}: {r.content} (출처: {r.source}, 신뢰도: {r.confidence.value})"
            for r in research_results
        ])

        key_insights = context.data.get("key_insights", [])

        prompt = f"""다음 정보를 바탕으로 PPT 슬라이드 구조를 생성하세요.

주제: {presentation.topic}
청중: {presentation.audience}
톤: {presentation.tone}

리서치 결과:
{research_summary}

핵심 인사이트:
{', '.join(key_insights)}

다음 JSON 형식으로 슬라이드 구조를 생성하세요 (5-7장):
{{
    "storyline": "전체 스토리라인 요약",
    "slides": [
        {{
            "slide_type": "title/content/section/two_column/conclusion",
            "title": "슬라이드 제목",
            "body": ["핵심 포인트 1", "핵심 포인트 2", "핵심 포인트 3"],
            "key_message": "이 슬라이드의 핵심 메시지",
            "notes": "발표자 노트",
            "reasoning": "이 슬라이드가 필요한 이유"
        }}
    ],
    "structure_reasoning": "이 구조를 선택한 이유"
}}"""

        result = self.router.generate_json(self.task_type, prompt, self.system_prompt)

        slides = []
        slide_type_map = {
            "title": SlideType.TITLE,
            "content": SlideType.CONTENT,
            "section": SlideType.SECTION,
            "two_column": SlideType.TWO_COLUMN,
            "image": SlideType.IMAGE,
            "chart": SlideType.CHART,
            "conclusion": SlideType.CONCLUSION
        }

        for i, slide_data in enumerate(result.get("slides", []), 1):
            slide_type = slide_type_map.get(
                slide_data.get("slide_type", "content"),
                SlideType.CONTENT
            )

            content = SlideContent(
                title=slide_data.get("title", ""),
                body=slide_data.get("body", []),
                notes=slide_data.get("notes", "")
            )

            slide = Slide(
                slide_type=slide_type,
                content=content,
                order=i,
                key_message=slide_data.get("key_message", ""),
                reasoning=slide_data.get("reasoning", "")
            )

            slides.append(slide)

        # 컨텍스트에 구조 정보 저장
        context.data["storyline"] = result.get("storyline", "")
        context.data["structure_reasoning"] = result.get("structure_reasoning", "")

        print(f"\n[Structure Skill] {len(slides)}개 슬라이드 구조 생성 완료")
        print(f"[스토리라인] {result.get('storyline', '')[:100]}...")

        return slides
