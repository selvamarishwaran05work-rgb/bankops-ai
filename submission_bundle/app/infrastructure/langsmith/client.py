import os

from app.config.settings import settings


class LangSmithClient:

    def configure(self):

        if not settings.langsmith_api_key:
            print("LangSmith disabled")
            return

        os.environ["LANGCHAIN_TRACING_V2"] = (
            str(settings.langsmith_tracing).lower()
        )

        os.environ["LANGCHAIN_API_KEY"] = (
            settings.langsmith_api_key
        )

        os.environ["LANGCHAIN_PROJECT"] = (
            settings.langsmith_project
        )

        print("LangSmith configured")


langsmith_client = LangSmithClient()