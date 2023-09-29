"""
Object holding a task button data
"""

class TaskData:

    def __init__(self, task_name: str, id: int = 0, complete: bool = False) -> None:
        self.task_name = task_name
        self.id = id
        self.complete = complete