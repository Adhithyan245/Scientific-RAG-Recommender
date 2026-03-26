import sys
import os
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

import faiss
import json
from app.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, FAISS_INDEX_PATH, CHUNKS_PATH, EMBEDDING_MODEL_NAME

from indexing.load_documents import load_text_documents
from indexing.preprocess_documents import preprocess
from indexing.chunk_documents import chunk_text
from indexing.create_embeddings import embed_chunks

def main():
    print("Loading documents...")
    docs = load_text_documents(RAW_DATA_DIR)
    
    print("Preprocessing...")
    docs = preprocess(docs)
    
    print("Chunking...")
    chunks = chunk_text(docs, chunk_size=50, overlap=10)
    
    if not chunks:
        print("No chunks generated. Make sure raw data exists.")
        return
        
    print(f"Creating embeddings using {EMBEDDING_MODEL_NAME}...")
    embeddings = embed_chunks(chunks, EMBEDDING_MODEL_NAME)
    
    print("Building FAISS index...")
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
    
    print("Saving index and chunks...")
    faiss.write_index(index, str(FAISS_INDEX_PATH))
    with open(CHUNKS_PATH, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2)
        
    print("Indexing pipeline complete.")

if __name__ == "__main__":
    main()
