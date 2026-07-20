from app.workflow.base_workflow import BaseWorkflow
from app.domain.models.investigation_request import InvestigationRequest
from app.domain.models.investigation_response import InvestigationResponse
from app.services.ai_service import ai_service


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


class LLMWorkflow(BaseWorkflow):

    def execute(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content":
                f"""
Customer ID:
{request.customer_id}

Issue:
{request.issue}
"""
            }
        ]

        answer = ai_service.generate(messages)

        escalation = any(
            word in answer.lower()
            for word in ["fraud", "escalate", "unknown", "uncertain"]
        )

        confidence = 0.9 if not escalation else 0.7

        return InvestigationResponse(
            recommendation=answer,
            confidence=confidence,
            escalation_required=escalation
        )