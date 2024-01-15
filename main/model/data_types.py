"""
Object holding a task button data
"""
from enum import Enum

class Era(Enum):
    ALL = 0
    DAILY = 0
    MONTHLY = 1

class TaskData:
    def __init__(self, task_name: str, id: int = 0, complete: bool = False, era: Era = Era.DAILY) -> None:
        self.task_name = task_name
        self.id = id
        self.complete = complete
        self.era = era