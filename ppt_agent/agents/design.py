"""
Design Agent (Gemini)
- 디자인 시스템 생성 (컬러, 폰트, 레이아웃)
- 시각적 일관성 유지
- 청중과 톤에 맞는 스타일 제안
"""

from typing import Optional

from ..config import TaskType, AgentConfig
from ..models.slide import DesignSystem, Presentation
from .base import BaseAgent, AgentContext


class DesignAgent(BaseAgent):
    """
    Design Agent (Gemini)

    역할:
    1. 주제, 청중, 톤에 맞는 디자인 시스템 생성
    2. 컬러 팔레트 + 레이아웃 옵션 제안
    3. 시각적 일관성 검토
    """

    def __init__(self, config: Optional[AgentConfig] = None):
        super().__init__(
            name="Design Agent",
            task_type=TaskType.DESIGN,
            config=config
        )

    @property
    def system_prompt(self) -> str:
        return """You are a professional presentation design expert.

Role:
1. Create cohesive design systems for presentations
2. Select color palettes that match the topic and audience
3. Ensure visual consistency and modern aesthetics

Design Principles:
- Use color psychology appropriately for the context
- Ensure high contrast for readability
- Follow modern, clean design trends
- Consider cultural context (Korean business presentations)

Always respond in JSON format with Korean text for content."""

    def generate_design_system(
        self,
        context: AgentContext,
        num_options: int = 3
    ) -> list[DesignSystem]:
        """디자인 시스템 옵션 생성"""
        self.log_decision(
            action="디자인 시스템 생성 시작",
            reasoning=f"주제: {context.topic}, 청중: {context.audience}, 톤: {context.tone}"
        )

        print(f"\n{self.explain_llm_choice()}")

        prompt = f"""Create {num_options} different design system options for a presentation.

Topic: {context.topic}
Target Audience: {context.audience}
Tone: {context.tone}

For each option, provide a complete design system in this JSON format:
{{
    "options": [
        {{
            "name": "Option name (e.g., 'Corporate Blue', 'Modern Gradient')",
            "description": "Brief description of the design style",
            "primary_color": "#HEXCODE (main brand color)",
            "secondary_color": "#HEXCODE (supporting color)",
            "accent_color": "#HEXCODE (highlight color)",
            "background_color": "#HEXCODE (slide background)",
            "text_color": "#HEXCODE (main text color)",
            "font_title": "Korean font name (e.g., '맑은 고딕', '나눔스퀘어')",
            "font_body": "Korean font name",
            "font_size_title": 44,
            "font_size_body": 18,
            "style_keywords": ["keyword1", "keyword2"],
            "reasoning": "Why this design fits the context"
        }}
    ],
    "recommendation": 0,
    "recommendation_reason": "Why this option is recommended"
}}

Consider:
- Color psychology for the topic
- Professional vs creative balance based on audience
- Korean business presentation norms
- Readability and accessibility"""

        try:
            result = self.generate_json(prompt)
        except Exception as e:
            # Gemini 연결 실패 시 Claude로 폴백
            self.log_decision(
                action="Gemini 폴백",
                reasoning=f"Gemini 연결 실패, 기본 디자인 사용: {str(e)}",
                confidence=0.6
            )
            return [self._get_default_design(context)]

        options = []
        for opt_data in result.get("options", []):
            design = DesignSystem(
                primary_color=opt_data.get("primary_color", "#1E3A8A"),
                secondary_color=opt_data.get("secondary_color", "#3B82F6"),
                accent_color=opt_data.get("accent_color", "#F59E0B"),
                background_color=opt_data.get("background_color", "#FFFFFF"),
                text_color=opt_data.get("text_color", "#1F2937"),
                font_title=opt_data.get("font_title", "맑은 고딕"),
                font_body=opt_data.get("font_body", "맑은 고딕"),
                font_size_title=opt_data.get("font_size_title", 44),
                font_size_body=opt_data.get("font_size_body", 18)
            )
            options.append(design)

            self.log_decision(
                action=f"디자인 옵션: {opt_data.get('name', 'Unknown')}",
                reasoning=opt_data.get("reasoning", "")
            )

        # 추천 옵션 기록
        recommendation_idx = result.get("recommendation", 0)
        self.log_decision(
            action=f"추천 옵션: #{recommendation_idx + 1}",
            reasoning=result.get("recommendation_reason", "")
        )

        context.data["design_options"] = options
        context.data["design_recommendation"] = recommendation_idx

        return options

    def _get_default_design(self, context: AgentContext) -> DesignSystem:
        """톤에 따른 기본 디자인"""
        tone_designs = {
            "professional": DesignSystem(
                primary_color="#1E3A8A",
                secondary_color="#3B82F6",
                accent_color="#F59E0B",
                background_color="#FFFFFF",
                text_color="#1F2937"
            ),
            "casual": DesignSystem(
                primary_color="#7C3AED",
                secondary_color="#A78BFA",
                accent_color="#F472B6",
                background_color="#FAFAFA",
                text_color="#374151"
            ),
            "academic": DesignSystem(
                primary_color="#1F2937",
                secondary_color="#4B5563",
                accent_color="#059669",
                background_color="#FFFFFF",
                text_color="#111827"
            )
        }
        return tone_designs.get(context.tone, tone_designs["professional"])

    def evaluate_visual_quality(
        self,
        presentation: Presentation
    ) -> dict:
        """시각적 품질 평가 (Phase 3에서 이미지 분석 추가)"""
        self.log_decision(
            action="시각적 품질 평가",
            reasoning="디자인 일관성 및 가독성 검토"
        )

        # 기본 평가 (색상 대비, 폰트 크기 등)
        design = presentation.design

        # 색상 대비 체크 (간단한 휴리스틱)
        def hex_to_luminance(hex_color: str) -> float:
            hex_color = hex_color.lstrip('#')
            r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return (0.299 * r + 0.587 * g + 0.114 * b) / 255

        bg_lum = hex_to_luminance(design.background_color)
        text_lum = hex_to_luminance(design.text_color)
        contrast_ratio = abs(bg_lum - text_lum)

        evaluation = {
            "contrast_ratio": round(contrast_ratio, 2),
            "contrast_pass": contrast_ratio > 0.4,
            "font_size_pass": design.font_size_body >= 16,
            "slide_count": len(presentation.slides),
            "has_title_slide": any(s.slide_type.value == "title" for s in presentation.slides),
            "has_conclusion": any(s.slide_type.value == "conclusion" for s in presentation.slides),
            "overall_pass": True
        }

        evaluation["overall_pass"] = all([
            evaluation["contrast_pass"],
            evaluation["font_size_pass"],
            evaluation["has_title_slide"]
        ])

        self.log_decision(
            action="평가 완료",
            reasoning=f"전체 통과: {evaluation['overall_pass']}, 대비율: {evaluation['contrast_ratio']}"
        )

        return evaluation

    def execute(self, context: AgentContext) -> list[DesignSystem]:
        """디자인 Agent 실행"""
        options = self.generate_design_system(context)

        context.add_decision(
            action="Design Agent 실행 완료",
            reasoning=f"{len(options)}개 디자인 옵션 생성"
        )

        return options
