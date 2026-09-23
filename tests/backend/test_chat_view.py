from unittest.mock import patch
from rest_framework.test import APITestCase

class TestChatView(APITestCase):
    def test_chat_view_missing_payload(self):
        response = self.client.post('/api/chat/', {}, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertTrue(response.json()['error'])

    def test_chat_view_missing_document_id(self):
        response = self.client.post('/api/chat/', {'query': 'What is notice period?'}, format='json')
        self.assertEqual(response.status_code, 400)

    @patch("api.services.vector_service.search_similar_chunks", return_value=["Notice period is 60 days."])
    @patch("api.services.gemini_service.answer_document_query", return_value="The notice period is 60 days.")
    def test_chat_view_success(self, mock_gemini, mock_vector):
        response = self.client.post('/api/chat/', {'query': 'What is notice period?', 'document_id': 'doc-123'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['answer'], "The notice period is 60 days.")

    @patch("api.services.vector_service.search_similar_chunks", return_value=[])
    def test_chat_view_no_context_fallback(self, mock_vector):
        response = self.client.post('/api/chat/', {'query': 'Unrelated question', 'document_id': 'doc-123'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("couldn't find any relevant content", response.json()['answer'])
