# myfwia/agents/supervisor.py

from .agent import Agent

class Supervisor(Agent):
    """
    Representa un agente supervisor que evalúa las respuestas de otros agentes.
    """
    def __init__(self, verbose=True):
        super().__init__(
            role="Supervisor de IA",
            goal="Evaluar y supervisar el trabajo de otros agentes.",
            backstory="Soy el supervisor encargado de asegurar que las respuestas sean precisas y completas.",
            verbose=verbose,
        )

    def evaluate_response(self, response):
        if "error" in response.lower():
            return "Evaluación: La respuesta contiene un error."
        return "Evaluación: La respuesta parece correcta."