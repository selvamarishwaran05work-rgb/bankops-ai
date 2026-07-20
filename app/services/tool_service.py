from app.tools.tool_registry import tool_registry


class ToolService:

    def execute(self, tool_name, **kwargs):

        tool = tool_registry.get(tool_name)

        if tool is None:
            raise Exception(f"Tool '{tool_name}' not found.")

        return tool.execute(**kwargs)

    def get_tool_definitions(self):

        return [
            tool.definition
            for tool in tool_registry.list_tools()
        ]


tool_service = ToolService()