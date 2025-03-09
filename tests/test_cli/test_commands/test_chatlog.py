import json

from argparse import Namespace
from io import StringIO
from unittest import TestCase
from unittest.mock import mock_open, patch

from src.cli import chatlog


class TestChatlog(TestCase):
    """Test chatlog command."""
    def setUp(self):
        self.mock_data = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            ]
        self.mock_json = json.dumps(self.mock_data)
        self.patcher_stdout = patch("sys.stdout", new_callable=StringIO)
        self.mock_stdout = self.patcher_stdout.start()

    def tearDown(self):
        self.patcher_stdout.stop()

    def test_chatlog_add(self):
        """Test chatlog() with add command."""
        user_content = "Hello2"
        assistant_content = "Hi2"
        expected = self.mock_data + [
            {"role": "user", "content": user_content},
            {"role": "assistant", "content": assistant_content},
        ]
        args = Namespace(
            chatlog_command="add",
            user=user_content,
            assistant=assistant_content
        )
        with patch("builtins.open", mock_open(
                read_data=self.mock_json)) as mock_file:
            chatlog(args)
            written_data = "".join(
                call[0][0] for call in mock_file().write.call_args_list)
            self.assertEqual(json.loads(written_data), expected)

    def test_chatlog_get(self):
        """Test chatlog() with get command."""
        args = Namespace(chatlog_command="get")
        with patch("builtins.open", mock_open(
                read_data=self.mock_json)):
            chatlog(args)
            expected = "\n".join(
                f"{log['role']}: {log['content']}" for log in self.mock_data)
            self.assertEqual(self.mock_stdout.getvalue().strip(), expected)

    def test_chatlog_clear(self):
        """Test chatlog() with clear command."""
        args = Namespace(chatlog_command="clear")
        with patch("builtins.open", mock_open(
                read_data=self.mock_json)) as mock_file:
            chatlog(args)
            expected = []
            written_data = "".join(
                call[0][0] for call in mock_file().write.call_args_list)
            self.assertEqual(json.loads(written_data), expected)
