import unittest
from unittest.mock import patch, MagicMock
from api.services import gemini_service

class TestGeminiService(unittest.TestCase):
    @patch.object(gemini_service, 'GEMINI_API_KEY', None)
    def test_call_gemini_missing_api_key(self):
        with self.assertRaises(EnvironmentError) as ctx:
            gemini_service._call_gemini("Test prompt")
        self.assertIn("GEMINI_API_KEY environment variable not set.", str(ctx.exception))

    @patch.object(gemini_service, 'GEMINI_API_KEY', 'test-api-key')
    @patch("requests.post")
    def test_call_gemini_success(self, mock_post):
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {
            'candidates': [
                {'content': {'parts': [{'text': 'Summary of contract text'}]}}
            ]
        }
        mock_post.return_value = mock_response

        result = gemini_service._call_gemini("Summarize this text")
        self.assertEqual(result, "Summary of contract text")

    @patch.object(gemini_service, 'GEMINI_API_KEY', 'test-api-key')
    @patch("requests.post", side_effect=Exception("Connection timed out"))
    def test_call_gemini_api_failure(self, mock_post):
        with self.assertRaises(RuntimeError) as ctx:
            gemini_service._call_gemini("Test prompt")
        self.assertIn("AI service is currently unavailable.", str(ctx.exception))

    @patch.object(gemini_service, '_call_gemini', return_value="1. Plain English Summary")
    def test_generate_plain_summary(self, mock_call):
        result = gemini_service.generate_plain_summary("Legal text content")
        self.assertEqual(result, "1. Plain English Summary")

    @patch.object(gemini_service, '_call_gemini')
    def test_extract_clause_risks_json_parsing(self, mock_call):
        valid_json_markdown = """```json
        [
            {"clause": "Unilateral termination", "severity": "High", "rationale": "Allows instant cancellation."}
        ]
        ```"""
        mock_call.return_value = valid_json_markdown
        risks = gemini_service.extract_clause_risks("Legal contract content")
        self.assertEqual(len(risks), 1)
        self.assertEqual(risks[0]["severity"], "High")
        self.assertEqual(risks[0]["clause"], "Unilateral termination")

    @patch.object(gemini_service, '_call_gemini', return_value="Invalid non-JSON response")
    def test_extract_clause_risks_corrupt_json(self, mock_call):
        risks = gemini_service.extract_clause_risks("Legal contract content")
        self.assertEqual(risks, [])

    @patch.object(gemini_service, '_call_gemini', return_value="The notice period is 30 days.")
    def test_answer_document_query(self, mock_call):
        answer = gemini_service.answer_document_query("What is notice period?", ["Notice period is 30 days."])
        self.assertEqual(answer, "The notice period is 30 days.")

    @patch.object(gemini_service, '_call_gemini')
    def test_compare_contracts(self, mock_call):
        diff_json = """[
            {"topic": "Termination Clause", "version_a": "30 days notice", "version_b": "Immediate termination", "severity": "High"}
        ]"""
        mock_call.return_value = diff_json
        diffs = gemini_service.compare_contracts("Text A", "Text B")
        self.assertEqual(len(diffs), 1)
        self.assertEqual(diffs[0]["topic"], "Termination Clause")
        self.assertEqual(diffs[0]["severity"], "High")

if __name__ == '__main__':
    unittest.main()
