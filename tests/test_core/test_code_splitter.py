from unittest import TestCase
from unittest.mock import patch

from src.clemment.core.code_splitter import CodeSplitter


class TestCodeSplitter(TestCase):
    def setUp(self):
        self.model = "gpt-4"
        self.token_limit = 32
        self.chunk_size = 30
        with patch(
            "src.clemment.core.code_splitter.MODEL_TOKEN_LIMITS",
                {self.model: self.token_limit}):
            self.code_splitter = CodeSplitter(
                model=self.model, chunk_size=self.chunk_size)

    def test_init_with_invalid_chunk_size(self):
        """
        Test that CodeSplitter raises ValueError if chunk size exceeds
        model token limit.
        """
        with self.assertRaises(ValueError), patch(
            "src.clemment.core.code_splitter.MODEL_TOKEN_LIMITS",
                {self.model: self.token_limit}):
            CodeSplitter(model=self.model, chunk_size=self.token_limit + 1)

    def test_count_tokens(self):
        """Test _count_tokens method works correctly."""
        code = "def hello_world():\n    print('Hello, world!')"
        expected_token_count = 12
        actual_token_count = self.code_splitter._count_tokens(code)

        self.assertEqual(actual_token_count, expected_token_count)

    def test_split_code_integrity(self):
        """
        Test that the split code maintains functions and classes integrity.
        """
        function_part = """def a_function():\n    print("Hello, world!")"""
        class_part = (
            "class AClass:\n"
            "    def __init__(self):\n"
            "        self.value = 42\n"
            "    def method(self):\n"
            "        return self.value"
        )
        code = function_part + '\n' + class_part

        splits = self.code_splitter.split_code(code)

        self.assertEqual(len(splits), 2)
        self.assertIn(function_part, splits[0])
        self.assertIn(class_part, splits[1])
        self.assertNotIn(class_part, splits[0])
        self.assertNotIn(function_part, splits[1])

    def test_split_code_within_token_limit(self):
        """
        Test that the split code does not exceed the token limit.
        """
        code = "def hello_world():\n    print('Hello, world!')"
        splits = self.code_splitter.split_code(code)

        for split in splits:
            self.assertLessEqual(
                self.code_splitter._count_tokens(split),
                self.token_limit)
