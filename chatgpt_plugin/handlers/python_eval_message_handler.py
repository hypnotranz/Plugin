import traceback
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
import logging
import json
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
class PythonEvalMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'python-eval'

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        code = message.data.get('content')
        try:
            result = eval(code)
            response_message = Message({
                "message_type": "response",
                "stdout": result, "stderr": '',
            })

        except Exception as e:
            result = traceback.format_exc()
            response_message = Message({
                "message_type": "response",
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": str(e),
            })
        logger.info(f"Returning {json.dumps(response_message.to_dict())}")
        message_store.add_message(response_message)
