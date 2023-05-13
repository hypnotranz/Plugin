# send_message.py
from quart import request, jsonify, abort
import json
import xmltodict
from xml.etree import ElementTree as ET
import logging

async def send_message(dispatcher):
    content_type = request.headers.get('Content-Type')
    raw_data = await request.get_data()

    logging.info(f"Received raw message: {raw_data.decode()}")

    if content_type == 'application/json':
        try:
            message = json.loads(raw_data)
        except json.JSONDecodeError:
            abort(400, description="Invalid JSON")
    elif content_type == 'application/xml':
        try:
            message = xmltodict.parse(raw_data.decode())
        except ET.ParseError:
            abort(400, description="Invalid XML")
    else:
        abort(400, description="Unsupported Content-Type, only application/json and application/xml are supported")

    logging.info(f"Parsed message: {message}")

    # Here is where you'd pass the message to your message handler
    dispatcher.dispatch_message(message)

    return jsonify({"status": "Message received successfully"})
