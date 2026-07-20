from app.tools.tool_registry import tool_registry
from app.tools.knowledge_tool import tool as knowledge_tool
from app.tools.transaction_tool import TransactionTool
from app.tools.customer_tool import CustomerTool


def register_tools():

    if tool_registry.list_tools():
        return

    tool_registry.register(knowledge_tool)
    tool_registry.register(TransactionTool())
    tool_registry.register(CustomerTool())


