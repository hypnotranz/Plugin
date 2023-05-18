from chatgpt_plugin.dispatcher import Dispatcher
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.endpoints.rest_message_source import RestMessageSource
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

# Initialize the dispatcher with the message store and message handler
dispatcher = Dispatcher(message_store, message_handler)

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
