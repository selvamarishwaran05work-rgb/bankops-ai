from app.ingestion.embedding_service import embedding_service
from app.infrastructure.vectorstore.pinecone_client import pinecone_client


class KnowledgeService:

    def __init__(self):
        self.index = pinecone_client.get_index()

    def search(self, query, top_k=3):

        embedding = embedding_service.create_embedding(query)

        results = self.index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )

        contexts = []

        for match in results.matches:
            contexts.append(match.metadata["text"])

        return "\n\n".join(contexts)


knowledge_service = KnowledgeService()