from langchain_core.messages import AIMessage, HumanMessage

from app.domain.models.investigation_request import InvestigationRequest
from app.services.investigation_service import investigation_service


def test_get_thread_state_returns_persisted_messages(tmp_path, monkeypatch):
    thread_id = "resume-thread"
    monkeypatch.setattr(investigation_service, "_checkpoint_path", lambda _: tmp_path / f"{thread_id}.json")

    request = InvestigationRequest(customer_id="C100", issue="Check this case")
    investigation_service._save_state(
        thread_id,
        {
            "request": request,
            "messages": [HumanMessage(content="Check this case"), AIMessage(content="I am reviewing it")],
            "plan": None,
            "tool_outputs": [],
            "response": "Resolved",
            "confidence": 0.82,
            "latency": 1.2,
            "escalation_required": False,
        },
    )

    state = investigation_service.get_thread_state(thread_id)

    assert state["request"].customer_id == "C100"
    assert len(state["messages"]) == 2
    assert state["messages"][0].content == "Check this case"
    assert state["messages"][1].content == "I am reviewing it"
