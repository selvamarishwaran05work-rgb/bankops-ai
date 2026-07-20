import uuid
from pathlib import Path

import streamlit as st

from app.startup.bootstrap import bootstrap
from app.domain.models.investigation_request import InvestigationRequest
from app.services.investigation_service import investigation_service
from app.services.feedback_service import feedback_service

bootstrap()

st.set_page_config(page_title="BankOps AI", page_icon="🏦", layout="wide")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

CHECKPOINT_DIR = Path("data/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def list_threads():
    if not CHECKPOINT_DIR.exists():
        return []
    return sorted(
        [p.stem for p in CHECKPOINT_DIR.glob("*.json") if p.is_file()],
        reverse=True,
    )


st.title("🏦 BankOps AI Investigation Console")
st.caption("Resume a prior case, continue a conversation, or start a fresh investigation.")

with st.sidebar:
    st.header("Conversation")
    thread_options = list_threads()
    if thread_options:
        selected_thread = st.selectbox(
            "Select a conversation to resume",
            options=thread_options,
            index=thread_options.index(st.session_state.thread_id) if st.session_state.thread_id in thread_options else 0,
        )
        if selected_thread != st.session_state.thread_id:
            st.session_state.thread_id = selected_thread
            st.rerun()
    else:
        st.info("No saved conversations yet.")

    if st.button("🆕 New Conversation"):
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

    st.divider()
    st.subheader("🗂 Checkpoint")
    checkpoint_summary = investigation_service.get_checkpoint_summary(st.session_state.thread_id)
    st.json(checkpoint_summary)

customer = st.text_input("Customer ID")
issue = st.text_area("Describe the investigation request", height=120)

if st.button("Investigate", use_container_width=True):
    request = InvestigationRequest(customer_id=customer, issue=issue)
    result = investigation_service.investigate(request=request, thread_id=st.session_state.thread_id)

    st.subheader("💬 Conversation")
    for message in result.get("messages", []):
        if hasattr(message, "type"):
            role = message.type
            content = message.content
        else:
            role = message.get("role", "assistant")
            content = message.get("content", "")

        if role in {"assistant", "ai", "system"}:
            with st.chat_message("assistant"):
                st.write(content)
        else:
            with st.chat_message("user"):
                st.write(content)

    st.subheader("🧠 Planner Thought")
    if result.get("plan"):
        st.info(result["plan"].thought)

    st.subheader("📋 Execution Plan")
    if result.get("plan"):
        for index, step in enumerate(result["plan"].steps, start=1):
            with st.expander(f"Step {index}: {step.tool}"):
                st.write("**Reason**")
                st.write(step.reason)
                st.write("**Arguments**")
                st.json(step.arguments)

    st.subheader("🛠 Tool Outputs")
    for output in result.get("tool_outputs", []):
        with st.expander(output["tool"]):
            st.write(output["output"])

    st.subheader("✅ Final Recommendation")
    st.success(result["response"])

    st.subheader("📈 Investigation Metrics")
    if result.get("checkpoint"):
        with st.expander("🗂 Checkpoint Details"):
            st.json(result["checkpoint"])

    confidence = result.get("confidence") or 0.0
    latency = result.get("latency") or 0.0
    escalation = result.get("escalation_required") or False

    col1, col2, col3 = st.columns(3)
    col1.metric("Confidence", f"{confidence:.0%}")
    col2.metric("Latency", f"{latency:.2f} sec")
    col3.metric("Escalation", "Yes" if escalation else "No")

    st.divider()
    st.subheader("⭐ Feedback")
    col1, col2 = st.columns(2)
    if col1.button("👍 Helpful"):
        feedback_service.add_feedback({"customer": customer, "issue": issue, "rating": "positive"})
        st.success("Feedback saved.")
    if col2.button("👎 Not Helpful"):
        feedback_service.add_feedback({"customer": customer, "issue": issue, "rating": "negative"})
        st.success("Feedback saved.")

    feedback = feedback_service.get_recent_feedback()
    positive = len([x for x in feedback if x["rating"] == "positive"])
    negative = len([x for x in feedback if x["rating"] == "negative"])
    c1, c2 = st.columns(2)
    c1.metric("👍 Positive", positive)
    c2.metric("👎 Negative", negative)
    if negative > positive:
        st.warning("Adaptive behavior is being tuned from recent negative feedback.")
    else:
        st.success("Adaptive behavior is currently performing well.")
