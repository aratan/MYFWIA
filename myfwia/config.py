# myfwia/config.py

import json

def load_config(config_path="config.json"):
    """
    Carga la configuración desde un archivo JSON.
    :param config_path: Ruta al archivo de configuración.
    :return: Diccionario con la configuración.
    """
    with open(config_path, "r") as config_file:
        return json.load(config_file)