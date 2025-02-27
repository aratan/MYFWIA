# myfwia/utils/time.py

from datetime import datetime
from .task import register_task

def get_current_time():
    current_time = datetime.now(datetime.timezone.utc).time()
    return current_time.strftime('%H:%M:%S')

register_task("get_current_time", get_current_time)