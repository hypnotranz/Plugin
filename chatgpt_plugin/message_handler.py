# message_handler.py

import logging
import subprocess
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.plugin import Plugin
import json

class MessageHandler: # This class is responsible for handling messages
    def __init__(self, message_store: MessageStore):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        self.logger.addHandler(handler)

        self.message_store = message_store

    def process_message(self, message: Message):
        self.logger.info(f"Processing message: {message.data}")

        message_type = message.data.get('message_type')
        content = message.data.get('content')

        if message_type == 'wsl-bash':
            self.logger.info(f"Handling wsl-bash message: {message}")
            self.handle_wsl_bash(message)

    def handle_wsl_bash(self, message):
        self.logger.info(f"Handling status update: {message}")

        command = message.data.get("content")

        if not command:
            self.logger.error("Invalid command")
            return

        self.logger.info(f"Executing command: {command}")

        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate()
            if process.returncode != 0:
                raise Exception(stderr)
            else:
                response_message = Message({
                    "parent_id": message.message_id,
                    "sender_actor": message.recipient_actor,
                    "sender_agent": message.recipient_agent,
                    "log_correlation_path": message.log_correlation_path,
                    "recipient_agent": message.sender_agent,
                    "recipient_actor": message.sender_actor,
                    "message_type": "response",
                    "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                    "content": {"command": command, "stdout": stdout, "stderr": stderr},
                })
                self.logger.info(f"Adding response message to store: {response_message.to_dict()}")
                self.message_store.add_message(response_message)
        except Exception as e:
            self.logger.error(f"Failed to execute command: {e}")
            response_message = Message({
                "parent_id": message.message_id,
                "sender_actor": message.recipient_actor,
                "sender_agent": message.recipient_agent,
                "log_correlation_path": message.log_correlation_path,
                "recipient_agent": message.sender_agent,
                "recipient_actor": message.sender_actor,
                "message_type": "response",
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "content": {"command": command, "error": str(e)},
            })
            self.logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            self.message_store.add_message(response_message)

    def handle_message(self, message):
        # Process the message and return a response
        self.process_message(message)
        response_messages = self.message_store.get_responses()
        if response_messages:
            return response_messages[0].data
        else:
            return None
