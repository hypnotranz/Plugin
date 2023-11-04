# dispatcher.py
from chatgpt_plugin.endpoints.message import Message
import logging

from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.message_store import MessageStore


class Dispatcher:
    def __init__(self, message_store: MessageStore, message_handler: MessageHandler):
        self._plugins = []
        self._message_store = message_store
        self._message_handler = message_handler

    def register_plugin(self, plugin):
        self._plugins.append(plugin)

    def dispatch_message(self, message: Message):
        self._message_store.add_message(message)
        self._message_handler.process_message(message)
        for plugin in self._plugins:
            if plugin.filter(message):
                plugin.handle_message(message)
#                self._message_store.add_message(Message(response))

    def get_responses(self, message_id):
        return self._message_store.get_responses

    def get_plugins(self):
        return self._plugins

    def get_message_handler(self):
        return self._message_handler