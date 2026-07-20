from pydantic import BaseModel
from typing import List

from app.domain.models.plan_step import PlanStep


class ExecutionPlan(BaseModel):
    thought: str
    steps: List[PlanStep]