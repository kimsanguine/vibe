"""
PPT Agent - 메인 실행 파일
Multi-LLM 구조: Claude (논리) + Gemini (시각)
Phase 1 MVP: Orchestrator + Research + Export
"""

import argparse
import sys
from pathlib import Path

from .config import get_config, AgentConfig
from .models.slide import Presentation
from .agents.orchestrator import OrchestratorAgent, HITLRequest
from .agents.research import ResearchAgent
from .skills.structure import StructureSkill
from .skills.export import ExportSkill


class PPTAgent:
    """
    PPT Agent 메인 클래스

    Phase 1 MVP 워크플로우:
    1. Orchestrator: 요청 분석 및 계획 수립
    2. Research Agent: 주제 리서치
    3. Structure Skill: 슬라이드 구조 생성
    4. Export Skill: PPTX 파일 생성
    """

    def __init__(self, config: AgentConfig = None):
        self.config = config or get_config()

        # Agents
        self.orchestrator = OrchestratorAgent(self.config)
        self.research_agent = ResearchAgent(self.config)

        # Skills
        self.structure_skill = StructureSkill(self.config)
        self.export_skill = ExportSkill(self.config)

    def run(self, user_input: str, output_path: str = None) -> str:
        """PPT 생성 실행"""
        print("\n" + "="*60)
        print("🎯 PPT Agent - Phase 1 MVP")
        print("="*60)

        # 1. 요청 분석
        print("\n📋 Step 1: 요청 분석")
        context = self.orchestrator.analyze_request(user_input)

        # 2. 계획 수립
        print("\n📋 Step 2: 실행 계획 수립")
        self.orchestrator.create_plan(context)
        self.orchestrator.print_todos()

        # 3. HITL #1: 요청 확인
        print("\n📋 Step 3: 사용자 확인")
        presentation, context = self.orchestrator.execute(context)

        # 4. 리서치
        print("\n🔍 Step 4: 주제 리서치")
        self.orchestrator.update_todo("주제 리서치", "in_progress")
        research_results = self.research_agent.execute(context)
        presentation.research_results = research_results
        self.orchestrator.update_todo("주제 리서치", "completed", f"{len(research_results)}개 정보 수집")

        # 5. 슬라이드 구조 생성
        print("\n📝 Step 5: 슬라이드 구조 생성")
        self.orchestrator.update_todo("슬라이드 구조 생성", "in_progress")
        slides = self.structure_skill.generate_structure(presentation, research_results, context)
        for slide in slides:
            presentation.add_slide(slide)
        self.orchestrator.update_todo("슬라이드 구조 생성", "completed", f"{len(slides)}장 생성")

        # 6. PPTX 파일 생성
        print("\n📦 Step 6: PPTX 파일 생성")
        self.orchestrator.update_todo("PPTX 파일 생성", "in_progress")
        output_file = self.export_skill.export(presentation, output_path)
        self.orchestrator.update_todo("PPTX 파일 생성", "completed", output_file)

        # 최종 결과
        print("\n" + "="*60)
        print("✅ PPT 생성 완료!")
        print("="*60)
        self.orchestrator.print_todos()

        print(f"\n📁 출력 파일: {output_file}")
        print(f"📊 슬라이드 수: {len(presentation.slides)}장")
        print(f"🔍 리서치 결과: {len(presentation.research_results)}개")

        return output_file


def main():
    """CLI 엔트리포인트"""
    parser = argparse.ArgumentParser(
        description="PPT Agent - AI 기반 PPT 자동 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  ppt-agent "AI 기술 트렌드 2024"
  ppt-agent "스타트업 투자 유치 전략" -o pitch_deck.pptx
  ppt-agent "기후변화 대응 방안" --audience "정책 결정자"
        """
    )

    parser.add_argument(
        "topic",
        nargs="?",
        help="PPT 주제"
    )

    parser.add_argument(
        "-o", "--output",
        help="출력 파일 경로 (기본: ./output/<topic>.pptx)"
    )

    parser.add_argument(
        "--audience",
        default="일반",
        help="대상 청중 (기본: 일반)"
    )

    parser.add_argument(
        "--tone",
        choices=["professional", "casual", "academic"],
        default="professional",
        help="프레젠테이션 톤 (기본: professional)"
    )

    parser.add_argument(
        "--no-hitl",
        action="store_true",
        help="HITL(Human-in-the-Loop) 비활성화"
    )

    args = parser.parse_args()

    # 주제가 없으면 대화형 모드
    if not args.topic:
        print("\n🎯 PPT Agent - AI 기반 PPT 자동 생성")
        print("="*40)
        args.topic = input("\nPPT 주제를 입력하세요: ").strip()

        if not args.topic:
            print("주제가 입력되지 않았습니다.")
            sys.exit(1)

    # 청중 정보 추가
    user_input = args.topic
    if args.audience != "일반":
        user_input += f"\n대상 청중: {args.audience}"
    if args.tone != "professional":
        user_input += f"\n톤: {args.tone}"

    # PPT 생성
    try:
        agent = PPTAgent()

        # HITL 비활성화 옵션
        if args.no_hitl:
            agent.orchestrator.max_hitl = 0

        output_file = agent.run(user_input, args.output)

        print(f"\n✅ 완료! 파일: {output_file}")

    except KeyboardInterrupt:
        print("\n\n취소되었습니다.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        raise


if __name__ == "__main__":
    main()
