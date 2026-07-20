from openai import OpenAI

from app.config.settings import settings


class AIGateway:
    """
    Creates and manages OpenAI-compatible clients.
    """

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )

    def get_client(self):
        return self.client


ai_gateway = AIGateway()