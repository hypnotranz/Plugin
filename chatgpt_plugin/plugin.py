# plugin.py
from chatgpt_plugin.endpoints.message import Message

import logging


import logging
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore

class Plugin:
    def __init__(self, message_store: MessageStore):
        from chatgpt_plugin.message_handler import MessageHandler
        self._message_handler = MessageHandler(message_store)  # Default MessageHandler
        self.logger = logging.getLogger(__name__)

    def filter(self, message: Message):  # Expect a Message object
        # Always process the message
        return True

    def handle_message(self, message: Message):  # Expect a Message object
        self.logger.info(f"Received message in Plugin: {message}")
        if self.filter(message):
            self._message_handler.process_message(message)
