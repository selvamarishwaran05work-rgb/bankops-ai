from app.planner.planner import planner


def planner_node(state):
    request = state["request"]

    plan = planner.create_plan(request)

    state["plan"] = plan

    return state