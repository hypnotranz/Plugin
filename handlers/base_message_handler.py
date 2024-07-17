from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
import logging
import inspect
import re

class BaseMessageHandler:
    @classmethod
    def read_class(cls, message: Message, message_store: MessageStore):

        # Implement the logic for 'read_class' here
        logger = logging.getLogger(cls.__name__)
        logger.info(f"Executing read_class method for {cls.__name__}")
        source_code = inspect.getsource(cls)
        logger.info(f"Source code: {source_code}")
        response_message = Message({
            "message_type": "response",
            "stdout": source_code,  # set the response content here
            "stderr": '',
        })
        logger.info(f"Adding response message to store: {response_message.to_dict()}")
        message_store.add_message(response_message)



    @classmethod
    def count_tokens(cls, message: Message, message_store: MessageStore):
        # Get the code using the read_class method
        logger = logging.getLogger(cls.__name__)
        source_code = inspect.getsource(cls)

        # Split the code into tokens using regular expressions
        tokens = re.findall(r'\w+|[^\w\s]', source_code)
        number_of_tokens = len(tokens)

        response_message = Message({
            "message_type": "response",
            "stdout": number_of_tokens,  # set the response content here
            "stderr": '',
        })
        logger.info(f"Adding response message to store: {response_message.to_dict()}")
        message_store.add_message(response_message)


    @classmethod
    def get_message_type(cls):
        return 'base-message'

    @classmethod
    def get_message_structure(cls):
        return {
            "message_type": cls.get_message_type(),
            "content": ""
        }

    @classmethod
    def inspect(cls):
        return inspect.getsource(cls)

    @classmethod
    def handle_message(cls, message, message_store: MessageStore):
        logger = logging.getLogger(cls.__name__)
        logger.info(f"Handling {cls.get_message_type()}: {message}")

        if not cls.check_parameters(message):
            logger.error("Invalid parameters")
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": "Invalid parameters",
                "manifest": cls.get_manifest()
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)
            return

        response_message = None  # Initialize response_message to None

        try:
            # Process system message
            if cls.handle_system_message(logger, message, message_store):
                return  # If handle_system_message returns True, exit the method

            # If handle_system_message returns False, call the handle method
            response_message = cls.handle(message)

            logger.info(f"Adding response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)
        except Exception as e:
            logger.error(f"Failed to handle {cls.get_message_type()}: {e}")
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": str(e),
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)



    @classmethod
    def handle_system_message(cls, logger, message, message_store):
        logger.info("Processing System Segment")
        message_dict = message.to_dict()
        if 'message_type' in message_dict:  # Access 'message_type' field
            message_type = message_dict['message_type']
            if '.' in message_type:  # If message_type contains a dot
                _, method_name = message_type.split('.', 1)  # Split message_type into base_message_type and method_name
            else:
                method_name = message_dict['content'].replace('()', '')  # remove the parentheses
            logger.info(f"Method name: {method_name}")
            # Check if the method exists in the class
            instance = cls()  # create an instance of the class

            if hasattr(instance, method_name):
                logger.info(f"Method {method_name} exists in the class")
                method = getattr(instance, method_name)
                # Call the method and get the result
                result = method()
                logger.info(f"Result of method call: {result}")
                # Create a response message with the result
                response_message = Message({
                    "message_type": "response",
                    "stdout": str(result),  # set the response content here
                    "stderr": '',
                })
                logger.info(f"Adding response message to store: {response_message.to_dict()}")
                message_store.add_message(response_message)
                return True
            else:
                logger.info(f"Method {method_name} does not exist in the class")
        return False

    @classmethod
    def handle(cls, message: Message) -> Message:
        response_message = Message({
            "message_type": "response",
            "stdout": "base message received",  # set the response content here
            "stderr": '',
        })
        return response_message

    @classmethod
    def get_manifest(cls):
        return cls.get_message_structure()

    @classmethod
    def check_parameters(cls, message: Message) -> bool:
        message_dict = message.to_dict()  # convert the Message object to a dictionary
        required_keys = set(cls.get_message_structure().keys())
        # Check if all required keys are present
        if not required_keys.issubset(set(message_dict.keys())):
            return False

        # Additional validation
        if not isinstance(message_dict.get('message_type'), str):
            return False
        if not isinstance(message_dict.get('content'), str):
            return False

        return True

    @classmethod
    def get_usage(cls):
        return "Description of the handler."

    @classmethod
    def get_examples(cls):
        return [cls.get_message_structure()]

