# File: database_diagram_handler.py

import logging
import psycopg2
import xml.etree.ElementTree as ET
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_store import MessageStore
from handlers.base_message_handler import BaseMessageHandler  # Import BaseMessageHandler
class DatabaseDiagramMessageHandler(BaseMessageHandler):
    @staticmethod
    def get_message_type():
        return 'generate-database-diagram'

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
        logger.info(f"Generating database diagram: {message}")

        db_config = DatabaseDiagramMessageHandler._load_db_config_from_xml()

        conn = None
        cur = None
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()

            # Extract tables
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'dl';")
            tables = cur.fetchall()

            diagram_data = {}

            # Extract columns and relationships for each table
            for table in tables:
                table_name = table[0]
                cur.execute(f"SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_schema = 'dl' AND table_name = '{table_name}';")
                columns = cur.fetchall()

                cur.execute(f"SELECT conname, a.attname AS foreign_key, af.attname AS referenced_key, c.confrelid::regclass AS referenced_table FROM pg_attribute AS a JOIN pg_constraint AS c ON a.attnum = ANY(c.conkey) JOIN pg_attribute AS af ON af.attnum = ANY(c.confkey) AND af.attrelid = c.confrelid WHERE c.confrelid = 'dl.{table_name}'::regclass;")
                relationships = cur.fetchall()

                diagram_data[table_name] = {
                    "columns": columns,
                    "relationships": relationships
                }

            response_message = Message({
                "message_type": "response",
                "stdout": diagram_data,
                "stderr": '',
            })
            logger.info(f"Adding database diagram data to store: {response_message.to_dict()}")
            message_store.add_message(response_message)

        except Exception as e:
            error_message = f"Failed to generate database diagram: {e}"
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


