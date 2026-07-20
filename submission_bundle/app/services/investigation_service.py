import json
import time
from pathlib import Path

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from app.domain.models.investigation_request import InvestigationRequest
from app.graph.graph_builder import graph


class InvestigationService:

    def investigate(
        self,
        request,
        thread_id,
    ):

        state = self._load_or_initialize_state(request, thread_id)
        state["request"] = request
        state["messages"].append(HumanMessage(content=request.issue))

        config = {
            "configurable": {
                "thread_id": thread_id
            }
        }

        start = time.perf_counter()

        result = graph.invoke(
            state,
            config=config
        )

        latency = time.perf_counter() - start

        result["latency"] = latency
        result["thread_id"] = thread_id
        result["checkpoint"] = self.get_checkpoint_summary(thread_id)

        self._save_state(thread_id, result)

        return result

    def get_checkpoint_summary(self, thread_id):
        checkpoint_path = self._checkpoint_path(thread_id)
        summary = {
            "thread_id": thread_id,
            "checkpoint_id": None,
            "message_count": 0,
            "history_count": 0,
            "path": str(checkpoint_path),
        }

        if checkpoint_path.exists():
            try:
                payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
                summary["message_count"] = len(payload.get("messages", []))
                summary["history_count"] = 1
                summary["checkpoint_id"] = payload.get("thread_id")
                summary["status"] = "loaded"
            except Exception as exc:
                summary["error"] = str(exc)
        else:
            summary["status"] = "not_started"

        return summary

    def _checkpoint_path(self, thread_id):
        root = Path(__file__).resolve().parents[2]
        checkpoint_dir = root / "data" / "checkpoints"
        checkpoint_dir.mkdir(parents=True, exist_ok=True)
        safe_thread_id = str(thread_id).replace("/", "_").replace("\\", "_")
        return checkpoint_dir / f"{safe_thread_id}.json"

    def get_thread_state(self, thread_id):
        checkpoint_path = self._checkpoint_path(thread_id)
        if not checkpoint_path.exists():
            return None

        try:
            payload = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            return {
                "request": InvestigationRequest(
                    customer_id=payload.get("request", {}).get("customer_id", ""),
                    issue=payload.get("request", {}).get("issue", ""),
                ),
                "messages": [
                    self._deserialize_message(message)
                    for message in payload.get("messages", [])
                ],
                "plan": payload.get("plan"),
                "tool_outputs": payload.get("tool_outputs", []),
                "response": payload.get("response"),
                "confidence": payload.get("confidence"),
                "latency": payload.get("latency"),
                "escalation_required": payload.get("escalation_required", False),
            }
        except Exception:
            return None

    def _load_or_initialize_state(self, request, thread_id):
        existing_state = self.get_thread_state(thread_id)
        if existing_state is not None:
            return existing_state

        return {
            "request": request,
            "messages": [HumanMessage(content=request.issue)],
            "plan": None,
            "tool_outputs": [],
            "response": None,
            "confidence": None,
            "latency": None,
            "escalation_required": False,
        }

    def _save_state(self, thread_id, result):
        checkpoint_path = self._checkpoint_path(thread_id)
        payload = {
            "thread_id": thread_id,
            "request": self._to_jsonable(result.get("request")),
            "messages": self._serialize_messages(result.get("messages", [])),
            "plan": self._to_jsonable(result.get("plan")),
            "tool_outputs": self._to_jsonable(result.get("tool_outputs", [])),
            "response": result.get("response"),
            "confidence": result.get("confidence"),
            "latency": result.get("latency"),
            "escalation_required": result.get("escalation_required", False),
        }
        checkpoint_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    def _serialize_messages(self, messages):
        serialized = []
        for message in messages or []:
            if hasattr(message, "type") or hasattr(message, "role"):
                role = getattr(message, "type", None) or getattr(message, "role", None)
                content = getattr(message, "content", "")
                if role and content is not None:
                    serialized.append({"role": self._normalize_role(role), "content": content})
            elif isinstance(message, dict):
                role = message.get("role")
                content = message.get("content")
                if role and content is not None:
                    serialized.append({"role": self._normalize_role(role), "content": content})
        return serialized

    def _deserialize_message(self, message):
        role = self._normalize_role(message.get("role", "human"))
        content = message.get("content", "")

        if role == "assistant":
            return AIMessage(content=content)
        if role == "system":
            return SystemMessage(content=content)
        return HumanMessage(content=content)

    def _normalize_role(self, role):
        normalized = str(role).lower()
        mapping = {
            "human": "user",
            "ai": "assistant",
            "assistant": "assistant",
            "user": "user",
            "system": "system",
        }
        return mapping.get(normalized, normalized)

    def _to_jsonable(self, value):
        if hasattr(value, "model_dump"):
            return value.model_dump()
        if hasattr(value, "dict"):
            return value.dict()
        if isinstance(value, dict):
            return {key: self._to_jsonable(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._to_jsonable(item) for item in value]
        return value


investigation_service = InvestigationService()