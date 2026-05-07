from llm_integration import LlmIntegration

class GroqAdapter(LlmIntegration):
    def __init__(self, client):
        self.client = client

    def client_communication(self, message:list[dict], model: str) -> str:
        chat_completion = self.client.chat.completions.create(
            messages=message,
            model=model
        )
        return chat_completion.choices[0].message.content