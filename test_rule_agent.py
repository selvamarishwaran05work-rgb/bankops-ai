from app.application.investigation_controller import InvestigationController
from app.domain.models.investigation_request import InvestigationRequest

controller = InvestigationController()

request = InvestigationRequest(
    customer_id="C12345",
    issue="Customer reports duplicate debit card transaction yesterday."
)

response = controller.investigate(request)

print(response.model_dump())