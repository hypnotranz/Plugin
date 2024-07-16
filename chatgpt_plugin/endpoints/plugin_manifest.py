# plugin_manifest.py
from quart import request
import quart
import json

from chatgpt_plugin.dispatcher import Dispatcher


async def plugin_manifest(dispatcher):
    message_handler = dispatcher.get_message_handler()  # Assuming you have this method on the dispatcher

    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        plugin_manifest_data = json.loads(text)

        # Get the example payloads from the MessageHandler
        example_payloads = message_handler.get_all_examples()  # Assuming this method returns the examples

        # Append the example payloads to the description_for_model
        plugin_manifest_data["description_for_model"] += "\nExample Payloads:\n" + json.dumps(example_payloads)

        return quart.Response(json.dumps(plugin_manifest_data), mimetype="text/json")
