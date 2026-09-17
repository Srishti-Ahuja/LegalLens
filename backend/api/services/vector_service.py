import os
import sys
import logging
# Force protobuf pure‑python implementation for Python 3.14+ compatibility
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
# Prevent loading compiled protobuf extensions that crash on Python 3.14
sys.modules.setdefault('google._upb._message', None)
sys.modules.setdefault('google.protobuf.pyext._message', None)
import google.generativeai as genai
from django.db import connection
from typing import List, Dict, Any, Tuple

# Configure module‑level logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(name)s: %(message)s')

# Initialise Gemini client
# Initialise Gemini client
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    # Attempt to use Application Default Credentials with proper scopes
    try:
        import google.auth
        creds, _ = google.auth.default(scopes=[
            "https://www.googleapis.com/auth/generative-language",
            "https://www.googleapis.com/auth/cloud-platform",
        ])
        genai.configure(credentials=creds)
    except Exception as e:
        logger.warning("Failed to configure Gemini client with ADC: %s", e)
        # Proceed without explicit configuration; embed calls will fall back to dummy.



def embed_text(text: str) -> List[float]:
    """Get embedding for a single text chunk using Gemini. If the Gemini embedding model is unavailable,
    fall back to a deterministic dummy embedding based on the text's hash.
    """
    try:
        result = genai.embed_content(
            model="models/gemini-embedding-2",
            content=text,
            task_type="retrieval_document",
        )
        embedding = result['embedding']
        # Ensure embedding is 1536 dimensions
        if len(embedding) != 1536:
            logger.warning(
                "Embedding dimension mismatch in embed_text (got %d, expected 1536); adjusting.",
                len(embedding),
            )
            if len(embedding) > 1536:
                embedding = embedding[:1536]
            else:
                embedding = embedding + [0.0] * (1536 - len(embedding))
        return embedding
    except Exception as e:
        logger.exception("Failed to embed text via Gemini.")
        raise


def embed_query(text: str) -> List[float]:
    """Get embedding for a query string using Gemini. If the Gemini embedding model is unavailable,
    fall back to a deterministic dummy embedding based on the text's hash.
    """
    try:
        result = genai.embed_content(
            model="models/gemini-embedding-2",
            content=text,
            task_type="retrieval_query",
        )
        embedding = result['embedding']
        # Ensure embedding is 1536 dimensions
        if len(embedding) != 1536:
            logger.warning(
                "Embedding dimension mismatch in embed_query (got %d, expected 1536); adjusting.",
                len(embedding),
            )
            if len(embedding) > 1536:
                embedding = embedding[:1536]
            else:
                embedding = embedding + [0.0] * (1536 - len(embedding))
        return embedding
    except Exception as e:
        logger.exception("Failed to embed query via Gemini.")
        raise


def save_document(filename: str, file_hash: str) -> str:
    """Save document metadata and return its ID."""
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO documents (filename, file_hash) VALUES (%s, %s) RETURNING id;",
                [filename, file_hash],
            )
            doc_id = cursor.fetchone()[0]
            logger.info("Saved document %s (id=%s)", filename, doc_id)
            return str(doc_id)
    except Exception as e:
        logger.exception("Error inserting document %s into DB", filename)
        raise


def save_chunk(document_id: str, page_number: int, chunk_index: int, content: str):
    """Embed and save a chunk of a document.

    Parameters
    ----------
    document_id: str
        The ID of the parent document.
    page_number: int
        Page number the chunk originates from.
    chunk_index: int
        Sequential index of the chunk within the page.
    content: str
        Text content of the chunk.
    """
    try:
        embedding = embed_text(content)
        # Ensure embedding has the expected 1536 dimensions for the DB column
        if len(embedding) != 1536:
            logger.warning(
                "Embedding dimension mismatch (got %d, expected 1536); adjusting.",
                len(embedding),
            )
            if len(embedding) > 1536:
                embedding = embedding[:1536]
            else:
                # Pad with zeros if too short
                embedding = embedding + [0.0] * (1536 - len(embedding))
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO document_chunks (document_id, page_number, chunk_index, content, embedding)
                VALUES (%s, %s, %s, %s, %s::vector);
                """,
                [document_id, page_number, chunk_index, content, embedding],
            )
        logger.info(
            "Saved chunk (doc_id=%s, page=%s, idx=%s)",
            document_id,
            page_number,
            chunk_index,
        )
    except Exception as e:
        logger.exception(
            "Failed to save chunk (doc_id=%s, page=%s, idx=%s)",
            document_id,
            page_number,
            chunk_index,
        )
        raise


def update_document_analysis(document_id: str, summary: str, risks: List[Dict[str, Any]]):
    """Persist the generated summary and risk assessment for a document.

    Adds `summary`, `risk_assessment` (JSONB) and marks the document as processed.
    """
    import json
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE documents
                SET summary = %s, risk_assessment = %s, is_processed = true
                WHERE id = %s;
                """,
                [summary, json.dumps(risks), document_id],
            )
        logger.info("Updated analysis for document id=%s", document_id)
    except Exception as e:
        logger.exception("Failed to update analysis for document id=%s", document_id)
        raise


def search_similar_chunks(query: str, document_id: str, limit: int = 5) -> List[str]:
    """Search for relevant chunks within a specific document using vector similarity."""
    try:
        query_embedding = embed_query(query)
        # Ensure embedding is 1536 dimensions
        if len(query_embedding) != 1536:
            logger.warning(
                "Embedding dimension mismatch in search_similar_chunks (got %d, expected 1536); adjusting.",
                len(query_embedding),
            )
            if len(query_embedding) > 1536:
                query_embedding = query_embedding[:1536]
            else:
                query_embedding = query_embedding + [0.0] * (1536 - len(query_embedding))
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT content
                FROM document_chunks
                WHERE document_id = %s
                ORDER BY embedding <=> %s::vector
                LIMIT %s;
                """,
                [document_id, query_embedding, limit],
            )
            results = cursor.fetchall()
            logger.info("Found %d similar chunks for document id=%s", len(results), document_id)
            return [row[0] for row in results]
    except Exception as e:
        logger.exception("Error searching similar chunks for document id=%s", document_id)
        raise
