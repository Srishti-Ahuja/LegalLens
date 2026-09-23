import os
import sys
import io
from unittest.mock import MagicMock
from pypdf import PdfWriter

# Ensure backend directory is in sys.path
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legal_project.settings')
import django
django.setup()

def get_sample_pdf_bytes():
    """Generates a valid minimalist PDF file in memory."""
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    buffer = io.BytesIO()
    writer.write(buffer)
    buffer.seek(0)
    return buffer.getvalue()

def setup_mock_db(test_instance):
    """Mocks Django connection.cursor on a test instance."""
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ["mock-doc-uuid-1234"]
    mock_cursor.fetchall.return_value = [["This is a mocked extracted PDF chunk content for QA."]]
    
    mock_conn = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
    return mock_cursor, mock_conn
