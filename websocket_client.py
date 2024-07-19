import asyncio
import websockets
import requests
import logging
import traceback
import sys
import json

logging.basicConfig(level=logging.DEBUG)

class PingPongFilter(logging.Filter):
    def filter(self, record):
        if "keepalive ping" in record.getMessage() or "keepalive pong" in record.getMessage():
            return False
        return True

# Apply the filter to suppress keepalive pings and pongs logs
logging.getLogger('websockets.client').addFilter(PingPongFilter())

async def forward_to_rest(method, url, headers, data):
    logging.info(f"WebSocket client: Forwarding message to REST server: {method} {url}")
    logging.debug(f"Headers: {headers}")
    logging.debug(f"Data: {data}")
    try:
        response = requests.request(method, url, headers=headers, data=data)
        logging.info(f"WebSocket client: Received response from REST server: {response.status_code}")
        logging.debug(f"Response: {response.text}")
        return response.text
    except Exception as e:
        logging.error(f"WebSocket client: Error forwarding message to REST server: {e}")
        logging.error(traceback.format_exc())
        return "Error forwarding message to REST server"

async def connectivity_check(websocket, connection_id):
    ping_message = {
        "sender_actor": "root",
        "message_type": "wsl-bash",
        "content": "pwd",
        "connection_id": connection_id
    }
    headers = {"Content-Type": "application/json"}
    url = "http://localhost:5003/send-message"
    logging.info("WebSocket client: Performing initial connectivity check")
    response = await forward_to_rest("POST", url, headers, json.dumps(ping_message))
    logging.info(f"WebSocket client: Initial connectivity check response: {response}")

async def listen(ws_url, connection_id=None):
    while True:
        try:
            async with websockets.connect(ws_url) as websocket:
                logging.info(f"WebSocket client: Connected to proxy server at {ws_url}")

                if connection_id:
                    # Try to resume with the previous connection ID
                    await websocket.send(json.dumps({"message_type": "resume", "connection_id": connection_id}))
                else:
                    # Receive the connection ID from the proxy server
                    initial_message = await websocket.recv()
                    initial_data = json.loads(initial_message)
                    connection_id = initial_data['connection_id']
                    logging.info(f"WebSocket client: Received new connection_id: {connection_id}")

                # Perform initial connectivity check
                await connectivity_check(websocket, connection_id)

                while True:
                    message = await websocket.recv()
                    logging.info(f"WebSocket client: Received message from proxy: {message}")

                    # Assuming message is a JSON string with the necessary information
                    envelope = json.loads(message)
                    request_info = envelope.get("envelope")
                    data = envelope.get("data")
                    method = request_info.get("method", "POST")
                    path = request_info.get("path", "/send-message")
                    headers = request_info.get("headers", {})
                    request_id = request_info.get("request_id")
                    logging.debug(f"WebSocket client: Handling request with request_id: {request_id}")

                    url = f"http://localhost:5003{path}"
                    response = await forward_to_rest(method, url, headers, data)
                    logging.info(f"WebSocket client: Forwarded message to REST server and got response")
                    logging.debug(f"Response: {response}")

                    # Attach request_id to the response before sending it back
                    response_data = json.loads(response)
                    if isinstance(response_data, list):
                        for item in response_data:
                            item['request_id'] = request_id
                    else:
                        response_data['request_id'] = request_id
                    await websocket.send(json.dumps(response_data))
                    logging.info(f"WebSocket client: Sent response back to proxy: {response_data}")
        except websockets.exceptions.ConnectionClosed as e:
            logging.info(f"WebSocket client: Connection closed with error: {e}")
            logging.info("WebSocket client: Attempting to reconnect...")
            await asyncio.sleep(5)  # Wait before trying to reconnect
        except Exception as e:
            logging.error(f"WebSocket client: Unexpected error: {e}")
            logging.error(traceback.format_exc())
            await asyncio.sleep(5)  # Wait before trying to reconnect

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python websocket_client.py <ws_url>")
        sys.exit(1)
    ws_url = sys.argv[1]
    connection_id = sys.argv[2] if len(sys.argv) > 2 else None
    asyncio.get_event_loop().run_until_complete(listen(ws_url, connection_id))
