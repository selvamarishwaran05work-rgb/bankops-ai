from openai import OpenAI

from app.config.settings import settings


class EmbeddingService:

    def __init__(self):

        self.client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )

    def create_embedding(self, text):

        response = self.client.embeddings.create(
            model=settings.embedding_model,
            input=text
        )

        return response.data[0].embedding


embedding_service = EmbeddingService()