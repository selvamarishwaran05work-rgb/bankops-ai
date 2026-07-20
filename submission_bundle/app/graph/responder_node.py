from langchain_core.messages import AIMessage

from app.prompting.prompt_builder import prompt_builder
from app.services.ai_service import ai_service


def responder_node(state):

    # -----------------------------------------
    # Build final prompt
    # -----------------------------------------

    messages = prompt_builder.build_messages(
        request=state["request"],
        tool_outputs=state["tool_outputs"],
        conversation_history=state["messages"]
    )

    # -----------------------------------------
    # Generate answer
    # -----------------------------------------

    answer = ai_service.generate(
        messages=messages
    )

    # -----------------------------------------
    # Store response
    # -----------------------------------------

    state["response"] = answer

    # -----------------------------------------
    # Simple confidence calculation
    # -----------------------------------------

    answer_lower = answer.lower()

    confidence = 0.95

    if any(
        word in answer_lower
        for word in [
            "uncertain",
            "unknown",
            "insufficient",
            "unable",
            "cannot determine",
            "not enough information"
        ]
    ):
        confidence = 0.70

    # -----------------------------------------
    # Escalation detection
    # -----------------------------------------

    escalation = any(
        word in answer_lower
        for word in [
            "fraud",
            "escalate",
            "aml",
            "compliance",
            "high risk",
            "suspicious"
        ]
    )

    state["confidence"] = confidence
    state["escalation_required"] = escalation

    # -----------------------------------------
    # Save assistant response into memory
    # -----------------------------------------

    state["messages"].append(
        AIMessage(
            content=answer
        )
    )

    return state