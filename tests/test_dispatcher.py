import unittest
from unittest.mock import patch, MagicMock
from chatgpt_plugin.dispatcher import Dispatcher
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.endpoints.message import Message

class TestDispatcher(unittest.TestCase):
    def setUp(self):
        self.message_store = MessageStore()
        self.message_handler = MessageHandler(self.message_store)
        self.dispatcher = Dispatcher(self.message_store, self.message_handler)
        self.test_message = Message({
            'sender_actor': 'chatgpt://developer_1',
            'sender_agent': 'http://localhost:5003/send-message',
            'log_correlation_path': '1234',
            'recipient_agent': 'http://localhost:5003/send-message',
            'recipient_actor': 'unix_manager',
            'message_type': 'wsl-bash',
            'subject': 'Test command',
            'content': 'echo "Hello, world!"'
        })

    @patch('subprocess.Popen')
    def test_dispatch(self, mock_popen):
        mock_process = MagicMock()
        mock_process.communicate.return_value = ("Hello, world!\n", "")
        mock_process.returncode = 0
        mock_popen.return_value = mock_process

        self.dispatcher.dispatch_message(self.test_message)
        response_messages = self.message_store.get_responses
        self.assertTrue(response_messages, "No response messages were created.")
        response_message = response_messages[0]
        self.assertEqual(response_message.data['content']['stdout'], "Hello, world!\n")


if __name__ == '__main__':
    unittest.main()
