import json
import re
import logging
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler

class CodeSnippetHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'code-snippet'


    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling code-snippet: {message}")

        try:
            data = json.loads(message.content)
            file_path = data['file_path']
            before_regex = data['before_regex']
            after_regex = data['after_regex']

            with open(file_path, 'r') as file:
                text = file.read()

            pattern = f"{before_regex}.*{after_regex}"
            snippet = re.search(pattern, text, flags=re.DOTALL)

            if snippet is not None:
                snippet_text = snippet.group()
            else:
                snippet_text = "No matching snippet found."

            response_message = Message({
                "message_type": "response",
                "stdout": snippet_text,
                "stderr": '',
            })
            logger.info(f"Adding response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)
        except Exception as e:
            logger.error(f"Failed to correctly handle code-snippet: {e}")
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": str(e),
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)
