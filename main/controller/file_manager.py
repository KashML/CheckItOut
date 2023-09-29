
import os
import main
from typing import Dict, List
import pandas as pd

from main.model.data_types import TaskData

MAIN_DIR_PATH = os.path.dirname(main.__file__)
CSV_NAME = "task_database.csv"
CSV_PATH = os.path.join(MAIN_DIR_PATH, CSV_NAME)


NAME = "NAME"
STATUS = "STATUS"


class FileManager:

    def __init__(self) -> None:
        pass
         
    def write_to_csv(self, task_list: List[TaskData]) -> None:
        """Converts task list into a dataframe and saves it as csv"""

        table = pd.DataFrame(columns=[NAME, STATUS])

        for task in task_list:
            table.loc[len(table.index)] = [task.task_name, task.complete]

        table.to_csv(CSV_PATH)

    def load_from_csv(self) -> pd.DataFrame:
        """Loads a dataframe"""
        return pd.read_csv(CSV_PATH)
    
    def load_as_list(self) -> list:
        """Loads a list of TaskData Objects"""
        table = self.load_from_csv()
        data_list = table.apply(lambda row: TaskData(task_name=row[NAME], complete=row[STATUS]), axis=1).tolist()

        for d in data_list:
            print(d.task_name, d.complete)

        return data_list






