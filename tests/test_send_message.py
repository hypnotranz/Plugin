#test_send_message.py

import unittest
from unittest.mock import patch, MagicMock
from quart import Quart
from quart.testing import QuartClient
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.endpoints.send_message import send_message
from chatgpt_plugin.endpoints.get_messages import get_messages

app = Quart(__name__)

@app.route('/send-message', methods=['POST'])
async def handle_send_message():
    return await send_message(MessageHandler(MessageStore()))

class TestSendMessage(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = QuartClient(self.app)

    @patch.object(MessageHandler, 'dispatch_message', new_callable=MagicMock)
    async def test_send_message(self, mock_dispatch_message):
        message = {
            'sender_actor': 'chatgpt://developer_1',
            'sender_agent': 'http://localhost:5003/send-message',
            'log_correlation_path': '1234',
            'recipient_agent': 'http://localhost:5003/send-message',
            'recipient_actor': 'unix_manager',
            'message_type': 'wsl-bash',
            'subject': 'Test command',
            'content': 'echo "Hello, world!"'
        }

        response = await self.client.post('/send-message', json=message)
        mock_dispatch_message.assert_called_once()
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
