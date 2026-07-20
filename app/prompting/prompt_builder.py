import json

from app.domain.models.investigation_request import InvestigationRequest


SYSTEM_PROMPT = """
You are an AI Banking Investigation Assistant.

Responsibilities:
- Never hallucinate customer information.
- Never fabricate banking policies.
- Never approve money movement.
- Never initiate transactions.
- Never provide legal advice.
- Base your answers ONLY on the retrieved banking policy and tool outputs.
- If sufficient information is unavailable, clearly state the limitation.
- Escalate ambiguous, fraud, or high-risk cases.
- Produce clear, structured, professional recommendations.
"""


class PromptBuilder:

    def build_messages(
        self,
        request: InvestigationRequest,
        tool_outputs: list,
        conversation_history: list,
    ):
        retrieved_information = self._format_tool_outputs(tool_outputs)

        user_prompt = f"""
Current Investigation

Customer ID:
{request.customer_id}

Issue:
{request.issue}

Use the retrieved investigation data below to answer the user's request.
"""

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "system",
                "content": f"""
Retrieved Investigation Data

{retrieved_information}

Use ONLY the above information while answering.
If the information is insufficient, clearly mention that.
""",
            },
        ]

        for history_item in conversation_history:
            if isinstance(history_item, dict):
                role = history_item.get("role")
                content = history_item.get("content")
            else:
                role = getattr(history_item, "type", None) or getattr(history_item, "role", None)
                content = getattr(history_item, "content", None)

            if role and content is not None:
                normalized_role = str(role).lower()
                mapping = {
                    "human": "user",
                    "ai": "assistant",
                    "assistant": "assistant",
                    "user": "user",
                    "system": "system",
                    "function": "function",
                    "tool": "tool",
                    "developer": "developer",
                }
                messages.append(
                    {
                        "role": mapping.get(normalized_role, normalized_role),
                        "content": content,
                    }
                )

        messages.append(
            {
                "role": "user",
                "content": user_prompt,
            }
        )

        return messages

    def _format_tool_outputs(self, tool_outputs):
        sections = []

        for item in tool_outputs:
            sections.append(f"Tool : {item['tool']}")
            sections.append(f"Reason : {item['reason']}")
            sections.append("Output:")

            if isinstance(item["output"], (dict, list)):
                sections.append(json.dumps(item["output"], indent=2))
            else:
                sections.append(str(item["output"]))

            sections.append("\n---------------------------------\n")

        return "\n".join(sections)


prompt_builder = PromptBuilder()