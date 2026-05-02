from abc import ABC, abstractmethod

class LlmIntegration(ABC):
    @abstractmethod
    def client_communication(self,message:list [dict], model: str) -> str:
        ...