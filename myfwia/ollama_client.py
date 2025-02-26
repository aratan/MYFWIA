# myfwia/ollama_client.py

import ollama

class OllamaClient:
    """
    Cliente reutilizable para interactuar con Ollama.
    """
    def __init__(self, host):
        self.client = ollama.Client(host=host)

    def generate_response(self, model, prompt):
        response = self.client.generate(model=model, prompt=prompt)
        return response['response']