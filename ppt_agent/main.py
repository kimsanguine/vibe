"""
PPT Agent - 메인 실행 파일
Multi-LLM 구조: Claude (논리) + Gemini (시각)
Phase 2: Orchestrator + Research + Structure + Design + Export
"""

import argparse
import sys
from pathlib import Path

from .config import get_config, AgentConfig
from .models.slide import Presentation
from .agents.orchestrator import OrchestratorAgent, HITLRequest
from .agents.research import ResearchAgent
from .agents.design import DesignAgent
from .skills.structure import StructureSkill
from .skills.design import DesignSkill
from .skills.export import ExportSkill


class PPTAgent:
    """
    PPT Agent 메인 클래스

    Phase 2 워크플로우:
    1. Orchestrator: 요청 분석 및 계획 수립
    2. Research Agent (Claude): 주제 리서치
    3. Structure Skill (Claude): 슬라이드 구조 생성
    4. Design Agent (Gemini): 디자인 시스템 생성
    5. Export Skill: PPTX 파일 생성
    """

    def __init__(self, config: AgentConfig = None):
        self.config = config or get_config()

        # Agents
        self.orchestrator = OrchestratorAgent(self.config)
        self.research_agent = ResearchAgent(self.config)
        self.design_agent = DesignAgent(self.config)

        # Skills
        self.structure_skill = StructureSkill(self.config)
        self.design_skill = DesignSkill(self.config)
        self.export_skill = ExportSkill(self.config)

    def run(self, user_input: str, output_path: str = None) -> str:
        """PPT 생성 실행"""
        print("\n" + "="*60)
        print("🎯 PPT Agent - Phase 2 (Multi-LLM)")
        print("   Claude (논리) + Gemini (시각)")
        print("="*60)

        # 1. 요청 분석
        print("\n📋 Step 1: 요청 분석 [Claude]")
        context = self.orchestrator.analyze_request(user_input)

        # 2. 계획 수립
        print("\n📋 Step 2: 실행 계획 수립")
        self._create_phase2_plan()
        self.orchestrator.print_todos()

        # 3. HITL #1: 요청 확인
        print("\n📋 Step 3: 사용자 확인 [HITL #1]")
        presentation, context = self.orchestrator.execute(context)

        # 4. 리서치
        print("\n🔍 Step 4: 주제 리서치 [Claude]")
        self.orchestrator.update_todo("주제 리서치", "in_progress")
        research_results = self.research_agent.execute(context)
        presentation.research_results = research_results
        self.orchestrator.update_todo("주제 리서치", "completed", f"{len(research_results)}개 정보 수집")

        # 5. 디자인 시스템 생성
        print("\n🎨 Step 5: 디자인 시스템 생성 [Gemini]")
        self.orchestrator.update_todo("디자인 시스템 생성", "in_progress")
        design_options = self.design_agent.execute(context)

        # HITL #2: 디자인 선택
        if design_options and len(design_options) > 1:
            recommended_idx = context.data.get("design_recommendation", 0)
            hitl_response = self.orchestrator.request_hitl(HITLRequest(
                question="디자인 옵션을 선택해주세요.",
                context=f"추천: 옵션 {recommended_idx + 1}",
                options=[f"옵션 {i+1}" for i in range(len(design_options))]
            ))

            if hitl_response:
                try:
                    selected_idx = int(hitl_response.replace("옵션", "").strip()) - 1
                    if 0 <= selected_idx < len(design_options):
                        presentation.design = design_options[selected_idx]
                    else:
                        presentation.design = design_options[recommended_idx]
                except (ValueError, IndexError):
                    presentation.design = design_options[recommended_idx]
            else:
                presentation.design = design_options[recommended_idx]
        elif design_options:
            presentation.design = design_options[0]

        self.orchestrator.update_todo("디자인 시스템 생성", "completed", f"Primary: {presentation.design.primary_color}")

        # 6. 슬라이드 구조 생성
        print("\n📝 Step 6: 슬라이드 구조 생성 [Claude]")
        self.orchestrator.update_todo("슬라이드 구조 생성", "in_progress")
        slides = self.structure_skill.generate_structure(presentation, research_results, context)
        for slide in slides:
            presentation.add_slide(slide)
        self.orchestrator.update_todo("슬라이드 구조 생성", "completed", f"{len(slides)}장 생성")

        # HITL #3: 구조 확인
        slide_summary = "\n".join([f"  {i+1}. {s.content.title}" for i, s in enumerate(presentation.slides)])
        hitl_response = self.orchestrator.request_hitl(HITLRequest(
            question="슬라이드 구조를 확인해주세요. 수정이 필요하면 말씀해주세요.",
            context=f"슬라이드 구성:\n{slide_summary}",
            options=["확인, 진행해주세요", "수정이 필요합니다"]
        ))

        if hitl_response and "수정" in hitl_response:
            modification = self.orchestrator.request_hitl(HITLRequest(
                question="어떤 부분을 수정할까요?",
                required=True
            ))
            if modification:
                context.requirements.append(f"슬라이드 수정: {modification}")
                # 구조 재생성
                presentation.slides = []
                slides = self.structure_skill.generate_structure(presentation, research_results, context)
                for slide in slides:
                    presentation.add_slide(slide)

        # 7. 시각적 품질 평가
        print("\n✅ Step 7: 시각적 품질 평가 [Gemini]")
        self.orchestrator.update_todo("시각적 품질 평가", "in_progress")
        visual_eval = self.design_agent.evaluate_visual_quality(presentation)
        eval_status = "통과" if visual_eval["overall_pass"] else "개선 필요"
        self.orchestrator.update_todo("시각적 품질 평가", "completed", eval_status)

        # 8. PPTX 파일 생성
        print("\n📦 Step 8: PPTX 파일 생성")
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
        print(f"🎨 디자인: Primary {presentation.design.primary_color}")
        print(f"✅ 시각 평가: {eval_status}")

        return output_file

    def _create_phase2_plan(self):
        """Phase 2 실행 계획"""
        self.orchestrator.todos = []
        self.orchestrator.add_todo("사용자 요청 확인 (HITL#1)", "Orchestrator")
        self.orchestrator.add_todo("주제 리서치", "Research Agent [Claude]")
        self.orchestrator.add_todo("디자인 시스템 생성", "Design Agent [Gemini]")
        self.orchestrator.add_todo("슬라이드 구조 생성", "Structure Skill [Claude]")
        self.orchestrator.add_todo("시각적 품질 평가", "Design Agent [Gemini]")
        self.orchestrator.add_todo("PPTX 파일 생성", "Export Skill")


def main():
    """CLI 엔트리포인트"""
    parser = argparse.ArgumentParser(
        description="PPT Agent - AI 기반 PPT 자동 생성 (Multi-LLM)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  ppt-agent "AI 기술 트렌드 2024"
  ppt-agent "스타트업 투자 유치 전략" -o pitch_deck.pptx
  ppt-agent "기후변화 대응 방안" --audience "정책 결정자"

LLM 라우팅:
  - Claude: 논리적 태스크 (리서치, 구조화, Export)
  - Gemini: 시각적 태스크 (디자인, Asset, 시각 평가)
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
        print("   Multi-LLM: Claude + Gemini")
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
