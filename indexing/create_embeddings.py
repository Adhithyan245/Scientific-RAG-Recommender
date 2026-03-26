from sentence_transformers import SentenceTransformer
import numpy as np

def embed_chunks(chunks: list, model_name: str) -> np.ndarray:
    encoder = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    if not texts:
        return np.array([])
    embeddings = encoder.encode(texts).astype("float32")
    return embeddings
