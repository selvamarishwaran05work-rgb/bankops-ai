from app.workflow.base_workflow import BaseWorkflow
from app.domain.models.investigation_request import InvestigationRequest
from app.domain.models.investigation_response import InvestigationResponse
from app.services.ai_service import ai_service
from app.services.knowledge_service import knowledge_service
from app.prompting.prompt_builder import prompt_builder
from app.services.tool_service import tool_service
from app.planner.planner import planner
from app.graph.graph_builder import graph

SYSTEM_PROMPT = """
You are an AI Banking Investigation Assistant.

Your responsibilities:
- Understand banking investigation requests.
- Never hallucinate customer information.
- Never approve transactions.
- Never move money.
- Recommend investigation steps.
- Escalate ambiguous or risky cases.
Return concise recommendations.
"""


from app.services.investigation_service import investigation_service


class LLMWorkflow(BaseWorkflow):

    def execute(self, request):

        result = investigation_service.investigate(request)

        return InvestigationResponse(
            recommendation=result["response"],
            confidence=0.9,
            escalation_required=False
        )