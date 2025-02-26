# myfwia/utils/task.py

task_registry = {}

def register_task(task_name, task_function):
    """
    Registra una función de tarea en el registro.
    :param task_name: Nombre de la tarea.
    :param task_function: Función que ejecuta la tarea.
    """
    task_registry[task_name] = task_function