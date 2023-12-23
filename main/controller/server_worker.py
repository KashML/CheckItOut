from typing import Tuple, List
from PyQt5.QtCore import QThread, pyqtSignal
from main.model.data_types import TaskData
from server.server import ServerController
import time

class ServerWorker(QThread):
    
    finishedSignal = pyqtSignal(bool, bool,list)  # Signal to send results or status back to the main thread
    startSignal = pyqtSignal()

    def run(self) -> Tuple[bool,bool,list]:
        """Fetches task list from the cloud
        
        Returns:
            status: Bool indicating the status of the connection
            clear: Bool indicating if we need to clear all tasks
            task_list: A list containing TaskData's
        """
        self.startSignal.emit()
        
        self.sleep(5)
        server_cntrl: ServerController = ServerController()
        status = server_cntrl.establish_connection()

        # Exit if error 
        if status != True:
            self.finishedSignal.emit(False, False, [])
            return
        
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

        self.finishedSignal.emit(status, clear, task_list)
        
