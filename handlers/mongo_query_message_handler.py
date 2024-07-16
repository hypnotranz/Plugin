import logging
from pymongo import MongoClient
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler


class MongoQueryMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'mongo-db-query'

    @staticmethod
    def _load_db_config():
        # Modify this method to load the MongoDB configuration as needed

        config = {
            "host": 'localhost',
            "port": 27017,
            "username": 'admin',
            "password": 'Password123',
            "authSource": 'agents',

        }
        return config

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling mongo-db-query: {message}")

        content = message.data.get("content")
        if not content:
            error_message = "No query details provided"
            logger.error(error_message)
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": error_message,
            })
            message_store.add_message(response_message)
            return

        operation = content.get("operation")
        collection_name = content.get("collection")
        db_config = MongoQueryMessageHandler._load_db_config()
        client = MongoClient(**db_config)
        db = client['test']
        collection = db[collection_name]

        try:
            results_list = []  # Initialize results_list

            if operation == "find":
                query = content.get("query")
                results = collection.find(query)
                results_list = []
                for result in results:
                    # Convert ObjectId to string
                    result['_id'] = str(result['_id'])
                    results_list.append(result)

            elif operation == "insert":
                document = content.get("document")
                results = collection.insert_one(document)
                results_list = [results.inserted_id]
            # Handle other operations as needed
            else:
                error_message = f"Unsupported operation: {operation}"
                logger.error(error_message)
                results_list = [error_message]  # Assign a value to results_list for unsupported operations

            response_message = Message({
                "message_type": "response",
                "stdout": results_list,
                "stderr": '',
            })
            logger.info(f"Adding response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

        except Exception as e:
            error_message = f"Failed to execute mongo-db-query: {e}"
            logger.error(error_message)
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": error_message,
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

        finally:
            client.close()
