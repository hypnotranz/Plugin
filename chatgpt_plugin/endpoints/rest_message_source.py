# chatgpt_plugin/endpoints/rest_message_source.py
import logging
import quart
import quart_cors
from quart import send_file
import traceback
from quart import request, Response

from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.endpoints.send_message import send_message
from chatgpt_plugin.endpoints.get_messages import get_messages
from chatgpt_plugin.endpoints.plugin_manifest import plugin_manifest
from chatgpt_plugin.endpoints.openapi_spec import openapi_spec

from chatgpt_plugin.message_source import MessageSource
import warnings
import asyncio

# Ignore asyncio 'task took too long' warnings
warnings.filterwarnings('ignore', category=RuntimeWarning, module='asyncio')




class RestMessageSource(MessageSource):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher  # store the dispatcher instance
        self.app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
        logging.basicConfig(level=logging.INFO)



        @self.app.route("/send-message", methods=['POST'])
        async def send_message_route():
            logging.info(f"Received request");
            request_data = await quart.request.get_json(force=True)
            logging.info(f"Received request_data: {request_data}")
            message = Message(request_data)
            return await send_message(self.dispatcher, message)

        @self.app.route("/get-messages", methods=['POST'])
        async def get_messages_route():
            try:
                return await get_messages(self.dispatcher)
            except Exception as e:
                error_message = str(e)
                call_stack = traceback.format_exc()
                detailed_error_message = f"{error_message}\nCall Stack:\n{call_stack}"
                return quart.jsonify({"status": "Server Error", "content": detailed_error_message}), 500

        @self.app.route('/logo.png')
        async def plugin_logo():
            return await send_file('logo.png', mimetype='image/png')

        @self.app.route("/.well-known/ai-plugin.json", methods=['GET'])
        async def plugin_manifest_route():
            return await plugin_manifest(self.dispatcher)

        @self.app.route("/ai-plugin.json", methods=['GET'])
        async def plugin_manifest_route_alias():
            return await plugin_manifest(self.dispatcher)

        self.app.route("/openapi.yaml", methods=['GET'])(openapi_spec)

    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=5003)

    async def receive_message(self):
        pass

    async def handle_message(self, message):
        self.dispatcher.dispatch_message(message)
