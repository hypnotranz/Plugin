import unittest
from chatgpt_plugin.message_store import MessageStore
from chatgpt_plugin.endpoints.message import Message

class TestMessageStore(unittest.TestCase):
    def setUp(self):
        self.message_store = MessageStore()

    def test_add_and_get_message(self):
        message = Message({
            "sender_actor": "chatgpt://root/project_id",
            "sender_agent": "http://ip:port/endpoint",
            "log_correlation_path": "kabana:guid1",
            "recipient_agent": "http://chatgpt-plugin-url",
            "recipient_actor": "chatgpt://plugin_id",
            "message_type": "wsl-bash",
            "subject": "echo 'Hello, world!'",
            "content": "echo 'Hello, world!'"
        })
        self.message_store.add_message(message)
        retrieved_message = self.message_store.get_message(message.message_id)
        self.assertEqual(message, retrieved_message)

    def test_get_responses(self):
        parent_message = Message({
            "sender_actor": "chatgpt://root/project_id",
            "sender_agent": "http://ip:port/endpoint",
            "log_correlation_path": "kabana:guid1",
            "recipient_agent": "http://chatgpt-plugin-url",
            "recipient_actor": "chatgpt://plugin_id",
            "message_type": "wsl-bash",
            "subject": "echo 'Hello, world!'",
            "content": "echo 'Hello, world!'"
        })
        self.message_store.add_message(parent_message)

        child_message = Message({
            "sender_actor": "chatgpt://plugin_id",
            "sender_agent": "http://chatgpt-plugin-url",
            "log_correlation_path": "kabana:guid2",
            "recipient_agent": "http://ip:port/endpoint",
            "recipient_actor": "chatgpt://root/project_id",
            "message_type": "wsl-bash",
            "subject": "echo 'Hello, world!'",
            "content": "Hello, world!",
            "parent_id": parent_message.message_id  # Corrected field name
        })
        self.message_store.add_message(child_message)

        responses = self.message_store.get_responses
        self.assertEqual(len(responses), 1)
        self.assertEqual(responses[0], child_message)

if __name__ == '__main__':
    unittest.main()
