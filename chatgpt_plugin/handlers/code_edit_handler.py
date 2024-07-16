import json
import re
import logging
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler


class CodeEditHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'code-edit'

    @staticmethod
    def check_parameters(message):
        required_params = ['file_path', 'transformations']
        for param in required_params:
            if param not in message.data:
                raise ValueError(f"Missing required parameter: {param}")

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling code-edit: {message}")

        try:
            CodeEditHandler.check_parameters(message)

            data = json.loads(message.content)
            file_path = data['file_path']
            transformations = data['transformations']

            with open(file_path, 'r') as file:
                text = file.read()

            for transformation in transformations:
                before_regex = transformation['before_regex']
                after_regex = transformation['after_regex']
                replacement_text = transformation['replacement_text']
                pattern = f"{before_regex}.*{after_regex}"
                text = re.sub(pattern, replacement_text, text, flags=re.DOTALL)

            with open(file_path, 'w') as file:
                file.write(text)

            response_message = Message({
                "message_type": "response",
                "stdout": "Code edit completed successfully",
                "stderr": '',
            })
            logger.info(f"Adding response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)
        except Exception as e:
            logger.error(f"Failed to handle code-edit: {e}")
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": str(e),
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)
