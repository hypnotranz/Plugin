# chatgpt_plugin.py
from chatgpt_plugin.endpoints.message import Message

class Plugin:
    def __init__(self, message_handler):
        self._message_handler = message_handler

    def filter(self, message: Message):
        # Only process 'wsl-bash' messages
        return message.message_type == 'wsl-bash' or message.message_type == 'dev_team'

    def handle_message(self, message: Message):
        if self.filter(message):
            self._message_handler.process_message(message)

