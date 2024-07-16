# message_source.py
from chatgpt_plugin.endpoints.message import Message

from abc import ABC, abstractmethod


class MessageSource(ABC):
    @abstractmethod
    async def receive_message(self):
        pass

    def contains_message(self, message_id):
        return message_id in self._messages
