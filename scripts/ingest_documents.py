import uuid

from app.ingestion.document_loader import document_loader
from app.ingestion.chunking_service import chunking_service
from app.ingestion.embedding_service import embedding_service
from app.infrastructure.vectorstore.pinecone_client import pinecone_client

documents = document_loader.load_documents("data/policies")

index = pinecone_client.get_index()

for doc in documents:

    chunks = chunking_service.split(doc["content"])

    for i, chunk in enumerate(chunks):

        embedding = embedding_service.create_embedding(chunk)

        index.upsert(
            vectors=[
                {
                    "id": str(uuid.uuid4()),
                    "values": embedding,
                    "metadata": {
                        "document": doc["filename"],
                        "chunk": i,
                        "text": chunk
                    }
                }
            ]
        )

print("Documents successfully ingested.")