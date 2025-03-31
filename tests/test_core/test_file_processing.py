from unittest import TestCase
from unittest.mock import MagicMock, patch, mock_open

from clemment.core.file_processing import process_file, analyse_comments_in_path


class TestHelperFunctions(TestCase):
    def setUp(self):
        self.comment_analyser = MagicMock()
        self.comment_analyser.analyse_comments.return_value = [(1, "A")]
        self.comment_analyser.total_prompt_tokens = 100
        self.comment_analyser.total_completion_tokens = 50
        self.patcher_open = patch(
            'builtins.open', new_callable=mock_open, read_data='source code')
        self.patcher_open.start()

    def tearDown(self):
        self.patcher_open.stop()

    def test_process_file(self):
        response = process_file("path/to/file.py", self.comment_analyser)
        self.assertEqual(response, {
            "file_path": "path/to/file.py",
            "suggestions": [(1, "A")],
            "prompt_tokens": 100,
            "completion_tokens": 50
        })

    @patch("os.path.isfile")
    @patch("os.walk")
    def test_analyse_comments_in_path_with_dir(
            self, mock_walk, mock_isfile):
        """
        Test that analyse_comments_in_path processes
        all files in a directory.
        """
        path = "path/to/directory"
        filenames = ["file1.py", "file2.py"]
        mock_isfile.return_value = False
        mock_walk.return_value = [(path, [], filenames)]
        response = analyse_comments_in_path(path, self.comment_analyser)
        expected = [
            {
                "file_path": f"{path}/{filename}",
                "suggestions": [(1, "A")],
                "prompt_tokens": 100,
                "completion_tokens": 50
            }
            for filename in filenames
        ]
        self.assertEqual(response, expected)

    @patch("os.path.isfile")
    def test_analyse_comments_in_path_with_file(self, mock_isfile):
        """
        Test that analyse_comments_in_path processes
        a single file.
        """
        path = "path/to/file.py"
        mock_isfile.return_value = True
        response = analyse_comments_in_path(path, self.comment_analyser)
        self.assertEqual(response, [{
            "file_path": path,
            "suggestions": [(1, "A")],
            "prompt_tokens": 100,
            "completion_tokens": 50
        }])
