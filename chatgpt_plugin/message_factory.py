# message_factory.py
from chatgpt_plugin.endpoints.message import Message

class MessageFactory:
    def create_message(self, data):
        return Message(data)
