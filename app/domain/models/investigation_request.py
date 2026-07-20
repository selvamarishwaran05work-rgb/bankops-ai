from pydantic import BaseModel


class InvestigationRequest(BaseModel):

    customer_id: str

    issue: str