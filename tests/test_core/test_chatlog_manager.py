import json
from unittest import TestCase
from unittest.mock import mock_open, patch

from clemment.core.chatlog_manager import ChatLogManager


class TestChatlogManager(TestCase):
    def setUp(self):
        self.mock_data = [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hi"},
            ]
        self.mock_json = json.dumps(self.mock_data)
        self.open_mock = mock_open(read_data=self.mock_json)
        with patch(
                "clemment.core.chatlog_manager.open", self.open_mock, create=True):
            self.chatlog_manager = ChatLogManager("file")

    def test_add_chatlog(self):
        original_length = len(self.chatlog_manager.chatlog)
        user_input = "Hello"
        assistant_response = "Hi"
        self.chatlog_manager.add_chatlog(user_input, assistant_response)

        self.assertEqual(
            len(self.chatlog_manager.chatlog), original_length + 2)
        self.assertEqual(
            self.chatlog_manager.chatlog[-1]['role'], "assistant")
        self.assertEqual(
            self.chatlog_manager.chatlog[-1]['content'], assistant_response)
        self.assertEqual(self.chatlog_manager.chatlog[-2]['role'], "user")
        self.assertEqual(
            self.chatlog_manager.chatlog[-2]['content'], user_input)

    def test_get_chatlog(self):
        chatlog = self.chatlog_manager.get_chatlog()

        self.assertEqual(chatlog, self.chatlog_manager.chatlog)

    def test_clear_chatlog(self):
        self.chatlog_manager.clear_chatlog()

        self.assertEqual(len(self.chatlog_manager.chatlog), 0)

    def test_save_chatlog(self):
        user_content = "Hello world"
        assistant_content = "Hi world"
        with patch(
                "clemment.core.chatlog_manager.open", self.open_mock) as mock_file:
            self.chatlog_manager.clear_chatlog()
            self.chatlog_manager.add_chatlog(user_content, assistant_content)
            self.chatlog_manager.save_chatlog()

            expected = [
                {"role": "user", "content": user_content},
                {"role": "assistant", "content": assistant_content},
            ]
            written_data = "".join(
                call[0][0] for call in mock_file().write.call_args_list)

            self.assertEqual(json.loads(written_data), expected)
