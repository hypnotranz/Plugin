import subprocess
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
import logging
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler

class WslBashMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'wsl-bash'

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling status update: {message}")

        command = message.data.get("content")

        if not command:
            logger.error("Invalid command")
            return

        logger.info(f"Executing command: {command}")

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
                error_message = stderr if stderr else "Command failed with exit status " + str(process.returncode)
                response_message = Message({
                    "message_type": "response",
                    "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                    "error": error_message,
                    "pdf_files": subprocess.os.getcwd(),
                })
                logger.info(f"Adding error response message to store: {response_message.to_dict()}")
                message_store.add_message(response_message)
            else:
                response_message = Message({
                    "message_type": "response",
                    "stdout": stdout, "stderr": stderr,
                })
            logger.info(f"Adding response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)
        except Exception as e:
            logger.error(f"Failed to execute command: {e}")
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": str(e),
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)


    @classmethod
    def get_examples(cls):
        return [
            {"message_type": "wsl-bash", "content": "ls -la"},
            {"message_type": "wsl-bash", "content": "mkdir new_directory"}
        ]
