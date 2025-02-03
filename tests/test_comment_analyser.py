import os
from openai import OpenAI
from unittest import TestCase
from unittest.mock import Mock, patch

from comment_analyser import CommentAnalyser


class TestCommentAnalyser(TestCase):
    def setUp(self):
        self.comment_analyser = CommentAnalyser()
        self.mock_openai_response = Mock(
            choices=[Mock(message=Mock(content="1 A"),
                          message=Mock(content="2 B"))],
            usage=Mock(completion_tokens=50, prompt_tokens=100)
        )

    def test_init_with_api_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            comment_analyser = CommentAnalyser()
            self.assertEqual(comment_analyser.api_key, "test-key")
    
    def test_init_without_api_key(self):
        with self.assertRaises(ValueError):
            CommentAnalyser()
    
    @patch('openai.OpenAI.chat.completions.create')
    def test_analyse_comments(self, mock_openai):
        mock_openai.return_value = self.mock_openai_response
        suggestions = self.comment_analyser.analyse_comments("prompt", "model")

        self.assertEqual(suggestions, [(1, "A"), (2, "B")])
        self.assertEqual(self.comment_analyser.total_completion_tokens, 50)
        self.assertEqual(self.comment_analyser.total_prompt_tokens, 100)

    def test_split_prompt(self):
        model_token_limit = 50
        prompt = "a" * 100
        with patch.object(self.comment_analyser.token_limits, "get_token_limit",
                          return_value=model_token_limit):
            chunks = self.comment_analyser._split_prompt(prompt, "a-model")
            self.assertEqual(len(chunks), 2)
            self.assertEqual(len(chunks[0]), model_token_limit)

    @patch('openai.OpenAI.chat.completions.create')
    def test_get_openai_response(self, mock_openai):
        mock_openai.return_value = self.mock_openai_response
        response = self.comment_analyser._get_openai_response("prompt", "model")

        self.assertEqual(response, ["1 A", "2 B"])
        self.assertEqual(self.comment_analyser.total_completion_tokens, 50)
        self.assertEqual(self.comment_analyser.total_prompt_tokens, 100)

    @patch('openai.OpenAI.chat.completions.create')
    def test_parse_openai_response(self, mock_openai):
        mock_openai.return_value = self.mock_openai_response
        response = self.comment_analyser._get_openai_response("prompt", "model")

        suggestions = self.comment_analyser._parse_openai_response(response)
        self.assertEqual(suggestions, [(1, "A"), (2, "B")])
