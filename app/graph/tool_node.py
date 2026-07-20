from app.services.tool_service import tool_service


def tool_node(state):

    plan = state["plan"]

    tool_outputs = []

    if plan is None:
        state["tool_outputs"] = []
        return state

    for step in plan.steps:

        tool_name = step.tool

        arguments = step.arguments or {}

        print(f"\nExecuting Tool : {tool_name}")
        print(arguments)

        try:

            output = tool_service.execute(
                tool_name,
                **arguments
            )

        except Exception as ex:

            output = f"Tool execution failed : {str(ex)}"

        tool_outputs.append(
            {
                "tool": tool_name,
                "reason": step.reason,
                "arguments": arguments,
                "output": output
            }
        )

    state["tool_outputs"] = tool_outputs

    return state