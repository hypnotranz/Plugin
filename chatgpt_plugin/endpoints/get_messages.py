# Filename: get_messages.py
from quart import request, jsonify, abort
from xml.etree import ElementTree as ET
import logging
import os

from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.plugin import Plugin


async def get_messages(dispatcher):
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        message_data = await request.get_json(force=True)
    else:
        abort(400, description="Unsupported Content-Type, only application/json and application/xml are supported")

    logging.info(f"Received message: {message_data}")

    # Create a Message object from the parsed data
    message = Message(message_data)

    # Here is where you'd pass the message to your message handler
    dispatcher.dispatch_message(message)

    # Retrieve the processed messages using the getter methods
    plugins = dispatcher.get_plugins()
    processed_messages = []

    processed_messages = dispatcher.get_responses(0)
    processed_messages = [message.to_dict() for message in processed_messages]
    return jsonify(processed_messages)
