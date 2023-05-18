# plugin.py
from chatgpt_plugin.endpoints.message import Message

import logging

class Plugin:
    def __init__(self, message_handler):
        self._message_handler = message_handler
        self.logger = logging.getLogger(__name__)

    def filter(self, message: dict):  # Expect a dictionary
        # Always process the message
        return True

    def handle_message(self, message: dict):  # Expect a dictionary
        self.logger.info(f"Received message in Plugin: {message}")
        if self.filter(message):  # Pass the dictionary directly
            self._message_handler.process_message(Message(message))


    def get_message_handler(self):
        return self._message_handler