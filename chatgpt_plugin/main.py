from chatgpt_plugin.dispatcher import Dispatcher
from chatgpt_plugin.chatgpt_plugin import Plugin
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.endpoints.rest_message_source import RestMessageSource


# Initialize the dispatcher
dispatcher = Dispatcher()

# Initialize a list of plugins
plugins = [Plugin(MessageHandler())]

# Register plugins with the dispatcher
for plugin in plugins:
    dispatcher.register_plugin(plugin)

# Initialize a list of message sources
sources = [RestMessageSource(dispatcher)]

# Start message sources
for source in sources:
    source.run()

# Here you would typically have a loop that dispatches messages from the sources
# Something like this:
# while True:
#     for source in sources:
#         message = source.receive_message()
#         dispatcher.dispatch_message(message)
