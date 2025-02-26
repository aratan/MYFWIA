# myfwia/agents/translator.py

from .agent import Agent  # Import relativo
import logging

class Translator(Agent):
    """
    Representa un agente que traduce texto entre idiomas.
    """
    def __init__(self, verbose=True):
        super().__init__(
            role="Traductor de IA",
            goal="Traducir texto entre idiomas.",
            backstory="Soy un agente especializado en traducción automática.",
            verbose=verbose,
        )

    def execute_task(self, task_description):
        """
        Ejecuta una tarea de traducción.
        :param task_description: Descripción de la tarea (por ejemplo, "Traduce 'hello' al español").
        :return: Texto traducido.
        """
        if self.verbose:
            logging.info(f"{self.role} está ejecutando la tarea: {task_description}")
        
        # Simulación de traducción básica
        text_to_translate = task_description.split("Traduce ")[1].split(" al ")[0]
        target_language = task_description.split(" al ")[1]

        translations = {
            "hello": {"es": "hola", "fr": "bonjour"},
            "world": {"es": "mundo", "fr": "monde"},
        }

        word = text_to_translate.strip().lower()
        if word in translations and target_language in translations[word]:
            return translations[word][target_language]
        else:
            return f"No se pudo traducir '{text_to_translate}' al {target_language}."