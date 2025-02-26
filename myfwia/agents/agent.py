# myfwia/agents/agent.py

class Agent:
    """
    Representa un agente con un rol específico y capacidad para ejecutar tareas.
    """
    def __init__(self, role, goal, backstory, verbose=True):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.verbose = verbose

    def execute_task(self, task_description):
        if self.verbose:
            print(f"\n{self.role} está ejecutando la tarea: {task_description}")
        return "Respuesta por defecto"