import logging
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler

class EchoMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'echo'

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Echoing message: {message}")

        response_message = Message({
            "message_type": "response",
            "stdout": message.data.get("content"),
            "stderr": '',
        })

        logger.info(f"Adding response message to store: {response_message.to_dict()}")
        message_store.add_message(response_message)

    @classmethod
    def get_examples(cls):
        return [{"message_type": "echo", "content": "This is a test message"}]
