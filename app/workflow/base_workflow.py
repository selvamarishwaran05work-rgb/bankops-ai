from abc import ABC, abstractmethod

from app.domain.models.investigation_request import InvestigationRequest
from app.domain.models.investigation_response import InvestigationResponse


class BaseWorkflow(ABC):

    @abstractmethod
    def execute(
        self,
        request: InvestigationRequest,
    ) -> InvestigationResponse:
        pass