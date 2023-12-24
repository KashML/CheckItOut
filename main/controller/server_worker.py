from typing import Tuple, List
from PyQt5.QtCore import QThread, pyqtSignal
from main.model.data_types import TaskData, Era
from server.server import ServerController
from main.controller.helper import find_era, strip_era
import time



class ServerWorker(QThread):
    
    finishedSignal = pyqtSignal(bool, bool,list)  # Signal to send results or status back to the main thread
    startSignal = pyqtSignal()

    def run(self) -> Tuple[bool,bool,list]:
        """Fetches task list from the cloud
        
        Returns:
            status: Bool indicating the status of the connection
            clear: Bool indicating if we need to clear all tasks currently in the database
            task_list: A list containing TaskData's
        """
        self.startSignal.emit()

        #
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

            # Ensure it's a task list
            if "task" not in subject.lower():
                continue

            print(f" 1st - {find_era(subject.lower())} ")
            default_era = find_era(subject.lower()) if find_era(subject.lower()) is not None else Era.DAILY

            lines = body.splitlines()
            # Logic to determine append or overwrite
            if "clear" in lines[0].lower():
                clear = True
                lines = lines[1:]

            for line in lines:

                era_flag = default_era
                if find_era(line) is not None:
                    era_flag = find_era(line)
                    line = strip_era(line)


                print("find_era(line)")
                task_list.append(TaskData(task_name=line, complete=False, era=era_flag))
        
        server_cntrl.close()
        print("Cloud Update Done")

        self.finishedSignal.emit(status, clear, task_list)
        
