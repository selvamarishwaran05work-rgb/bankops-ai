import json
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

from app.startup.bootstrap import bootstrap
from app.domain.models.investigation_request import InvestigationRequest
from app.services.investigation_service import investigation_service
from app.services.feedback_service import feedback_service

bootstrap()

st.set_page_config(page_title="BankOps AI", page_icon="🏦", layout="wide")

CHECKPOINT_DIR = Path("data/checkpoints")
CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)


def list_threads():
    if not CHECKPOINT_DIR.exists():
        return []
    return sorted(
        [p.stem for p in CHECKPOINT_DIR.glob("*.json") if p.is_file()],
        reverse=True,
    )


def load_thread_meta(thread_id):
    checkpoint_path = CHECKPOINT_DIR / f"{thread_id}.json"
    if not checkpoint_path.exists():
        return {"preview": "No activity yet", "updated_at": "New", "message_count": 0, "customer_id": "-"}

    try:
        payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        request = payload.get("request", {}) or {}
        customer_id = request.get("customer_id") or "-"
        messages = payload.get("messages", [])
        preview = ""
        if messages:
            last_message = messages[-1]
            preview = last_message.get("content", "")
            if len(preview) > 70:
                preview = preview[:67] + "..."
        updated_at = "Saved"
        if checkpoint_path.exists():
            updated_at = datetime.fromtimestamp(checkpoint_path.stat().st_mtime).strftime("%b %d, %H:%M")
        return {
            "preview": preview or "No activity yet",
            "updated_at": updated_at,
            "message_count": len(messages),
            "customer_id": customer_id,
        }
    except Exception:
        return {"preview": "Unavailable", "updated_at": "Unknown", "message_count": 0, "customer_id": "-"}


def get_thread_status(meta, is_active):
    if is_active:
        return {"label": "Open", "color": "#247a3d", "bg": "#e8f5e9"}
    if meta.get("message_count", 0) >= 4:
        return {"label": "Completed", "color": "#6a3d9a", "bg": "#efe7fa"}
    return {"label": "Open", "color": "#247a3d", "bg": "#e8f5e9"}


def get_thread_avatar(meta, is_active):
    if is_active:
        return "💬"
    if meta.get("customer_id", "-") != "-":
        return "🏦"
    return "🗂"


def render_adaptive_insights():
    insights = feedback_service.get_feedback_insights()
    positive = insights["positive_count"]
    negative = insights["negative_count"]

    st.subheader("📈 Adaptive Insights")
    c1, c2, c3 = st.columns(3)
    c1.metric("👍 Positive", positive)
    c2.metric("👎 Negative", negative)
    c3.metric("🧠 Summary", insights["adaptive_summary"])

    if insights["recent_comments"]:
        st.caption("Recent feedback comments")
        for entry in insights["recent_comments"]:
            with st.container():
                st.caption(f"{entry['rating'].title()} · {entry['customer']}")
                st.write(entry["comment"])


def render_thread_state(thread_state):
    if not thread_state:
        return

    st.success("Resume point loaded from the last saved checkpoint")
    st.caption("You can continue this investigation from the previously saved context below.")

    st.subheader("💬 Conversation History")
    for message in thread_state.get("messages", []):
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

    plan = thread_state.get("plan")
    if plan:
        st.subheader("🧠 Last Planner Context")
        thought = None
        steps = []

        if hasattr(plan, "thought"):
            thought = plan.thought
            steps = getattr(plan, "steps", []) or []
        elif isinstance(plan, dict):
            thought = plan.get("thought")
            steps = plan.get("steps", []) or []

        if thought:
            st.info(f"Planner summary: {thought}")
        elif plan:
            st.info("Planner details were saved but could not be rendered as structured text.")

        if steps:
            st.caption("Continue from the last planned step")
            for index, step in enumerate(steps, start=1):
                tool_name = None
                reason = None
                arguments = {}
                if hasattr(step, "tool"):
                    tool_name = step.tool
                    reason = getattr(step, "reason", None)
                    arguments = getattr(step, "arguments", {}) or {}
                elif isinstance(step, dict):
                    tool_name = step.get("tool")
                    reason = step.get("reason")
                    arguments = step.get("arguments", {}) or {}

                if tool_name:
                    with st.expander(f"Step {index}: {tool_name}"):
                        if reason:
                            st.write("**Reason**")
                            st.write(reason)
                        if arguments:
                            st.write("**Arguments**")
                            st.json(arguments)

    if thread_state.get("tool_outputs"):
        st.subheader("🛠 Tool Outputs")
        for output in thread_state.get("tool_outputs", []):
            with st.expander(output["tool"]):
                st.write(output["output"])

    if thread_state.get("response"):
        st.subheader("✅ Final Recommendation")
        st.success(thread_state["response"])

    if thread_state.get("confidence") is not None or thread_state.get("latency") is not None or thread_state.get("escalation_required") is not None:
        st.subheader("📈 Investigation Metrics")
        confidence = thread_state.get("confidence") or 0.0
        latency = thread_state.get("latency") or 0.0
        escalation = thread_state.get("escalation_required") or False
        col1, col2, col3 = st.columns(3)
        col1.metric("Confidence", f"{confidence:.0%}")
        col2.metric("Latency", f"{latency:.2f} sec")
        col3.metric("Escalation", "Yes" if escalation else "No")


