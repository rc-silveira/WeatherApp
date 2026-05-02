import os

import ollama
from groq import Groq

from adapters.groq_adapter import GroqAdapter
from adapters.ollama_adapter import OllamaAdapter
from llm_integration import LlmIntegration

def create_llm_client() -> LlmIntegration:
    provider = os.environ.get("AI_PROVIDER")
    if provider == "groq":
        return GroqAdapter(Groq(api_key=os.environ.get("GROQ_API_KEY")))
    elif provider == "ollama":
        return OllamaAdapter(ollama)
    else:
        raise ValueError(f"Unknown provider: {provider}")