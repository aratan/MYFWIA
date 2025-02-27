# myfwia/agents/supervisor.py
from .agent import Agent

class Supervisor(Agent):
    """Agente supervisor para verificar y corregir respuestas."""
    def __init__(self):
        super().__init__(
            role="Supervisor IA",
            goal="Verificar y corregir información.",
            backstory="Experto en detectar errores y mejorar la precisión.",
            verbose=True,
        )