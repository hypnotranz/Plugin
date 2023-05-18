import unittest
from unittest.mock import patch, MagicMock
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.message_store import MessageStore
from unittest.mock import ANY

class TestMessageHandler(unittest.TestCase):
    def setUp(self):
        self.message_store = MessageStore()
        self.message_handler = MessageHandler(self.message_store)
        self.test_message = Message({
            'sender_actor': 'chatgpt://developer_1',
            'sender_agent': 'http://localhost:5003/send-message',
            'log_correlation_path': '1234',
            'recipient_agent': 'http://localhost:5003/send-message',
            'recipient_actor': 'unix_manager',
            'message_type': 'wsl-bash',
            'content': 'echo "Hello, world!"'
        })

    @patch('subprocess.Popen')
    def test_handle_wsl_bash(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Hello, world!\n", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        self.message_handler.handle_wsl_bash(self.test_message)
        response_message = self.message_store.get_responses[0]
        self.assertEqual(response_message.data['content']['stdout'], "Hello, world!\n")


    @patch('subprocess.Popen')
    def test_handle_wsl_bash_invalid_command(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("", "Command not found")
        mock_process.returncode = 1
        mock_popen.return_value = mock_process

        self.message_handler.handle_wsl_bash(self.test_message)
        response_message = self.message_store.get_responses[0]
        self.assertEqual(response_message.data['content']['error'], "Command not found")


    @patch('subprocess.Popen')
    def test_handle_wsl_bash_valid_command(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Hello, world!\n", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        self.test_message.data['content'] = 'echo "Hello, world!"'
        self.message_handler.handle_wsl_bash(self.test_message)
        response_message = self.message_store.get_responses[0]
        self.assertEqual(response_message.data['content']['stdout'], "Hello, world!\n")


    def test_process_message(self):
        message_data = {
            "sender_actor": "chatgpt://root/project_id",
            "sender_agent": "http://ip:port/endpoint",
            "log_correlation_path": "kabana:guid1",
            "recipient_agent": "http://chatgpt-plugin-url",
            "recipient_actor": "chatgpt://plugin_id",
            "message_type": "wsl-bash",
            "content": "echo 'Hello, world!'"
        }
        message = Message(message_data)
        self.message_handler.process_message(message)
        response_message = self.message_store.get_responses[0]
        self.assertEqual(response_message.data['content']['stdout'], "Hello, world!\n")


if __name__ == '__main__':
    unittest.main()
