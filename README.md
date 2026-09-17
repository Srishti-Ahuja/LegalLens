# LegalLens

## 1. About the Application
LegalLens is an AI‑powered legal document assistant. Users can upload contracts or agreements, receive plain‑English summaries, risk matrices, and ask contextual questions about the content. Unlike generic chatbots, LegalLens:
- Understands the structure of legal documents and extracts clause‑level information.
- Provides risk assessments specific to the uploaded document.
- Stores embeddings for fast similarity search, enabling accurate Q&A.
- Offers a focused UI for uploading, summarizing, and interacting with a single document.

## 2. System Architecture
```
+-------------------+       +---------------------------+
|   Frontend (React| <---> |  Backend (Django REST API) |
|   + Next.js)      |       |  - PDF extraction & chunk |
+-------------------+       |  - Gemini embedding service |
                            |  - PostgreSQL with vector column |
                            |  - Chat endpoint (retrieval + Gemini) |
                            +---------------------------+
```
The frontend communicates with the backend via REST endpoints (`/api/upload/`, `/api/chat/`). The backend stores document chunks in PostgreSQL, uses Google Gemini for embeddings and summarization, and returns answers to the UI.

## 3. Tech Stack Used
- **Frontend**: Next.js (React), Tailwind CSS, TypeScript
- **Backend**: Django + Django REST Framework, PostgreSQL (vector extension)
- **AI Services**: Google Generative AI (Gemini models) for embeddings, summarization, and Q&A
- **Other**: Docker (optional containerisation), Python virtualenv, Node.js

## 4. Commands to Run
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver   # defaults to http://localhost:8000

# Frontend
cd ../frontend
npm install
npm run dev   # starts Next.js on http://localhost:3000
```
Make sure the required environment variables (`GEMINI_API_KEY`, `GEMINI_MODEL`, etc.) are set before starting the services.
