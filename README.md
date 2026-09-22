# LegalLens

## 1. About the Application
LegalLens is an AI‑powered legal document assistant designed to bridge the gap between complex legal jargon and everyday understanding. Users can upload contracts or agreements, receive plain‑English summaries, risk matrices, and ask contextual questions about the content.

### Why LegalLens is Better Than a Generic Chatbot
Unlike generic chatbots (like ChatGPT or standard Gemini) where you simply paste a large wall of text, LegalLens is purpose-built for legal workflows:
- **Zero Hallucination Guardrails:** Generic chatbots often "make up" legal terms or draw on outside knowledge. LegalLens strictly confines its answers to the four corners of your uploaded document. If an answer isn't in the contract, LegalLens explicitly tells you it's not specified.
- **Automated Risk Profiling:** It doesn't just read the text; it proactively scans for common predatory terms (e.g., blanket indemnifications, auto-renewals, unilateral terminations) and flags them with severity ratings.
- **Precision Retrieval (RAG):** Pasting a 50-page contract into a standard chatbot often exceeds memory limits or causes the AI to "forget" the middle sections. LegalLens uses intelligent chunking and vector search to pinpoint the exact clauses relevant to your question, ensuring high accuracy on massive documents.
- **Structured Legal Interface:** The UI is designed specifically for reviewing contracts, showing you the plain English summary alongside the original risk matrix, separated from the Q&A interface.

## 2. System Architecture
```text
+-------------------+       +---------------------------+
|   Frontend (React | <---> |  Backend (Django REST API)|
|   + Next.js)      |       |  - Chunking & Guardrails  |
+-------------------+       |  - Gemini API Integration |
                            |  - pgvector Database      |
                            +---------------------------+
```
The architecture is built on a robust Retrieval-Augmented Generation (RAG) pipeline:
- **Document Chunking:** When a PDF is uploaded, it isn't fed to the AI all at once. The backend extracts the text and breaks it down into small, semantically meaningful "chunks" (by page and paragraph). This ensures the AI never loses context when reading long contracts.
- **Vector Embedding:** Each chunk is sent to Google's Gemini Embedding model, which converts the text into a mathematical vector (a list of 1536 numbers). These vectors are saved in a PostgreSQL database using the `pgvector` extension.
- **Similarity Search:** When a user asks a question, the question is also converted into a vector. The database mathematically compares the question's vector to all document chunks to instantly find the 5 most relevant paragraphs.
- **Guardrails:** The relevant chunks are passed to the Gemini LLM with strict systemic guardrails, forcing the AI to answer *only* using the provided text and preventing it from dispensing generalized, unverified legal advice.

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
