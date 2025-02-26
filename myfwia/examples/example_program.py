# examples/example_program.py

from myfwia import Agent, Supervisor, Translator, Task, task_registry, OllamaClient, load_config
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Cargar configuración
config = load_config()

# Inicializar el cliente Ollama
ollama_client = OllamaClient(host=config["ollama_host"])

# Crear agentes
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

# Definir tareas
tareas = [
    Task(description="¿Cuál es la capital de Francia?", agent=agente1),
    Task(description="get_temperature París", agent=agente2),
    Task(description="get_current_time", agent=agente3),
    Task(description="Traduce 'hello' al español", agent=agente4),
    Task(description="get_weather_forecast París", agent=agente2),
]

# Función para ejecutar una tarea
def execute_task(tarea, ollama_client):
    logging.info(f"Asignando tarea a: {tarea.agent.role}")
    task_type = tarea.description.split()[0].lower()

    if task_type in task_registry:
        resultado = task_registry[task_type](tarea.description)
    else:
        response = ollama_client.generate_response(model=config["default_model"], prompt=tarea.description)
        resultado = response
    return (tarea.agent.role, resultado)

# Ejecutar el programa
if __name__ == "__main__":
    logging.info("Iniciando la ejecución de las tareas...")

    resultados = {}
    for tarea in tareas:
        role, resultado = execute_task(tarea, ollama_client)
        resultados[role] = resultado

    # Mostrar resultados
    logging.info("--- Resultados de las tareas ---")
    for role, resultado in resultados.items():
        logging.info(f"{role} respondió:\n{resultado}")

    # Supervisión
    logging.info("--- Evaluación del Supervisor ---")
    for role, resultado in resultados.items():
        evaluacion = supervisor.evaluate_response(resultado)
        logging.info(f"El supervisor evaluó la respuesta de {role}: {evaluacion}")