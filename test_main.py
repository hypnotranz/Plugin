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
            "sender_actor": "chatgpt://developer_1/",
            "sender_agent": "http://localhost:5003/git-manager",
            "log_correlation_path": "kabana:guid11",
            "recipient_agent": "http://git-manager-url",
            "recipient_actor": "git_manager",
            "message_type": "wsl-bash",
            "subject": "Clone Git repository",
            "content": "git clone http://github.com/repo.git"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
