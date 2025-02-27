# myfwia/utils/time.py
from datetime import datetime
import pytz  # Importa pytz
from .task import register_task

def get_current_time():
    utc_timezone = pytz.utc  # Define la zona horaria UTC con pytz
    current_time = datetime.now(utc_timezone).time() # Usa utc_timezone
    return current_time.strftime('%H:%M:%S')

register_task("get_current_time", get_current_time)