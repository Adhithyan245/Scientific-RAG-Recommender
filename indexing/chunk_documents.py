def chunk_text(docs: list, chunk_size: int = 100, overlap: int = 20) -> list:
    chunks = []
    for doc in docs:
        words = doc["content"].split()
        for i in range(0, len(words), max(1, chunk_size - overlap)):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append({
                "instrument": doc["instrument"],
                "text": chunk
            })
    return chunks
