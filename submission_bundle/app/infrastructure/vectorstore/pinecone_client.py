from pinecone import Pinecone
from app.config.settings import settings


class PineconeClient:

    def __init__(self):
        self.pc = Pinecone(api_key=settings.pinecone_api_key)
        self.index = self.pc.Index(settings.pinecone_index_name)

    def get_index(self):
        return self.index


pinecone_client = PineconeClient()