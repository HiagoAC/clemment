from unittest import TestCase
from unittest.mock import mock_open, patch

from core.chatlog_manager import ChatLogManager


class TestChatlogManager(TestCase):
    def setUp(self):
        self.mock_file_data = '[{"role": "user", "content": "Hello World"},' \
                              '{"role": "assistant", "content": "Hi World"}]'
        self.open_mock = mock_open(read_data=self.mock_file_data)
        with patch("chatlog_manager.open", self.open_mock, create=True):
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
        with patch("chatlog_manager.open", self.open_mock, create=True):
            self.chatlog_manager.clear_chatlog()
            self.chatlog_manager.add_chatlog("Hello", "Hi")
            self.chatlog_manager.save_chatlog()

            # Assert what is written to file is the same as what is in chatlog 
            self.assertEqual()
