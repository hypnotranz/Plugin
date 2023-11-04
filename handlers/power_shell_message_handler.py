import subprocess
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
import logging
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
class PowerShellMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'powershell'

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling PowerShell command: {message}")

        command = message.data.get("content")

        if not command:
            logger.error("Invalid command")
            return

        logger.info(f"Executing PowerShell command: {command}")

        # Prefix the command with 'powershell' to ensure it's executed in PowerShell
        full_command = f"powershell {command}"

        try:
            process = subprocess.Popen(
                full_command,
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
            logger.error(f"Failed to execute PowerShell command: {e}")
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": str(e),
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

    @classmethod
    def get_examples(cls):
        return [
       #     {"message_type": "powershell", "content": "Get-Content -Path 'pathtofilefile.txt'"},
      #      {"message_type": "powershell", "content": "(Get-Content 'pathtofilefile.txt') -replace 'oldString', 'newString' | Set-Content 'C:pathtofilefile.txt'"}
        ]
