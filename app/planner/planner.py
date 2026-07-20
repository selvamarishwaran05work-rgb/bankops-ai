import json

from app.domain.models.execution_plan import ExecutionPlan
from app.services.ai_service import ai_service
from app.prompting.tool_prompt_builder import tool_prompt_builder
from app.services.tool_service import tool_service
from app.services.feedback_service import feedback_service
import app.tools.register_tools
from langsmith import traceable  
class Planner:
    @traceable(name="Planner")
    def create_plan(self, request) -> ExecutionPlan:

        tool_definitions = tool_service.get_tool_definitions()

        tool_prompt = tool_prompt_builder.build(tool_definitions)
        feedback = feedback_service.get_recent_feedback()
        negative = len(
            [
                x for x in feedback
                if x["rating"] == "negative"
            ]
        )

        positive = len(
            [
                x for x in feedback
                if x["rating"] == "positive"
            ]
        )

        adaptive_prompt = ""

        if negative > positive:

            adaptive_prompt = """
        Recent users reported that previous investigation plans were not detailed enough.

        Generate:
        - More detailed plans
        - Clear reasoning
        - Fewer unnecessary tool calls
        - Better structured execution steps.
        """
        system_prompt = f"""
You are an AI Planning Agent for a Banking Investigation System.

Your ONLY responsibility is planning.

DO NOT answer the customer.

{tool_prompt}
{adaptive_prompt}
IMPORTANT RULES

1. You MUST choose ONLY from the available tool names.
2. Never invent tool names.
3. Never leave the tool field empty.
4. Use the minimum number of tools required.
5. Do NOT perform the investigation.
6. Your only job is to produce an execution plan.

Return ONLY valid JSON.

Schema

{{
    "thought":"High level reasoning",

    "steps":[
        {{
            "tool":"search_bank_policy",

            "reason":"Why this tool is required",

            "arguments":{{}}
        }}
    ]
}}
"""

        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"""
    Customer ID:
    {request.customer_id}

    Issue:
    {request.issue}
    """
            }
        ]

        response = ai_service.generate(messages=messages)

        print("\n===== RAW LLM RESPONSE =====")
        print(response)
        print("============================\n")

        try:
            plan_dict = json.loads(response)
            return ExecutionPlan.model_validate(plan_dict)

        except Exception as ex:
            raise Exception(
                f"Planner returned invalid response.\n\n{response}"
            ) from ex


planner = Planner()