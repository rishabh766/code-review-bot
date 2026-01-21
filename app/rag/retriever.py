import numpy as np
from app.rag.indexer import FAISSIndexer
from app.rag.embedder import GeminiEmbeddings

class Retriever:
    def __init__(self, indexer : FAISSIndexer):
        self.indexer = indexer
        self.embedder = GeminiEmbeddings()

    def retrieve_context(self, query_diff : str, k : int = 3) -> str:
        if not self.indexer.index or not query_diff:
            return ""
        query_vec = self.embedder.embed_text(query_diff)
        if not query_vec:
            return ""
        
        query_np = np.array([query_vec]).astype('float32')
        distances, indices = self.indexer.index.search(query_np, k)

        context_parts = []
        found_indices = indices[0]

        for idx in found_indices:
            if idx == -1: continue
            doc = self.indexer.documents[idx]
            context_parts.append(f"--- File: {doc['filename']} ---\n{doc['content'][:1500]}")

        return "\n\n".join(context_parts)