import asyncio
import websockets
import logging
import traceback
from aiohttp import web
import signal
import socket
import json

logging.basicConfig(level=logging.DEBUG)

# Store connected WebSocket clients
websocket_clients = set()

# Queue to handle incoming REST requests
request_queue = asyncio.Queue()
# Dictionary to map request IDs to response futures
response_futures = {}

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

# Function to handle WebSocket connections
async def handle_websocket(websocket):
    logging.info(f"Proxy server: New WebSocket connection established")
    websocket_clients.add(websocket)
    try:
        while True:
            message = await request_queue.get()
            logging.debug(f"Proxy server: Forwarded REST message to WebSocket client: {message}")
            await websocket.send(message)
            response = await websocket.recv()
            logging.debug(f"Proxy server: Received response from WebSocket client: {response}")
            request_queue.task_done()

            # Extract the request ID from the response
            response_data = json.loads(response)
            if isinstance(response_data, list):
                for item in response_data:
                    request_id = item.get('request_id')
                    logging.debug(f"Proxy server: Extracted request_id {request_id} from response list item")
                    if request_id and request_id in response_futures:
                        # Remove the request_id from the response
                        del item['request_id']
                        response_futures[request_id].set_result(json.dumps(response_data))
                        del response_futures[request_id]
            else:
                request_id = response_data.get('request_id')
                logging.debug(f"Proxy server: Extracted request_id {request_id} from response data")
                if request_id and request_id in response_futures:
                    # Remove the request_id from the response
                    del response_data['request_id']
                    response_futures[request_id].set_result(json.dumps([response_data]))
                    del response_futures[request_id]
    except websockets.exceptions.ConnectionClosed as e:
        logging.info(f"Proxy server: WebSocket connection closed with error: {e}")
    finally:
        websocket_clients.remove(websocket)

# Function to handle REST calls
async def handle_rest(request):
    try:
        data = await request.text()
        logging.debug(f"Proxy server: Received REST call with data: {data}")

        if websocket_clients:
            request_id = str(id(request))
            logging.debug(f"Proxy server: Generated request_id: {request_id}")
            request_info = {
                "method": request.method,
                "path": request.path,
                "headers": dict(request.headers),
                "data": data,
                "request_id": request_id
            }
            response_future = asyncio.Future()
            response_futures[request_id] = response_future
            await request_queue.put(json.dumps(request_info))
            logging.debug(f"Proxy server: Added REST message to queue: {request_info}")

            # Wait for the WebSocket client to handle the request and get the response
            response = await response_future
            logging.debug(f"Proxy server: Sending response back to initial caller: {response}")
            return web.Response(text=response)
        else:
            logging.error("Proxy server: No WebSocket clients connected to handle the request")
            return web.Response(status=500, text="No WebSocket clients connected")
    except Exception as e:
        logging.error(f"Proxy server: Error handling REST call: {e}")
        logging.error(traceback.format_exc())
        return web.Response(status=500, text="Internal Server Error")

# Create aiohttp web application
app = web.Application()
app.router.add_post('/send-message', handle_rest)

# Function to start REST server
async def start_rest_server(port):
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', port)
    await site.start()
    logging.info(f"Proxy server: REST server running on http://localhost:{port}")

# Function to shutdown the server
async def shutdown(loop):
    logging.info("Proxy server: Shutting down")
    for ws in websocket_clients:
        await ws.close()
    loop.stop()

def signal_handler(signal, frame, loop):
    logging.info("Proxy server: Received termination signal")
    asyncio.ensure_future(shutdown(loop))

# Main function to start the server
def main(override_port_ws=None, override_port_rest=None):
    port_ws = override_port_ws if override_port_ws else find_free_port()
    port_rest = override_port_rest if override_port_rest else find_free_port()

    start_server = websockets.serve(handle_websocket, "localhost", port_ws)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    loop.run_until_complete(start_rest_server(port_rest))
    logging.info(f"Proxy server: WebSocket server running on ws://localhost:{port_ws}")
    logging.info(f"Proxy server: REST server running on http://localhost:{port_rest}")
    logging.info(f"To start the WebSocket client, use the following command:")
    logging.info(f"python websocket_client.py {port_ws}")

    signal.signal(signal.SIGINT, lambda s, f: signal_handler(s, f, loop))
    signal.signal(signal.SIGTERM, lambda s, f: signal_handler(s, f, loop))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.run_until_complete(shutdown(loop))
        loop.close()

# Run the main function
if __name__ == "__main__":
    import sys

    port_ws = int(sys.argv[1]) if len(sys.argv) > 1 else None
    port_rest = int(sys.argv[2]) if len(sys.argv) > 2 else None
    main(port_ws, port_rest)
