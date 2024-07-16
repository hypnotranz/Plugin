import openai

class ChatGptAPI:
    def __init__(self):
        pass

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
        openai.api_key = ""

        try:

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.8,
                top_p=0.9,
                n=3,
                stop="Thank you.",
                max_tokens=1000,
                presence_penalty=-0.5,
                frequency_penalty=0.5,
                user="1234abcd"
            )
            if response.choices:
                generated_text = response.choices[0].message["content"]
                print(generated_text)
                return generated_text
        except openai.OpenAIError as e:
            print(f"OpenAI API error: {e}")
            return ""
