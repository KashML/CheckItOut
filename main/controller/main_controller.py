import copy

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from typing import Dict

from main.model.model import AppModel
from main.view import AppView
from main.Widgets.task_button import TaskbuttonWidget
from main.controller.helper import validate_text_input
from main.controller.file_manager import FileManager
from main.controller.splunk_logger import SplunkLogger
from main.model.data_types import TaskData
from main.controller.server_worker import ServerWorker


class AppController:
    
    def __init__(self, model, view):
        
        self.model: AppModel = model
        self.view: AppView = view
        self.file_manager = FileManager()

        splunk_log = SplunkLogger(status_bar_view=self.view)
        self.log = splunk_log.log


        # Counter for the TaskWidgets
        self.task_num = 0
        self.task_button_dict: Dict[int:TaskbuttonWidget] = {}


        # Connect UI interactions to model manipulations
        self.view.add_task_btn.clicked.connect(self.add_task)

        self.cloud_worker = None
        self.cloud_worker_create() 
        self.view.cloud_update.clicked.connect(self.cloud_worker_start)

        self.view.window.closeEvent = self.clean_up
        self.view.clear_all_action.triggered.connect(self.clear_all_action)
        self.view.save_action.triggered.connect(self.save_action)
        self.view.load_last_action.triggered.connect(self.load_last_save)

        # Load previous data
        self.load_data()
        self.update_progress_bar()
        
        
        
    
        self.log("Initialized Controller")
    
    def add_task(self) -> None:
        """Handles the action of adding a task by the user
        """

        #Update View side
        task_name = validate_text_input(self.view.add_task_line.text())
        self.view.add_task_line.clear()
        self.log(f"Adding a new task : {task_name}")
        
        self.create_task(task_name=task_name)


    def click_task(self, checked):
        """Handles the action of a task being clicked"""

        # Handle view side
        button: TaskbuttonWidget = self.view.app.sender()
        button.toggle(checked)

        # Handle model side
        self.model.add_clicked(id=button.id, checked=checked)

        self.update_progress_bar()
    
    def remove_task(self):
        """Handles the action of deleting a task by double clicking on it"""

        button: TaskbuttonWidget = self.view.app.sender()
        self.delete_task(id=button.id)
        
    
    def clean_up(self, event)-> None:
        """Cleaning up tasks"""

        self.log("Saving current tasks.....")
        self.file_manager.write_to_csv(self.model.get_task_list())

        self.log("Exiting App")
        event.accept()

    def create_task(self, task_name: str, complete: bool = False) -> None:
        """Creates a new task"""

        # Handle view
        new_task = TaskbuttonWidget(task_name=task_name, id=self.task_num)
        new_task.clicked.connect(self.click_task)
        new_task.doubleClicked.connect(self.remove_task)
        new_task.setChecked(complete)
        new_task.toggle(complete)
        self.view.task_frame_layout.addWidget(new_task)

        # Handle model side
        task_data = TaskData(task_name=task_name, id=self.task_num, complete=complete)
        self.model.add_task(task_data)
        
        # Update the controller
        self.task_button_dict[self.task_num] = new_task
        self.task_num = self.task_num + 1

    def delete_task(self, id: int) -> None:
        """Deletes a task"""
        
        # Handle Model Side
        self.model.remove_task(id)
        

        # Handle View side
        button = self.task_button_dict.get(id)
        self.view.task_frame_layout.removeWidget(button)
        button.hide()
        button.deleteLater()
        self.update_progress_bar()

        # Update Controller
        self.task_button_dict.pop(id)


    def load_data(self) -> None:
        """Load previous tasks from memory"""
        
        data_list: list[TaskData] = self.file_manager.load_as_list()
        for task in data_list:
            
            # Handle view side
            self.create_task(task_name=task.task_name, complete=task.complete)


        self.log(f"{len(data_list)} tasks loaded")
    
    def update_progress_bar(self) -> None:
        """Updates progress by quering the model"""
        
        # Get rate of completion
        status = self.model.get_completion_rate()
        self.view.progress_bar.set_value(int(status))

    
    def clear_all_action(self) -> None:
        """Clears all existing tasks on the App"""

        key_list = list(self.task_button_dict.keys())
    
        for key in key_list:
            self.delete_task(key)

    def save_action(self) -> None:
        """Saves curent task to file when user clicks save"""

        self.log("Saving current tasks.....")
        self.file_manager.write_to_csv(self.model.get_task_list())

    def load_last_save(self) -> None:
        """Loads last save when user clicks save"""
        self.load_data()

    def log(self, message: str) -> None:
        self.view.status_bar.showMessage(message)

    def cloud_worker_create(self) -> None:
        self.server_worker: ServerWorker = ServerWorker()
        self.server_worker.startSignal.connect(self.cloud_worker_start_gui_update)
        self.server_worker.finishedSignal.connect(self.cloud_worker_end)

    def cloud_worker_start(self) -> None:
        if self.server_worker.isRunning():  # If thread is running, terminate it (use with caution)
            self.server_worker.terminate()
            self.server_worker.wait() 

        self.cloud_worker_create()
        self.server_worker.start()    

    def cloud_worker_start_gui_update(self) -> None:
        self.log("Fetching data from server. Please wait .....")
    
    def cloud_worker_end(self, status, clear, task_list) -> None:
        if clear is True:
            self.clear_all_action()

        if status is False:
            self.log("Cloud Update failed")
            return
        
        for task in task_list:
            self.create_task(task_name=task.task_name, complete=task.complete)

        self.log("Complete")


