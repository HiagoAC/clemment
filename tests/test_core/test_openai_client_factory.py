import os
from openai import OpenAI
from unittest import TestCase
from unittest.mock import patch

from src.clemment.core.openai_client_factory import OpenAIClientFactory


class TestOpenAIClientFactory(TestCase):
    def setUp(self):
        self.factory = OpenAIClientFactory()

    def test_create_client_with_api_key(self):
        comment_analyser = self.factory.create_client("test-key")

        self.assertEqual(comment_analyser.api_key, "test-key")
        self.assertIsInstance(comment_analyser, OpenAI)

    def test_create_client_with_env_api_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            comment_analyser = self.factory.create_client()

            self.assertEqual(comment_analyser.api_key, "test-key")
            self.assertIsInstance(comment_analyser, OpenAI)

    @patch("os.getenv", return_value=None)
    def test_create_client_without_api_key(self, mock_getenv):
        with self.assertRaises(ValueError):
            self.factory.create_client()
