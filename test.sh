#!/bin/bash


# Run tests
python -m unittest tests.test_message
python -m unittest tests.test_message_store
python -m unittest tests.test_message_handler
python -m unittest tests.test_dispatcher
python -m unittest tests.test_message_flows
python -m unittest tests.test_send_message

#pytest tests/test_endpoints.py


# Start the server
#DEBUG=True python -m chatgpt_plugin.main &

# Get server PID
SERVER_PID=$!

# Wait for server to start
sleep 5


echo 'Running tests...'
# Run tests

 # python -m unittest tests.test_main.py




# Stop server
kill $SERVER_PID

# Done
echo 'Done.'
