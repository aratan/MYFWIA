# myfwia/utils/temperature.py

from duckduckgo_search import DDGS
from functools import lru_cache
from .task import register_task  # Import relativo

@lru_cache(maxsize=128)
def get_temperature(city):
    query = f"temperatura actual en {city}"
    with DDGS() as ddgs:
        results = list(ddgs.text(query))
    if results:
        for result in results:
            snippet = result.get('body', '').lower()
            if "temperature" in snippet or "°c" in snippet or "°f" in snippet:
                return snippet
    return "No se pudo encontrar la temperatura."

register_task("get_temperature", get_temperature)