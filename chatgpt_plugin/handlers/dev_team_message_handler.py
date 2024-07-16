from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.gpt import ChatGptAPI
import logging
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
class DevTeamMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'dev_team'

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling dev_team message: {message}")

        chat_gpt = ChatGptAPI()

        messages = chat_gpt.wrap_message_for_gpt(message.data.get('content'))
        response = chat_gpt.generate_response(messages)

        response_message = Message({
            "message_type": "response",
            "stdout": response, "stderr": '',
        })
        message_store.add_message(response_message)
        print(response_message)

    @classmethod
    def get_examples(cls):
        return [
            {"message_type": "dev_team", "content": "Implement a function to calculate the Fibonacci sequence up to the nth element."},
            {"message_type": "dev_team", "content": "Can you explain the difference between a class and an object in object-oriented programming?"}
        ]