if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "thread_created" not in st.session_state:
    st.session_state.thread_created = False

if "dashboard_view" not in st.session_state:
    st.session_state.dashboard_view = "investigate"


st.title("🏦 BankOps AI Investigation Console")
st.caption("Resume a prior case, continue a conversation, or start a fresh investigation.")

nav_col1, nav_col2 = st.columns([1, 1])
with nav_col1:
    if st.button("🧭 Dashboard", use_container_width=True, type="secondary"):
        st.session_state.dashboard_view = "dashboard"
with nav_col2:
    if st.button("🧠 Investigate", use_container_width=True, type="primary"):
        st.session_state.dashboard_view = "investigate"

st.divider()

st.markdown(
    """
    <style>
    div[data-testid="stSidebar"] .stButton > button {
        border: 1px solid #dfe3e8;
        border-radius: 12px;
        padding: 0.55rem 0.7rem;
        background: #ffffff;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.05);
    }
    div[data-testid="stSidebar"] .stButton > button:hover {
        border-color: #4f46e5;
        box-shadow: 0 4px 10px rgba(79, 70, 229, 0.12);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Conversation")
    thread_options = list_threads()

    if thread_options:
        st.caption("Saved conversations")
        thread_summaries = []
        for thread_id in thread_options:
            meta = load_thread_meta(thread_id)
            thread_summaries.append((thread_id, meta))

        thread_summaries.sort(key=lambda item: item[1]["updated_at"], reverse=True)

        for thread_id, meta in thread_summaries:
            is_active = thread_id == st.session_state.thread_id
            status = get_thread_status(meta, is_active)
            avatar = get_thread_avatar(meta, is_active)
            st.markdown(
                f"""
                <div style="border:1px solid #e2e8f0; border-radius:14px; padding:10px 12px; margin:6px 0 10px; background:linear-gradient(145deg, #fbfdff, #f5f7fb); box-shadow:0 2px 6px rgba(15,23,42,0.04);">
                  <div style="display:flex; align-items:center; gap:10px; margin-bottom:7px;">
                    <div style="width:34px; height:34px; border-radius:999px; display:flex; align-items:center; justify-content:center; background:{status['bg']}; font-size:1rem;">{avatar}</div>
                    <div style="flex:1; min-width:0;">
                      <div style="font-weight:700; font-size:0.95rem;">{thread_id[:8]}...</div>
                      <div style="font-size:0.76rem; color:#64748b;">{meta['updated_at']} · {meta['message_count']} msgs</div>
                    </div>
                    <span style="padding:4px 8px; border-radius:999px; background:{status['bg']}; color:{status['color']}; font-size:0.72rem; font-weight:700;">{status['label']}</span>
                  </div>
                  <div style="font-size:0.84rem; color:#334155; line-height:1.35; margin-bottom:7px;">{meta['preview']}</div>
                  <div style="font-size:0.74rem; color:#64748b;">Customer: {meta['customer_id']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(
                f"Open thread",
                key=f"thread_{thread_id}",
                use_container_width=True,
            ):
                st.session_state.thread_id = thread_id
                st.session_state.thread_created = True
                st.session_state.dashboard_view = "investigate"
                st.rerun()
    else:
        st.info("No saved conversations yet.")

    st.divider()
    if st.button("🆕 New Conversation", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.thread_created = False
        st.session_state.dashboard_view = "investigate"
        st.rerun()

    st.divider()
    st.subheader("🗂 Current Thread")
    st.code(st.session_state.thread_id)
    checkpoint_summary = investigation_service.get_checkpoint_summary(st.session_state.thread_id)
    st.json(checkpoint_summary)

if st.session_state.dashboard_view == "dashboard":
    st.subheader("📊 Resume Dashboard")
    st.caption("Select an existing conversation to reopen it and continue from the last saved checkpoint.")

    thread_options = list_threads()
    if not thread_options:
        st.info("No saved conversations are available yet.")
        st.stop()

    for thread_id in thread_options:
        meta = load_thread_meta(thread_id)
        is_active = thread_id == st.session_state.thread_id
        status = get_thread_status(meta, is_active)
        avatar = get_thread_avatar(meta, is_active)
        with st.container():
            st.markdown(
                f"""
                <div style="border:1px solid #dbeafe; border-radius:16px; padding:14px; margin-bottom:12px; background:linear-gradient(135deg, #f8fbff, #eef5ff);">
                  <div style="display:flex; align-items:center; gap:10px; margin-bottom:8px;">
                    <div style="width:42px; height:42px; border-radius:50%; display:flex; align-items:center; justify-content:center; background:{status['bg']}; font-size:1.1rem;">{avatar}</div>
                    <div style="flex:1;">
                      <div style="font-weight:700;">{thread_id}</div>
                      <div style="font-size:0.84rem; color:#64748b;">{meta['updated_at']} · {meta['message_count']} messages</div>
                    </div>
                    <span style="padding:5px 9px; border-radius:999px; background:{status['bg']}; color:{status['color']}; font-size:0.75rem; font-weight:700;">{status['label']}</span>
                  </div>
                  <div style="font-size:0.95rem; color:#334155; margin-bottom:10px;">{meta['preview']}</div>
                  <div style="font-size:0.84rem; color:#64748b; margin-bottom:10px;">Customer: {meta['customer_id']}</div>
                  <div style="display:flex; gap:8px; flex-wrap:wrap;">
                    <a href="#" onclick="window.location.reload()"> </a>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button(f"Resume {thread_id[:8]}...", key=f"resume_{thread_id}", use_container_width=False):
                st.session_state.thread_id = thread_id
                st.session_state.thread_created = True
                st.session_state.dashboard_view = "investigate"
                st.rerun()

    render_adaptive_insights()
    st.stop()

saved_state = investigation_service.get_thread_state(st.session_state.thread_id)
customer_value = ""
issue_value = ""
if saved_state and saved_state.get("request"):
    customer_value = saved_state["request"].customer_id or ""
    issue_value = saved_state["request"].issue or ""

render_thread_state(saved_state)

customer = st.text_input("Customer ID", value=customer_value)
issue = st.text_area("Describe the investigation request", height=120, value=issue_value)

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
    feedback_note = st.text_area("Share your feedback comment", height=80, placeholder="Tell us what was helpful or what should improve")
    col1, col2 = st.columns(2)
    if col1.button("👍 Helpful"):
        feedback_service.add_feedback({
            "customer": customer,
            "issue": issue,
            "rating": "positive",
            "comment": feedback_note or "Helpful response",
        })
        st.success("Feedback saved.")
    if col2.button("👎 Not Helpful"):
        feedback_service.add_feedback({
            "customer": customer,
            "issue": issue,
            "rating": "negative",
            "comment": feedback_note or "Needs improvement",
        })
        st.success("Feedback saved.")

    insights = feedback_service.get_feedback_insights()
    positive = insights["positive_count"]
    negative = insights["negative_count"]
    render_adaptive_insights()

    if negative > positive:
        st.warning("Adaptive behavior is being tuned from recent negative feedback.")
    else:
        st.success("Adaptive behavior is currently performing well.")
