# test_main.py

import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

    # ... existing test cases ...

    def test_send_message_json(self):
        url = 'http://localhost:5003/send-message'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "sender_actor": "chatgpt://root/project_id",
            "sender_agent": "http://ip:port/endpoint",
            "log_correlation_path": "kabana:guid1",
            "recipient_agent": "http://chatgpt-plugin-url",
            "recipient_actor": "chatgpt_plugin",
            "message_type": "wsl-bash",
            "subject": "Execute find command to get a listing of the plugin directory code",
            "content": "find chatgpt_plugin -name \"*.py\" -exec cat {} \\;"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn('status', response_data)
        self.assertEqual(response_data['status'], 'success')

    def test_send_message_invalid_json(self):
        url = 'http://localhost:5003/send-message'
        headers = {'Content-Type': 'application/json'}
        payload = "{invalid_json}"
        response = requests.post(url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 400)

    def test_send_message_unsupported_content_type(self):
        url = 'http://localhost:5003/send-message'
        headers = {'Content-Type': 'text/plain'}
        payload = "unsupported content type"
        response = requests.post(url, headers=headers, data=payload)
        self.assertEqual(response.status_code, 400)


    def test_execute_find_command(self):
        url = 'http://localhost:5003/send-message'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "sender_actor": "chatgpt://root/project_id",
            "sender_agent": "http://ip:port/endpoint",
            "log_correlation_path": "kabana:guid1",
            "recipient_agent": "http://chatgpt-plugin-url",
            "recipient_actor": "chatgpt_plugin",
            "message_type": "find-cat",
            "subject": "Execute find command to get a listing of the plugin directory code",
            "content": "find chatgpt_plugin -name \"*.py\" -exec cat {} \\;"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)

    def test_execute_invalid_command(self):
        url = 'http://localhost:5003/send-message'
        headers = {'Content-Type': 'application/json'}
        payload = {
            "sender_actor": "chatgpt://root/project_id",
            "sender_agent": "http://ip:port/endpoint",
            "log_correlation_path": "kabana:guid1",
            "recipient_agent": "http://chatgpt-plugin-url",
            "recipient_actor": "chatgpt_plugin",
            "message_type": "wsl-bash",
            "subject": "Execute invalid command",
            "content": "invalid_command"
        }
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        try:
            self.assertIn("error", response_data)
        except AssertionError:
            print(f"Test failed. Response data: {response_data}")
            raise

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
        url = 'http://localhost:5003/.well-known/ai-plugin.json'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

    def test_openapi_spec(self):
        url = 'http://localhost:5003/openapi.yaml'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
