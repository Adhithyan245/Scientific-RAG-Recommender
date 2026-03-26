# Scientific RAG Recommender - Frontend UI

This is a lightweight, minimalistic frontend built with plain HTML, CSS, and JavaScript designed to interface directly with the Scientific RAG Recommender FastAPI backend.

## Features
- **No Build Step**: Just open the HTML file.
- **REST Integration**: Seamlessly sends structural JSON queries to `POST /recommend`.
- **Health Polling**: Validates the backend is running locally via `GET /health` on page load.
- **Clean UI**: Responsive, card-based interface with subtle transitions and clear warning indicators.

## Running Locally

1. **Start the API Backend**:
   Ensure your FastAPI backend is running on `http://127.0.0.1:8000`.
   If it's not running, navigate to your backend project directory and start it:
   ```bash
   python -m uvicorn app.main:app --reload
   ```

2. **Serve or Open the UI**:
   Since it uses plain HTML, CSS, and vanilla JS, you have a few options:
   
   - **Option A (Simplest)**: Just double-click `index.html` to open it directly in any modern browser. 
   
   - **Option B (Recommended)**: Serve via Python's built-in HTTP server:
     ```bash
     cd ui
     python -m http.server 3000
     ```
     Then open `http://localhost:3000` in your browser.

## CORS Configuration
The backend's `app/main.py` has been updated to include `CORSMiddleware` which allows the local UI (running on `file://` or `localhost:3000`) to communicate freely with the backend on port 8000.
