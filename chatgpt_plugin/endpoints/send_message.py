# send_message.py
from chatgpt_plugin.endpoints.message import Message
from quart import request, jsonify, abort
from xml.etree import ElementTree as ET
import logging
import json
import xmltodict
import uuid
from chatgpt_plugin.message_factory import MessageFactory

message_factory = MessageFactory()


async def parse_message_data(message: Message):
    if message is None:
        content_type = request.headers.get('Content-Type')
        raw_data = await request.get_data()

    logging.info(f"Received raw message: {raw_data.decode()}")

    if content_type == 'application/json':
        try:
            message_data = json.loads(raw_data)
            if not all(key in message_data for key in (
            'sender_actor', 'sender_agent', 'log_correlation_path', 'recipient_agent', 'recipient_actor',
            'message_type', 'subject')):
                abort(400, description="Invalid JSON: missing required fields")
            message = message_factory.create_message(message_data)
        except json.JSONDecodeError:
            abort(400, description="Invalid JSON")
    elif content_type == 'application/xml':
        try:
            message_data = xmltodict.parse(raw_data.decode())
            message = message_factory.create_message(message_data)
        except ET.ParseError:
            abort(400, description="Invalid XML")
    else:
        abort(400, description="Unsupported Content-Type, only application/json and application/xml are supported")

    logging.info(f"Parsed message: {message.data}")

    return message


async def send_message(dispatcher, message: Message):
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        message_data = await request.get_json(force=True)
    else:
        abort(400, description="Unsupported Content-Type, only application/json and application/xml are supported")

    logging.info(f"Received message: {message_data}")

    # Generate a unique ID for the message
    message_id = str(uuid.uuid4())

    message_data['message_id'] = message_id

    # Create a Message object from the parsed data, passing the unique ID
    message = Message(message_data)

    # Here is where you'd pass the message to your message handler
    dispatcher.dispatch_message(message)

    # Retrieve the processed messages using the getter methods
    plugins = dispatcher.get_plugins()
    processed_messages = []

    processed_messages = dispatcher.get_responses(0)
    processed_messages = [message.to_dict() for message in processed_messages]

    # Log the processed messages
    logging.info(f"Processed messages: {processed_messages}")

    responses = jsonify(processed_messages)

    # Log the JSONified response
    logging.info(f"JSONified response: {responses}")

    return responses

