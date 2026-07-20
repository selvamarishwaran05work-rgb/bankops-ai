from app.planner.planner import planner
from langchain_core.messages import HumanMessage



def planner_node(state):

    request = state["request"]

    state["messages"].append(
    HumanMessage(content=request.issue)
)

    plan = planner.create_plan(request)

    state["plan"] = plan

    return state