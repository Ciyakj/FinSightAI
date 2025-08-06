from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class FinancialRAG:
    def __init__(self):
        self.chunks = []
        self.vectorizer = TfidfVectorizer()
        self.embeddings = None

    def add_chunks(self, chunks):
        self.chunks = chunks
        self.embeddings = self.vectorizer.fit_transform(chunks)

    def query(self, question, top_k=3):
        question_vec = self.vectorizer.transform([question])
        similarities = cosine_similarity(question_vec, self.embeddings).flatten()
        top_indices = similarities.argsort()[::-1][:top_k]
        return "\n".join([self.chunks[i] for i in top_indices])
