from app.workflow.base_workflow import BaseWorkflow
from app.domain.models.investigation_request import InvestigationRequest
from app.domain.models.investigation_response import InvestigationResponse


class RuleBasedWorkflow(BaseWorkflow):

    def execute(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:

        issue = request.issue.lower()

        if "duplicate" in issue:

            return InvestigationResponse(
                recommendation=(
                    "Check yesterday's debit card transactions "
                    "and verify duplicate entries."
                ),
                confidence=0.70,
                escalation_required=False,
            )

        if "fraud" in issue:

            return InvestigationResponse(
                recommendation=(
                    "Potential fraud detected. Escalate immediately "
                    "to the Fraud Investigation Team."
                ),
                confidence=0.90,
                escalation_required=True,
            )

        return InvestigationResponse(
            recommendation=(
                "Unable to determine investigation path. "
                "Escalate to a Customer Service Representative."
            ),
            confidence=0.30,
            escalation_required=True,
        )