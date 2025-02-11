from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from commands.run import run


class TestRun(TestCase):
    @patch("run.analyse_comments_in_path")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_valid_path(self, mock_stdout, mock_analyse_comments_in_path):
        """Test run() with one valid path."""
        mock_analyse_comments_in_path.return_value = [
            {
                "file_path": "test.py",
                "suggestions": [(1, "Suggestion 1"), (2, "Suggestion 2")],
                "prompt_tokens": 2,
                "completion_tokens": 3,
            }
        ]
        run({"paths": ["test.py"]})
        expected_output = (
            "Total prompt tokens: 2\n"
            "Total completion tokens: 3\n"
            "Suggestions:\n"
            "File: test.py\n"
            "Line 1: Suggestion 1\n"
            "Line 2: Suggestion 2\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)
