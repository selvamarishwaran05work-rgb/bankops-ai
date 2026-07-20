from app.graph.graph_builder import graph
from app.domain.models.investigation_request import InvestigationRequest

request = InvestigationRequest(
    customer_id="C12345",
    issue="Customer reports duplicate debit card transaction yesterday."
)

state = {
    "request": request,
    "messages": [],
    "plan": None,
    "tool_outputs": [],
    "response": None
}

result = graph.invoke(state)

print("\n========== FINAL RESPONSE ==========\n")
print(result["response"])