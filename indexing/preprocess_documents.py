def clean_text(text: str) -> str:
    text = text.replace("\r", " ")
    text = " ".join(text.split())
    return text

def preprocess(docs: list) -> list:
    for doc in docs:
        doc["content"] = clean_text(doc["content"])
    return docs
