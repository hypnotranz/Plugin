# chatgpt_plugin.py
class Plugin:
    def __init__(self, message_handler):
        self._message_handler = message_handler

    def filter(self, message):
        # implement filter logic here
        pass

    def handle_message(self, message):
        if self.filter(message):
            self._message_handler.process_message(message)
