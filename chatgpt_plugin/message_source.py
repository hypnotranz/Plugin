# message_source.py
from abc import ABC, abstractmethod

class MessageSource(ABC):
    @abstractmethod
    async def receive_message(self):
        pass
