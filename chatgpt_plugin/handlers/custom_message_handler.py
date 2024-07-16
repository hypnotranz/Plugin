from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
import logging

class CustomMessageHandler(BaseMessageHandler):
    @classmethod
    def get_message_type(cls):
        return 'custom-message'

    @classmethod
    def handle(cls, message: Message) -> Message:
        response_message = Message({
            "message_type": "response",
            "stdout": "custom message received",  # set the response content here
            "stderr": '',
        })
        return response_message
