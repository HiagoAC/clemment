from io import StringIO
from unittest import TestCase
from unittest.mock import patch

from cli.parser import parse_arguments


class TestParser(TestCase):
    """Test the command line argument parser."""
    def setUp(self):
        self.patcher_output = patch.multiple(
            "sys", stdout=StringIO(), stderr=StringIO())
        self.mock_output = self.patcher_output.start()

    def tearDown(self):
        self.patcher_output.stop()

    def test_run_command_no_path(self):
        """Test run command with no paths."""
        with patch("argparse._sys.argv", ["", "run"]):
            args = parse_arguments()
            self.assertEqual(args.command, "run")
            self.assertEqual(args.paths, [])

    def test_run_command_with_paths(self):
        """Test run command with paths."""
        with patch("argparse._sys.argv", ["", "run", "path1", "path2"]):
            args = parse_arguments()
            self.assertEqual(args.command, "run")
            self.assertEqual(args.paths, ["path1", "path2"])

    def test_chatlog_add_command(self):
        """Test chatlog add command."""
        with patch("argparse._sys.argv",
                   ["", "chatlog", "add", "-u", "user", "-a", "assistant"]):
            args = parse_arguments()
            self.assertEqual(args.command, "chatlog")
            self.assertEqual(args.chatlog_command, "add")
            self.assertEqual(args.user, "user")
            self.assertEqual(args.assistant, "assistant")

    def test_chatlog_get_command(self):
        """Test chatlog get command."""
        with patch("argparse._sys.argv", ["", "chatlog", "get"]):
            args = parse_arguments()
            self.assertEqual(args.command, "chatlog")
            self.assertEqual(args.chatlog_command, "get")

    def test_chatlog_clear_command(self):
        """Test chatlog clear command."""
        with patch("argparse._sys.argv", ["", "chatlog", "clear"]):
            args = parse_arguments()
            self.assertEqual(args.command, "chatlog")
            self.assertEqual(args.chatlog_command, "clear")

    def test_chatlog_add_missing_user(self):
        """Test chatlog add command with user argument missing."""
        with patch("argparse._sys.argv",
                   ["", "chatlog", "add", "-a", "assistant"]):
            with self.assertRaises(SystemExit):
                parse_arguments()

    def test_chatlog_add_missing_assistant(self):
        """Test chatlog add command with assistant argument missing."""
        with patch("argparse._sys.argv",
                   ["", "chatlog", "add", "-u", "user"]):
            with self.assertRaises(SystemExit):
                parse_arguments()
