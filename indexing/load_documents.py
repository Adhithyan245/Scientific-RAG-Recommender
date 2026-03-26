import os
from pathlib import Path

def load_text_documents(raw_data_dir: Path) -> list:
    docs = []
    if not raw_data_dir.exists():
        return docs
        
    for file in os.listdir(raw_data_dir):
        if file.endswith(".txt"):
            with open(raw_data_dir / file, "r", encoding="utf-8") as f:
                content = f.read()
                instrument = file.split(".")[0].upper()
                docs.append({
                    "instrument": instrument,
                    "content": content
                })
    return docs
