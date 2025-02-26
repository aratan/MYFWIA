# main.py

import ollama
import json
from concurrent.futures import ThreadPoolExecutor
from agents.agent import Agent
from agents.supervisor import Supervisor
from agents.translator import Translator
from tasks.task import Task
from utils.task import task_registry
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cargar configuración desde config.json
with open("config.json", "r") as config_file:
    config = json.load(config_file)

# Inicialización del cliente Ollama
client = ollama.Client(host=config["ollama_host"])

# Creación de los agentes
agente1 = Agent(
    role="Asistente de IA #1",
    goal="Ayudar a responder preguntas generales.",
    backstory="Soy el primer asistente de IA entrenado para localizar información geográfica.",
    verbose=True,
)

agente2 = Agent(
    role="Asistente de IA #2",
    goal="Buscar información en internet.",
    backstory="Soy el segundo asistente de IA entrenado para buscar datos en línea.",
    verbose=True,
)

agente3 = Agent(
    role="Asistente de IA #3",
    goal="Proporcionar información temporal.",
    backstory="Soy el tercer asistente de IA entrenado para proporcionar la hora actual.",
    verbose=True,
)

agente4 = Translator(verbose=True)
supervisor = Supervisor(verbose=True)

# Definición de las tareas
tareas = [
    Task(description="¿Cuál es la capital de Francia?", agent=agente1),
    Task(description="Obtener temperatura en París", agent=agente2),
    Task(description="Obtener hora en París", agent=agente3),
    Task(description="Traduce 'hello' al español", agent=agente4),
    Task(description="Obtener pronóstico del tiempo en París", agent=agente2),
]

# Función para ejecutar una tarea
def execute_task(tarea):
    logging.info(f"Asignando tarea a: {tarea.agent.role}")
    task_type = tarea.description.split()[0].lower()

    # Verificar si la tarea está registrada en task_registry
    if task_type in task_registry:
        resultado = task_registry[task_type](tarea.description)
    else:
        # Si no está registrada, usar el modelo de lenguaje de Ollama
        response = client.generate(model=config["default_model"], prompt=tarea.description)
        resultado = response['response']

    # Asegurarse de que el resultado sea una cadena de texto
    if not isinstance(resultado, str):
        logging.error(f"Error: La tarea asignada a {tarea.agent.role} no devolvió una cadena de texto. Resultado: {resultado}")
        resultado = "Error: Resultado no válido."

    return (tarea.agent.role, resultado)

# Ejecución del sistema
if __name__ == "__main__":
    logging.info("Iniciando la ejecución de las tareas...")

    resultados = {}

    # 1. Ejecutar tareas en serie (agente1 y agente4)
    for tarea in tareas:
        if tarea.agent in [agente1, agente4]:
            role, resultado = execute_task(tarea)
            resultados[role] = resultado

    # 2. Ejecutar tareas en paralelo (agente2 y agente3)
    with ThreadPoolExecutor() as executor:
        tareas_paralelas = [tarea for tarea in tareas if tarea.agent in [agente2, agente3]]
        futures = [executor.submit(execute_task, tarea) for tarea in tareas_paralelas]
        for future in futures:
            role, resultado = future.result()
            resultados[role] = resultado

    # Mostrar los resultados obtenidos
    logging.info("--- Resultados de las tareas ---")
    for role, resultado in resultados.items():
        logging.info(f"{role} respondió:\n{resultado}")

    # Supervisión de las respuestas por parte del supervisor
    logging.info("--- Evaluación del Supervisor ---")
    evaluaciones = {}
    for role, resultado in resultados.items():
        # Asegurarse de que el resultado sea una cadena de texto
        if not isinstance(resultado, str):
            logging.error(f"Error: El resultado de {role} no es una cadena de texto. Resultado: {resultado}")
            evaluacion = "Evaluación: El resultado no es válido."
        else:
            evaluacion = supervisor.evaluate_response(resultado)
        evaluaciones[role] = evaluacion
        logging.info(f"El supervisor evaluó la respuesta de {role}: {evaluacion}")