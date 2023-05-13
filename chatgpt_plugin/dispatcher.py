# dispatcher.py
class Dispatcher:
    def __init__(self):
        self._plugins = []

    def register_plugin(self, plugin):
        self._plugins.append(plugin)

    def dispatch_message(self, message):
        for plugin in self._plugins:
            if plugin.filter(message):
                plugin.handle_message(message)
