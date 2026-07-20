from pathlib import Path


class DocumentLoader:

    def load_documents(self, folder):

        docs = []

        for file in Path(folder).glob("*.txt"):

            docs.append({
                "filename": file.name,
                "content": file.read_text(encoding="utf-8")
            })

        return docs


document_loader = DocumentLoader()