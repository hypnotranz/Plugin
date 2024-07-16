import asynctest
from chatgpt_plugin.endpoints.message import Message
from chatgpt_plugin.message_handler import MessageHandler
from chatgpt_plugin.message_store import MessageStore

class TestMessageFlow(asynctest.TestCase):
    def setUp(self):
        self.message_store = MessageStore()  # Create a real message_store
        self.message_handler = MessageHandler(self.message_store)  # Pass it to the MessageHandler
        self.test_message = Message({
            'sender_actor': 'chatgpt://developer_1',
            'sender_agent': 'http://localhost:5003/send-message',
            'log_correlation_path': '1234',
            'recipient_agent': 'http://localhost:5003/send-message',
            'recipient_actor': 'unix_manager',
            'message_type': 'wsl-bash',
            'subject': 'Test command',
            'content': 'echo "Hello, world!"'
        })

    def test_message_flow(self):
        # Process the message
        self.message_handler.process_message(self.test_message)

        # Get the message_id of the response message from the message_store
        response_message_id = next(iter(self.message_store._store))

        # Get the response message using the message_id
        response_message = self.message_store.get_message(response_message_id)

        # Check that the response message is in the message_store
        self.assertEqual(response_message.data, self.message_store._store[response_message_id].data)

        # Check that the response message content is the expected output of the command
        self.assertEqual(response_message.data['content']['stdout'], "Hello, world!\n")


if __name__ == '__main__':
    asynctest.main()
