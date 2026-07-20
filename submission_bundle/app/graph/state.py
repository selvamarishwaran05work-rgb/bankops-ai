from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages
from app.domain.models.investigation_request import InvestigationRequest
from app.domain.models.execution_plan import ExecutionPlan


class GraphState(TypedDict):
    request: InvestigationRequest
    messages: Annotated[list, add_messages]
    plan: ExecutionPlan | None
    tool_outputs: list
    response: str | None
    latency: float | None
    confidence: float | None
    escalation_required: bool