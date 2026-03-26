import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from app.config import FAISS_INDEX_PATH, CHUNKS_PATH, EMBEDDING_MODEL_NAME

class Retriever:
    def __init__(self):
        try:
            self.encoder = SentenceTransformer(EMBEDDING_MODEL_NAME)
        except Exception as e:
            print(f"Failed to load sentence transformer check resources: {e}")
            self.encoder = None
            
        if FAISS_INDEX_PATH.exists() and CHUNKS_PATH.exists():
            try:
                self.index = faiss.read_index(str(FAISS_INDEX_PATH))
                with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
                    self.chunks = json.load(f)
            except Exception as e:
                print(f"Failed to load FAISS index or chunks: {e}")
                self.index = None
                self.chunks = []
        else:
            self.index = None
            self.chunks = []
            
    def retrieve(self, query: str, top_k: int = 3) -> list:
        if not self.index or not self.chunks or not self.encoder:
            return []
            
        try:
            query = query or ""
            query_vector = self.encoder.encode([query]).astype("float32")
            search_k = min(top_k * 3, len(self.chunks))
            
            distances, indices = self.index.search(query_vector, search_k)
            
            results = []
            seen_texts = set()
            
            for i, idx in enumerate(indices[0]):
                if idx != -1 and idx < len(self.chunks):
                    # Safely handle missing dict fields
                    chunk_data = self.chunks[idx]
                    if not isinstance(chunk_data, dict): continue
                    
                    text_clean = chunk_data.get("text", "").strip()
                    if text_clean and text_clean not in seen_texts:
                        seen_texts.add(text_clean)
                        results.append({
                            "chunk": text_clean,
                            "instrument": str(chunk_data.get("instrument", "Unknown")),
                            "distance": float(distances[0][i])
                        })
                        if len(results) >= top_k:
                            break
            return results
        except Exception as e:
            print(f"Retrieval Exception: {e}")
            return []
