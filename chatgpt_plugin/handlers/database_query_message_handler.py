import logging
import psycopg2
import xml.etree.ElementTree as ET
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
class DatabaseQueryMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'db-query'

    @staticmethod
    def _load_db_config_from_xml():
        tree = ET.parse('handlers/extractData.xml')
        root = tree.getroot()

        config = {
            "host": root.findtext('connectionString').split("//")[1].split(":")[0],
            "port": root.findtext('connectionString').split(":")[2].split("/")[0],
            "dbname": root.findtext('connectionString').split("/")[-1],
            "user": root.findtext('userid'),
            "password": root.findtext('password')
        }
        return config

    @staticmethod
    def handle_message(message, message_store: MessageStore):
        logger = logging.getLogger(__name__)
        logger.info(f"Handling db-query: {message}")

        # Extract SQL from the message
        sql = message.data.get("content")
        if not sql:
            error_message = "No SQL provided"
            logger.error(error_message)
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": error_message,
            })
            message_store.add_message(response_message)
            return

        db_config = DatabaseQueryMessageHandler._load_db_config_from_xml()

        conn = None
        cur = None
        try:
            # Connect to the database using the loaded config
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            cur.execute(sql)
            results = cur.fetchall()

            response_message = Message({
                "message_type": "response",
                "stdout": results,
                "stderr": '',
            })
            logger.info(f"Adding response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

        except Exception as e:
            error_message = f"Failed to execute db-query: {e}"
            logger.error(error_message)
            response_message = Message({
                "subject": "Response to " + (message.subject if message.subject is not None else "unknown subject"),
                "error": error_message,
            })
            logger.info(f"Adding error response message to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()
