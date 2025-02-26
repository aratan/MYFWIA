# myfwia/tasks/task.py

class Task:
    """
    Representa una tarea con una descripción específica y un agente asignado.
    """
    def __init__(self, description, agent):
        self.description = description
        self.agent = agent