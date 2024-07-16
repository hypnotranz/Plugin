-e from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.gpt import ChatGptAPI
import logging
from handlers.base_message_handler import BaseMessageHandler

class DevTeamMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return "dev-team"

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling dev_team message: {message}")

        chat_gpt = ChatGptAPI()

        try:
            messages = chat_gpt.wrap_message_for_gpt(message.data.get("content"))
            logger.info(f"Wrapped message for GPT: {messages}")

            response = chat_gpt.generate_response(messages)
            logger.info(f"Response from GPT: {response}")

            response_message = Message({
                "message_type": "response",
                "stdout": response,
                "stderr": ""
            })
            logger.info(f"Adding response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

        except Exception as e:
            logger.error(f"Failed to process dev_team message: {e}")
            response_message = Message({
                "message_type": "response",
                "error": str(e)
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

    @classmethod
    def get_examples(cls):
        return [
            {"message_type": "dev-team", "content": "Implement a function to calculate the Fibonacci sequence up to the nth element."},
            {"message_type": "dev-team", "content": "Can you explain the difference between a class and an object in object-oriented programming?"}
        ]
