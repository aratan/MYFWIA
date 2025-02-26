# myfwia/__init__.py

# Importar los módulos principales del framework
from .agents import Agent, Supervisor, Translator
from .tasks import Task
from .utils.task import task_registry
from .ollama_client import OllamaClient
from .config import load_config