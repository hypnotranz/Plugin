# message_store.py
import logging

logging.basicConfig(level=logging.INFO)

from chatgpt_plugin.endpoints.message import Message


class MessageStore:
    def __init__(self):
        self._store = {}

    def add_message(self, message):
        self._store[message.message_id] = message
        logging.info(f"Message stored: {message.message_id}")
        logging.info(f"Current store: {self._store}")

    def get_message(self, message_id):
        logging.info(f"Getting message: {message_id}")
        message = self._store.get(message_id)
        logging.info(f"Retrieved message: {message}")
        logging.info(f"Current store: {self._store}")
        return message

    @property
    def get_responses(self):
        return [msg for msg in self._store.values()]

    def contains_message(self, message_id):
        return message_id in self._store
