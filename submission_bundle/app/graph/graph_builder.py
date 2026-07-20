from pathlib import Path

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.graph.state import GraphState
from app.graph.planner_node import planner_node
from app.graph.tool_node import tool_node
from app.graph.responder_node import responder_node

builder = StateGraph(GraphState)

builder.add_node("planner", planner_node)
builder.add_node("tools", tool_node)
builder.add_node("responder", responder_node)

builder.set_entry_point("planner")

builder.add_edge("planner", "tools")
builder.add_edge("tools", "responder")
builder.add_edge("responder", END)

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CHECKPOINT_DB = PROJECT_ROOT / "data" / "checkpoints.sqlite"
CHECKPOINT_DB.parent.mkdir(parents=True, exist_ok=True)

checkpointer = MemorySaver()

graph = builder.compile(
    checkpointer=checkpointer
)