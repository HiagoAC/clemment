import os
from openai import OpenAI
from unittest import TestCase
from unittest.mock import patch

from src.clemment.core.openai_client_factory import OpenAIClientFactory


class TestOpenAIClientFactory(TestCase):
    def setUp(self):
        self.factory = OpenAIClientFactory()

    def test_create_client_with_api_key(self):
        openai_client = self.factory.create_client("test-key")

        self.assertEqual(openai_client.api_key, "test-key")
        self.assertIsInstance(openai_client, OpenAI)

    def test_create_client_with_env_api_key(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            openai_client = self.factory.create_client()

            self.assertEqual(openai_client.api_key, "test-key")
            self.assertIsInstance(openai_client, OpenAI)

    @patch("os.getenv", return_value=None)
    def test_create_client_without_api_key(self, mock_getenv):
        with self.assertRaises(RuntimeError):
            self.factory.create_client()
