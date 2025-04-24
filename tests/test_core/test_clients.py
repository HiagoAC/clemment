import os
from openai import OpenAI
from unittest import TestCase
from unittest.mock import patch

from src.clemment.core.clients import create_openai_client


class TestClients(TestCase):

    def test_create_openai_client_success(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            openai_client = create_openai_client()

            self.assertEqual(openai_client.api_key, "test-key")
            self.assertIsInstance(openai_client, OpenAI)
