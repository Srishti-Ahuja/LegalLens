import unittest
from unittest.mock import MagicMock, patch
import conftest
from api.services.pdf_service import mask_pii, extract_and_chunk_pdf

class TestPdfService(unittest.TestCase):
    def test_mask_pii_ssn(self):
        raw_text = "User SSN is 123-45-6789 for identification."
        masked = mask_pii(raw_text)
        self.assertIn("[REDACTED SSN]", masked)
        self.assertNotIn("123-45-6789", masked)

    def test_mask_pii_email(self):
        raw_text = "Contact support at alice.smith@lawfirm.org for details."
        masked = mask_pii(raw_text)
        self.assertIn("[REDACTED EMAIL]", masked)
        self.assertNotIn("alice.smith@lawfirm.org", masked)

    def test_mask_pii_phone(self):
        raw_text = "Call us at 800-555-0199 today."
        masked = mask_pii(raw_text)
        self.assertIn("[REDACTED PHONE]", masked)
        self.assertNotIn("800-555-0199", masked)

    def test_extract_and_chunk_pdf_valid(self):
        pdf_bytes = conftest.get_sample_pdf_bytes()
        chunks = list(extract_and_chunk_pdf(pdf_bytes, "test.pdf", chunk_size=500, overlap=50))
        self.assertIsInstance(chunks, list)

    @patch("api.services.pdf_service.PdfReader")
    def test_extract_and_chunk_pdf_encrypted(self, mock_pdf_reader_cls):
        mock_reader = MagicMock()
        mock_reader.is_encrypted = True
        mock_reader.decrypt.side_effect = Exception("Decryption failed")
        mock_pdf_reader_cls.return_value = mock_reader

        with self.assertRaises(ValueError) as ctx:
            list(extract_and_chunk_pdf(b"dummy pdf bytes", "encrypted.pdf"))
        self.assertIn("File is encrypted and cannot be processed.", str(ctx.exception))

if __name__ == '__main__':
    unittest.main()
