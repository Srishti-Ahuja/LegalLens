from unittest.mock import patch
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import conftest

class TestUploadView(APITestCase):
    def test_upload_view_no_file(self):
        response = self.client.post('/api/upload/')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()['error'])
        self.assertEqual(response.json()['message'], 'No file provided.')

    def test_upload_view_invalid_file_type(self):
        txt_file = SimpleUploadedFile("contract.txt", b"Hello world text content", content_type="text/plain")
        response = self.client.post('/api/upload/', {'file': txt_file}, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['code'], 'INVALID_FILE_TYPE')

    def test_upload_view_file_too_large(self):
        large_content = b"a" * (10 * 1024 * 1024 + 1)
        large_file = SimpleUploadedFile("big.pdf", large_content, content_type="application/pdf")
        response = self.client.post('/api/upload/', {'file': large_file}, format='multipart')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['code'], 'FILE_TOO_LARGE')

    @patch("api.services.vector_service.save_document", return_value="doc-uuid-999")
    @patch("api.services.vector_service.save_chunk")
    @patch("api.services.vector_service.update_document_analysis")
    @patch("api.services.gemini_service.generate_plain_summary", return_value="Summary text")
    @patch("api.services.gemini_service.extract_clause_risks", return_value=[{"clause": "c1", "severity": "Low", "rationale": "r1"}])
    @patch("api.services.pdf_service.extract_and_chunk_pdf", return_value=[
        {"document_name": "contract.pdf", "page_number": 1, "chunk_index": 0, "content": "PDF clause content"}
    ])
    def test_upload_view_success(self, mock_pdf, mock_risks, mock_summary, mock_update, mock_chunk, mock_doc):
        pdf_bytes = conftest.get_sample_pdf_bytes()
        pdf_file = SimpleUploadedFile("contract.pdf", pdf_bytes, content_type="application/pdf")
        response = self.client.post('/api/upload/', {'file': pdf_file}, format='multipart')

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['document_id'], "doc-uuid-999")
        self.assertEqual(data['summary'], "Summary text")
        self.assertEqual(len(data['risks']), 1)
