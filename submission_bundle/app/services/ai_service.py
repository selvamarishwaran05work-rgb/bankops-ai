from app.infrastructure.ai.gateway import ai_gateway
from app.config.settings import settings
from langsmith import traceable



class AIService:

    def __init__(self):
        self.client = ai_gateway.get_client()

    @traceable(name="AI Generation")
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

        try:
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as exc:
            fallback = "I’m unable to generate a response right now because the AI service is unavailable."
            if "temperature" in str(exc) and "unsupported" in str(exc).lower():
                params.pop("temperature", None)
                response = self.client.chat.completions.create(**params)
                return response.choices[0].message.content
            raise RuntimeError(f"AI generation failed: {exc}") from exc

ai_service = AIService()