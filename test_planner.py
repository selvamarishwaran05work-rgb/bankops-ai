from app.planner.planner import planner
from app.domain.models.investigation_request import InvestigationRequest

request = InvestigationRequest(
    customer_id="C12345",
    issue="Customer reports duplicate debit card transaction yesterday."
)

plan = planner.create_plan(request)

print("=" * 60)
print("PLANNER THOUGHT")
print("=" * 60)
print(plan.thought)

print("\n" + "=" * 60)
print("PLAN STEPS")
print("=" * 60)

for i, step in enumerate(plan.steps, start=1):
    print(f"\nStep {i}")
    print(f"Tool      : {step.tool}")
    print(f"Reason    : {step.reason}")
    print(f"Arguments : {step.arguments}")