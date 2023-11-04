import logging
import subprocess
import os
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.plugin import Plugin
from chatgpt_plugin.gpt import ChatGptAPI
import traceback
import pkgutil

import json


class MessageHandler:  # This class is responsible for handling messages
    def __init__(self, message_store: MessageStore):
        self.handlers = {}
        self.load_handlers()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))  # Corrected 'lacevelname' to 'levelname'

        self.logger.addHandler(handler)

        self.message_store = message_store

    def load_handlers(self):
        # Assuming all handler modules are in a directory named 'handlers'
        package_name = 'handlers'
        package = __import__(package_name, fromlist=[""])

        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = __import__(f"{package_name}.{module_name}", fromlist=[""])
            handler_class_name = ''.join(word.capitalize() for word in module_name.split('_'))
            handler_class = getattr(module, handler_class_name)
            message_type = handler_class.get_message_type()
            self.handlers[message_type] = handler_class  # store the class, not the handle_message method

    def process_message(self, message: Message):
        self.logger.info(f"Loading handlers: {message.data}")
        self.load_handlers()

        self.logger.info(f"Processing message: {message.data}")

        message_type = message.data.get('message_type')
        content = message.data.get('content')

        # Split the message_type by dot
        message_type_parts = message_type.split('.', 1)

        if len(message_type_parts) == 2:
            # If there are two parts, the first part is the handler and the second part is the method
            handler_name, method_name = message_type_parts
        else:
            # If there is only one part, it's just the handler name and there is no specific method
            handler_name = message_type_parts[0]
            method_name = None

        self.logger.info(f"Handler name: {handler_name}, Method name: {method_name}")

        if handler_name == 'get-message-types':
            self.handle_get_available_message_types_message(message)
        elif handler_name in self.handlers:
            handler_class = self.handlers[handler_name]
            self.logger.info(f"Handler class: {handler_class.__name__}")
            if method_name:
                self.logger.info(f"Method name: {method_name}")
                method = getattr(handler_class, method_name, None)
                if method:
                    self.logger.info(f"Method: {method}")
                    if callable(method):
                        self.logger.info(f"Method is callable")
                        method(message, self.message_store)
                    else:
                        self.logger.info(f"Method is not callable")
                else:
                    self.logger.info(f"Method not found in handler class")
            else:
                # Otherwise, call the handle_message method on an instance of the handler class
                handler = handler_class()  # create an instance of the handler class
                self.logger.info(f"Calling handle_message of handler {handler_name}")
                handler.handle_message(message, self.message_store)

    def handle_message(self, message):
        # Process the message and return a response
        self.process_message(message)
        response_messages = self.message_store.get_responses()
        if response_messages:
            return response_messages[0].data
        else:
            return None

    def get_complete_manifest(self):
        # Include the manifest data for the "get-message-types" message type
        complete_manifest = {
            "get-message-types": {
                "message_type": "get-message-types",
                "examples": [
                    {"message_type": "get-message-types", "content": ""},
                ]
            }
        }

        # Include the manifest data for the other message types
        for handler_class in self.handlers.values():
            message_type = handler_class.get_message_type()
            complete_manifest[message_type] = handler_class.get_manifest()

        return complete_manifest

    def handle_get_available_message_types_message(self, message):
        # Get the complete manifest data
        manifest_data = self.get_complete_manifest()

        # Create a response message with the manifest data
        response_message = Message({
            "message_type": "response",
            "content": manifest_data
        })

        # Add the response message to the store
        self.message_store.add_message(response_message)

    def get_all_usage(self):
        usage = {}
        for handler_class in self.handlers.values():
            message_type = handler_class.get_message_type()
            usage[message_type] = handler_class.get_usage()
        return usage

    def get_all_examples(self):
        examples = {
            "get-message-types": [
                {"message_type": "get-message-types", "content": " "},
                {"message_type": "get-message-types", "content": " "}
            ]
        }

        for handler_class in self.handlers.values():
            message_type = handler_class.get_message_type()
            examples[message_type] = handler_class.get_examples()

        examples_string = " ".join(str(example) for example_list in examples.values() for example in example_list)
        return examples_string

    def handle_manifest_message(self, message):
        # Get the complete manifest data
        manifest_data = self.get_complete_manifest()

        # Create a response message with the manifest data
        response_message = Message({
            "message_type": "response",
            "content": manifest_data
        })

        # Add the response message to the store
        self.message_store.add_message(response_message)
