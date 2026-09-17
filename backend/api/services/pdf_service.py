import io
import re
from typing import Generator, Dict, Any
from pypdf import PdfReader

def mask_pii(text: str) -> str:
    """Mask basic PII (SSN, Phone Numbers, Emails) to protect privacy before embedding."""
    # Mask SSN
    text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[REDACTED SSN]', text)
    # Mask Emails
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[REDACTED EMAIL]', text)
    # Mask standard US Phone numbers (very basic regex)
    text = re.sub(r'\b\d{3}[-.\s]??\d{3}[-.\s]??\d{4}\b', '[REDACTED PHONE]', text)
    return text

def extract_and_chunk_pdf(file_obj: bytes, filename: str, chunk_size: int = 800, overlap: int = 100) -> Generator[Dict[str, Any], None, None]:
    """
    Generator that parses a PDF and yields chunks of text to keep memory low.
    """
    reader = PdfReader(io.BytesIO(file_obj))
    if getattr(reader, "is_encrypted", False):
        # Try to decrypt with empty password (common for PDFs with restrictions)
        try:
            reader.decrypt("")
        except Exception:
            raise ValueError("File is encrypted and cannot be processed.")
        if getattr(reader, "is_encrypted", False):
            raise ValueError("File is encrypted and cannot be processed.")
    
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue
            
        text = mask_pii(text)
        
        # Simple chunking
        start = 0
        chunk_idx = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            yield {
                "document_name": filename,
                "page_number": page_num + 1,
                "chunk_index": chunk_idx,
                "content": chunk.strip()
            }
            
            start += (chunk_size - overlap)
            chunk_idx += 1
