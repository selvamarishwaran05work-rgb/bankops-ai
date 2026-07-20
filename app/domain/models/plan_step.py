from pydantic import BaseModel
from typing import Dict, Any


class PlanStep(BaseModel):
    tool: str
    reason: str
    arguments: Dict[str, Any]