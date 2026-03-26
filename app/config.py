import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROMPTS_DIR = BASE_DIR / "prompts"

FAISS_INDEX_PATH = PROCESSED_DATA_DIR / "faiss_index.bin"
CHUNKS_PATH = PROCESSED_DATA_DIR / "chunks.json"

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GENERATION_MODEL_NAME = "google/flan-t5-small"
