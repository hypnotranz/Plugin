import json
import logging
import xmltodict
from quart import request, jsonify, abort
from xml.etree import ElementTree as ET
import json
import quart
import quart_cors
import subprocess
from quart import request


app = quart_cors.cors(quart.Quart(__name__), allow_origin="https://chat.openai.com")

logging.basicConfig(level=logging.INFO)

@app.before_request
async def log_request_info():
    # logging.info('Headers: %s', request.headers)
    logging.info('Body: %s', await request.get_data())

@app.after_request
async def log_response_info(response):
    logging.info('Response: %s', await response.get_data())
    return response
@app.post("/send-message")
async def send_message():
    content_type = request.headers.get('Content-Type')
    raw_data = await request.get_data()

    # Log the raw received message
    logging.info(f"Received raw message: {raw_data}")

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

    # Log the parsed message
    logging.info(f"Parsed message: {message}")

    # TODO: Implement your message handling logic here
    # For now, we'll just return a success status
    return jsonify({"status": "Message received successfully"})



@app.post("/get-messages")
async def get_messages():
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

    # Log the received message
    logging.info(f"Received message: {message}")

    # TODO: Implement your message retrieval and filtering logic here
    # For now, we'll just return an empty list
    messages = []

    return jsonify(messages)

@app.get("/logo.png")
async def plugin_logo():
    filename = 'logo.png'
    return await quart.send_file(filename, mimetype='image/png')

@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest():
    host = request.headers['Host']
    with open("./.well-known/ai-plugin.json") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/json")

@app.get("/openapi.yaml")
async def openapi_spec():
    host = request.headers['Host']
    with open("openapi.yaml") as f:
        text = f.read()
        return quart.Response(text, mimetype="text/yaml")

@app.post("/execute-command")
async def execute_command():
    request_data = await quart.request.get_json(force=True)
    command = request_data.get("command")
    stdin = request_data.get("stdin")

    logging.info(f"Executing command: {command}")

    process = subprocess.Popen(
        command,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    stdout, stderr = process.communicate(stdin)

    logging.info(f"Command output (stdout): {stdout}")
    logging.info(f"Command output (stderr): {stderr}")

    return quart.jsonify({"command": command, "stdout": stdout, "stderr": stderr})

def main():
    app.run(debug=True, host="0.0.0.0", port=5003)

if __name__ == "__main__":
    main()
