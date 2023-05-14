import logging
import quart
import quart_cors
from quart import send_file


from chatgpt_plugin.endpoints.send_message import send_message
from chatgpt_plugin.endpoints.get_messages import get_messages
from chatgpt_plugin.endpoints.plugin_manifest import plugin_manifest
from chatgpt_plugin.endpoints.openapi_spec import openapi_spec
from chatgpt_plugin.endpoints.execute_command import execute_command

from chatgpt_plugin.message_source import MessageSource

class RestMessageSource(MessageSource):
    def __init__(self, dispatcher):
        self.dispatcher = dispatcher  # store the dispatcher instance
        self.app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")
        logging.basicConfig(level=logging.INFO)

        @self.app.before_request
        async def log_request_info():
            from quart import request  # Import here
            logging.info('Body: %s', (await request.get_data()).decode())

        @self.app.after_request
        async def log_response_info(response):
            if "text" in response.mimetype or "json" in response.mimetype:
                logging.info('Response: %s', (await response.get_data()).decode())
            else:
                logging.info('Response: Binary data not logged')
            return response

        @self.app.route("/send-message", methods=['POST'])
        async def send_message_route():
            return await send_message(self.dispatcher)

        @self.app.route("/get-messages", methods=['POST'])
        async def get_messages_route():
            return await get_messages(self.dispatcher)

        @self.app.route('/logo.png')
        async def plugin_logo():
            return await send_file('logo.png', mimetype='image/png')


        self.app.route("/.well-known/ai-chatgpt_plugin.json", methods=['GET'])(plugin_manifest)
        self.app.route("/openapi.yaml", methods=['GET'])(openapi_spec)
        self.app.route("/execute-command", methods=['POST'])(execute_command)

    def run(self):
        self.app.run(debug=True, host="0.0.0.0", port=5003)

    async def receive_message(self):
        pass

    async def handle_message(self, message):
        # Here you can handle the incoming message as you wish
        pass
