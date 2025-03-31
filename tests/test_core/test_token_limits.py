from unittest import TestCase

from src.clemment.core.token_limits import TokenLimits


class TestTokenLimits(TestCase):
    def setUp(self):
        self.token_limits = TokenLimits()

    def test_get_token_limit_with_known_model(self):
        token_limit = self.token_limits.get_token_limit("o1")
        self.assertEqual(
            token_limit, self.token_limits._model_token_limits["o1"])

    def test_get_token_limit_with_unknown_model(self):
        token_limit = self.token_limits.get_token_limit("unknown-model")
        self.assertEqual(
            token_limit, min(self.token_limits._model_token_limits.values()))
