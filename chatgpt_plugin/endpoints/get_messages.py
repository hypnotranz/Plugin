# get_messages.py
from quart import request, jsonify, abort
from xml.etree import ElementTree as ET
import logging

async def get_messages(dispatcher):
    content_type = request.headers.get('Content-Type')

    if content_type == 'application/json':
        message = await request.get_json(force=True)
    elif content_type == 'application/xml':
        xml_data = await request.get_data()
        try:
            message = ET.fromstring(xml_data.decode())
        except ET.ParseError:
            abort(400, description="Invalid XML")
    else:
        abort(400, description="Unsupported Content-Type, only application/json and application/xml are supported")

    logging.info(f"Received message: {message}")

    # Here is where you'd pass the message to your message handler
    dispatcher.dispatch_message(message)

    return jsonify([])  # I'm assuming that the get-messages endpoint should return an empty list
