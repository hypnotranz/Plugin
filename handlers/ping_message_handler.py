import socket
import os
import inspect
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.gpt import ChatGptAPI
from handlers.base_message_handler import BaseMessageHandler
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
class PingMessageHandler(BaseMessageHandler):

    @classmethod
    def get_message_type(cls):
        return 'ping'

    @classmethod
    def handle(cls, message, message_store):
        # Get IP address
        ip_address = socket.gethostbyname(socket.gethostname())

        # Get agent process info
        agent_process_info = os.getpid()



        response_content = {
            "ip_address": ip_address,
            "agent_process_info": agent_process_info,
            "method_reflection": method_reflection,
        }

        response_message = Message({
            "message_type": "response",
            "stdout": response_content, "stderr": '',
        })
        message_store.add_message(response_message)
        print(response_message)
