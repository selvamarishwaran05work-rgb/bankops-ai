from app.infrastructure.ai.gateway import ai_gateway
from app.config.settings import settings


class AIService:

    def __init__(self):
        self.client = ai_gateway.get_client()

    def generate(
        self,
        messages,
        model=None,
        temperature=None,
        max_tokens=None,
        response_format=None,
    ):
        params = {
            "model": model or settings.chat_model,
            "messages": messages,
        }

        if temperature is not None:
            params["temperature"] = temperature

        response = self.client.chat.completions.create(**params)
        return response.choices[0].message.content


ai_service = AIService()