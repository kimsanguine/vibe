"""
슬라이드 및 프레젠테이션 데이터 모델
"""

from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from datetime import datetime


class SlideType(Enum):
    """슬라이드 유형"""
    TITLE = "title"
    CONTENT = "content"
    SECTION = "section"
    TWO_COLUMN = "two_column"
    IMAGE = "image"
    CHART = "chart"
    CONCLUSION = "conclusion"


class ConfidenceLevel(Enum):
    """신뢰도 레벨"""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ResearchResult:
    """리서치 결과"""
    topic: str
    content: str
    source: str
    confidence: ConfidenceLevel
    timestamp: datetime = field(default_factory=datetime.now)
    reasoning: str = ""  # Glass Box: 결정 근거

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "content": self.content,
            "source": self.source,
            "confidence": self.confidence.value,
            "timestamp": self.timestamp.isoformat(),
            "reasoning": self.reasoning
        }


@dataclass
class SlideContent:
    """슬라이드 콘텐츠"""
    title: str
    body: list[str] = field(default_factory=list)
    notes: str = ""
    image_path: Optional[str] = None
    chart_data: Optional[dict] = None


@dataclass
class Slide:
    """단일 슬라이드"""
    slide_type: SlideType
    content: SlideContent
    order: int
    key_message: str = ""  # 핵심 메시지
    reasoning: str = ""  # Glass Box: 이 슬라이드가 필요한 이유

    def to_dict(self) -> dict:
        return {
            "slide_type": self.slide_type.value,
            "order": self.order,
            "title": self.content.title,
            "body": self.content.body,
            "notes": self.content.notes,
            "key_message": self.key_message,
            "reasoning": self.reasoning
        }


@dataclass
class DesignSystem:
    """디자인 시스템 (Phase 2에서 Gemini가 생성)"""
    primary_color: str = "#1E3A8A"  # 기본 파란색
    secondary_color: str = "#3B82F6"
    accent_color: str = "#F59E0B"
    background_color: str = "#FFFFFF"
    text_color: str = "#1F2937"
    font_title: str = "맑은 고딕"
    font_body: str = "맑은 고딕"
    font_size_title: int = 44
    font_size_body: int = 18


@dataclass
class Presentation:
    """프레젠테이션 전체"""
    topic: str
    audience: str = ""
    tone: str = "professional"  # professional, casual, academic
    slides: list[Slide] = field(default_factory=list)
    research_results: list[ResearchResult] = field(default_factory=list)
    design: DesignSystem = field(default_factory=DesignSystem)
    created_at: datetime = field(default_factory=datetime.now)

    def add_slide(self, slide: Slide):
        """슬라이드 추가"""
        slide.order = len(self.slides) + 1
        self.slides.append(slide)

    def to_dict(self) -> dict:
        return {
            "topic": self.topic,
            "audience": self.audience,
            "tone": self.tone,
            "slides": [s.to_dict() for s in self.slides],
            "research_results": [r.to_dict() for r in self.research_results],
            "created_at": self.created_at.isoformat()
        }
