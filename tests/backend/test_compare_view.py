from unittest.mock import patch
from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
import conftest

class TestCompareView(APITestCase):
    def test_compare_view_missing_files(self):
        response = self.client.post('/api/compare/', {})
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()['error'])

    @patch("api.services.gemini_service.compare_contracts")
    def test_compare_view_success(self, mock_compare):
        mock_diff = [
            {"topic": "Termination Clause", "version_a": "30 days", "version_b": "60 days", "severity": "Medium"}
        ]
        mock_compare.return_value = mock_diff

        pdf_bytes = conftest.get_sample_pdf_bytes()
        file_a = SimpleUploadedFile("contract_v1.pdf", pdf_bytes, content_type="application/pdf")
        file_b = SimpleUploadedFile("contract_v2.pdf", pdf_bytes, content_type="application/pdf")

        response = self.client.post('/api/compare/', {'file_a': file_a, 'file_b': file_b}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['diff'], mock_diff)
