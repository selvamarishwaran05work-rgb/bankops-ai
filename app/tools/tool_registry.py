from app.tools.customer_tool import CustomerTool
from app.tools.knowledge_tool import tool as knowledge_tool
from app.tools.transaction_tool import TransactionTool


class ToolRegistry:

    def __init__(self):
        self.tools = {}

    def register(self, tool):
        definition = getattr(tool, "definition", None)
        if definition is None:
            raise AttributeError(f"Tool {tool} does not define a definition")

        name = definition.get("name")
        if not name:
            raise ValueError(f"Tool definition for {tool} is missing a name")

        self.tools[name] = tool

    def get(self, tool_name):
        return self.tools.get(tool_name)

    def list_tools(self):
        return list(self.tools.values())


tool_registry = ToolRegistry()