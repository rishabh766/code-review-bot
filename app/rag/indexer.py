import faiss
import numpy as np
from app.rag.embedder import GeminiEmbeddings

class FAISSIndexer:
    def __init__(self):
        self.embedder = GeminiEmbeddings()
        self.index = None
        self.documents = []
        self.dimension = 768

    def index_repo(self, file_contents : dict):
        print(f"[RAG] Indexing {len(file_contents)} files with real embeddings...")
        vectors = []
        self.documents = []

        for filename, content in file_contents.items():
            if not content.strip():
                continue
            emb = self.embedder.embed_text(content)
            if emb:
                vectors.append(emb)
                self.documents.append({"filename" : filename, "content" : content})

        if not vectors:
            print("No valid vectors created")
            return
        
        vectors_np = np.array(vectors).astype('float32')
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(vectors_np)

        print(f"[RAG] Index built with {self.index.ntotal} vectors")

        
            
