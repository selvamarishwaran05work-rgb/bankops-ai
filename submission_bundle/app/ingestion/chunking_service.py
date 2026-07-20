from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChunkingService:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100
        )

    def split(self, text):

        return self.splitter.split_text(text)


chunking_service = ChunkingService()