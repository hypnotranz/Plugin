from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
from chatgpt_plugin.dispatcher import Dispatcher

class ManifestMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'manifest'

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        dispatcher = Dispatcher()

        # Get the complete manifest data
        manifest_data = dispatcher.get_complete_manifest()

        # Create a response message with the manifest data
        response_message = Message({
            "message_type": "response",
            "content": manifest_data
        })

        # Add the response message to the store
        message_store.add_message(response_message)

    @classmethod
    def get_examples(cls):
        return [
            {"message_type": "manifest", "content": "get_all_usage"},
            {"message_type": "manifest", "content": "get_all_examples"}
        ]
