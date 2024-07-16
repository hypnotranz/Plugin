from chatgpt_plugin.dispatcher import Dispatcher
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.endpoints.rest_message_source import RestMessageSource
from chatgpt_plugin.plugin import Plugin
import asyncio
import os

# Set the environment variable for asyncio debugging
os.environ['PYTHONASYNCIODEBUG'] = '0'

# Get the event loop
loop = asyncio.get_event_loop()

# Set the debug mode
loop.set_debug(False)

# Initialize the message store
message_store = MessageStore()

# Initialize the message handler
message_handler = MessageHandler(message_store)

# Initialize the new plugin
wsl_bash_plugin = Plugin(message_store)

# Initialize the dispatcher with the message store, message handler, and the new plugin
dispatcher = Dispatcher(message_store, message_handler)

# Register the new plugin with the dispatcher
dispatcher.register_plugin(wsl_bash_plugin)

# Initialize a list of message sources
sources = [RestMessageSource(dispatcher)]

# Start message sources
for source in sources:
    source.run()
