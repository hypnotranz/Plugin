import unittest
import requests
import json
import subprocess
import time

class TestMain(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = subprocess.Popen(["python", "main.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)  # Wait for the server to start

    @classmethod
    def tearDownClass(cls):
        cls.server.terminate()
        cls.server.wait()

    def test_send_message(self):
        url = 'http://localhost:5003/send-message'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "sender_actor": "chatgpt://developer/jiri-1",
            "sender_agent": "http://localhost:5003/developer_1",
            "log_correlation_path": "550e8400-e29b-41d4-a716-446655440000/6ba7b810-9dad-11d1-80b4-00c04fd430c8",
            "recipient_agent": "http://localhost:5003/developer_1",
            "recipient_actor": "developer",
            "message_type": "wsl-bash",
            "subject": "Clone Git repository",
            "content": "git clone http://github.com/repo.git"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)

    def test_get_messages(self):
        url = 'http://localhost:5003/get-messages'
        headers = {'Content-Type': 'application/json'}
        payload = {}  # adjust as needed
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)

    def test_logo(self):
        url = 'http://localhost:5003/logo.png'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_plugin_manifest(self):
        url = 'http://localhost:5003/.well-known/ai-chatgpt_plugin.json'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_openapi_spec(self):
        url = 'http://localhost:5003/openapi.yaml'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_execute_command(self):
        url = 'http://localhost:5003/execute-command'
        headers = {'Content-Type': 'application/json'}
        payload = {}  # adjust as needed
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
