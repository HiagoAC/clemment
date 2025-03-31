from argparse import Namespace
from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from clemment.cli import run


class TestRun(TestCase):
    @patch("os.path.exists", return_value=True)
    @patch("clemment.cli.commands.run.analyse_comments_in_path")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_valid_path(
            self, mock_stdout, mock_analyse_comments_in_path, _):
        """Test run() with one valid path."""
        mock_analyse_comments_in_path.return_value = [
            {
                "file_path": "test.py",
                "suggestions": [(1, "Suggestion 1"), (2, "Suggestion 2")],
                "prompt_tokens": 2,
                "completion_tokens": 3,
            }
        ]
        args = Namespace(paths=["test.py"])
        run(args)
        expected_output = (
            "Total prompt tokens: 2\n"
            "Total completion tokens: 3\n"
            "Suggestions:\n"
            "File: test.py\n"
            "Line 1: Suggestion 1\n"
            "Line 2: Suggestion 2\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("os.path.exists", return_value=True)
    @patch("clemment.cli.commands.run.analyse_comments_in_path")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_multiple_valid_paths(
            self, mock_stdout, mock_analyse_comments_in_path, _):
        """Test run() with multiple valid paths."""
        file_path = "a_test_file.py"
        suggestions = [(1, "Suggestion 1"), (2, "Suggestion 2")]
        prompt_tokens = 2
        completion_tokens = 3
        mock_analyse_comments_in_path.return_value = [
            {
                "file_path": file_path,
                "suggestions": suggestions,
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
            }
        ]
        args = Namespace(paths=["test.py", "test2.py"])
        run(args)
        expected_output = (
            f"Total prompt tokens: {prompt_tokens*2}\n"
            f"Total completion tokens: {completion_tokens*2}\n"
            "Suggestions:\n"
            f"File: {file_path}\n"
            f"Line {suggestions[0][0]}: {suggestions[0][1]}\n"
            f"Line {suggestions[1][0]}: {suggestions[1][1]}\n"
            f"File: {file_path}\n"
            f"Line {suggestions[0][0]}: {suggestions[0][1]}\n"
            f"Line {suggestions[1][0]}: {suggestions[1][1]}\n"
        )
        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("os.path.exists", return_value=True)
    @patch("os.getcwd", return_value="current_dir")
    @patch("clemment.cli.commands.run.analyse_comments_in_path")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_no_paths(
            self, mock_stdout, mock_analyse_comments_in_path, mock_getcwd, _):
        """
        Test run() uses the current directory with no paths are given to it.
        """
        args = Namespace(paths=[])
        run(args)
        mock_analyse_comments_in_path.assert_called_once_with("current_dir")

    @patch("clemment.cli.commands.run.analyse_comments_in_path")
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_with_invalid_path(
            self, mock_stdout, mock_analyse_comments_in_path):
        """Test run() with one invalid path."""
        mock_analyse_comments_in_path.return_value = []
        invalid_path = "invalid_path"
        args = Namespace(paths=[invalid_path])
        with self.assertRaises(ValueError):
            run(args)
