"""
Design Skill (Gemini)
- 컬러 팔레트 생성
- 타이포그래피 시스템
- 레이아웃 템플릿
- 모던 스타일 가이드
"""

from typing import Optional
from dataclasses import dataclass

from ..config import TaskType, AgentConfig, get_config
from ..llm.router import LLMRouter
from ..models.slide import DesignSystem, SlideType


@dataclass
class LayoutTemplate:
    """레이아웃 템플릿"""
    name: str
    slide_type: SlideType
    title_position: tuple  # (left, top, width, height) in inches
    content_position: tuple
    image_position: Optional[tuple] = None
    description: str = ""


class DesignSkill:
    """
    Design Skill (Gemini)

    역할:
    1. 컬러 팔레트 생성 및 조화 검증
    2. 타이포그래피 시스템 정의
    3. 슬라이드 레이아웃 템플릿 제공
    4. 모던 스타일 가이드
    """

    # 한국 비즈니스 프레젠테이션 색상 팔레트
    KOREAN_BUSINESS_PALETTES = {
        "corporate_blue": {
            "primary": "#1E3A8A",
            "secondary": "#3B82F6",
            "accent": "#F59E0B",
            "background": "#FFFFFF",
            "text": "#1F2937"
        },
        "modern_navy": {
            "primary": "#0F172A",
            "secondary": "#334155",
            "accent": "#22D3EE",
            "background": "#F8FAFC",
            "text": "#0F172A"
        },
        "tech_gradient": {
            "primary": "#4F46E5",
            "secondary": "#7C3AED",
            "accent": "#06B6D4",
            "background": "#FFFFFF",
            "text": "#1E293B"
        },
        "nature_green": {
            "primary": "#047857",
            "secondary": "#10B981",
            "accent": "#F59E0B",
            "background": "#FFFFFF",
            "text": "#1F2937"
        },
        "warm_coral": {
            "primary": "#DC2626",
            "secondary": "#F87171",
            "accent": "#FBBF24",
            "background": "#FFFBEB",
            "text": "#1F2937"
        }
    }

    # 한국어 폰트 추천
    KOREAN_FONTS = {
        "professional": {
            "title": "맑은 고딕",
            "body": "맑은 고딕"
        },
        "modern": {
            "title": "나눔스퀘어",
            "body": "나눔고딕"
        },
        "creative": {
            "title": "나눔바른펜",
            "body": "나눔고딕"
        },
        "academic": {
            "title": "본명조",
            "body": "본고딕"
        }
    }

    # 레이아웃 템플릿
    LAYOUTS = {
        SlideType.TITLE: LayoutTemplate(
            name="title_centered",
            slide_type=SlideType.TITLE,
            title_position=(1, 2.5, 8, 1.5),
            content_position=(1, 4, 8, 0.75),
            description="중앙 정렬 타이틀 슬라이드"
        ),
        SlideType.CONTENT: LayoutTemplate(
            name="content_standard",
            slide_type=SlideType.CONTENT,
            title_position=(0.5, 0.5, 9, 1),
            content_position=(0.5, 1.5, 9, 4.5),
            description="표준 콘텐츠 레이아웃"
        ),
        SlideType.TWO_COLUMN: LayoutTemplate(
            name="two_column",
            slide_type=SlideType.TWO_COLUMN,
            title_position=(0.5, 0.5, 9, 1),
            content_position=(0.5, 1.5, 4, 4.5),
            image_position=(5, 1.5, 4.5, 4.5),
            description="2단 레이아웃"
        ),
        SlideType.IMAGE: LayoutTemplate(
            name="image_focus",
            slide_type=SlideType.IMAGE,
            title_position=(0.5, 0.3, 9, 0.75),
            content_position=(0.5, 4.5, 4, 1),
            image_position=(0.5, 1.2, 9, 3.2),
            description="이미지 중심 레이아웃"
        )
    }

    def __init__(self, config: Optional[AgentConfig] = None):
        self.config = config or get_config()
        self.router = LLMRouter(self.config)
        self.task_type = TaskType.DESIGN

    def generate_color_palette(
        self,
        topic: str,
        tone: str,
        audience: str
    ) -> dict:
        """주제와 톤에 맞는 컬러 팔레트 생성"""
        print(f"\n[Design Skill] 컬러 팔레트 생성 - 톤: {tone}")

        # 톤에 따른 기본 팔레트 선택
        tone_palette_map = {
            "professional": "corporate_blue",
            "casual": "tech_gradient",
            "academic": "modern_navy"
        }

        base_palette_name = tone_palette_map.get(tone, "corporate_blue")

        # Gemini로 커스텀 팔레트 생성 시도
        try:
            prompt = f"""Generate a color palette for a presentation.

Topic: {topic}
Tone: {tone}
Audience: {audience}

Based on the topic and context, suggest a color palette in JSON format:
{{
    "primary": "#HEXCODE",
    "secondary": "#HEXCODE",
    "accent": "#HEXCODE",
    "background": "#HEXCODE",
    "text": "#HEXCODE",
    "reasoning": "Why these colors work for this context"
}}

Consider color psychology and Korean business culture."""

            result = self.router.generate_json(self.task_type, prompt)

            print(f"[Design Skill] Gemini 생성 팔레트: {result.get('reasoning', '')[:50]}...")

            return {
                "primary": result.get("primary", "#1E3A8A"),
                "secondary": result.get("secondary", "#3B82F6"),
                "accent": result.get("accent", "#F59E0B"),
                "background": result.get("background", "#FFFFFF"),
                "text": result.get("text", "#1F2937")
            }

        except Exception as e:
            print(f"[Design Skill] Gemini 폴백 → 기본 팔레트 사용: {base_palette_name}")
            return self.KOREAN_BUSINESS_PALETTES[base_palette_name]

    def get_typography(self, tone: str) -> dict:
        """톤에 맞는 타이포그래피 반환"""
        tone_font_map = {
            "professional": "professional",
            "casual": "modern",
            "academic": "academic"
        }
        font_style = tone_font_map.get(tone, "professional")
        return self.KOREAN_FONTS[font_style]

    def get_layout(self, slide_type: SlideType) -> LayoutTemplate:
        """슬라이드 타입에 맞는 레이아웃 반환"""
        return self.LAYOUTS.get(slide_type, self.LAYOUTS[SlideType.CONTENT])

    def create_design_system(
        self,
        topic: str,
        tone: str = "professional",
        audience: str = "일반"
    ) -> DesignSystem:
        """완전한 디자인 시스템 생성"""
        palette = self.generate_color_palette(topic, tone, audience)
        typography = self.get_typography(tone)

        design = DesignSystem(
            primary_color=palette["primary"],
            secondary_color=palette["secondary"],
            accent_color=palette["accent"],
            background_color=palette["background"],
            text_color=palette["text"],
            font_title=typography["title"],
            font_body=typography["body"],
            font_size_title=44,
            font_size_body=18
        )

        print(f"[Design Skill] 디자인 시스템 생성 완료")
        print(f"  - Primary: {design.primary_color}")
        print(f"  - Font: {design.font_title}")

        return design

    def validate_contrast(self, bg_color: str, text_color: str) -> bool:
        """색상 대비 검증 (WCAG 기준)"""
        def hex_to_rgb(hex_color: str) -> tuple:
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def luminance(rgb: tuple) -> float:
            r, g, b = [x / 255.0 for x in rgb]
            r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
            g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
            b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
            return 0.2126 * r + 0.7152 * g + 0.0722 * b

        bg_lum = luminance(hex_to_rgb(bg_color))
        text_lum = luminance(hex_to_rgb(text_color))

        lighter = max(bg_lum, text_lum)
        darker = min(bg_lum, text_lum)

        contrast_ratio = (lighter + 0.05) / (darker + 0.05)

        # WCAG AA 기준: 4.5:1 이상
        return contrast_ratio >= 4.5
