# myfwia/utils/time.py

from datetime import datetime
from .task import register_task

def get_current_time():
    return datetime.now().strftime("%H:%M")

register_task("get_current_time", get_current_time)