
class AgentBase:
    def __init__(self):
        pass





    @staticmethod
    def get_thread_context(sample_message):
        messages = [
            {
                "role": "user",
                "content": sample_message
            }
        ]

        return messages

    @staticmethod
    def wrap_message_for_gpt(sample_message):
        messages = [
            {
                "role": "user",
                "content": sample_message
            }
        ]

        return messages

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