<<<<<<< HEAD
# Scientific RAG-based Instrument Recommendation System

## Overview
This project is an advanced, production-style Scientific RAG (Retrieval-Augmented Generation) based Instrument Recommendation System. It takes structured scientific requirements as input (research objective, sample type, domain, etc.) and recommends the Top 3 most suitable scientific instruments (e.g., XRD, SEM, FTIR) using a hybrid AI approach. 

The system provides not just an answer, but transparent reasoning, clear limitations, and explicit warnings based on deterministic rules.

## System Architecture
The application is built completely locally (zero external APIs) with the following modular components:
- **API Backend**: FastAPI providing a robust `POST /recommend` endpoint and a `GET /health` check.
- **UI Frontend**: Lightweight Vanilla HTML/CSS/JS interface that dynamically visualizes the results.
- **RAG Subsystem**:
  - **Vector DB**: FAISS index built locally.
  - **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`.
  - **Generation Engine**: `google/flan-t5-small` local HuggingFace LLM configured to output strict JSON schemas.
- **Rule Engine**: Evaluates domain-specific heuristics and constraints, affecting both rankings and confidence.

## RAG Functionality
The Retrieval-Augmented Generation pipeline prevents hallucinations and grounds answers in scientific literature:
1. **Indexing**: Raw text knowledge about instruments is chunked and embedded into a FAISS index.
2. **Retrieval**: User search constraints are converted to a semantic query to retrieve the top unique chunks.
3. **Reasoning Formation**: The `google/flan-t5-small` model digests the clean context and strictly separates its reasoning from known limitations in a structured JSON format.
4. **Ranking & Formatting**: The retrieved chunks and rule outcomes re-rank the top 3 recommendations.

## Hybrid AI Design (Rules + LLM)
The system leverages a Hybrid AI architecture, combining the probabilistic reasoning of an LLM with a deterministic Rule Engine:
- **Rule Engine**: Rapidly catches hard scientific constraints (e.g. "Liquids are incompatible with standard XRD" or "Optical cannot achieve atomic resolution").
- **LLM Reasoner**: Synthesizes nuanced connections between the research objective and the instrument's capabilities based on the retrieved vector chunks.
- **Outcome**: The rule engine dictates penalties to ranking scores, generates explicit warnings, and lowers confidence if conflicts exist, keeping the LLM grounded.

## Confidence Scoring
The overall system confidence score (0 to 1) is dynamically calculated using:
- **Retrieval Similarity**: Normalized FAISS distances of the supporting chunks.
- **Support Volume**: The number of unique retrieved chunks found.
- **Rule Violations**: Flat penalties applied per triggered heuristic warning.
- **Input Completeness**: Deductions for missing optional inputs (like sensitivity or resolution).
The combination yields a transparent confidence score along with a human-readable `confidence_explanation`.

## How to Run

1. **Install Dependencies**
   Ensure you have a modern Python environment.
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Indexing Pipeline**
   Build the FAISS databases and vector embeddings before the API runs:
   ```bash
   python indexing/build_faiss_index.py
   ```

3. **Start the API Backend**
   ```bash
   uvicorn app.main:app --reload
   ```
   The backend will start at `http://127.0.0.1:8000`.

4. **Open the UI**
   Open `ui/index.html` directly in any web browser. No local web server is strictly required for the frontend, but you can use `python -m http.server 8080` in the `ui` directory if preferred.

## Sample Input / Output

**Input Request:**
```json
{
  "research_objective": "Determine phase composition and crystal structure",
  "sample_type": "Powder",
  "domain": "Materials Science",
  "sensitivity": "Medium",
  "resolution": "High",
  "constraints": "Non-destructive testing required",
  "debug": true
}
```

**Output Response:**
```json
{
  "recommendations": [
    {
      "instrument": "XRD",
      "reasoning": "XRD is the premier method for determining phase compositions of crystalline solid powders.",
      "alternatives": ["SEM", "FTIR"],
      "limitations": "Requires crystalline samples; unable to detect amorphous phases efficiently.",
      "score": 0.95
    },
    {
      "instrument": "SEM",
      "reasoning": "Alternative option based on partial match. Score: 0.65",
      "alternatives": [],
      "limitations": "May not fully meet all constraints. Please check warnings.",
      "score": 0.65
    }
  ],
  "confidence": 0.9,
  "confidence_explanation": "Strong match with high confidence based on retrieved literature.",
  "warnings": [],
  "debug_info": {
     "retrieved_chunks": [...],
     "scores": {...}
  }
}
```

## Screenshots

> *Add screenshots representing the fresh UI with the top 3 rankings, the warning cards, and the dynamic Confidence Progress Bar here.*
=======
# Scientific-RAG-Recommender
AI-powered scientific instrument recommendation system using RAG, hybrid reasoning, and FastAPI
>>>>>>> 4fddcc8b32928a690e51acdb34267d3d6f9e27af
