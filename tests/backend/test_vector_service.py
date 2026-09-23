import unittest
from unittest.mock import patch, MagicMock
import conftest
from api.services import vector_service

class TestVectorService(unittest.TestCase):
    def setUp(self):
        self.mock_cursor, self.mock_conn = conftest.setup_mock_db(self)

    @patch("google.generativeai.embed_content")
    def test_embed_text_truncates_and_pads(self, mock_embed):
        # Truncation test
        mock_embed.return_value = {'embedding': [0.1] * 2000}
        res = vector_service.embed_text("Sample chunk text")
        self.assertEqual(len(res), 1536)

        # Padding test
        mock_embed.return_value = {'embedding': [0.1] * 1000}
        res_short = vector_service.embed_text("Sample chunk text")
        self.assertEqual(len(res_short), 1536)
        self.assertEqual(res_short[1000:], [0.0] * 536)

    @patch("django.db.connection.cursor")
    def test_save_document(self, mock_cursor_fn):
        mock_cursor_fn.return_value.__enter__.return_value = self.mock_cursor
        doc_id = vector_service.save_document("test_contract.pdf", "hash12345")
        self.assertEqual(doc_id, "mock-doc-uuid-1234")
        self.mock_cursor.execute.assert_called_once()
        self.assertIn("INSERT INTO documents", self.mock_cursor.execute.call_args[0][0])

    @patch.object(vector_service, "embed_text", return_value=[0.1] * 1536)
    @patch("django.db.connection.cursor")
    def test_save_chunk(self, mock_cursor_fn, mock_embed):
        mock_cursor_fn.return_value.__enter__.return_value = self.mock_cursor
        vector_service.save_chunk("mock-doc-uuid-1234", page_number=1, chunk_index=0, content="Clause text")
        self.mock_cursor.execute.assert_called_once()
        self.assertIn("INSERT INTO document_chunks", self.mock_cursor.execute.call_args[0][0])

    @patch("django.db.connection.cursor")
    def test_update_document_analysis(self, mock_cursor_fn):
        mock_cursor_fn.return_value.__enter__.return_value = self.mock_cursor
        risks = [{"clause": "Unilateral termination", "severity": "High", "rationale": "High risk"}]
        vector_service.update_document_analysis("mock-doc-uuid-1234", "Plain summary", risks)
        self.mock_cursor.execute.assert_called_once()
        self.assertIn("UPDATE documents", self.mock_cursor.execute.call_args[0][0])

    @patch.object(vector_service, "embed_query", return_value=[0.1] * 1536)
    @patch("django.db.connection.cursor")
    def test_search_similar_chunks(self, mock_cursor_fn, mock_embed_q):
        mock_cursor_fn.return_value.__enter__.return_value = self.mock_cursor
        results = vector_service.search_similar_chunks("What is termination period?", "mock-doc-uuid-1234")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], "This is a mocked extracted PDF chunk content for QA.")

if __name__ == '__main__':
    unittest.main()
