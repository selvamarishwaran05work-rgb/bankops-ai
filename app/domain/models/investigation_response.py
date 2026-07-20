from pydantic import BaseModel


class InvestigationResponse(BaseModel):

    recommendation: str

    confidence: float

    escalation_required: bool