import os
from unittest import TestCase
from unittest.mock import patch

from src.clemment.config import get_openai_api_key


class TestConfig(TestCase):
    def test_get_openai_api_key_success(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
            key = get_openai_api_key()

            self.assertEqual(key, "test-key")

    @patch("os.getenv", return_value=None)
    def test_get_openai_api_key_not_set(self, mock_getenv):
        with self.assertRaises(RuntimeError):
            get_openai_api_key()
