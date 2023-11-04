import os
import boto3
import openai
import json




class ChatGptAPI:
    def __init__(self):
        pass

    @staticmethod
    def wrap_message_for_lambda(sample_messages):
        # Mock the Lambda event and context
        event = {
            "Records": [
                {
                    "body": json.dumps(sample_messages)
                }
            ]
        }
        context = {}
        return context, event

    @staticmethod
    def wrap_message_for_gpt(sample_message):
        messages = [
            {
                "role": "user",
                "content": sample_message
            }
        ]

        return messages

    def generate_response(self, messages):
        openai.api_key = "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"

        parameters = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.8,
            "top_p": 0.9,
            "n": 3,
            #   "stream": false,
            "stop": "Thank you.",
            "max_tokens": 1000,
            "presence_penalty": -0.5,
            "frequency_penalty": 0.5,
            # "logit_bias": {"Paris": 100},
            "user": "1234abcd"
        }

        try:
            print(messages)
            response = openai.ChatCompletion.create(**parameters)
            if response.choices:
                generated_text = response.choices[0].message
                print(generated_text)
            else:
                print("No text generated")
                generated_text = ""
            return generated_text

        except openai.error.InvalidRequestError as e:
            print(f"Invalid Request Error: {e}")
        except openai.error.AuthenticationError as e:
            print(f"Authentication Error: {e}")
        except openai.error.APIConnectionError as e:
            print(f"API Connection Error: {e}")
        except openai.error.OpenAIError as e:
            print(f"OpenAI Error: {e}")
