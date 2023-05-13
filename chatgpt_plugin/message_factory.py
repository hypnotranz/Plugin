# message_factory.py
from .message import Message

class MessageFactory:
    def create_message(self, data):
        return Message(data)
