# Scientific RAG Recommender

## Overview
This project is an AI-powered system that recommends the most suitable scientific instruments based on a research problem.

Instead of just giving an answer, the system explains:
- why a particular instrument is recommended
- what its limitations are
- what alternatives can be used
- how confident the system is in its recommendation

The goal is to make scientific decision-making more structured, transparent, and reliable.

---

## What this system does
You provide:
- your research objective  
- the type of sample  
- the scientific domain  
- any constraints (like non-destructive testing)

The system returns:
- top 3 recommended instruments  
- clear reasoning  
- alternative methods  
- limitations  
- confidence score  
- warnings (if something doesn’t match)

---

## How it works (simple explanation)

1. The system reads your input  
2. It searches through scientific knowledge stored locally  
3. It finds the most relevant information  
4. It applies rule-based checks (to avoid incorrect suggestions)  
5. It generates a final recommendation with explanation  

This ensures the system is not just guessing, but making informed decisions.

---

## Key Features
- AI-powered recommendations  
- Clear reasoning (not just answers)  
- Confidence scoring  
- Warning system for incorrect inputs  
- Works completely offline (no external APIs)  
- Simple web interface  

---

## Tech Stack
- Python  
- FastAPI  
- FAISS (for fast information retrieval)  
- Sentence Transformers  
- HuggingFace Transformers  
- HTML, CSS, JavaScript (for UI)  

---

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Build the data index
```bash
python indexing/build_faiss_index.py
```
###3. Start the backend
```bash
uvicorn app.main:app --reload
```
###4. Run the UI
```bash
cd ui
python -m http.server 5500
```
