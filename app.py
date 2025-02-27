# app.py
from myfwia import (
    Agent,
    Task,
    task_registry,
    OllamaClient,
    load_config,
    Translator
)
import logging
import colorlog
from concurrent.futures import ThreadPoolExecutor

# Configuración de logging con colores
log_level = logging.INFO
log_format = (
    "%(log_color)s%(asctime)s - %(levelname)s - "
    "%(message_log_color)s%(message)s"
)
log_colors = {
    "DEBUG": "cyan",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red,bg_white",
}
secondary_log_colors = {
    "message": {
        "INFO": "blue",
        "WARNING": "purple",
    },
}

# Configuración del logger
logging.basicConfig(level=log_level)
logger = logging.getLogger()

# Limpiar handlers existentes para evitar duplicados
if logger.hasHandlers():
    logger.handlers.clear()

# Handler de consola con colores
handler = logging.StreamHandler()
formatter = colorlog.ColoredFormatter(
    log_format,
    log_colors=log_colors,
    secondary_log_colors=secondary_log_colors,
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Cargar configuración del proyecto
config = load_config()
ollama_client = OllamaClient(host=config["ollama_host"])

# --- Definición de Agentes ---
class Agent1(Agent):
    """Agente especializado en respuestas geográficas."""
    def __init__(self):
        super().__init__(
            role="Geógrafo IA",
            goal="Responder preguntas sobre geografía.",
            backstory="Entrenado para identificar capitales y ubicaciones.",
            verbose=True,
        )

class Agent2(Agent):
    """Agente especializado en búsquedas en internet."""
    def __init__(self):
        super().__init__(
            role="Buscador IA",
            goal="Obtener datos de internet.",
            backstory="Experto en buscar información en tiempo real.",
            verbose=True,
        )

class TimeAgent(Agent):
    """Agente dedicado a información temporal."""
    def __init__(self):
        super().__init__(
            role="Reloj IA",
            goal="Proporcionar tiempo y fechas.",
            backstory="Mantiene la hora actualizada.",
            verbose=True,
        )

# Instanciar agentes
agente_geografico = Agent1()
agente_internet = Agent2()
agente_tiempo = TimeAgent()
agente_traductor = Translator()

# --- Definición de Tareas ---
tareas = [
    Task(
        description="¿Cuál es la capital de Francia?",
        agent=agente_geografico
    ),
    Task(
        description="get_temperature París",
        agent=agente_internet
    ),
    Task(description="get_current_time", agent=agente_tiempo),
    Task(
        description="get_weather_forecast París",
        agent=agente_internet
    ),
    Task(
        description="Traduce 'hello' al español",
        agent=agente_traductor
    ),
    Task(
        description="¿Cuál es la marca de perfume más cara?",
        agent=agente_internet
    ),
]

# --- Lógica de Ejecución ---
def execute_task(tarea: Task, ollama_client: OllamaClient) -> tuple[str, str]:
    """Ejecuta una tarea y maneja el registro de resultados."""
    logger.info(f"Asignando tarea a: {tarea.agent.role}")
    task_type = tarea.description.split(maxsplit=1)[0].lower()
    
    try:
        if task_type in task_registry:
            resultado = task_registry[task_type](tarea.description)
        else:
            response = ollama_client.generate_response(
                model=config["default_model"],
                prompt=tarea.description
            )
            resultado = response
    except Exception as e:
        logger.error(f"Error ejecutando tarea: {str(e)}")
        resultado = "Error al procesar la solicitud"
    
    return (tarea.agent.role, resultado)

def main():
    """Función principal para ejecutar el sistema de agentes."""
    logger.info("🚀 Iniciando ejecución de tareas...")
    
    resultados = {}
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(execute_task, tarea, ollama_client)
            for tarea in tareas
        ]
        
        for future in futures:
            role, resultado = future.result()
            resultados[role] = resultado
    
    # Mostrar resultados con formato mejorado
    logger.info("\n--- 🎯 Resultados Obtenidos ---")
    for role, resultado in resultados.items():
        logger.info(f"🔍 {role} respondió:")
        logger.info(f"    {resultado}\n")

if __name__ == "__main__":
    main()