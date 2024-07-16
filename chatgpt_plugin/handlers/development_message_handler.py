from handlers.base_message_handler import BaseMessageHandler


class DevelopmentMessageHandler(BaseMessageHandler):
    @classmethod
    def get_message_type(cls):
        return 'development'

