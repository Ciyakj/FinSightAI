# utils/rag_retriever.py

class FinanceRAGRetriever:
    def __init__(self):
        self.chunks = []

    def add_chunks(self, chunks):
        self.chunks.extend(chunks)

    def query(self, question):
        # Just return the most recent 3 chunks
        return self.chunks[:3] if self.chunks else ["No relevant context found."]
