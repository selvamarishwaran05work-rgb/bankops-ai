from fastapi import FastAPI

from app.services.investigation_service import investigation_service
from app.domain.models.investigation_request import InvestigationRequest
from fastapi import FastAPI

from app.startup.bootstrap import bootstrap

bootstrap()

app = FastAPI()


@app.post("/investigate")
def investigate(request: InvestigationRequest):

    result = investigation_service.investigate(request)

    return {
        "planner": result["plan"].thought,
        "tool_outputs": result["tool_outputs"],
        "response": result["response"]
    }