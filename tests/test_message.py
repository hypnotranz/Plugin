# test_message_handler.py

import logging
logging.basicConfig(level=logging.INFO)

import sys
import os
import unittest

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.endpoints.message import Message


class TestMessage(unittest.TestCase):

    def test_message_creation(self):
        message_data = {
            "sender_actor": "chatgpt://root/project_id",
            "sender_agent": "http://ip:port/endpoint",
            "log_correlation_path": "kabana:guid1",
            "recipient_agent": "http://chatgpt-plugin-url",
            "recipient_actor": "chatgpt://plugin_id",
            "message_type": "wsl-bash",
            "subject": "echo 'Hello, world!'",
            "content": "echo 'Hello, world!'"
        }
        message = Message(message_data)
        self.assertEqual(message.data, message_data)

