from llm_integration import LlmIntegration

class OllamaAdapter(LlmIntegration):
    def __init__(self, client):
        self.client = client

    def client_communication(self, message: list[dict], model: str) -> str:
        response = self.client.chat(
            model=model,
            messages=message
        )
        return response['message']['content']