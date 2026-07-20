from app.infrastructure.langsmith.client import langsmith_client
from app.tools.register_tools import register_tools

_initialized = False


def bootstrap():

    global _initialized

    if _initialized:
        return

    register_tools()

    langsmith_client.configure()

    _initialized = True

    print("Application bootstrapped successfully")