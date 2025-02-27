# app.py
from myfwia import (
    Agent,
    Task,
    task_registry,
    OllamaClient,
    load_config,
    Translator,
    Supervisor  # Asegúrate de tener Supervisor importado
)
import logging
import colorlog
from concurrent.futures import ThreadPoolExecutor

# Configuración de logging con colores (igual que antes)
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

# Configuración del logger (igual que antes)
logging.basicConfig(level=log_level)
logger = logging.getLogger()
if logger.hasHandlers():
    logger.handlers.clear()
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

# --- Definición de Agentes (igual que antes + Supervisor) ---
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

class Supervisor(Agent): # Asegúrate de que tu clase Supervisor esté definida así o similar en myfwia/agents/supervisor.py
    """Agente supervisor para verificar y corregir respuestas."""
    def __init__(self):
        super().__init__(
            role="Supervisor IA",
            goal="Verificar y corregir información.",
            backstory="Experto en detectar errores y mejorar la precisión.",
            verbose=True,
        )

# Instanciar agentes (igual que antes + Supervisor)
agente_geografico = Agent1()
agente_internet = Agent2()
agente_tiempo = TimeAgent()
agente_traductor = Translator()
agente_supervisor = Supervisor()

# --- Lógica de Ejecución (MODIFICADA para supervisión con PROMPT DE PRECISIÓN) ---
def execute_task(tarea: Task, ollama_client: OllamaClient) -> tuple[str, str]:
    """Ejecuta una tarea, la supervisa y maneja el registro de resultados."""
    logger.info(f"Asignando tarea a: {tarea.agent.role}")
    parts = tarea.description.split(maxsplit=1)
    task_type = parts[0].lower()
    task_args = parts[1] if len(parts) > 1 else None

    initial_result = None

    try:
        if task_type in task_registry:
            if task_args:
                initial_result = task_registry[task_type](task_args)
            else:
                initial_result = task_registry[task_type]()
        else:
            response = ollama_client.generate_response(
                model=config["default_model"],
                prompt=tarea.description
            )
            initial_result = response
    except Exception as e:
        logger.error(f"Error ejecutando tarea: {str(e)}")
        return (tarea.agent.role, "Error al procesar la solicitud")

    # --- Supervisión del resultado - PROMPT DE PRECISIÓN FACTUAL ---
    logger.info(f"Supervisando resultado de {tarea.agent.role} (precisión)...")
    supervision_prompt = (
        f"Tarea original: '{tarea.description}'. "
        f"Resultado del agente {tarea.agent.role}: '{initial_result}'. "
        f"**Verifica cuidadosamente si la respuesta es FACTUALMENTE correcta y precisa.** "
        f"Corrige cualquier información incorrecta o engañosa. "
        f"Si la respuesta es correcta, simplemente confírmala. Devuelve solo el resultado corregido o confirmado."
    )

    try:
        supervision_response = ollama_client.generate_response(
            model=config["default_model"],
            prompt=supervision_prompt
        )
        resultado_supervisado = supervision_response
        logger.info(f"Resultado supervisado (precisión): {resultado_supervisado}")
    except Exception as e:
        logger.error(f"Error durante la supervisión (precisión): {str(e)}")
        resultado_supervisado = f"Error al supervisar el resultado por precisión. Resultado original: {initial_result}"

    return (tarea.agent.role, resultado_supervisado)


def main():
    """Función principal para ejecutar el sistema de agentes."""

    logger.info("🚀 Iniciando ejecución de tareas...")

    # --- Solicitar PAÍS al usuario ---
    dato_usuario = input("Introduce el país para las tareas (ej. Francia, España, Japón): ")

    # --- Definición de Tareas (AHORA se usa dato_usuario) ---
    tareas = [
        Task(
            description=f"¿Cuál es la capital de {dato_usuario}?", # Usar dato_usuario
            agent=agente_geografico
        ),
        Task(
            description=f"get_temperature {dato_usuario}", # Usar dato_usuario
            agent=agente_internet
        ),
        Task(description="get_current_time", agent=agente_tiempo),
        Task(
            description=f"get_weather_forecast {dato_usuario}", # Usar dato_usuario
            agent=agente_internet
        ),
        Task(
            description=f"Traduce el saludo tipico de {dato_usuario} al español", # Usar dato_usuario
            agent=agente_traductor
        ),
        Task(
            description=f"¿Cuál es la marca de perfume más cara en {dato_usuario}?", # Usar dato_usuario
            agent=agente_internet
        ),
    ]

    resultados = {}
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(execute_task, tarea, ollama_client)
            for tarea in tareas
        ]

        for future in futures:
            role, resultado = future.result()
            resultados[role] = resultado

    # Mostrar resultados con formato mejorado (igual que antes)
    logger.info("\n--- 🎯 Resultados Obtenidos ---")
    for role, resultado in resultados.items():
        logger.info(f"🔍 {role} respondió:")
        logger.info(f"    {resultado}\n")


if __name__ == "__main__":
    main()