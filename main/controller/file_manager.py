import os
import main
from typing import Dict, List, Tuple
import pandas as pd

from main.model.data_types import TaskData, Era
from server.server import ServerController

MAIN_DIR_PATH = os.path.dirname(main.__file__)
CSV_NAME = "task_database.csv"
CSV_PATH = os.path.join(MAIN_DIR_PATH, CSV_NAME)

REMOTE_FILENAME = "tast_list_remote.txt"
REMOTE_FILEPATH = os.path.join(MAIN_DIR_PATH, REMOTE_FILENAME)


NAME = "NAME"
STATUS = "STATUS"
ERA = "ERA"

class FileManager:

    def __init__(self) -> None:
        pass
         
    def write_to_csv(self, task_list: List[TaskData]) -> None:
        """Converts task list into a dataframe and saves it as csv"""

        table = pd.DataFrame(columns=[NAME, STATUS, ERA])

        for task in task_list:
            table.loc[len(table.index)] = [task.task_name, task.complete, task.era.name]

        table.to_csv(CSV_PATH)

    def load_from_csv(self) -> pd.DataFrame:
        """Loads a dataframe"""
        return pd.read_csv(CSV_PATH)
    
    def load_as_list(self) -> list:
        """Loads a list of TaskData Objects"""
        table = self.load_from_csv()
        table[ERA] = table[ERA].apply(lambda x: Era[x])
        data_list = table.apply(lambda row: TaskData(task_name=row[NAME], complete=row[STATUS], era=row[ERA]), axis=1).tolist()


        for d in data_list:
            print(d.task_name, d.complete)

        return data_list
    
    def fetch_from_server(self) -> Tuple[bool,bool,list]:
        """Fetches task list from the cloud
        
        Returns:
            status: Bool indicating the status of the connection
            clear: Bool indicating if we need to clear all tasks
            task_list: A list containing TaskData's
        """
        
        
        server_cntrl: ServerController = ServerController()
        status = server_cntrl.establish_connection()

        # Exit if error 
        if status is not True:
            return False,False,[]
        
        clear = False
        email_data: list = server_cntrl.get_data()
        task_list: List[TaskData] = []

        for subject,body in email_data:
            
            # Ensure its a task list
            if "task" in subject.lower():
    
                lines = body.splitlines()            
                # Logic to determine append or overwrite
                if "clear" in lines[0].lower():
                    clear = True
                    for line in lines[1:]:
                        task_list.append(TaskData(task_name=line, complete=False))
                    

                else:
                    for line in lines:
                        task_list.append(TaskData(task_name=line, complete=False))
        
        server_cntrl.close()
        print("Cloud Update Done")
        return status, clear, task_list









