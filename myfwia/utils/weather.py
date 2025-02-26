# myfwia/utils/weather.py

from duckduckgo_search import DDGS
from functools import lru_cache
from .task import register_task

@lru_cache(maxsize=128)
def get_weather_forecast(city):
    query = f"pronóstico del tiempo en {city}"
    with DDGS() as ddgs:
        results = list(ddgs.text(query))
    if results:
        for result in results:
            snippet = result.get('body', '').lower()
            if "forecast" in snippet or "pronóstico" in snippet:
                return snippet
    return "No se pudo encontrar el pronóstico del tiempo."

register_task("get_weather_forecast", get_weather_forecast)