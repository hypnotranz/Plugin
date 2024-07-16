#message.py
import uuid
import logging
logging.basicConfig(level=logging.INFO)

import uuid
import logging

logging.basicConfig(level=logging.INFO)


class Message:
    def __init__(self, data):
        self.data = data
        self.message_id = 1
        #logging.info(f"Message created with ID: {self.message_id} and data: {self.data}")

        self.parent_id = data.get('parent_id')
        self.sender_actor = data.get('sender_actor')
        self.sender_agent = data.get('sender_agent')
        self.log_correlation_path = data.get('log_correlation_path')
        self.recipient_agent = data.get('recipient_agent')
        self.recipient_actor = data.get('recipient_actor')
        self.message_type = data.get('message_type')
        self.subject = data.get('subject')
        self.content = data.get('content')

    def to_dict(self):
        return {
            "data": self.data,
            "message_id": self.message_id,
   #         "parent_id": self.parent_id,
   #         "sender_actor": self.sender_actor,
   #         "sender_agent": self.sender_agent,
   #         "log_correlation_path": self.log_correlation_path,
   #         "recipient_agent": self.recipient_agent,
   #         "recipient_actor": self.recipient_actor,
            "message_type": self.message_type,
   #         "subject": self.subject,
            "content": self.content,
        }
