import os
from openai import OpenAI
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from core.comment_analyser import CommentAnalyser


class TestCommentAnalyser(TestCase):
    def setUp(self):
        mock_client = MagicMock()
        mock_client.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="1, A")),
                     Mock(message=Mock(content="2, B"))],
            usage=Mock(completion_tokens=50, prompt_tokens=100)
        )

        self.comment_analyser = CommentAnalyser(client=mock_client)

    def test_analyse_comments(self):
        suggestions = self.comment_analyser.analyse_comments("prompt", "model")

        self.assertEqual(suggestions, [(1, "A")])
        self.assertEqual(self.comment_analyser.total_completion_tokens, 50)
        self.assertEqual(self.comment_analyser.total_prompt_tokens, 100)

    def test_split_prompt(self):
        model_token_limit = 100 # chunk_size = 75
        prompt = "a" * 151
        with patch.object(self.comment_analyser.token_limits, "get_token_limit",
                          return_value=model_token_limit):
            chunks = self.comment_analyser._split_prompt(prompt, "a-model")
            self.assertEqual(len(chunks), 3)
            self.assertEqual(len(chunks[0]), model_token_limit*0.75)

    def test_get_openai_response(self):
        response = self.comment_analyser._get_openai_response("prompt", "model")

        self.assertEqual(response, ["1, A", "2, B"])
        self.assertEqual(self.comment_analyser.total_completion_tokens, 50)
        self.assertEqual(self.comment_analyser.total_prompt_tokens, 100)

    def test_parse_openai_response(self):
        response = self.comment_analyser._get_openai_response("prompt", "model")

        suggestions = self.comment_analyser._parse_openai_response(response)
        self.assertEqual(suggestions, [(1, "A")])
